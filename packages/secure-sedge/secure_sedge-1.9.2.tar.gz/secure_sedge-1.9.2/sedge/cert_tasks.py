import importlib
from glob import glob
import json
import logging
import os
import posixpath
import random
import socket
import sys
from tempfile import NamedTemporaryFile

from convocations.aws.base import AwsTask
from raft import task
import yaml
from boto3 import Session
from sewer.config import ACME_DIRECTORY_URL_STAGING, ACME_DIRECTORY_URL_PRODUCTION
from sewer.dns_providers.cloudflare import CloudFlareDns
from .sedge_client import SedgeClient
from .dns_providers.route53 import Route53Dns
from .dns_providers.akamai import AkamaiDns


log = logging.getLogger(__name__)
ACL = 'bucket-owner-full-control'


def new_cert(
        hostname, alt_domains, email=None, profile=None,
        provider_klass=None):
    """
    :param str hostname:
        the fqdn of the local host for which we are creating the cert

    :param str alt_domains:
        a comma-separated list of alternative domains to also
        requests certs for.

    :param str email:
        the email of the contact on the cert

    :param str profile:
        the name of the aws profile to use to connect boto3 to
        appropriate credentials
    :param type provider_klass:

    """
    alt_domains = alt_domains.split(',') if alt_domains else []
    provider_klass = provider_klass or Route53Dns
    url = ACME_DIRECTORY_URL_PRODUCTION
    if os.environ.get('DEBUG'):
        url = ACME_DIRECTORY_URL_STAGING
    client = SedgeClient(
        hostname, domain_alt_names=alt_domains, contact_email=email,
        provider=provider_klass(profile), ACME_AUTH_STATUS_WAIT_PERIOD=5,
        ACME_AUTH_STATUS_MAX_CHECKS=180, ACME_REQUEST_TIMEOUT=60,
        ACME_DIRECTORY_URL=url, LOG_LEVEL='INFO')
    certificates = client.cert()
    account_key = client.account_key
    key = client.certificate_key
    return certificates, account_key, key


def get_certificate(ns, hostname, profile=None):
    if not ns.startswith('/'):
        ns = f'/{ns}'
    hostname = hostname.replace('*', 'star')
    try:
        session = Session(profile_name=profile)
        ssm = session.client('ssm')
        name = '/'.join([ ns, 'apps_keystore', hostname, 'account_key' ])
        account_key = get_chunked_ssm_parameter(name, profile=profile)
        log.info('account key retrieved')
        name = '/'.join([ ns, 'apps_keystore', hostname, 'key' ])
        response = ssm.get_parameter(Name=name, WithDecryption=True)
        key = response['Parameter']['Value']
        log.info('private key retrieved')
        name = '/'.join([ ns, 'apps_keystore', hostname, 'cert' ])
        certificate = get_chunked_ssm_parameter(name, profile=profile)
        log.info('public cert retrieved')
    except:  # noqa: E722, pylint: disable=bare-except
        account_key = None
        key = None
        certificate = None
    return certificate, account_key, key


def get_file_from_s3(s3, bucket, ns, filename, decode=True):
    filename = filename.replace('*', 'star')
    key = filename
    if ns:
        key = posixpath.join(ns, key)
    log.info('retrieving s3://%s/%s', bucket, key)
    response = s3.get_object(Bucket=bucket, Key=key)
    data = response['Body'].read()
    if decode:
        data = data.decode('utf-8')
    return data


def get_certificate_from_s3(bucket, ns, hostname, profile=None):
    hostname = hostname.replace('*', 'star')
    account_key = None
    key_content = None
    certificate = None
    try:
        log.info('connecting to aws with profile [%s]', profile)
        session = Session(profile_name=profile)
        s3 = session.client('s3')
    except Exception as ex:  # noqa: E722, pylint: disable=broad-except,
        log.info('exception connecting to s3: %s', ex)
        return certificate, account_key, key_content

    try:
        account_key = get_file_from_s3(s3, bucket, None, 'global.account_key')
        log.info('[%s] account key retrieved', profile)
    except Exception as ex:  # noqa: E722, pylint: disable=broad-except,
        log.info('[%s] exception getting account key: %s', profile, ex)

    try:
        key_content = get_file_from_s3(s3, bucket, ns, f'{hostname}.key')
        log.info('[%s] private key retrieved', profile)
    except Exception as ex:  # noqa: E722, pylint: disable=broad-except,
        log.info('exception getting private key: %s', ex)

    try:
        certificate = get_file_from_s3(s3, bucket, ns, f'{hostname}.crt')
        log.info('[%s] public cert retrieved', profile)
    except Exception as ex:  # noqa: E722, pylint: disable=broad-except,
        log.info('exception retrieving public cert: %s', ex)
    return certificate, account_key, key_content


