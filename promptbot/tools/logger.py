import logging
import sys

from .config_manager import config


def get_logger(logger_name: str = "promptbot", log_level: str = config["promptbot"]["log_level"]) -> logging.Logger:
    """
    Returns a logger object specified by `logger_name`. If the object does not exist, the function will create a
    new logger object and set the logger level to the input `log_level` parameter.

    :param logger_name: (Optional) A string representing the desired name of the logger object. Default is "promptbot".
    :param log_level: (Optional) A string representing the desired logging level for the logger object. Default is the value of 'log_level' in the 'promptbot' section of the config file.
    :return: A logger object with the specified name and logging level.
    """
    # Check if logger already exists
    if logger_name in logging.Logger.manager.loggerDict:
        return logging.getLogger(logger_name)
    # Create a logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level.upper())
    # Create handler for STDOUT
    stdout_handler = logging.StreamHandler(sys.stdout)
    # Create a formatter
    formatter = logging.Formatter(config["promptbot"]["log_format"])
    # Add the formatter to the handlers
    stdout_handler.setFormatter(formatter)
    # Add the handler to the logger
    logger.addHandler(stdout_handler)
    # Return the logger object
    return logger
