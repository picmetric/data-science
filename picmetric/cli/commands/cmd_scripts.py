import subprocess, click, os

@click.command()
@click.argument('path', default='picmetric')
def cli(path):
    # needs to be dependent on FLASK_ENV

    # For runnin locally
    # full_path = os.path.join('scripts', path)

    # for docker
    full_path = os.path.join('data-science', 'picmetric', 'scripts', path)
    cmd = f'python {full_path}'

    # for adjusting file path from inside docker
    # cmd = 'python -c "import os; print(os.getcwd())"'
    return subprocess.call(cmd, shell=True)
