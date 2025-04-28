# 🧰 ten-utils

> A Python toolkit with commonly used development utilities: logging, in-memory buffers, env variable loading, and more — designed to reduce boilerplate and accelerate development.

[![PyPI version](https://badge.fury.io/py/ten-utils.svg)](https://pypi.org/project/ten-utils/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Ten-o69/ten-utils/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Downloads](https://img.shields.io/pypi/dm/ten-utils.svg)](https://pypi.org/project/ten-utils/)

---

## ✨ Features

- ✅ Structured logging with file support(at the time of version 0.0.14 the file saving functionality has not yet been implemented)
- ✅ Memory-based buffer system
- ✅ Env file loading with type validation
- 🛠️ More utilities coming soon...

## 📦 Installation
You can install `ten-utils` using pip:

```bash
pip install ten-utils
```

Or with development tools:

```bash
pip install ten-utils[dev]
```

---

## 🚀 Quick Start
So far, the library has a few utilities like this:

- `log` - Utility for logging any actions in the code. The tool implements the main class `Logger` and the class for configuration of the main class `LoggerConfig`.
- `buffer` - A utility that creates a value inside the program memory and stores it until it is disabled or intentionally deleted by the user using a method.
- `env_loader` - A utility for loading and validating environment variables using a `.env` file.

### Quick start for `log` utility

```python
from ten_utils.log.logger import Logger
from ten_utils.log.config import LoggerConfig


# Set global configuration
LoggerConfig().set_default_level_log(1)       # Set minimum level to INFO
LoggerConfig().set_save_log_to_file(False)    # Don't write to file

# Create logger instance
logger = Logger(__name__)  # or any other logger name

# Logging
logger.debug("This is a debug message")     # Will be ignored (default = INFO)
logger.info("App started successfully")
logger.warning("This is a warning")
logger.error("An error occurred")
```

You can also change the configuration at any time within the code. 
A new instance of the `Logger` class will use the new configuration you set, 
while an old instance of the `Logger` class will use the old configuration.

```python
from ten_utils.log.logger import Logger
from ten_utils.log.config import LoggerConfig


LoggerConfig().set_default_level_log(1)       # Set minimum level to INFO
LoggerConfig().set_save_log_to_file(False)    # Don't write to file

# Create logger instance
logger = Logger(__name__)

# Logging
logger.debug("This is a debug message")     # Will be ignored (default = INFO)
logger.info("App started successfully")
logger.warning("This is a warning")
logger.error("An error occurred")

# Installing a new configuration
LoggerConfig().set_default_level_log(2)       # Set minimum level to WARNING
LoggerConfig().set_save_log_to_file(True)     # Enable file output

# Creating a new instance
logger1 = Logger(__name__)

# Logging
logger1.debug("This is a debug message 1")     # Will be ignored (default = WARNING)
logger1.info("App started successfully 1")     # Will be ignored (default = WARNING)
logger1.warning("This is a warning 1")
logger1.error("An error occurred 1")
```

#### Warning:
> - Logs will not be saved to a file, because at the time of v0.0.14 this is not yet implemented.

It's also worth talking about the `logger.critical` methods:
```python
from ten_utils.log.logger import Logger
from ten_utils.log.config import LoggerConfig


LoggerConfig().set_default_level_log(4)     # Set minimum level to CRITICAL

logger = Logger(__name__)

logger.critical("Critical log!")
```

There is an important point that when `logger.critical` is triggered, the programme crashes with the message: `Process finished with exit code 1`.
This behaviour occurs because `logger.critical` executes `exit(1)` at the end of execution.

### Quick start for `buffer` utility

```python
from ten_utils.buffer import Buffer


buffer = Buffer()

# Set a value named 'Test' with a value of 'True'.
buffer.set("Test", True)

# Getting value from buffer
value = buffer.get("Test")
print(value)

# Clearing the entire buffer
buffer.clear()
```

#### Info:
> - The `Buffer` class is implemented using the metaclass `Singleton`. Therefore
an instance of the `Buffer` class can be initialised once and
used throughout the programme

### Quick start for `env_loader` utility

```python
from ten_utils.env_loader import EnvLoader

# Create instance and load .env file
env_loader = EnvLoader(".env")

# Reading environment variables
db_name = env_loader.load("DB_NAME", str)
port = env_loader.load("PORT", int)
is_active = env_loader.load("IS_ACTIVE", bool)
allowed_hosts = env_loader.load("ALLOWED_HOSTS", list)

print(db_name, port, is_active, allowed_hosts)
```

Example `.env` file:
```dotenv
DB_NAME=mydatabase
PORT=5432
IS_ACTIVE=true
ALLOWED_HOSTS=localhost,127.0.0.1,example.com
```

---

## 🧪 Running Tests

```bash
pytest tests/ --disable-warnings -v
```

To install test/dev dependencies:

```bash
pip install ten-utils[dev]
```

---

## 📜 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Александр Караваев**  
[Email](mailto:234iskateli234@gmail.com)  
[GitHub Profile](https://github.com/Ten-o69)

---

## 💡 Contributing

Contributions, issues and feature requests are welcome!  
Feel free to open a [discussion](https://github.com/Ten-o69/ten-utils/discussions) or a [pull request](https://github.com/Ten-o69/ten-utils/pulls).
