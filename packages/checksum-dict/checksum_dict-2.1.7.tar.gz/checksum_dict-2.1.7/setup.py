from glob import glob
from pathlib import Path
from setuptools import setup, find_packages

from mypyc.build import mypycify

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="checksum_dict",
    description="checksum_dict's objects handle the simple but repetitive task of checksumming addresses before setting/getting dictionary values.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="BobTheBuidler",
    author_email="bobthebuidlerdefi@gmail.com",
    url="https://github.com/BobTheBuidler/checksum_dict",
    packages=find_packages(),
    use_scm_version={
        "root": ".",
        "relative_to": __file__,
        "local_scheme": "no-local-version",
        "version_scheme": "python-simplified-semver",
    },
    setup_requires=["setuptools_scm"],
    install_requires=["cchecksum>=0.0.3", "mypy_extensions>=0.4.2"],
    package_data={"checksum_dict": ["py.typed"]},
    include_package_data=True,
    ext_modules=mypycify(
        [
            "checksum_dict/_utils.py",
            "checksum_dict/base.py",
            "checksum_dict/default.py",
            "--strict",
            "--pretty",
            "--install-types",
            "--disable-error-code=unused-ignore",
            "--disable-error-code=import-not-found",
            "--disable-error-code=import-untyped",
            "--disable-error-code=attr-defined",
            "--disable-error-code=no-any-return",
        ],
    ),
    zip_safe=False,
)
