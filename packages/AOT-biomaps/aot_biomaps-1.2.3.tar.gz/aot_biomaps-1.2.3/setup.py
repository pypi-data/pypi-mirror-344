from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys

class CustomInstall(install):
    def run(self):
        # Run the standard install process
        install.run(self)
        # Run the script to install CuPy
        subprocess.run([sys.executable, 'AOT_biomaps/install_cupy.py'], check=True)


setup(
    name='AOT_biomaps',
    version='1.2.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'k-wave-python',
        'GPUtil'
    ],
    author='Lucas Duclos',
    author_email='lucas.duclos@universite-paris-saclay.fr',
    description='Acousto-Optic Tomography',
    long_description=open('C:/Users/duclos/Desktop/AcoustoOpticTomography/TomographyAcoustoOptic/README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/LucasDuclos/AcoustoOpticTomography',
        cmdclass={
        'install': CustomInstall,
    },
)
