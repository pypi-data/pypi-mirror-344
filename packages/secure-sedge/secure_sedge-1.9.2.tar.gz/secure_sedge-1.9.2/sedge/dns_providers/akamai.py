import logging
import os
from urllib.parse import urljoin

import requests
from akamai.edgegrid import EdgeGridAuth
from sewer.dns_providers.common import BaseDns


log = logging.getLogger(__name__)


class AkamaiDns(BaseDns):
    def __init__(self, client_token=None, client_secret=None,
                 access_token=None, base_url=None, **kwargs):
        super().__init__(**kwargs)
        self.session = None
        self.client_token = client_token or os.environ.get('AKAMAI_CLIENT_TOKEN')
        self.client_secret = client_secret or os.environ.get('AKAMAI_CLIENT_SECRET')
        self.access_token = access_token or os.environ.get('AKAMAI_ACCESS_TOKEN')
        self.base_url = base_url or os.environ.get('AKAMAI_BASE_URL')
        self.zone_map = None
        self.old_records = {}

    def get_session(self):
        if self.session:
            return self.session
        self.session = requests.Session()
        self.session.auth = EdgeGridAuth(
            client_token=self.client_token,
            client_secret=self.client_secret,
            access_token=self.access_token,
        )
        self.session.headers = {
            'accept': 'application/json',
        }
        return self.session

    def make_url(self, path):
        return urljoin(self.base_url, path)

    def get_recordset(self, zone, name, type_):
        log.info('[akamai] getting recordset %s / %s', name, type_)
        route = f'config-dns/v2/zones/{zone}/names/{name}/types/{type_}'
        session = self.get_session()
        response = session.get(self.make_url(route))
        if response.status_code == 200:
            log.info('[akamai] found recordset %s / %s', name, type_)
            return response.json()
        return None

    @classmethod
    def yield_txt_values(cls, rdata):
        values = set()
        for x in rdata:
            value = x
            if not x.startswith('"') and not x.endswith('"'):
                value = f'"{x}"'
            if value not in values:
                values.add(value)
                yield value

    @classmethod
    def fix_txt_rdata(cls, rdata, type_):
        if not isinstance(rdata, list):
            rdata = [rdata]
        if type_ == 'TXT':
            rdata = list(cls.yield_txt_values(rdata))
        return rdata

    def update_recordset(self, zone, name, type_, rdata, ttl=300):
        log.info('[akamai] updating recordset %s / %s', name, type_)
        route = f'config-dns/v2/zones/{zone}/names/{name}/types/{type_}'
        session = self.get_session()
        rdata = self.fix_txt_rdata(rdata, type_)
        payload = {
            'name': name,
            'type': type_,
            'ttl': ttl,
            'rdata': rdata,
        }
        response = session.put(self.make_url(route), json=payload)
        if response.status_code in (200, 201, 204):
            log.info('[akamai] updated recordset %s / %s => %s', name, type_, rdata)
            if response.text:
                return response.json()
        return None

    def create_recordset(self, zone, name, type_, rdata, ttl=300):
        log.info('[akamai] creating recordset %s / %s', name, type_)
        route = f'/config-dns/v2/zones/{zone}/names/{name}/types/{type_}'
        session = self.get_session()
        rdata = self.fix_txt_rdata(rdata, type_)
        payload = {
            'name': name,
            'type': type_,
            'ttl': ttl,
            'rdata': rdata,
        }
        response = session.post(self.make_url(route), json=payload)
        if response.status_code in (200, 201, 204):
            log.info('[akamai] created recordset %s / %s', name, type_)
            if response.text:
                return response.json()
        return None

    def delete_recordset(self, zone, name, type_):
        log.info('[akamai] deleting recordset %s / %s', name, type_)
        route = f'config-dns/v2/zones/{zone}/names/{name}/types/{type_}'
        session = self.get_session()
        response = session.delete(self.make_url(route))
        if response.status_code in (200, 201, 204):
            log.info('[akamai] deleted recordset %s / %s', name, type_)
            if response.text:
                return response.json()
        return None

    def resolve_zone(self, name):
        log.info('[akamai] resolving zone of %s', name)
        zone = None
        pieces = name.split('.')
        zone_map = self.get_zones()
        while pieces:
            zone = '.'.join(pieces)
            if zone in zone_map:
                log.info('[akamai] found zone %s', zone)
                return zone
            pieces = pieces[1:]
        raise ValueError(f'No zone found for {name}')

    def create_dns_record(self, domain_name, domain_dns_value):
        """
        Method that creates/adds a dns TXT record for a domain/subdomain name on
        a chosen DNS provider.

        :param domain_name: :string: The domain/subdomain name whose dns record ought to be
            created/added on a chosen DNS provider.
        :param domain_dns_value: :string: The value/content of the TXT record that will be
            created/added for the given domain/subdomain

        This method should return None

        Basic Usage:
            If the value of the `domain_name` variable is example.com and the value of
            `domain_dns_value` is HAJA_4MkowIFByHhFaP8u035skaM91lTKplKld
            Then, your implementation of this method ought to create a DNS TXT record
            whose name is '_acme-challenge' + '.' + domain_name + '.'
            (ie: _acme-challenge.example.com. )
            and whose value/content is HAJA_4MkowIFByHhFaP8u035skaM91lTKplKld

            Using a dns client like dig(https://linux.die.net/man/1/dig) to do a dns
            lookup should result
            in something like:
                dig TXT _acme-challenge.example.com
                ...
                ;; ANSWER SECTION:
                _acme-challenge.example.com. 120 IN TXT "HAJA_4MkowIFByHhFaP8u035skaM91lTKplKld"
                _acme-challenge.singularity.brandur.org. 120 IN TXT "9C0DqKC_4MkowIFByHhFaP8u0Zv4z7Wz2IHM91lTKec"
            Optionally, you may also use an online dns client like:
            https://toolbox.googleapps.com/apps/dig/#TXT/

            Please consult your dns provider on how/format of their DNS TXT
            records.  You may also want to consult the cloudflare DNS implementation
            that is found in this repository.
        """
        name = f'_acme-challenge.{domain_name}'
        type_ = 'TXT'
        zone = self.resolve_zone(domain_name)
        existing_record = self.get_recordset(zone, name, type_)
        if existing_record:
            self.old_records.setdefault(name, existing_record)
            rdata = existing_record['rdata'] + [domain_dns_value]
            self.update_recordset(zone, name, type_, rdata)
        else:
            self.create_recordset(zone, name, type_, domain_dns_value)

    def delete_dns_record(self, domain_name, domain_dns_value):
        """
        Method that deletes/removes a dns TXT record for a domain/subdomain name on
        a chosen DNS provider.

        :param domain_name: :string: The domain/subdomain name whose dns record ought to be
            deleted/removed on a chosen DNS provider.
        :param domain_dns_value: :string: The value/content of the TXT record that will be
            deleted/removed for the given domain/subdomain

        This method should return None
        """
        name = f'_acme-challenge.{domain_name}'
        type_ = 'TXT'
        zone = self.resolve_zone(domain_name)
        x = self.get_recordset(zone, name, type_)
        if not x:
            return
        rdata = [ i for i in x['rdata'] if domain_dns_value not in i ]
        if rdata:
            self.update_recordset(zone, name, type_, rdata, ttl=x['ttl'])
        else:
            self.delete_recordset(zone, name, type_)

    def recordsets(self, zone, type_=None):
        route = f'config-dns/v2/zones/{zone}/recordsets'
        params = {
            'showAll': 'true',
        }
        if type_:
            params['types'] = type_
        session = self.get_session()
        response = session.get(self.make_url(route), params=params)
        return response.json()['recordsets']

    def get_zones(self):
        if self.zone_map:
            return self.zone_map
        log.info('[akamai] getting all zones')
        session = self.get_session()
        params = { 'showAll': 'true', 'types': 'PRIMARY', }
        route = 'config-dns/v2/zones'
        response = session.get(self.make_url(route), params=params)
        zones = response.json()['zones']
        log.info('[akamai] found %s zones', len(zones))
        zone_map = { x['zone']: x for x in zones }
        self.zone_map = zone_map
        return self.zone_map
