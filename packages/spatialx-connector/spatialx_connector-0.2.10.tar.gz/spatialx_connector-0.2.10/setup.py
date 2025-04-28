from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

BASE_PACKAGE = "spatialx_connector"
BASE_IMPORT = "spatialx_connector"


def _install_requires():
    return [
        "pydantic==2.7.2",
        "requests==2.32.3",
        "tqdm==4.66.4",
        "zarr== 2.18.2",
        "scanpy==1.11.0",
        "matplotlib==3.10.0",
        "spatialdata==0.2.5",
        "anndata==0.10.8",
    ]


setup(
    name=BASE_PACKAGE,
    version="0.2.10",
    author="BioTuring",
    author_email="support@bioturing.com",
    url="https://alpha.bioturing.com",
    description="BioTuring SpatialX Connector",
    package_dir={BASE_IMPORT: "spatialx_connector"},
    packages=[BASE_IMPORT, *find_packages()],
    zip_safe=False,
    install_requires=_install_requires(),
    long_description=long_description,
    long_description_content_type="text/markdown",
)