def get_chunked_ssm_parameter(name, profile=None):
    session = Session(profile_name=profile)
    ssm = session.client('ssm')
    rg = []
    for n in range(1, 10):
        try:
            st = f'{name}{n}'
            log.info('[ssm]  getting %s', st)
            response = ssm.get_parameter(Name=st, WithDecryption=True)
            rg.append(response['Parameter']['Value'])
        except:  # noqa: E722, pylint: disable=bare-except
            break
    data = ''.join(rg)
    return data


def get_pfx(bucket, key, profile=None):
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    key = key.replace('*', 'star')
    if not key.lower().endswith('.pfx'):
        key = f'{key}.pfx'
    pfx_data = get_file_from_s3(s3, bucket, None, key, False)
    log.info('[pfx]  read %s bytes', len(pfx_data))
    return pfx_data


def build_profile_map(hostname, alt_domains, profile):
    domains = None
    if alt_domains:
        if isinstance(alt_domains[0], dict):
            domains = alt_domains
            included = False
            for x in alt_domains:
                if x['name'] == hostname:
                    included = True
                    break
            if not included:
                domains.append({
                    'name': hostname,
                    'profile': profile,
                })
        else:
            domains = []
            included = False
            for x in alt_domains:
                domains.append({ 'name': x, 'profile': profile })
                if x == hostname:
                    included = True
            if not included:
                domains.append({
                    'name': hostname,
                    'profile': profile,
                })
    else:
        domains = [{
            'name': hostname,
            'profile': profile,
        }]

    return { x['name']: x['profile'] for x in domains }


def renew_cert(
        ns, hostname, alt_domains=None,
        email=None, bucket=None, tmp_dir=None, profile=None,
        bucket_profile=None, provider=None, **kwargs):
    log.info('[sedge.renew_cert] renewing cert for %s', hostname)
    if alt_domains:
        if isinstance(alt_domains, str):
            alt_domains = alt_domains.split(',')
    else:
        alt_domains = []
    _, account_key, key = get_certificate_from_s3(
        bucket, ns, hostname, bucket_profile)
    profile_map = build_profile_map(hostname, alt_domains, profile)
    if not provider:
        log.info('[sedge.renew_cert] no provider specified')
        cloudflare_token = kwargs.get('cloudflare_token') or os.environ.get('CLOUDFLARE_TOKEN')
        if cloudflare_token:
            log.info('[sedge.renew_cert] cloudflare_token specified, using cloudflare dns provider')
            provider = CloudFlareDns(CLOUDFLARE_TOKEN=cloudflare_token)
        else:
            log.info('[sedge.renew_cert] using route53 as dns provider')
            provider = Route53Dns(profile_map=profile_map)
    elif hasattr(provider, 'profile_map'):
        provider.profile_map = profile_map
    domain_alt_names = [ x for x in profile_map if x != hostname ]
    client = SedgeClient(
        hostname, domain_alt_names=domain_alt_names, contact_email=email,
        provider=provider, account_key=account_key,
        certificate_key=key, ACME_AUTH_STATUS_WAIT_PERIOD=15,
        ACME_AUTH_STATUS_MAX_CHECKS=60, ACME_REQUEST_TIMEOUT=15)
    if not account_key:
        client.acme_register()
        content = client.account_key
        save_account_key(bucket, ns, content, tmp_dir, bucket_profile)
    if not key:
        client.create_certificate_key()
        content = client.certificate_key
        save_key(bucket, ns, hostname, content, tmp_dir, bucket_profile)
    certificates = client.renew()
    account_key = client.account_key
    key = client.certificate_key
    return certificates, account_key, key


