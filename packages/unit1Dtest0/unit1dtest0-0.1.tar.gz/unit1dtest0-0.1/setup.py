from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as f:
        return f.read().splitlines()

required = parse_requirements('requirements.txt')

setup(
    name='unit1Dtest0',
    version='0.1',
    packages=find_packages(),
    install_requires=required,  # Dipendenze dal file requirements.txt
    description='Una breve descrizione del progetto',
    long_description="TEST",
    long_description_content_type='text/markdown',
    author='Il tuo nome',
    author_email='tuo@email.com',
    url='https://github.com/username/unit1Dtest0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'unit1Dtest0=unit1Dtest0.start:main',
        ],
    },
)

