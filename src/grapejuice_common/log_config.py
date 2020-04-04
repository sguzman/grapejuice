import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import IO, Union

from grapejuice_common.variables import logging_directory


class LoggerConfiguration:
    _output_stream: IO = sys.stdout
    _output_file: Union[str, Path] = None
    _formatter: logging.Formatter = None
    _environment_key: Union[str, None] = "LOG_LEVEL"
    _log_level_override: Union[str, None] = None
    _default_format_string = "[%(levelname)s] %(name)s:- %(message)s"

    def __init__(self):
        self._formatter = logging.Formatter(self._default_format_string)

    @property
    def use_output_stream(self):
        return self._output_stream is not None

    @property
    def output_stream(self):
        stream = self._output_stream
        assert stream is not None
        return stream

    @output_stream.setter
    def output_stream(self, stream: IO):
        self._output_stream = stream

    @property
    def use_output_file(self):
        return self._output_file is not None

    @property
    def output_file(self) -> str:
        return self._output_file

    @output_file.setter
    def output_file(self, path: str):
        self._output_file = path

        parent_file = os.path.dirname(path)
        os.makedirs(parent_file, exist_ok=True)

    @property
    def formatter(self) -> logging.Formatter:
        return self._formatter

    @property
    def log_level_str(self) -> str:
        if self._log_level_override is not None:
            return self._log_level_override.upper()

        if self._environment_key is not None and self._environment_key in os.environ:
            return os.environ[self._environment_key].upper()

        return "INFO"


def configure_logging(configuration: LoggerConfiguration = None):
    if configuration is None:
        configuration = LoggerConfiguration()

        datetime_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        configuration.output_file = os.path.join(logging_directory(), f"{datetime_now}.log")

    root_logger = logging.getLogger()

    if configuration.use_output_stream:
        stream_handler = logging.StreamHandler(configuration.output_stream)
        stream_handler.setFormatter(configuration.formatter)
        root_logger.addHandler(stream_handler)

    if configuration.use_output_file:
        file_handler = logging.FileHandler(configuration.output_file, "w+", "UTF-8")
        file_handler.setFormatter(configuration.formatter)
        root_logger.addHandler(file_handler)

    log_level = configuration.log_level_str
    assert hasattr(logging, log_level), \
        f"An invalid log level string was provided: {log_level}"

    root_logger.setLevel(getattr(logging, log_level))

    root_logger.info(f"Log level was set to '{log_level}'")
