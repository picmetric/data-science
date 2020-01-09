import subprocess, click, os

@click.command()
@click.argument('path', default='picmetric')
def cli(path):

    cmd = f'python {os.path.join('scripts', path+'.py')}'

    return subprocess.call(cmd, shell=True)
