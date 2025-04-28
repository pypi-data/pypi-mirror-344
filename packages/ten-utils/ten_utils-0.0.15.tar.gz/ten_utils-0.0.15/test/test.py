import tempfile
from pathlib import Path

from ten_utils.env_loader.loader import EnvLoader
from ten_utils.log import Logger, LoggerConfig


if __name__ == '__main__':
    LoggerConfig().set_default_level_log(1)

    logger = Logger(__name__)

    env_loader = EnvLoader(getenv_mode=False, path_to_env_file=".env")
    test = env_loader.load("TEST_DICT", type_env_var=dict)
    print(test, type(test))

    logger.debug("Debug message", additional_info=False)
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
