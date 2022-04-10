from setuptools import find_packages, setup

setup(
    author="Zackary Troop",
    name="py3grok",
    version="0.1.0",
    url="https://github.com/ztroop/py3grok",
    license="MIT",
    description="Parse strings and extract information from structured or unstructured data.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "regex>=2022.3.15",
    ],
    python_requires=">=3.7.*",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
