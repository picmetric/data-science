import subprocess

import click


@click.command()
@click.argument('path', default='picmetric')
def cli(path):
    cmd = 'python startmm.py'
    return subprocess.call(cmd, shell=True)
