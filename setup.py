import os
from setuptools import setup, find_packages
import shutil

if not os.path.exists('build'):
    os.makedirs('build')
shutil.copyfile('sshh.py', 'build/sshh')

setup(
    name='sshh',
    version='0.0.1',
    description='Easily manage ssh connections',
    author='Xavier Garnier',
    author_email='xavier.garnier@xgaia.fr',
    url='https://github.com/xgaia/sshh',
    download_url='https://github.com/xgaia/sshh/archive/0.0.1.git tar.gz',
    install_requires=['pyyaml'],
    packages=find_packages(),
    license='AGPL',
    platforms='Posix; MacOS X; Windows',
    scripts=["build/sshh"]
)
