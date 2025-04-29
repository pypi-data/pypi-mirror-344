from pathlib import Path

import setuptools

VERSION = "0.0.1"

NAME = "loynaz"

INSTALL_REQUIRES = [
    "baldor>=0.1.3"
]

setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Compute the Approximate Edge Dominating Set for undirected graph encoded in DIMACS format.",
    url="https://github.com/frankvegadelgado/loynaz",
    project_urls={
        "Source Code": "https://github.com/frankvegadelgado/loynaz",
        "Documentation Research": "https://dev.to/frank_vega_987689489099bf/efficient-edge-dominating-set-approximation-for-sparse-graphs-56d7",
    },
    author="Frank Vega",
    author_email="vega.frank@gmail.com",
    license="MIT License",
    classifiers=[
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
    ],
    python_requires=">=3.10",
    # Requirements
    install_requires=INSTALL_REQUIRES,
    packages=["loynaz"],
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'edge = loynaz.app:main',
            'test_edge = loynaz.test:main',
            'batch_edge = loynaz.batch:main'
        ]
    }
)