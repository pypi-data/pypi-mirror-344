from setuptools import setup, find_packages

setup(
    name='popgen3',
    version='3.0.3',  
    author="Fan Yu",
    author_email="fanyu4@asu.edu",
    description="Population synthesis and sample weighting tool.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/chnfanyu/PopGen",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=6.0",
        "numpy>=1.21.6",
        "pandas>=1.3.0",
        "scipy>=1.10.1",
    ],
    entry_points={
        "console_scripts": [
            "popgen=popgen.project:main"
        ]
    },
    package_data={
        'popgen': ['data/configuration_arizona.yaml', 'data/*.csv'],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
)
