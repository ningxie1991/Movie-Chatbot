from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    install_requires = f.read().splitlines()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='speakeasy',
    version='0.1.0',
    description='ATAI Class Project at UZH',
    author='Ning Xie',
    author_email='ning.xie@uzh.ch',
    url='https://github.com/ningxie1991/chatbot',
    license=license,
    install_requires=install_requires,
    packages=find_packages(exclude=('tests', 'docs'))
)

