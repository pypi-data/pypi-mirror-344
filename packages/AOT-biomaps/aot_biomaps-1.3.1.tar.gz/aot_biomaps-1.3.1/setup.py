from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys
import os

class CustomInstallCommand(install):
    def run(self):
        install.run(self)  # Run the standard install process
        subprocess.check_call([sys.executable, os.path.join(os.path.dirname(__file__), 'AOT_biomaps', 'post_install.py')])

setup(
    name='AOT_biomaps',
    version='1.3.1',
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
