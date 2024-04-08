from setuptools import find_packages, setup

from moonstreamdbv3.version import VERSION

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

setup(
    name="moonstreamdb-v3",
    version=VERSION,
    author="Bugout.dev",
    author_email="engineers@bugout.dev",
    license="Apache License 2.0",
    description="Moonstream V3 database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bugout-dev/moonstream",
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
    package_data={"moonstreamdbv3": ["py.typed"]},
    zip_safe=False,
    install_requires=["alembic", "psycopg2-binary", "sqlalchemy>=2.0.4"],
    extras_require={
        "dev": ["black", "isort", "mypy"],
        "distribute": ["setuptools", "twine", "wheel"],
    },
)
