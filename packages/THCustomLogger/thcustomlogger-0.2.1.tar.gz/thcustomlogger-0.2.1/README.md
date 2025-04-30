# THCustomLogger

A feature-rich Python logging package that extends the standard logging functionality with colored output, multiline formatting, and Git integration.

## Features

- 🎨 Colored console output
- 📝 Smart multiline message formatting
- 🔄 Automatic log rotation
- 🔍 Git integration (commit hash and tag information)
- 🔒 Thread-safe logging
- ⚙️ Configurable logging settings
- 📂 File and console handlers

## Table of Contents
<!-- TOC -->
<!-- TOC -->


## Installation
```bash
pip install THCustomLogger
```

## Quick Start
Basic Configuration
```python 
from THCustomLogger import LoggerFactory
# Get a logger instance
logger = LoggerFactory.get_logger(__name__)

# Basic logging
logger.info("Hello, World!")
logger.debug("Debug message") 
logger.warning("Warning message") 
logger.error("Error message")

# Multiline logging with custom formatting
logger.info("Multiple\nline\nmessage")

# Git information
logger.info(f"Current commit: {logger.get_commit_hash()}") 
logger.info(f"Latest tag: {logger.get_latest_tag()}")

# Logging with break lines
logger.info("Message with break line", extra={'msg_break': '*'})
```
Output
```terminaloutput
2025-04-29 11:00:00.625 | Line: 186 logger_setup.<module>             | INFO    : Hello, World!
2025-04-29 11:00:00.625 | Line: 188 logger_setup.<module>             | WARNING : Warning message
2025-04-29 11:00:00.625 | Line: 189 logger_setup.<module>             | ERROR   : Error message
2025-04-29 11:00:00.625 | Line: 192 logger_setup.<module>             | INFO    : Multiple
                                                                                  line
                                                                                  message
2025-04-29 11:00:00.632 | Line: 195 logger_setup.<module>             | INFO    : Current commit: afba168c52d65a621139c3b3e072a1fd991b26bd
2025-04-29 11:00:00.639 | Line: 107 logger_setup.get_latest_tag       | ERROR   : Error getting latest tag: fatal: No names found, cannot describe anything.

2025-04-29 11:00:00.640 | Line: 196 logger_setup.<module>             | INFO    : Latest tag: unknown
2025-04-29 11:00:00.640 | Line: 199 logger_setup.<module>             | INFO    : Message with break line
**********************************************************************************

2025-04-29 11:05:17.340 | Line: 172 logger_setup.example              | ERROR   : division by zero
Traceback (most recent call last):
  File "/Users/tylerhaunreiter/Desktop/Python/CustomLogger/src/THCustomLogger/logger_setup.py", line 170, in example
    1 / 0
    ~~^~~
ZeroDivisionError: division by zero
```

## Configuration

You can configure the logger using the `LoggerFactory.configure()` method:

```python 
from THCustomLogger import LoggerFactory
LoggerFactory.configure(console_enabled=True, 
                        file_enabled=True, 
                        log_level="INFO")
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| console_enabled | Enable console output | True |
| file_enabled | Enable file output | True |
| log_level | Logging level | "INFO" |
| rotation_when | Log rotation interval type (S/M/H/D/W) | "D" |
| rotation_interval | Number of intervals before rotation | 1 |
| backup_count | Number of backup files to keep | 7 |
| encoding | Log file encoding | "utf-8" |

## Features in Detail

### Colored Output

Console output is automatically colored based on log level:
- DEBUG: Green
- INFO: Light White
- WARNING: Light Yellow
- ERROR: Light Red
- CRITICAL: Bold Light Purple

### Multiline Formatting

Messages with multiple lines are automatically formatted with proper indentation:
```terminaloutput
2025-04-29 11:00:00.622 | Line: 165 logger_setup.main                 | INFO    : Commit hash: afba168c52d65a621139c3b3e072a1fd991b26bd
                                                                                  Latest tag:unknown
```



### Git Integration

Built-in methods to get Git information:

```python
# Get current commit hash
commit_hash = logger.get_commit_hash()
# Get latest tag
latest_tag = logger.get_latest_tag()
```


## Advanced Usage

### Custom Formatting

```python 
logger.info("Message with custom break", extra={'msg_break': '*'}) 
logger.info("No indent message\nSecond line", extra={'no_indent': True})
```

```terminaloutput
2025-04-29 11:05:17.343 | Line: 185 logger_setup.<module>             | INFO    : Message with custom break
**********************************************************************************
2025-04-29 11:05:17.343 | Line: 186 logger_setup.<module>             | INFO    : No indent message
Second line
```

### Thread Safety

The logger is thread-safe and can be used in multi-threaded applications:

python import threading
def worker(): logger = LoggerFactory.get_logger(**name**) logger.info("Working in thread")
threads = [threading.Thread(target=worker) for _ in range(3)] for thread in threads: thread.start()


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Author

Tyler Haunreiter

## Support

For support, please open an issue on the GitHub repository.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
