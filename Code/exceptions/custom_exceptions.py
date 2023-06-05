from Code.handlers.warning_window_handler import WarningWindow
from typing import Tuple


class CustomException(Exception):
    def __init__(self, error_info: Tuple[str, str, str, str]) -> None:
        super().__init__(error_info[1])
        self.error_info = WarningWindow(*error_info)
