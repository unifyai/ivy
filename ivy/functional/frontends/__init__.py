# flake8: noqa
from . import numpy
from . import jax
from . import torch
from . import tensorflow
import importlib

latest_version = {"torch": "1.12"}


def version_extractor(name, version):
    """

    Parameters
    ----------
    name
        the version specific name of the function for which the version support is to be provided. This
        function will have a "version_support" attribute.
    version
        the version of the current framework for which the support is to be provided, the
        version is inferred by importing the framework in the case of frontend version support
        and defaults to the highest available version in case of import failure
    Returns
    -------
        the name of the original function which will then point to the version specific function

    """
    version = str(version)
    if version.find("+") != -1:
        version = int(version[: version.index("+")].replace(".", ""))
    else:
        version = int(version.replace(".", ""))
    if "_to_" in name:
        i = name.index("_v_")
        e = name.index("_to_")
        version_start = name[i + 3 : e]
        version_start = int(version_start.replace("p", ""))
        version_end = name[e + 4 :]
        version_end = int(version_end.replace("p", ""))
        if version in range(version_start, version_end + 1):
            return name[0:i]
    elif "_and_above" in name:
        i = name.index("_v_")
        e = name.index("_and_")
        version_start = name[i + 3 : e]
        version_start = int(version_start.replace("p", ""))
        if version >= version_start:
            return name[0:i]
    else:
        print(
            name,
        )
        i = name.index("_v_")
        e = name.index("_and_")
        version_start = name[i + 3 : e]
        version_start = int(version_start.replace("p", ""))
        if version <= version_start:
            return name[0:i]


def version_handler(frontend):
    """

    Parameters
    ----------
    frontend
        the frontend module for which we provide the version support
    Returns
        The function doesn't return anything and upodates the frontend __dict__
        to make the original functiona name to point to the version specific one

    -------

    """
    f = str(frontend.__name__)
    f = f[f.index("frontends") + 10 :]
    try:
        f = importlib.import_module(f)
        f_version = f.__version__
    except Exception:
        f_version = latest_version[f]

    for i in list(frontend.__dict__):
        if hasattr(frontend.__dict__[i], "version_support"):
            orig_name = version_extractor(i, f_version)
            if orig_name:
                frontend.__dict__[orig_name] = frontend.__dict__[i]


version_handler(torch)
version_handler(tensorflow)
version_handler(jax)
