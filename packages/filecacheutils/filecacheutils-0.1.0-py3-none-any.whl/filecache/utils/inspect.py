import inspect as base_inspect
from collections.abc import Callable
from hashlib import sha256
from typing import Any

from ..typing import Hasher


def function_hash(function: Callable, *, hasher: Hasher | None = None) -> str:
    """
    Get the hexdigest of `function` (hex string of the hash of the function
    body).

    Arguments:
        function:
        hasher:
            Hashlib-compliant hasher, defaults to non-secure sha256.
    """

    hasher = sha256(usedforsecurity=False) if hasher is None else hasher
    hasher.update(bytes(base_inspect.getsource(function), encoding="utf-8"))
    function_hash = hasher.hexdigest()
    return function_hash


def bind_arguments(
    func: Callable, args, kwargs, ignore_in_kwargs: tuple[str, ...] = ()
):
    """
    Bind the arguments `args` and `kwargs` based on the call signature
    of `function`.

    Arguments:
        func:
        args:
        kwargs:
        ignore_in_kwargs:
            If not empty, should contain keys of items expected to be in `kwargs`.
            The keys will be deleted from `kwargs` and a partial bind
            will be performed where the ignored keys will not be present.
    """

    sig = base_inspect.signature(func)
    if len(ignore_in_kwargs) > 0:
        for ign in ignore_in_kwargs:
            del kwargs[ign]
        bound_args = sig.bind_partial(*args, **kwargs)
    else:
        bound_args = sig.bind(*args, **kwargs)
    bound_args.apply_defaults()
    return bound_args.arguments


def unique_name(obj: Callable | Any):
    """
    Return a unique name for `obj`.

    Arguments:
        obj:
            Function, method or class.
    """

    return f"{obj.__module__}.{obj.__qualname__}"