def save_account_key(bucket, ns, content, tmp_dir, profile):
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    filename = 'global.account_key'
    save_to_temp(tmp_dir, filename, content)
    if isinstance(content, str):
        content = content.encode('utf-8')
    s3_key = filename
    s3.put_object(Bucket=bucket, Key=s3_key, Body=content, ACL='bucket-owner-full-control')


def save_key(bucket, ns, hostname, content, tmp_dir, profile):
    session = Session(profile_name=profile)
    s3 = session.client('s3')
    hostname = hostname.replace('*', 'star')
    filename = f'{hostname}.key'
    save_to_temp(tmp_dir, filename, content)
    if isinstance(content, str):
        content = content.encode('utf-8')
    s3_key = posixpath.join(ns, filename)
    s3.put_object(Bucket=bucket, Key=s3_key, Body=content, ACL='bucket-owner-full-control')


def full_pfx(ctx, certificate, key, password=None, chain=None, legacy=False, include_chain=True):
    from cryptography.x509 import load_pem_x509_certificates
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.serialization import (
        BestAvailableEncryption,
        load_pem_private_key,
        NoEncryption,
        pkcs12,
        PrivateFormat,
    )
    from cryptography.hazmat.primitives.serialization.pkcs12 import \
        serialize_key_and_certificates
    if isinstance(certificate, str):
        certs = load_pem_x509_certificates(certificate.encode('utf-8'))
    else:
        certs = [ certificate ]
        if chain:
            certs += chain
    if isinstance(key, str):
        key = load_pem_private_key(key.encode('utf-8'), password=None)
    if not include_chain:
        certs = certs[:1]
    encryption = NoEncryption()
    if password:
        if legacy:
            alg = pkcs12.PBES.PBESv1SHA1And3KeyTripleDESCBC
            encryption = PrivateFormat.PKCS12.encryption_builder()
            encryption = encryption.kdf_rounds(50000)
            encryption = encryption.key_cert_algorithm(alg)
            encryption = encryption.hmac_hash(hashes.SHA1())
            encryption = encryption.build(password.encode('utf-8'))
        else:
            encryption = BestAvailableEncryption(password.encode('utf-8'))
    p12 = serialize_key_and_certificates(
        None,
        key,
        certs[0],
        certs[1:] or None,
        encryption)
    return p12


@task
def renew_all(ctx, dir_name=None, profile=None):
    """
    Requests a letsencrypt cert using route53 and sewer, also requests
    wildcard certs based on the provided hostname

    :param raft.context.Context ctx:
        the raft-provided context

    :param str dir_name:
        the config directory

    :param str profile:
        the name of the aws profile to use to connect boto3 to
        appropriate credentials

    """
    default_filename = os.path.join(dir_name, 'defaults.yml')
    defaults = {}
    if os.path.exists(default_filename):
        with open(default_filename, 'r') as f:
            defaults = yaml.load(f, Loader=yaml.SafeLoader)
    defaults = defaults or {}
    dir_name = os.path.join(dir_name, '*.yml')
    files = glob(dir_name)
    for filename in files:
        try:
            # don't let the failure of any one certificate
            # make it so that we don't try to renew the rest
            if filename.endswith('defaults.yml'):
                continue
            request_cert(ctx, filename, profile, defaults)
        except:  # noqa: E722, pylint: disable=bare-except, broad-except
            pass


def get_provider(provider_klass, values):
    provider_klass = provider_klass or values.get('dns_provider')
    provider = None
    if isinstance(provider_klass, str):
        module, klass = provider_klass.rsplit('.', 1)
        m = importlib.import_module(module)
        provider_klass = getattr(m, klass)
        provider = provider_klass()
    return provider


