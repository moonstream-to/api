from setuptools import find_packages, setup

long_description = ""
with open("README.md") as ifp:
    long_description = ifp.read()

setup(
    name="moonstream",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "bugout >= 0.1.18",
        "fastapi",
        "humbug>=0.2.7",
        "python-dateutil",
        "uvicorn",
        "types-python-dateutil",
        "types-requests",
    ],
    extras_require={
        "dev": ["black", "isort", "mypy"],
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
