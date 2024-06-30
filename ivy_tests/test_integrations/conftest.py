import ivy
import pytest

TARGET_FRAMEWORKS = ["numpy", "jax", "tensorflow"]
BACKEND_COMPILE = False
BACKEND = "all"


@pytest.fixture(autouse=True)
def run_around_tests():
    ivy.unset_backend()


def pytest_addoption(parser):
    parser.addoption(
        "--backend-compile",
        action="store_true",
        help="",
    )
    parser.addoption(
        "--backend",
        action="store",
        default="all",
        help="",
    )


def pytest_configure(config):
    getopt = config.getoption

    global BACKEND_COMPILE
    BACKEND_COMPILE = getopt("--backend-compile")

    global BACKEND
    BACKEND = getopt("--backend")


def pytest_generate_tests(metafunc):
    configs = list()
    if BACKEND not in ["jax", "numpy", "tensorflow", "torch"]:
        for target in TARGET_FRAMEWORKS:
            configs.append((target, BACKEND_COMPILE))
    else:
        configs.append((BACKEND, BACKEND_COMPILE))
    metafunc.parametrize("target_framework,backend_compile", configs)
