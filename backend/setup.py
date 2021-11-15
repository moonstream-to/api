from setuptools import find_packages, setup

from moonstreamapi.version import MOONSTREAMAPI_VERSION

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

setup(
    name="moonstreamapi",
    version=MOONSTREAMAPI_VERSION,
    packages=find_packages(),
    install_requires=[
        "appdirs",
        "boto3",
        "bugout",
        "fastapi",
        "moonstreamdb",
        "humbug",
        "pydantic",
        "pyevmasm",
        "python-dateutil",
        "python-multipart",
        "uvicorn",
        "web3",
    ],
    extras_require={
        "dev": ["black", "isort", "mypy", "types-requests", "types-python-dateutil"],
        "distribute": ["setuptools", "twine", "wheel"],
    },
    package_data={"moonstreamapi": ["py.typed"]},
    zip_safe=False,
    description="The Bugout blockchain inspector API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Bugout.dev",
    author_email="engineering@bugout.dev",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Software Development :: Libraries",
    ],
    url="https://github.com/bugout-dev/moonstream",
    entry_points={"console_scripts": ["mnstr=moonstreamapi.admin.cli:main"]},
)
