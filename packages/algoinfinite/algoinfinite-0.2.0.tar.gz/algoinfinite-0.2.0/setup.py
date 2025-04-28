from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="algoinfinite",
    version="0.2.0",
    author="Madan Mohan Behera",
    author_email="madanmohan14072002@gmail.com",
    description="A collection of algorithms and data structures in Python.",
    packages=find_packages(),
    license="MIT",
    install_requires=[
        "collections",
        "heapq",
        "math",
    ],
    keywords=[
        "algorithms",
        "data structures",
        "python",
        "algoinfinite",
        "sorting",
        "searching",
        "dynamic programming",
        "greedy algorithms",
    ],
    entry_points={
        "console_scripts":[
            "madan-hello = algoinfinite:hello",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)

