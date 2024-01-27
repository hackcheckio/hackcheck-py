EndpointBase: str = "https://api.hackcheck.io/"


def EndpointSearch(apiKey: str, field: str, query: str) -> str:
    return f"{EndpointBase}search/{apiKey}/{field}/{query}"


def EndpointCheck(apiKey: str, field: str, query: str) -> str:
    return f"{EndpointBase}search/check/{apiKey}/{field}/{query}"


def EndpointGetMonitors(apiKey: str) -> str:
    return f"{EndpointBase}monitors/{apiKey}/list"


def EndpointGetMonitor(apiKey: str, monitor_id: str) -> str:
    return f"{EndpointBase}monitors/{apiKey}/list/{monitor_id}"


def EndpointGetAssetMonitorSources(apiKey: str, monitor_id: str) -> str:
    return f"{EndpointBase}monitors/{apiKey}/sources/asset/{monitor_id}"


def EndpointGetDomainMonitorSources(apiKey: str, monitor_id: str) -> str:
    return f"{EndpointBase}monitors/{apiKey}/sources/domain/{monitor_id}"


def EndpointUpdateAssetMonitor(apiKey: str, monitor_id: str) -> str:
    return f"{EndpointBase}monitors/{apiKey}/update/asset/{monitor_id}"


def EndpointUpdateDomainMonitor(apiKey: str, monitor_id: str) -> str:
    return f"{EndpointBase}monitors/{apiKey}/update/domain/{monitor_id}"


def EndpointTogglePauseAssetMonitor(apiKey: str, monitor_id: str) -> str:
    return f"{EndpointBase}monitors/{apiKey}/pause/asset/{monitor_id}"


def EndpointTogglePauseDomainMonitor(apiKey: str, monitor_id: str) -> str:
    return f"{EndpointBase}monitors/{apiKey}/pause/domain/{monitor_id}"
