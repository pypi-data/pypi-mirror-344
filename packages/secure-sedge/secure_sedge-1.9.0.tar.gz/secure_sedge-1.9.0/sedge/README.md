# secure sedge

`sedge` is a collection of convocations that are designed
to serve the following purpose(s):

1. allows you to request certs
   from letsencrypt and then upload them to s3

2. allow individual servers to pull their individual certs from
   s3 and install them on both linux
   and windows.

3. that's it.

sedge is tightly integrated with aws and makes use of route53 and s3 
via ``boto3``.

## setup and installation

1. make sure you have python 3.8 installed

    a. ubuntu

        sudo apt -y update
        sudo add-apt-repository -y ppa:deadsnakes/ppa
        sudo apt -qq update
        sudo apt -y install python3.8 python3.8-dev python3.8-venv

    b. powershell

        choco install -y python3 --version 3.8.4 --params "/installdir:c:\python38"
        $mac = [System.EnvironmentVariableTarget]::Machine
        $path = [system.environment]::getenvironmentvariable('path', $mac)
        $path = "${path};c:\python38;c:\python38\scripts"
        [system.environment]::setenvironmentvariable('path', $path, $mac)

2. install secure_sedge using pip

        pip install secure_sedge


3. create one or more config file on your keystore

        mkdir -p /etc/sedge
        sudo chown -R sedge:sedge /etc/sedge

    in a file called `defaults.yml` we can specify defaults to use for all
    certs.  and then one yaml file per cert that we want sedge to renew.

        ---
        # the namespaces key will specify all of the namespaces in ssm
        # parameter store that the cert will be saved into
        namespaces:
          - dev
          - staging
            
        # the name of the profile in aws that we want to use
        profile: contoso
            
        # the primary hostname / subject identifier for the cert
        # we can specify a wildcard here, but no ip addresses
        hostname: computer.contoso.com
        bucket: keystore.contoso.com  
        buckets:
          - name: keystore.fabrikam.com
            assume_role: arn:aws:iam::0123456789:role/fabrikam-keystore 
          - name: keystore.example.com
            profile: example_profile

        # if dns is hosted in cloudflare, use the cloudflare_token parameter 
        cloudflare_token: token1  

        tmp_dir: /u/sedge_temp
        # any subject alternative domains that we also want secured by the cert
        # n.b., there can't be overlapping domains like having a wildcard
        # for the hostname and then a specific host.
        alt_domains:
          - computer.fabrikam.com
         

    certs created by `renew_all` will be stored in s3 at the following path:
    `s3://namespace/hostname.crt` and the private key will be
    stored at `s3://namespace/hostname.key`.

4. on the system on which the cert will be installed, use sedge to 
   download the cert from s3

   ```powershell
   sedge.exe install.rds --bucket bucket --key path/to/hostname.pfx
   ```

5. set up a cron job or scheduled task on your keystore to renew certs

        /path/to/sedge renew_all -d /path/to/config/dir

6. set up a cron job or scheduled task on your server to pull down the
   cert from ssm at regular intervals and install it

        /path/to/sedge install_cert -c /path/to/config/file

## aws permissions

Here is the recommended aws policy that you can setup for using sedge
with a particular route53 domain (below is in cloudformation-style yaml)

```yaml
  PolicyDocument:
    Version: "2012-10-17"
    Statement:
      - Effect: "Allow"
        Resource: "*"
        Action:
          - "route53:listhostedzones"
          - "route53:gethostedzone"
          - "route53:gethostedzonecount"
          - "route53:getchange"
          - "route53:listhostedzonesbyname"
          - "route53:listresourcerecordsets"
      - Effect: "Allow"
        Resource: !Sub "arn:aws:route53:::hostedzone/${HostedZoneId}"
        Action:
          - "route53:changeresourcerecordsets"
          - "route53:listresourcerecordsets"
      - Effect: "Allow"
        Resource:
          - !Sub "arn:aws:s3:::${Bucket}"
        Action:
          - "s3:ListBucket"
          - "s3:GetBucketLocation"
          - "s3:ListBucketMultipartUploads"
          - "s3:ListBucketVersions"
      - Effect: Allow
        Resource:
          - !Sub "arn:aws:s3:::${Bucket}/*"
        Action:
          - "s3:GetObject"
          - "s3:PutObject*"
          - "s3:DeleteObject"
          - "s3:AbortMultipartUpload"
          - "s3:ListMultipartUploadParts"
```

