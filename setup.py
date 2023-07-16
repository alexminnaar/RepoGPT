from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='repogpt',
    version='1.0.0',
    author='Alex Minnaar',
    description='An LLM-based coding mentor for your repository',
    url='https://github.com/alexminnaar/RepoGPT',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'repogpt-cli=repogpt.cli.cli:main'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)
