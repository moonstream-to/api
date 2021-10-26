from setuptools import find_packages, setup

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

setup(
    name="moonstream",
    version="0.0.2",
    packages=find_packages(),
    package_data={"moonstream": ["py.typed"]},
    install_requires=["requests", "dataclasses; python_version=='3.6'"],
    extras_require={
        "dev": [
            "black",
            "isort",
            "mypy",
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
)
