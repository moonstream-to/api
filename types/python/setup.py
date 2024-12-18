from setuptools import find_packages, setup

from moonstreamtypes.version import VERSION

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

setup(
    name="moonstream-types",
    version=VERSION,
    author="Moonstream.to",
    author_email="engineers@moonstream.to",
    license="Apache License 2.0",
    description="Moonstream types for various blockchains.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/moonstream-to/api",
    platforms="all",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    packages=find_packages(),
    package_data={"moonstreamtypes": ["py.typed"]},
    zip_safe=False,
    install_requires=[
        "moonstreamdb>=0.4.5",
        "moonstreamdb-v3>=0.1.2",
    ],
    extras_require={
        "dev": ["black", "isort", "mypy"],
        "distribute": ["setuptools", "twine", "wheel"],
    },
)
