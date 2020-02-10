import click
from OpenSSL import crypto
import sys


@click.command()
@click.option('-f', '--path-pfx-file', default='', help="Path to pfx file.")
@click.option('-p', '--password', default='', help="Password phrase.")
def check_pfx(path_pfx_file, password):
    p12 = crypto.load_pkcs12(open(path_pfx_file, 'rb').read(), password)
    click.echo(crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey()))
    click.echo(crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate()))
    click.echo(path_pfx_file)


def main():
    check_pfx()


if __name__ == '__main__':
    main()