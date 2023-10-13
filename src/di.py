import inspect
from typing import Any, Callable


def inject_dependencies(handler: Callable, dependencies: dict[str, Any]) -> Callable:
    """
    Inject dependencies into a handler function.

    Args:
        handler (Callable): Handler function to inject dependencies into.
        dependencies (dict[str, Any]): Dependencies to inject into the handler.

    Returns:
        Callable: Handler function with dependencies injected.
    """

    params = inspect.signature(handler).parameters
    deps = {
        name: dependency for name, dependency in dependencies.items() if name in params
    }
    return lambda message: handler(message, **deps)