def request_cert(ctx, filename, profile, defaults, provider_klass=None):
    log.info('processing %s', filename)
    with open(filename, 'r') as f:
        values = yaml.load(f, Loader=yaml.SafeLoader)
    for key, value in defaults.items():
        values.setdefault(key, value)
    provider = get_provider(provider_klass, values)
    namespaces = values.pop('namespaces', [])
    config_profile = values.pop('profile', None)
    profile = profile or config_profile
    ns = namespaces[0]
    bucket = values.pop('bucket', None)
    buckets = values.get('buckets') or []
    bucket_profile = profile
    if buckets:
        bucket = buckets[0]['name']
        bucket_profile = buckets[0].get('profile') or profile
    certificates, account_key, key = renew_cert(
        **values, ns=ns, profile=profile, provider=provider,
        bucket=bucket, bucket_profile=bucket_profile)
    pfx_password = values.pop('pfx_password', None)
    tmp_dir = values.pop('tmp_dir', '/tmp')
    save_to_file(
        ctx, tmp_dir, values['hostname'],
        certificates, account_key, key)
    if bucket:
        found = False
        for x in buckets:
            if x['name'] == bucket:
                found = True
                break
        if not found:
            buckets.append(dict(name=bucket))
    for x in buckets:
        bucket = x['name']
        role = x.get('assume_role')
        profile = x.get('profile') or profile
        for namespace in namespaces:
            save_to_s3(
                ctx, bucket, namespace, values['hostname'], certificates,
                account_key, key, tmp_dir=tmp_dir, profile=profile,
                pfx_password=pfx_password, role=role)


@task
def request(ctx, filename=None, profile=None):
    """
    Requests a letsencrypt cert using route53 and sewer, also requests
    wildcard certs based on the provided hostname

    :param raft.context.Context ctx:
        the raft-provided context

    :param str filename:
        the config file

    :param str profile:
        the name of the aws profile to use to connect boto3 to
        appropriate credentials

    """
    default_filename = os.path.join(os.path.dirname(filename), 'defaults.yml')
    defaults = {}
    if os.path.exists(default_filename):
        with open(default_filename, 'r') as f:
            defaults = yaml.load(f, Loader=yaml.SafeLoader)
    defaults = defaults or {}
    request_cert(ctx, filename, profile, defaults)


def save_to_temp(tmp_dir, filename, content):
    filename = os.path.join(tmp_dir, filename)
    log.info('saving %s', filename)
    filename = filename.replace('*', 'star')
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir, 0o755, True)
    if isinstance(content, str):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    else:
        with open(filename, 'wb') as f:
            f.write(content)


def save_to_file(ctx, tmp_dir, hostname, certificates, account_key, key):
    """
    saves the contents of the certificate, key, and account keys
    to a local directory for debugging
    """
    extensions = [ '', '.alt', '.02', '.03', '.04', '.05', '.06' ]
    for i, certificate in enumerate(certificates):
        st = extensions[i]
        extension = f'{st}.crt'
        filename = f'{hostname}{extension}'
        save_to_temp(tmp_dir, filename, certificate)
    contents = [
        ('.account_key', account_key),
        ('.key', key),
    ]
    for extension, content in contents:
        filename = f'{hostname}{extension}'
        save_to_temp(tmp_dir, filename, content)


def assume_role(session, role):
    sts = session.client('sts')
    r = sts.assume_role(RoleArn=role)
    creds = r['Credentials']
    return Session(
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken']
    )


def save_to_s3(ctx, bucket, ns, hostname, certificates, account_key, key,
               tmp_dir='/tmp', profile=None, pfx_password=None, role=None):
    """
    saves the contents of the certificate, key, and account keys
    to a local directory for debugging
    """
    extensions = [ '', '.alt', '.02', '.03', '.04', '.05', ]
    session = Session(profile_name=profile)
    if role:
        session = assume_role(session, role)
    s3 = session.client('s3')
    for i, certificate in enumerate(certificates):
        pfx_content = full_pfx(
            ctx, certificate, key, pfx_password,
            include_chain=False, legacy=True)
        modern_pfx_content = full_pfx(ctx, certificate, key, pfx_password)
        contents = [
            (f'{extensions[i]}.crt', certificate),
            ('.pfx', pfx_content),
            ('.modern.pfx', modern_pfx_content),
        ]
        for extension, content in contents:
            filename = f'{hostname}{extension}'
            filename = filename.replace('*', 'star')
            filename = posixpath.join(ns, filename)
            log.info('saving s3://%s/%s', bucket, filename)
            if isinstance(content, str):
                content = content.encode('utf-8')
            s3.put_object(Bucket=bucket, Key=filename, Body=content, ACL=ACL)

    filename = f'{hostname}.key'
    filename = filename.replace('*', 'star')
    filename = posixpath.join(ns, filename)
    log.info('saving s3://%s/%s', bucket, filename)
    s3.put_object(Bucket=bucket, Key=filename, Body=key, ACL='bucket-owner-full-control')


