from setuptools import find_packages, setup

from moonstream.version import MOONSTREAM_CLIENT_VERSION

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

setup(
    name="moonstream",
    version=MOONSTREAM_CLIENT_VERSION,
    packages=find_packages(),
    package_data={"moonstream": ["py.typed"]},
    install_requires=["requests", "pydantic", "dataclasses; python_version=='3.6'"],
    extras_require={
        "aws": ["boto3"],
        "dev": [
            "black",
            "mypy",
            "isort",
            "wheel",
            "types-requests",
            "types-dataclasses",
        ],
        "distribute": ["setuptools", "twine", "wheel"],
    },
    description="Moonstream: Open source blockchain analytics",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Moonstream",
    author_email="engineering@moonstream.to",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries",
    ],
    url="https://github.com/bugout-dev/moonstream",
    entry_points={"console_scripts": ["moonstream=moonstream.cli:main"]},
)
