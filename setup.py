from setuptools import setup

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='promptbot',
    version='0.0.1',
    author='Clayton Bezuidenhout',
    author_email='claytonbez.nl@gmail.com',
    description='A Python package for generating prompt bots on top of OpenAI\'s GTP Apis.',
    packages=['promptbot'],
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.9+',
        'License :: MIT License',
        'Operating System :: OS Independent',
    ],
)
