"""
Module for reading and parsing service metadata files.
"""

import os.path
import importlib
import json
from typing import Optional

from bisslog_schema.service_info import ServiceInfo

default_path_options = (
    "./metadata.yml",
    "./docs/metadata.yml",
    "./metadata.json",
    "./docs/metadata.json",
    "./metadata.yaml",
    "./docs/metadata.yaml",
)


def read_service_metadata(path: Optional[str] = None, encoding: str = "utf-8") -> ServiceInfo:
    """Read service metadata from a YAML or JSON file and parse it into a ServiceInfo object.

    If a path is provided, the function validates and reads the file. If no path is given,
    it attempts to find a file from a set of default path options.

    Parameters
    ----------
    path : Optional[str], default=None
        The specific file path to read. If None, searches default paths.
    encoding : str, default="utf-8"
        The file encoding to use when reading the file.

    Returns
    -------
    ServiceInfo
        The parsed service metadata as a ServiceInfo object.

    Raises
    ------
    ValueError
        If the given path does not exist or if no default file is found.
    """
    if path is not None:
        if not os.path.isfile(path):
            raise ValueError(f"Path {path} of metadata does not exist")
    else:
        for path_option in default_path_options:
            if os.path.isfile(path_option):
                path = path_option
                break
        if path is None:
            raise ValueError("No compatible default path could be found")

    with open(path, "r", encoding=encoding) as file:
        if path.endswith(".yml") or path.endswith(".yaml"):
            yaml = importlib.import_module("yaml")
            data = yaml.safe_load(file)
        elif path.endswith(".json"):
            data = json.load(file)
        else:
            raise ValueError("Unsupported file format: only YAML or JSON are allowed.")

    return ServiceInfo.from_dict(data)
