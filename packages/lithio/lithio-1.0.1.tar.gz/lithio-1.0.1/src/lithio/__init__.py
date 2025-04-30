from lithio.cli import *
import os

__version__ = "0.1.0"

__author__ = "voyager-2021"

__all__ = [
    "install_directory",
    "install_file",
    "install",
    "set_attributes",
    "strip_binary",
    "resolve_group",
    "resolve_user",
    "compute_checksum",
    "verify_checksum",
    "load_checksums",
    "app",
]

if __name__ == '__main__':
    app()
