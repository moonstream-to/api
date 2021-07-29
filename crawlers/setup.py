from setuptools import find_packages, setup

from moonstreamcrawlers.version import MOONSTREAMCRAWLERS_VERSION

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

setup(
    name="moonstreamcrawlers",
    version=MOONSTREAMCRAWLERS_VERSION,
    author="Bugout.dev",
    author_email="engineers@bugout.dev",
    license="Apache License 2.0",
    description="Moonstream crawlers",
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
    python_requires=">=3.6",
    packages=find_packages(),
    package_data={"moonstreamcrawlers": ["py.typed"]},
    zip_safe=False,
    install_requires=[
        "moonstreamdb @ git+https://git@github.com/bugout-dev/moonstream.git@a52a2b94533699927d555e050da2807adea4ba12#egg=moonstreamdb&subdirectory=db",
        "requests",
        "tqdm",
        "web3",
    ],
    extras_require={"dev": ["black", "mypy", "types-requests"]},
    entry_points={
        "console_scripts": ["moonstreamcrawlers=moonstreamcrawlers.cli:main"]
    },
)
