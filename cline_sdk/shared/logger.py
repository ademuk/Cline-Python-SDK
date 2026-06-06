"""Logger interface."""

from abc import ABC, abstractmethod
from typing import Any


class BasicLogger(ABC):
    """Basic logger interface."""

    @abstractmethod
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message."""
        pass

    @abstractmethod
    def log(self, message: str, severity: str = "info", **kwargs: Any) -> None:
        """Log message."""
        pass

    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message."""
        self.log(message, severity="error", **kwargs)


class DefaultLogger(BasicLogger):
    """Default console logger."""

    def debug(self, message: str, **kwargs: Any) -> None:
        print(f"[DEBUG] {message}")

    def log(self, message: str, severity: str = "info", **kwargs: Any) -> None:
        print(f"[{severity.upper()}] {message}")
