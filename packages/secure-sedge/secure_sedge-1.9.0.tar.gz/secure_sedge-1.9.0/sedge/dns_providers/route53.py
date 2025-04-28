from collections import defaultdict
from glob import glob
import logging
import os
import posixpath
import random
import socket
import sys
from tempfile import NamedTemporaryFile
from typing import Sequence, Dict, List, Set, Iterable, Any, Optional

from raft import task
import yaml
from boto3 import Session
from sewer.auth import ErrataItemType
from sewer.config import ACME_DIRECTORY_URL_STAGING  # noqa: F401, pylint: disable=unused-import
from sewer.dns_providers.common import dns_challenge
from sewer.dns_providers.cloudflare import CloudFlareDns
from sewer.dns_providers.route53 import Route53Dns as SewerRoute53Dns
from ..models import Route53Change


log = logging.getLogger(__name__)


class Route53Dns(SewerRoute53Dns):
    def __init__(self, profile_map):
        super().__init__()
        self.resource_records = defaultdict(set)
        self.change_map: Dict[str, Route53Change] = {}
        self.zone_ids = {}
        self.deletes = []
        self.undos: List[Route53Change] = []
        self.sessions_by_profile = {}
        self.sessions = {}
        self.profile_map = profile_map
        for name, profile in self.profile_map.items():
            rg = self.sessions_by_profile.get(profile)
            if not rg:
                session = Session(profile_name=profile)
                client = session.client('route53', config=self.aws_config)
                waiter = client.get_waiter('resource_record_sets_changed')
                rg = session, client, waiter
                self.sessions_by_profile[profile] = rg
            self.sessions[name] = rg

    def get_session(self, name):
        rg = self.get_session_client_waiter(name)
        return rg[0]

    def get_client(self, name):
        rg = self.get_session_client_waiter(name)
        return rg[1]

    def get_waiter(self, name):
        rg = self.get_session_client_waiter(name)
        return rg[2]

    def get_session_client_waiter(self, name):
        if name.endswith('.'):
            name = name[:-1]
        if name not in self.sessions and f'*.{name}' in self.sessions:
            name = f'*.{name}'
        session, client, waiter = self.sessions[name]
        return session, client, waiter

    def setup(self, challenges: Sequence[Dict[str, str]]) -> Sequence[ErrataItemType]:
        for x in challenges:
            domain_name = x['ident_value']
            session, client, waiter = self.get_session_client_waiter(domain_name)
            value = dns_challenge(x['key_auth'])
            challenge_domain = f'_acme-challenge.{domain_name}.'
            self.resource_records[challenge_domain].add(value)
            change = self.change_map.setdefault(
                challenge_domain,
                Route53Change(
                    name=challenge_domain,
                    domain=domain_name,
                    record_type='TXT',
                    values=set(),
                    session=session,
                    client=client,
                    waiter=waiter,
                ))
            change.values.add(f'"{value}"')
        self.find_zone_ids()
        self.handle_existing()
        self.create_dns_record(domain_name=None, domain_dns_value=None)
        return []

    def find_zone_ids(self):
        for x in self.change_map.values():
            pieces = x.domain.split('.')
            session, client, waiter = self.get_session_client_waiter(x.domain)
            while pieces:
                d = '.'.join(pieces)
                log.info('[route53] finding zone id for %s', d)
                zone_id = self.zone_ids.get(d)
                if not zone_id:
                    response = client.list_hosted_zones_by_name(DNSName=d)
                    for zone in response['HostedZones']:
                        if zone['Name'] == d:
                            zone_id = self.zone_ids[d] = zone['Id']
                            break
                if zone_id:
                    x.zone_id = zone_id
                    x.session = session
                    x.waiter = waiter
                    x.client = client
                    self.sessions[zone_id] = session, client, waiter
                    log.info('[route53] %s => %s', d, zone_id)
                    break
                pieces = pieces[1:]

    def change_batch(self, changes: List[Route53Change]):
        return {
            'Comment': 'letsencrypt dns certificate validation changes',
            'Changes': [{
                'Action': x.action,
                'ResourceRecordSet': {
                    'Name': x.name,
                    'Type': x.record_type,
                    'TTL': x.ttl,
                    'ResourceRecords': [
                        dict(Value=value)
                        for value in x.values
                    ],
                },
            } for x in changes],
        }

    def handle_existing(self):
        domain_records = defaultdict(list)
        for domain, st_id in self.zone_ids.items():
            client = self.get_client(st_id)
            paginator = client.get_paginator('list_resource_record_sets')
            log.info('[route53] listing zone for %s', domain)
            rg = paginator.paginate(HostedZoneId=st_id)
            for page in rg:
                domain_records[st_id] += page['ResourceRecordSets']
            log.info('[route53] found %s records', len(domain_records[st_id]))
        for x in self.change_map.values():
            records = domain_records[x.zone_id]
            for record in records:
                if record['Name'] == x.name:
                    log.info(
                        '[route53] found existing record for %s / %s',
                        x.name, record['Type'])
                    change = Route53Change(
                        name=record['Name'],
                        record_type=record['Type'],
                        values={ lx["Value"] for lx in record['ResourceRecords'] },
                        ttl=record['TTL'],
                        action='DELETE',
                        domain=x.domain,
                        zone_id=x.zone_id,
                        session=x.session,
                        client=x.client,
                        waiter=x.waiter,
                    )
                    if record['Type'] != x.record_type:
                        self.deletes.append(change)
                    else:
                        change.action = 'UPSERT'
                        self.undos.append(change)

    @classmethod
    def by_zone_id(cls, rg: Iterable[Route53Change]):
        by_zone_id = defaultdict(list)
        for x in rg:
            by_zone_id[x.zone_id].append(x)
        return by_zone_id

    def wait(self, zone_id, change_id):
        log.info('[route53 / %s] waiting for %s', zone_id, change_id)
        waiter = self.get_waiter(zone_id)
        waiter.wait(Id=change_id, WaiterConfig=dict(
            Delay=5,
            MaxAttempts=24,
        ))
        log.info('[route53 / %s] change is complete', zone_id)

    def change_and_wait(self, changes: Iterable[Route53Change]):
        result = {}
        for x in changes:
            log.info(
                '[route53] %s (%s) %s => %s',
                x.action, x.record_type, x.name, x.values)
        for zone_id, zone_changes in self.by_zone_id(changes).items():
            client = self.get_client(zone_id)
            response = client.change_resource_record_sets(
                HostedZoneId=zone_id,
                ChangeBatch=self.change_batch(zone_changes),
            )
            change_id = response['ChangeInfo']['Id']
            result[zone_id] = change_id
        for zone_id, change_id in result.items():
            self.wait(zone_id, change_id)
        return result

    def create_dns_record(self, domain_name, domain_dns_value):
        if domain_name and domain_dns_value:
            change = self.change_map.get(domain_name)
            if change:
                change.values.add(domain_dns_value)
        if self.deletes:
            self.change_and_wait(self.deletes)
        result = self.change_and_wait(self.change_map.values())
        return result

    def clear(self, challenges: Sequence[Dict[str, str]]) -> Sequence[ErrataItemType]:
        self.delete_dns_record(None, None)
        return []

    def delete_dns_record(self, domain_name, domain_dns_value):
        for x in self.change_map.values():
            if x.action == 'UPSERT':
                x.action = 'DELETE'
            elif x.action == 'DELETE':
                x.action = 'UPSERT'
        result = self.change_and_wait(self.change_map.values())
        for x in self.deletes:
            x.action = 'UPSERT'
            self.undos.append(x)
        if self.undos:
            self.change_and_wait(self.undos)
        return result
