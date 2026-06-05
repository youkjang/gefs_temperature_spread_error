from setuptools import setup, find_packages


setup(
    name="gefs-temperature-spread-error",
    version="0.1.0",
    description="GEFS 2-m temperature ensemble spread-error verification project",
    author="Youkyoung Jang",
    packages=find_packages(),
    install_requires=[
        "xarray",
        "numpy",
        "pandas",
        "matplotlib",
        "s3fs",
        "fsspec",
        "cfgrib",
        "eccodes",
    ],
    python_requires=">=3.9",
)
