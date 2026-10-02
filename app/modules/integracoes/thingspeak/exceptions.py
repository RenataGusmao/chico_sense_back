class ThingSpeakError(Exception):
    """Base error for ThingSpeak integration failures."""


class ThingSpeakConfigurationError(ThingSpeakError):
    """Raised when required ThingSpeak configuration is missing."""


class ThingSpeakConnectionError(ThingSpeakError):
    """Raised when ThingSpeak cannot be reached."""


class ThingSpeakTimeoutError(ThingSpeakError):
    """Raised when ThingSpeak does not respond within the configured timeout."""


class ThingSpeakHTTPError(ThingSpeakError):
    """Raised when ThingSpeak returns an unexpected HTTP status."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        super().__init__(message)


class ThingSpeakInvalidResponseError(ThingSpeakError):
    """Raised when ThingSpeak returns invalid or unexpected JSON."""

