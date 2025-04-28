from pathlib import Path
from typing import Any
import os
import json

from dotenv import load_dotenv

from ten_utils.common.validators import EnvLoaderValuesValidator
from ten_utils.common.errors import (
    FailedLoadEnvVariables,
    FailedConvertTypeEnvVar,
    NotFoundNameEnvVar,
)


class EnvLoader:
    """
    A class for loading and validating environment variables.

    This class loads environment variables from a specified `.env` file or directly
    from the system environment. It provides automatic type casting and validation,
    supporting types such as str, int, float, bool, list, tuple, and dict.
    """

    def __init__(
        self,
        path_to_env_file: str | Path | None = None,
        getenv_mode: bool = False,
    ):
        """
        Initialize the environment loader and optionally load the .env file.

        Args:
            path_to_env_file (str | Path | None): Path to the .env file. Optional.
            getenv_mode (bool): If True, environment variables are read from the
                system environment without loading a .env file.

        Raises:
            FailedLoadEnvVariables: If the .env file cannot be loaded and getenv_mode is False.
        """
        if not getenv_mode:
            loader_env_values = EnvLoaderValuesValidator(
                path_to_env_file=path_to_env_file,
            )

            self.path_to_env_file = loader_env_values.path_to_env_file
            load_result: bool = load_dotenv(dotenv_path=self.path_to_env_file)

            if not load_result:
                raise FailedLoadEnvVariables

    def load(self, name_env: str, type_env_var: type) -> Any:
        """
        Load and cast an environment variable to the specified type.

        Args:
            name_env (str): The name of the environment variable.
            type_env_var (type): The type to which the value should be cast.

        Returns:
            Any: The environment variable value cast to the specified type.

        Raises:
            NotFoundNameEnvVar: If the environment variable is not found.
            FailedConvertTypeEnvVar: If the value cannot be cast to the specified type.
            ValueError: If `type_env_var` is None.
        """
        env_value: str | None = os.getenv(name_env)
        if env_value is None:
            raise NotFoundNameEnvVar(name_env=name_env)

        if type_env_var is None:
            raise ValueError("The 'type_env_var' argument cannot be 'None'")

        elif type_env_var is list or type_env_var is tuple:
            return self.__convert_var_to_list_or_tuple(
                env_value=env_value,
                type_env_var=type_env_var,
            )

        elif type_env_var is bool:
            return self.__convert_var_to_bool(
                env_value=env_value,
            )

        elif type_env_var is dict:
            return json.loads(env_value)

        try:
            return type_env_var(env_value)

        except ValueError:
            raise FailedConvertTypeEnvVar(
                convert_type=type_env_var,
                value=env_value,
            )

    @staticmethod
    def __convert_var_to_list_or_tuple(
        env_value: str,
        type_env_var: type,
    ) -> list | tuple:
        """
        Convert a comma-separated string to a list or tuple of strings.

        Args:
            env_value (str): The environment variable value.
            type_env_var (type): Target type, either `list` or `tuple`.

        Returns:
            list | tuple: Parsed values as list or tuple.
        """
        env_value = env_value.split(",")
        env_value = [value for value in env_value if value]

        if type_env_var is tuple:
            return tuple(env_value)

        return env_value

    @staticmethod
    def __convert_var_to_bool(env_value: str) -> bool:
        """
        Convert a string to a boolean value.

        Args:
            env_value (str): The environment variable value.

        Returns:
            bool: Boolean representation of the input.

        Raises:
            FailedConvertTypeEnvVar: If the value is not a valid boolean string.

        Accepted true values: 'true', 'yes', '1'
        Accepted false values: 'false', 'no', '0'
        """
        true_values = ["true", "yes", "1"]
        false_values = ["false", "no", "0"]

        value_normalized = str(env_value).lower().strip()

        if value_normalized in true_values:
            return True

        if value_normalized in false_values:
            return False

        raise FailedConvertTypeEnvVar(
            convert_type=bool,
            value=env_value,
        )
