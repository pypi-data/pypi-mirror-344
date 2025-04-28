from setuptools import setup, find_packages

setup(
    name='AOT_biomaps',
    version='1.2.9',
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
    entry_points={
        'console_scripts': [
            'post_install_aot=AOT_biomaps.post_install:main',
        ],
    },
)