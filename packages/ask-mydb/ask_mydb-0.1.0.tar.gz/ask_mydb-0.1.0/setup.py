from setuptools import setup, find_packages

setup(
    name='askdb',
    version='0.1.0',
    author='Shanthosh',
    description='A simple and efficient database for storing and querying data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=["tests","examples"]),
    install_requires = [
        'sqlalchemy',
        'ollama',
        'openai',
    ]
)