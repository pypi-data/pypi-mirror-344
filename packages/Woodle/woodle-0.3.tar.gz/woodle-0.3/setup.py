from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

requires = [
    'pandas',
    'xlrd==1.2.0',
    'openpyxl'
]

setup(
    name="Woodle",
    version="0.3",
    description="Outil pour trnsformer un fichier de notes Moodle en fichier SNW.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/Epithumia/Woodle",
    packages=['woodle'],
    install_requires=requires,
    entry_points={
        'console_scripts': ['woodle=woodle.woodle:main'],
    }
)
