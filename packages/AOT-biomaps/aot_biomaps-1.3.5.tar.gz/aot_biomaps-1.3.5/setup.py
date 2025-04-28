from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys
import os

class CustomInstallCommand(install):
    """Customized setuptools install command - runs a script after installation."""
    def run(self):
        # Run the standard install process
        install.run(self)
        print("Running custom install script...")
        # Run the post-install script
        script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'post_install.py')
        print(f"Executing script at: {script_path}")
        subprocess.check_call([sys.executable, script_path])

setup(
    name='AOT_biomaps',
    version='1.3.5',
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
