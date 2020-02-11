import click
from OpenSSL import crypto
from jumpssh import SSHSession


@click.command()
@click.option('-f', '--path-pfx-file', default='', help="Path to pfx file.")
@click.option('-p', '--password', default='', help="Password phrase.")
@click.option('-r','--remote-host',help="Remote Host.")
@click.option('-b', '--bastion', defaulf="192.168.2.200", help="Bastion host.")
def check_pfx(path_pfx_file, password, bastion, remote_host):
    p12 = crypto.load_pkcs12(open(path_pfx_file, 'rb').read(), password)
    click.echo(crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey()))
    click.echo(crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate()))
    # click.echo(path_pfx_file)
    remote_ssl_backup(bastion, remote_host)


def remote_ssl_backup(bastion, remote_host):
    gateway_session = SSHSession(private_key_file='', host=bastion, port=7022, password=None,missing_host_key_policy='')


def main():
    check_pfx()


if __name__ == '__main__':
    main()