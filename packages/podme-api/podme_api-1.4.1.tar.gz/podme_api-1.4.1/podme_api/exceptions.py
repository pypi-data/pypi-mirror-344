"""podme_api exceptions."""


class PodMeApiError(Exception):
    """Generic PodMe exception."""


class PodMeApiNotFoundError(PodMeApiError):
    """PodMe not found exception."""


class PodMeApiConnectionError(PodMeApiError):
    """PodMe connection exception."""


class PodMeApiConnectionTimeoutError(PodMeApiConnectionError):
    """PodMe connection timeout exception."""


class PodMeApiRateLimitError(PodMeApiConnectionError):
    """PodMe Rate Limit exception."""


class PodMeApiAuthenticationError(PodMeApiError):
    """PodMe authentication exception."""


class PodMeApiUnauthorizedError(PodMeApiError):
    """PodMe unauthorized exception."""


class PodMeApiDownloadError(PodMeApiError):
    """PodMe download exception."""


class PodMeApiStreamUrlError(PodMeApiDownloadError):
    """PodMe stream_url exception."""


class PodMeApiPlaylistUrlNotFoundError(PodMeApiStreamUrlError):
    """PodMe playlist url not found exception."""


class PodMeApiStreamUrlNotFoundError(PodMeApiStreamUrlError):
    """PodMe stream url not found exception."""
