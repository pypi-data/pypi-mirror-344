import pytest
from unittest.mock import patch, MagicMock
from ten_utils.log.logger import Logger


@pytest.fixture
def mock_console_print():
    with patch("ten_utils.log.logger.Console.print") as mock_print:
        yield mock_print


@pytest.fixture
def logger():
    return Logger(name="TestLogger", level=0, save_file=False)


@pytest.mark.parametrize("level_method,level_name", [
    ("debug", "DEBUG"),
    ("info", "INFO"),
    ("warning", "WARNING"),
    ("error", "ERROR"),
])
def test_logging_levels(logger, mock_console_print, level_method, level_name):
    log_method = getattr(logger, level_method)
    log_method("Test message")

    assert mock_console_print.called
    args, _ = mock_console_print.call_args
    assert isinstance(args[0].plain, str)
    assert level_name in args[0].plain
    assert "Test message" in args[0].plain
    assert "TestLogger" in args[0].plain


def test_additional_info_false(logger, mock_console_print):
    logger.info("Simple message", additional_info=False)
    args, _ = mock_console_print.call_args
    output = args[0].plain
    assert "INFO" not in output
    assert "Simple message" in output


def test_critical_exits(logger):
    with patch("builtins.exit") as mock_exit:
        logger.critical("Fatal error", additional_info=True)
        mock_exit.assert_called_once_with(1)
