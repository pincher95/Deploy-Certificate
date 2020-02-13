import click
from OpenSSL import crypto
from jumpssh import SSHSession


@click.command()
@click.option('-f', '--path-pfx-file', default='', help="Path to pfx file.")
@click.option('-p', '--password', default='', help="pfx password.")
@click.option('-r', '--remote-host', default='', help="Remote Host.")
# @click.option('-t', '--file-type', type=click.Choice(['PFX', 'PEM'], case_sensitive=False))
@click.option('-b', '--bastion', default='192.168.2.200', help="Bastion host.", show_default=True)
def check_pfx(path_pfx_file, password, bastion, remote_host):
    p12 = crypto.load_pkcs12(open(path_pfx_file, 'rb').read(), password)
    click.echo(crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey()))
    click.echo(crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate()))
    private_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey())
    public_certificate = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate())
    # ca_certificate = crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_ca_certificates())
    # click.echo(path_pfx_file)
    # remote_ssl_backup(bastion, remote_host)
    gateway_session = SSHSession(host=bastion, port=7022, password=None,
                                 missing_host_key_policy=None, username='support')
    remote_session = gateway_session.get_remote_session(remote_host, password=None, username='root', port=7022)
    print(remote_session.get_cmd_output('ls -lta'))

# def remote_ssl_backup(bastion, remote_host):
#     click.echo(bastion)
#     click.echo(remote_host)
# gateway_session = SSHSession(private_key_file='', host=bastion, port=7022, password=None, missing_host_key_policy='')
    remote_session.close()
    gateway_session.close()

def main():
    check_pfx()


if __name__ == '__main__':
    main()