def save_to_ssm(ctx, ns, hostname, certificate, account_key, key, profile=None):
    session = Session(profile_name=profile)
    ssm = session.client('ssm')
    pfx_data = full_pfx(ctx, certificate, key)
    hostname = hostname.replace('*', 'star')
    prefix = ns
    if not prefix.startswith('/'):
        prefix = f'/{prefix}'
    prefix = os.path.join(prefix, 'apps_keystore', hostname)
    contents = [
        ('account_key', account_key),
        ('cert', certificate),
    ]
    for suffix, content in contents:
        name = os.path.join(prefix, suffix)
        log.info('saving %s', name)
        save_chunked_ssm_parameter(ns, name, content, 'String', profile)

    contents = [
        ('key', key),
    ]
    for suffix, content in contents:
        name = os.path.join(prefix, suffix)
        log.info('saving %s', name)
        try:
            ssm.put_parameter(
                Name=name,
                Description=f'sewer / certbot {suffix}',
                Value=content,
                Overwrite=True,
                Type='SecureString',
                KeyId=f'alias/{ns}')
        except Exception as ex:  # pylint: disable=broad-except
            log.info('exception saving to ssm: %s', ex)

    name = os.path.join(prefix, 'pfx')
    save_chunked_ssm_parameter(ns, name, pfx_data, 'SecureString', profile)


def save_chunked_ssm_parameter(ns, name, value, type_, profile=None):
    session = Session(profile_name=profile)
    ssm = session.client('ssm')
    pieces = []
    while value:
        pieces.append(value[:4096])
        value = value[4096:]
    for n, x in enumerate(pieces, 1):
        st = f'{name}{n}'
        log.info('saving %s', st)
        try:
            if type_ == 'SecureString':
                ssm.put_parameter(
                    Name=st,
                    Description='sewer / certbot',
                    Value=x,
                    Overwrite=True,
                    Type=type_,
                    KeyId=f'alias/{ns}')
            else:
                ssm.put_parameter(
                    Name=st,
                    Description='sewer / certbot',
                    Value=x,
                    Overwrite=True,
                    Type=type_)
        except Exception as ex:  # pylint: disable=broad-except
            log.info('exception saving to ssm: %s', ex)


@task
def install_cert(ctx, config, hostname=None):
    """
    installs a cert on the local system:

        on linux to /etc/ssl/certs
        on windows to cert:/localmachine/my
    """
    with open(config, 'r') as f:
        conf = yaml.load(f, Loader=yaml.SafeLoader)
    ns = conf['namespace']
    profile = conf.get('profile')
    owner = conf.get('owner', 'root')
    group = conf.get('group', owner)
    cert_filename = conf.get('certificate')
    key_filename = conf.get('key')
    hostname = hostname or conf.get('hostname')
    pfx_password = conf.get('pfx_password')
    bucket = conf.get('bucket')
    if not hostname:
        hostname = get_hostname(ctx)
    if is_linux():
        install_cert_on_linux(
            ctx, ns, hostname, profile,
            cert_filename, key_filename, owner, group, bucket=bucket)
    elif is_windows():
        install_cert_on_windows(ctx, bucket, hostname, profile, pfx_password)


def get_hostname(ctx):
    if is_linux():
        result = ctx.run('/bin/hostname')
        return result.stdout.strip()
    if is_windows():
        result = socket.getfqdn()
        return result
    return None


def install_cert_on_linux(
        ctx, ns, hostname, profile, cert_filename, key_filename,
        owner, group, bucket=None):
    if bucket:
        certificate, _, key = get_certificate_from_s3(bucket, ns, hostname, profile)
    else:
        certificate, _, key = get_certificate(ns, hostname, profile)
    if not cert_filename:
        st = f'{hostname}.bundled.crt'
        cert_filename = os.path.join('/etc/ssl/certs', st)
    if not key_filename:
        key_filename = os.path.join('/etc/ssl/private', f'{hostname}.key')
    with open(cert_filename, 'w') as f:
        f.write(certificate)
    ctx.run(f'chmod 0644 {cert_filename}')
    ctx.run(f'chown {owner}:{group} {cert_filename}')
    with open(key_filename, 'w', encoding='utf-8') as f:
        f.write(key)
    ctx.run(f'chmod 0600 {key_filename}')
    ctx.run(f'chown {owner}:{group} {key_filename}')


