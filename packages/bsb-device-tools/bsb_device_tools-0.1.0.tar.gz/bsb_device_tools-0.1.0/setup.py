# setup.py
from setuptools import setup, find_packages

setup(
    name='bsb-device-tools',
    version='0.1.0',
    author='Your Name',
    author_email='shawponsp6@gmail.com',
    description='Remote control tools for office devices (token-authenticated, encrypted)',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/BlackSpammerBd/bsb-device-tools',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'click',
        'colorama',
        'cryptography'
    ],
    entry_points={
        'console_scripts': [
            'bsb = bsb_device_tools.cli:cli',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
