from setuptools import setup, find_packages

setup(
    name='rpitx-control',
    version='0.4',
    description='Expansion board management application for working with rpitx and rpitx-ui',
    author='Ihar Yatsevich',
    author_email='igor.nikolaevich.96@gmail.com',
    license='GPL-3.0',
    url='https://github.com/IgrikXD/rpitx-expansion-board',
    packages=find_packages(),
    package_data={
        'ControlApplication': [
            'AmplifiersList/*.csv',
            'FiltersList/*.csv',
        ]
    },
    install_requires=[
        'colorama',
        'gpiozero',
        'pandas',
        'whiptail-dialogs @ https://github.com/IgrikXD/whiptail-dialogs/archive/master.tar.gz',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rpitx-control = ControlApplication.main:main',
        ],
    }
)