from setuptools import find_packages, setup

from mooncrawl.version import MOONCRAWL_VERSION

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

setup(
    name="mooncrawl",
    version=MOONCRAWL_VERSION,
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
    package_data={"mooncrawl": ["py.typed"]},
    zip_safe=False,
    install_requires=[
        "boto3",
        "bugout>=0.2.13",
        "chardet",
        "fastapi",
        "moonstreamdb>=0.4.5",
        "moonstreamdb-v3>=0.0.16",
        "moonstream-types>=0.0.9",
        "moonstream>=0.1.1",
        "moonworm[moonstream]>=0.9.3",
        "humbug",
        "pydantic==1.9.2",
        "python-dateutil",
        "requests",
        "tqdm",
        "uvicorn",
        "web3==5.27.0",
    ],
    extras_require={
        "dev": ["black", "isort", "mypy", "types-requests", "types-python-dateutil"],
        "distribute": ["setuptools", "twine", "wheel"],
    },
    entry_points={
        "console_scripts": [
            "crawler=mooncrawl.crawler:main",
            "contractcrawler=mooncrawl.contract.cli:main",
            "esd=mooncrawl.esd:main",
            "etherscan=mooncrawl.etherscan:main",
            "identity=mooncrawl.identity:main",
            "generic-crawler=mooncrawl.generic_crawler.cli:main",
            "moonworm-crawler=mooncrawl.moonworm_crawler.cli:main",
            "nft=mooncrawl.nft.cli:main",
            "statistics=mooncrawl.stats_worker.dashboard:main",
            "state-crawler=mooncrawl.state_crawler.cli:main",
            "metadata-crawler=mooncrawl.metadata_crawler.cli:main",
            "custom-crawler=mooncrawl.reports_crawler.cli:main",
            "leaderboards-generator=mooncrawl.leaderboards_generator.cli:main",
        ]
    },
)
