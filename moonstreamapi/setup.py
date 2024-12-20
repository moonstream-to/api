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
        "bugout>=0.2.15",
        "fastapi",
        "moonstream",
        "moonstreamdb>=0.4.5",
        "moonstreamdb-v3>=0.1.2",
        "moonstream-types>=0.0.9",
        "humbug",
        "pydantic==1.10.2",
        "pyevmasm",
        "python-dateutil",
        "python-multipart",
        "python-slugify",
        "uvicorn",
        "web3>=5.30.0, <6",
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
