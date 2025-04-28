from setuptools import setup, find_packages

setup(
    name='AOT_biomaps',
    version='1.3.6',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'k-wave-python',
        'GPUtil',
        'cupy',
    ],
    author='Lucas Duclos',
    author_email='lucas.duclos@universite-paris-saclay.fr',
    description='Acousto-Optic Tomography',
    url='https://github.com/LucasDuclos/AcoustoOpticTomography',
)
