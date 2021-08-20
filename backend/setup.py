from setuptools import find_packages, setup

from moonstream.version import MOONSTREAM_VERSION

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

setup(
    name="moonstream",
    version=MOONSTREAM_VERSION,
    packages=find_packages(),
    install_requires=["boto3", "bugout >= 0.1.17", "fastapi", "uvicorn"],
    extras_require={
        "dev": ["black", "mypy"],
        "distribute": ["setuptools", "twine", "wheel"],
    },
    package_data={"moonstream": ["py.typed"]},
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
    entry_points={"console_scripts": ["mnstr=moonstream.admin.cli:main"]},
)