def windows_version(ctx):
    import clr
    from Microsoft.Win32 import Registry
    from Microsoft.Win32 import RegistryHive
    key = r'SOFTWARE\Microsoft\Windows NT\CurrentVersion'
    current_version = Registry.LocalMachine.OpenSubKey(key)
    try:
        product_name = current_version.GetValue('ProductName')
        version = product_name.strip()
    except:  # noqa: E722, pylint: disable=bare-except
        version = None
    finally:
        current_version.Close()
    return version


@task
def install_cert_on_windows(
        ctx, bucket, key, profile, pfx_password=None, store=None):
    """
    pull a file from s3 and install in the localmachine/my cert store
    """
    import platform
    from cryptography.hazmat.primitives.serialization import pkcs12
    from cryptography.hazmat.primitives import hashes
    print('getting cert')
    pfx_data = get_pfx(bucket, key, profile)
    print('getting thumbprint')
    key, cert, chain = pkcs12.load_key_and_certificates(pfx_data, pfx_password)
    thumbprint = cert.fingerprint(hashes.SHA1()).hex().upper()
    f = NamedTemporaryFile(mode='w', delete=False)  # pylint: disable=consider-using-with
    filename = f.name
    print(f'importing pfx to cert store from {filename}')
    with open(filename, 'wb') as f:
        f.write(pfx_data)
    cmdlet = ''
    e = {}
    if not pfx_password and platform.release().startswith('2008'):
        chars = '0123456789abcdefghijklmnopqrstuvwxyz'
        pfx_password = [ random.choice(chars) for _ in range(16) ]
        pfx_password = ''.join(pfx_password)
        print(f'regenerating cert with password: {pfx_password}')
        pfx_data = full_pfx(ctx, cert, key, pfx_password, chain=chain, legacy=True)
        with open(filename, 'wb') as f:
            f.write(pfx_data)
    if pfx_password:
        password = '-password (ConvertTo-SecureString -f -a $env:SEDGE_PASSWORD)'
        e['SEDGE_PASSWORD'] = pfx_password
    else:
        password = "-password $null"
    if store:
        store_arg = rf"-certstorelocation 'cert:\localmachine\{store}'"
    else:
        store_arg = r'-certstorelocation cert:\localmachine\my'
    if platform.release().startswith('2008'):
        cmdlet = """
        using namespace System.Security.Cryptography.X509Certificates
        function Import-PfxCertificate {
            param([string]$filepath
              , [string]$root_store = 'localmachine'
              , [string]$store = 'My'
              , [security.securestring]$password = $null)
            Write-Host "importing $filepath"
            $pfx = new-object X509Certificate2
            $flags = [X509KeyStorageFlags]::Exportable
            $flags = $flags -bor [X509KeyStorageFlags]::MachineKeySet
            $flags = $flags -bor [X509KeyStorageFlags]::PersistKeySet
            $pfx.import($filepath, $password, $flags)
            $p = new-object X509Store($store, $root_store)
            $p.open('MaxAllowed')
            $exists = $false
            foreach ($x in $p.certificates) {
                if ($x.thumbprint -eq $pfx.thumbprint) {
                    Write-Host 'cert already exists in cert store'
                    $exists = $true
                }
            }
            if (!($exists)) {
                $p.add($pfx)
            }
            $p.close()
            return $pfx.thumbprint
        }
        """
        store_arg = ''
    lines = [
        cmdlet,
        f"$t = Import-PfxCertificate -filepath '{filename}' {password} "
        f"{store_arg}",
        'Write-Host $t',
    ]
    c = '\n'.join(lines)
    ctx.run(c, env=e)
    print(f'removing {filename}')
    os.remove(filename)
    return thumbprint


def is_linux():
    return sys.platform == 'linux'


def is_windows():
    return sys.platform == 'win32'


@task
def create_account_key(ctx, filename):
    """
    creates an account key and saves it to filename
    """
    import OpenSSL
    key_type = OpenSSL.crypto.TYPE_RSA
    key = OpenSSL.crypto.PKey()
    key.generate_key(key_type, 2048)
    st = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
    with open(filename, 'w') as f:
        f.write(st.decode())
