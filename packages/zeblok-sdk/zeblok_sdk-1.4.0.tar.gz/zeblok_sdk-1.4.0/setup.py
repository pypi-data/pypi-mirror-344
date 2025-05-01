from pip._internal.req import parse_requirements
from setuptools import setup, find_packages
from pathlib import Path
import zeblok

DESCRIPTION = 'Zeblok Python SDK'
LONG_DESCRIPTION = (Path(__file__).parent / "README.md").read_text()

setup(
    name="zeblok-sdk",
    version=zeblok.__version__,
    author="Karan Pathak",
    author_email="karan@dataturtles.com",
    maintainer='Zeblok, Karan Pathak',
    maintainer_email='zeblok@zeblok.com, karan.pathak@zeblok.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url="",
    packages=find_packages(),
    install_requires=[item.requirement for item in parse_requirements('requirements.txt', session=False)],
    python_requires=">=3.9",
    keywords=['zeblok', 'python-sdk', 'zeblok-sdk'],
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
