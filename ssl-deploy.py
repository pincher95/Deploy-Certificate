import click
from OpenSSL import crypto
from jumpssh import SSHSession


@click.command()
@click.option('-f', '--path-pfx-file', default='', help="Path to pfx file.")
@click.option('-p', '--password', default='', help="pfx password.")
@click.option('-r', '--remote-host', default='', help="Remote Host.")
@click.option('-b', '--bastion', default='192.168.2.200', help="Bastion host.", show_default=True)
def check_pfx(path_pfx_file, password, bastion, remote_host):
    p12 = crypto.load_pkcs12(open(path_pfx_file, 'rb').read(), password)
    private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
    public_certificate = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())
    # try:
    #     ca_certificate = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_ca_certificates())

    gateway_session = SSHSession(host=bastion, port=7022, password=None,
                                 missing_host_key_policy=None, username='support')
    remote_session = gateway_session.get_remote_session(remote_host, password=None, username='root', port=7022)
    remote_session.put('./remote_backup.sh', '/root/remote_backup.sh', owner='root', permissions='0700')
    remote_session.run_cmd('/root/remote_backup.sh')
    remote_session.file(remote_path='/etc/apache/passl/pa.cert.key', content=private_key, owner='root',
                        permissions='644')
    remote_session.file(remote_path='/etc/apache/passl/pa.cert.cert', content=public_certificate, owner='root',
                        permissions='644')
    # remote_session.file(remote_path='/etc/apache/passl/pa.cert.intermediate', content=ca_certificate, owner='root',
    #                     permissions='644')
    print(remote_session.get_cmd_output('ls -alh'))
    print(remote_session.get_cmd_output("ls -alh /etc/apache/passl/backup-$(date +'%F')"))
    print(remote_session.get_cmd_output('ls -alh /var/qmail/control/'))

    remote_session.close()
    gateway_session.close()


def main():
    check_pfx()


if __name__ == '__main__':
    main()
