def is_trusted_origin(scheme: str, host: str) -> bool:
    """Only allow sending requests to trusted hosts"""
    return scheme in ("https", "http+unix") or host in {"localhost", "127.0.0.1", "::1"}
