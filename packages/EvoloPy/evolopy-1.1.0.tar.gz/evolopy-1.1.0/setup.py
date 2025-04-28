from setuptools import setup, find_packages

# Read the contents of README.md file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='EvoloPy',
    version='1.1.0',
    description='An open source nature-inspired optimization toolbox for global optimization in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='EvoloPy Team',
    author_email='raneem.qaddoura@gmail.com',
    url='https://github.com/7ossam81/EvoloPy',
    # Explicitly specify package directories to ensure proper capitalization
    package_dir={'EvoloPy': 'EvoloPy'},
    packages=['EvoloPy', 'EvoloPy.optimizers'],
    include_package_data=True,
    install_requires=[
        'numpy>=1.19.0',
        'pandas>=1.0.0',
        'scipy>=1.5.0',
        'matplotlib>=3.3.0',
        'scikit-learn>=0.23.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
    ],
    python_requires='>=3.6',
    keywords='optimization, metaheuristic, nature-inspired, swarm-intelligence, evolutionary-algorithms',
    project_urls={
        'Source': 'https://github.com/7ossam81/EvoloPy',
        'Documentation': 'https://github.com/7ossam81/EvoloPy/wiki',
        'Bug Reports': 'https://github.com/7ossam81/EvoloPy/issues',
    },
    entry_points={
        'console_scripts': [
            'evolopy-run=EvoloPy.cli:run_cli',
        ],
    },
)