from typing import Tuple
from Code.handlers.warning_window_handler import WarningWindowHandler


class CustomException(Exception):
    def __init__(self, error_info: Tuple[str, str, str, str]) -> None:
        super().__init__(error_info[1])
        self.error_info = WarningWindowHandler(*error_info)
