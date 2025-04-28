import os
from pathlib import Path

import pytest

from ten_utils.env_loader import EnvLoader
from ten_utils.common.errors import (
    FailedLoadEnvVariables,
    FailedConvertTypeEnvVar,
    NotFoundNameEnvVar,
)
from ten_utils.common.singleton import Singleton


@pytest.fixture(autouse=True)
def reset_env_loader_singleton():
    Singleton.clear_instances()


@pytest.fixture
def env_file(tmp_path) -> Path:
    """
    Creates a temporary .env file with known values for testing.
    """
    env_content = (
        "STRING_VAR=hello\n"
        "INT_VAR=42\n"
        "FLOAT_VAR=3.14\n"
        "BOOL_TRUE=yes\n"
        "BOOL_FALSE=0\n"
        "LIST_VAR=a,b,c\n"
        "TUPLE_VAR=x,y,z\n"
        "EMPTY_VAR=\n"
    )

    env_path = tmp_path / ".env"
    env_path.write_text(env_content)
    return env_path


def test_env_loader_init_success(env_file):
    loader = EnvLoader(path_to_env_file=env_file)
    assert loader.path_to_env_file == env_file


def test_env_loader_missing_file(tmp_path):
    missing_path = tmp_path / ".env.missing"
    with pytest.raises(FailedLoadEnvVariables):
        EnvLoader(path_to_env_file=missing_path)


def test_load_str(env_file):
    loader = EnvLoader(path_to_env_file=env_file)
    result = loader.load("STRING_VAR", str)
    assert result == "hello"


def test_load_int(env_file):
    loader = EnvLoader(path_to_env_file=env_file)
    result = loader.load("INT_VAR", int)
    assert result == 42


def test_load_float(env_file):
    loader = EnvLoader(path_to_env_file=env_file)
    result = loader.load("FLOAT_VAR", float)
    assert result == 3.14


@pytest.mark.parametrize("name,expected", [
    ("BOOL_TRUE", True),
    ("BOOL_FALSE", False),
])
def test_load_bool(env_file, name, expected):
    loader = EnvLoader(path_to_env_file=env_file)
    result = loader.load(name, bool)
    assert result is expected


def test_load_list(env_file):
    loader = EnvLoader(path_to_env_file=env_file)
    result = loader.load("LIST_VAR", list)
    assert result == ["a", "b", "c"]


def test_load_tuple(env_file):
    loader = EnvLoader(path_to_env_file=env_file)
    result = loader.load("TUPLE_VAR", tuple)
    assert result == ("x", "y", "z")


def test_not_found_variable(env_file):
    loader = EnvLoader(path_to_env_file=env_file)
    with pytest.raises(NotFoundNameEnvVar):
        loader.load("MISSING_VAR", str)


def test_invalid_cast(env_file):
    loader = EnvLoader(path_to_env_file=env_file)
    with pytest.raises(FailedConvertTypeEnvVar):
        loader.load("STRING_VAR", int)


def test_invalid_bool_value(env_file):
    loader = EnvLoader(path_to_env_file=env_file)

    # Manually inject a bad value
    os.environ["BAD_BOOL"] = "maybe"
    with pytest.raises(FailedConvertTypeEnvVar):
        loader.load("BAD_BOOL", bool)
