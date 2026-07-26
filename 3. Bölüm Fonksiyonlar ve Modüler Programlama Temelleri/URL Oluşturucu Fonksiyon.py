def build_url(base_url, endpoint, param):
    """Verilen URL parçalarını birleştirerek URL döndürür."""
    return f"{base_url.rstrip('/')}/{endpoint.lstrip('/')}?id={param}"
