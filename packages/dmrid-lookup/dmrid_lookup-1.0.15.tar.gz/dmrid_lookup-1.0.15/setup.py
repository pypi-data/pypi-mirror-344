from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dmrid_lookup",
    version="1.0.15",
    author="Mark Cohen",
    author_email="k6ef@k6ef.net",
    description="A Python package for looking up DMR IDs from radioid.net",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/k6ef/dmrid_lookup",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
        "rich>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "dmrid_lookup=dmrid_lookup:main",
        ],
    },
)

