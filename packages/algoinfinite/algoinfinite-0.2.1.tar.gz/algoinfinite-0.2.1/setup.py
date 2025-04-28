from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="algoinfinite",
    version="0.2.1",
    author="Madan Mohan Behera",
    author_email="madanmohan14072002@gmail.com",
    description="A collection of algorithms and data structures in Python.",
    packages=find_packages(),
    python_requires='>=3.6',
    url='https://github.com/Madan1500/algoinfinite',
    license="MIT",
    install_requires=[
        # Add any dependencies your package needs here
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
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    entry_points={
        "console_scripts":[
            "madan-hello = algoinfinite:hello",
        ],
    },
    long_description=long_description,
    long_description_content_type="text/markdown",
)

