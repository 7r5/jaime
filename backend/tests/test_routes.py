from backend.routes import api_router


def test_api_router_includes_routes():
    prefixes = [route.include_context.prefix for route in api_router.routes if hasattr(route, "include_context")]
    assert "/webhook" in prefixes
    assert "/auth" in prefixes
    assert "/admin" in prefixes
