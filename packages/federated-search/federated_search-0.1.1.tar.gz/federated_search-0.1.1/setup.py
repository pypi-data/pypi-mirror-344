
from setuptools import setup, find_packages
import os

setup(
    name='federated_search',
    version='0.1.1',
    packages=find_packages(exclude=["venv", "__pycache__"]),
    install_requires=[
        'psycopg2-binary',
        'PyYAML',
       'ollama',
       'sentence-transformers',
       'haystack-ai'
    ],
    author='deepan',
    author_email='deepansundaram@ninjacart.com',
    description='Federated search module with PGVector and reranking support',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
    python_requires='>=3.13',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
