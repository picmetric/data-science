import subprocess, click, os

@click.command()
@click.argument('path', default='picmetric')
def cli(path):
    full_path = os.path.join(os.path.dirname(__file__), 'picmetric', 'scripts', path)
    cmd = f'python {full_path}'
    return subprocess.call(cmd, shell=True)
