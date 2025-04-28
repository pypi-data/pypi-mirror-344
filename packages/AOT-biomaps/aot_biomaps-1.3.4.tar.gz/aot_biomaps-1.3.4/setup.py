from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys
import os

class CustomInstallCommand(install):
    """Customized setuptools install command - runs a script after installation."""
    def run(self):
        
        install.run(self)
        script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'post_install.py')
        subprocess.check_call([sys.executable, script_path])

setup(
    name='AOT_biomaps',
    version='1.3.4',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'k-wave-python',
        'GPUtil'
    ],
    author='Lucas Duclos',
    author_email='lucas.duclos@universite-paris-saclay.fr',
    description='Acousto-Optic Tomography',
    url='https://github.com/LucasDuclos/AcoustoOpticTomography',
    cmdclass={
        'install': CustomInstallCommand,
    },
)
