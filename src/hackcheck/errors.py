class RateLimitError(Exception):
    def __init__(self, limit, remaining_requests):
        self.limit = limit
        self.remaining_requests = remaining_requests
        super().__init__("rate limit reached")


UnauthorizedIPAddressError = Exception("unauthorized ip address")


InvalidAPIKeyError = Exception("invalid api key")

ServerError = Exception("server returned an error")
