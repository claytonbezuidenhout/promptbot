import os

from setuptools import setup

cwd = os.path.dirname(__file__)
requirements = open(os.path.join(cwd, 'requirements.txt')).read()
readme = open(os.path.join(cwd, 'README.md')).read()

setup(
    name='promptbot',
    version='0.0.2-alpha.1',
    author='Clayton Bezuidenhout',
    author_email='claytonbez.nl@gmail.com',
    description='A Python package for generating prompt bots on top of OpenAI GTP Apis.',
    long_description=f"""{readme}""",
    long_description_content_type='text/markdown',
    packages=['promptbot'],
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
