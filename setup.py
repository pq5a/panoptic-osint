from setuptools import setup, find_packages

setup(
    name="panoptic-osint",
    version="1.0.0",
    description="PANOPTIC — a 27-module open-source intelligence (OSINT) reconnaissance framework.",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "dnspython>=2.4.2",
        "phonenumbers>=8.13.0",
        "exifread>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "panoptic=panoptic.cli:main",
        ],
    },
    python_requires=">=3.8",
)
