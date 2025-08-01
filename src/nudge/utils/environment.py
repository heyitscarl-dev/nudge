import os
import warnings

from functools import wraps
from typing import Any, Callable

class MissingEnvironmentVariableError(KeyError):
    """
    Raised when a required environment variable is missing.
    """

    def __init__(self, ident: str) -> None:
        super().__init__(f"Required environment variable '{ident}' not set.")


def get_environment_or_else(identifier: str, callback: Callable[[str], Any]):
    """
    Get an environment variable or call a fallback.

    Args:
        identifier: The name of the environment variable.
        callback: A callback to execute if the variable is not set.
                  Receives the identifier as an argument.
                  Should return a default/fallback value, or raise an error.

    Returns:
        The value of the environment variable or the result of `callback`.
    """
    value = os.getenv(identifier)
    return value or callback(identifier)

def get_environment_or_default(identifier: str, default: str):
    """
    Get an environment variable or return a default value- 

    Args:
        identifier: The name of the environment variable.
        default: The value returned, if the variable is not set.

    Returns:
        The value of the environment variable or the result of `callback`.
    """
    value = os.getenv(identifier)
    return value or default

def get_environment(identifier: str) -> str:
    """
    Get a required environment variable.

    Args:
        identifier: The name of the environment variable.

    Returns:
        The value of the environment variable.

    Raises:
        MissingEnvironmentVariableError: If the variable is not set.
    """
    def fail(_) -> None:
        raise MissingEnvironmentVariableError(identifier)

    return get_environment_or_else(identifier, fail)

def with_get_environment(identifier: str) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            value = get_environment(identifier)
            kwargs[identifier] = value 
            return func(*args, **kwargs)
        return wrapper
    return decorator

def with_try_get_environment(identifier: str) -> Callable[[Callable], Callable]:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            value = try_get_environment(identifier)
            kwargs[identifier] = value 
            return func(*args, **kwargs)
        return wrapper
    return decorator


def try_get_environment(identifier: str) -> str | None:
    """
    Try to get an environment variable without raising.

    Args:
        identifier: The name of the environment variable.

    Returns:
        The value of the environment variable, or None if missing.
        Emits a warning if the variable is not set.
    """
    def fail(_) -> None:
        warnings.warn(f"Environment variable '{identifier}' not set.", stacklevel=2)
        return None

    return get_environment_or_else(identifier, fail)
