import click
from OpenSSL import crypto
import sys


# @click.command()
# @click.option('--verbose', is_flag=True, help="Will print verbose messages.")
# def cli(verbose):
#     if verbose:
#         click.echo("We are in the verbose mode.")
#     click.echo("Hello World")


# @click.command()
# @click.option('-p', '--string_to_echo', help="Path to pfx file.")
# def echo(string_to_echo):
#     click.echo(string_to_echo)


@click.command()
#@click.option(-)
@click.option('-f', '--path-pfx-file', default='', help="Path to pfx file.")
@click.option('-p', '--password', default='', help="Password phrase.")
def check_pfx(path_pfx_file, password):
    p12 = crypto.load_pkcs12(open(path_pfx_file, 'rb').read(), password)
    click.echo(crypto.dump_privatekey(crypto.FILETYPE_PEM, p12.get_privatekey()))
    click.echo(crypto.dump_certificate(crypto.FILETYPE_PEM, p12.get_certificate()))
    click.echo(path_pfx_file)


def main():
    # cli()
    # echo()
    check_pfx()


if __name__ == '__main__':
    main()