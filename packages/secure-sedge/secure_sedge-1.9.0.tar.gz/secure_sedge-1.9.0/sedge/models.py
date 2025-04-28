from dataclasses import dataclass
from typing import Set, Optional, Any
from boto3.session import Session


@dataclass
class DnsChange:
    name: str = None
    values: Set[str] = None
    domain: str = None
    zone_id: str = None
    action: str = 'UPSERT'
    record_type: str = 'TXT'
    ttl: int = 60


@dataclass
class Route53Change(DnsChange):
    session: Optional[Session] = None
    client: Optional[Any] = None
    waiter: Optional[Any] = None

    def __post_init__(self):
        if self.domain and not self.domain.endswith('.'):
            self.domain = f'{self.domain}.'


