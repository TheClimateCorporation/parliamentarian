"""Setup script for parliament"""
import os
import re

from setuptools import find_packages, setup


HERE = os.path.dirname(__file__)
VERSION_RE = re.compile(r"""__version__ = ['"]([0-9.]+)['"]""")
TESTS_REQUIRE = ["coverage", "nose"]


def get_version():
    init = open(os.path.join(HERE, "parliamentarian", "__init__.py")).read()
    return VERSION_RE.search(init).group(1)


def get_description():
    return open(
        os.path.join(os.path.abspath(HERE), "README.md"), encoding="utf-8"
    ).read()


setup(
    name="parliamentarian",
    version=get_version(),
    author="Climate LLC",
    author_email="cloudeng@climate.com",
    description=("parliamentarian audits your AWS IAM policies"),
    long_description=get_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/TheClimateCorporation/parliamentarian",
    entry_points={"console_scripts": "parliamentarian=parliamentarian.cli:main"},
    test_suite="tests/unit",
    tests_require=TESTS_REQUIRE,
    extras_require={"dev": TESTS_REQUIRE + ["autoflake", "autopep8", "pylint"]},
    install_requires=["boto3", "jmespath", "pyyaml", "json-cfg"],
    setup_requires=["nose"],
    packages=find_packages(exclude=["tests*"]),
    package_data={
        "parliamentarian": ["iam_definition.json", "config.yaml"],
        "parliamentarian.community_auditors": ["config_override.yaml"],
    },
    zip_safe=True,
    license="BSD 3",
    keywords="aws parliamentarian iam lint audit",
    python_requires=">=3.6",
    classifiers=[
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3 :: Only",
        "Development Status :: 5 - Production/Stable",
    ],
)
