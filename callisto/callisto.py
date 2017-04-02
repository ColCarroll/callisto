import json
import os
import shutil

import click
from jupyter_client import kernelspec

VIRTUAL_ENV_VAR = 'VIRTUAL_ENV'


@click.command()
@click.option('-n', '--name',
              help='Name of kernel.  Must provide a kernel name or run in a virtual environment.',
              default='')
@click.option('-p', '--path', type=click.Path(),
              help='Path to add to the start of PYTHONPATH.', default='')
@click.option('-l', '--list', is_flag=True, help='Get information about the current kernel')
@click.option('-d', '--delete', is_flag=True, help='Delete the existing Jupyter kernel')
def cli(name, path, list, delete):
    """Manage jupyter kernel for this virtual environment."""
    if not in_virtual_env() and not name:
        raise click.UsageError('The environment variable {} is not set (usually this is set '
                               'automatically activating a virtualenv).  Please make sure you are '
                               'in a virtual environment!'.format(VIRTUAL_ENV_VAR))
    if list:
        success, kernel, kernel_path = read_kernel(name)
        if success:
            click.secho('Found kernel "{display_name}" at {kernel_path}:'.format(
                        kernel_path=kernel_path,
                        **kernel), fg='green')
            click.secho(json.dumps(kernel, indent=2))
        else:
            click.secho('No kernel found at {}'.format(kernel_path), fg='red')
    elif delete:
        success, kernel, kernel_path = delete_kernel(name)
        if success:
            click.secho('Deleted jupyter kernel "{display_name}" from {kernel_path}:'.format(
                kernel_path=kernel_path, **kernel), fg='green')
            click.secho(json.dumps(kernel, indent=2))
        else:
            click.secho('No kernel found to delete (checked {})'.format(kernel_path), fg='red')
    else:
        success, kernel, kernel_path = install_kernel(name, click.format_filename(path))
        if success:
            click.secho(
                'Successfully installed a new jupyter kernel "{display_name}":'.format(**kernel),
                fg='green')
            click.secho(json.dumps(kernel, indent=2))
            click.secho('See {} to edit.'.format(kernel_path), fg='green')
        else:
            click.secho('Failed to install a new jupyter kernel "{display_name}".\n'
                        'See {kernel_path} to confirm it isn\'t already there.'.format(
                            kernel_path=kernel_path, **kernel),
                        fg='red')


def in_virtual_env():
    """Check whether script is being run in a virtualenv."""
    return bool(os.getenv(VIRTUAL_ENV_VAR))


def delete_kernel(name):
    """Delete the jupyter kernel for the current virtualenv."""
    success, kernel, kernel_path = read_kernel(name)
    if success:
        shutil.rmtree(os.path.dirname(kernel_path))
    return success, kernel, kernel_path


def read_kernel(name):
    """Get information about the jupyter kernel for the current virtualenv."""
    display_name = get_display_name(name)
    kernel_path = get_kernel_path(display_name)
    if os.path.exists(kernel_path):
        with open(kernel_path, 'r') as buff:
            return True, json.load(buff), kernel_path
    else:
        return False, {}, kernel_path


def install_kernel(name, path):
    """Creates a jupyter kernel using the activated virtual environment."""
    display_name = get_display_name(name)
    executable = get_executable()
    env = get_env(path)
    kernel = get_kernel(display_name, executable, env)
    kernel_path = get_kernel_path(display_name)
    if confirm_kernel_path_is_safe(kernel_path):
        with open(kernel_path, 'w') as buff:
            json.dump(kernel, buff)
        return True, kernel, kernel_path
    return False, kernel, kernel_path


def get_kernel(display_name, executable, env):
    """Formats kernel in necessary format"""
    return {
        'argv': [
            executable,
            '-m',
            'ipykernel',
            '-f',
            '{connection_file}'],
        'display_name': display_name,
        'env': env,
        'language': 'python'
    }


def get_display_name(name):
    """Display name for kernel"""
    if name:
        return name
    return os.path.basename(os.getenv(VIRTUAL_ENV_VAR))


def get_executable():
    """Get the python executable path"""
    return os.path.join(os.getenv(VIRTUAL_ENV_VAR), 'bin', 'python')


def get_env(path):
    """Get any environment variables"""
    if path:
        return {'PYTHONPATH': '{}:PYTHONPATH'.format(path)}
    else:
        return {}


def get_kernel_path(display_name):
    """Convert display name into file-safe name"""
    safe_display = "".join([s if s.isalnum() else "_" for s in display_name])
    filename = os.path.join(safe_display, 'kernel.json')
    return os.path.join(kernelspec.jupyter_data_dir(), 'kernels', filename)


def confirm_kernel_path_is_safe(kernel_path):
    """Make sure necessary directory exists and a kernel with the same name does not exist"""
    if os.path.exists(kernel_path):
        return False
    directory = os.path.dirname(kernel_path)
    if not os.path.isdir(directory):
        os.makedirs(directory)
    return True
