import abc
import hashlib
from pathlib import Path
from typing import Self, Any, TypedDict, Callable
from functools import wraps
from contextlib import contextmanager

from .utils.string import pascal_to_snake_case
from .typing import Hasher
from .exceptions import StateNotFoundError

type CacheObject = Any
type StateCacheObject = Any


class CacherMetadata(TypedDict):

    hash_algorithm: str


class CacherState[T](TypedDict):

    metadata: CacherMetadata
    cache: T


class AbstractCacher(abc.ABC):

    name_as_snake = None

    @classmethod
    def _calculate_name(cls):

        cls.name_as_snake = pascal_to_snake_case(cls.__name__)

    def __init__(
        self,
        save_path: Path = None,
        *,
        hasher: Callable[[], Hasher] = lambda: hashlib.sha256(usedforsecurity=False),
        auto_save=False,
        auto_load=True,
    ):
        """

        Arguments:
            save_path:
                The path to save the cache to, by default
                "./{class_name}/cache", where {class_name} is the name
                of the class in snake case. (Assumes that the class name is
                Pascal case.)
            hasher:
                Factory returning a hashlib-type hasher.
            auto_save:
                Whether the cache should be automatically saved
                when a new value is set in it.

                NOTE: The behaviour for auto-save needs to be defined
                in inheriting classes. The methods `.perform_auto_save` and
                `.auto_save_after` should be used for this.
            auto_load:
                Whether an attempt should be made to automatically
                load the cache from `save_path`.

        """

        if self.name_as_snake is None:
            self._calculate_name()

        self.hasher = hasher
        self.cache = self.new_cache()
        self.save_path = self.create_save_path(save_path)
        self.save_path.parents[0].mkdir(parents=True, exist_ok=True)
        self._auto_save = False
        self.auto_save = auto_save

        if auto_load:
            self.init_load()

    def init_load(self):
        """
        Called during initialisation if `auto_load` is true.
        Should attempt to load the cache (e.g. using `.load_cache`).
        """
        try:
            self.load_cache(inplace=True)
        except StateNotFoundError:
            pass

    @property
    def auto_save(self):
        return self._auto_save

    @abc.abstractmethod
    def set_auto_save(self, val: bool):
        if not isinstance(val, bool):
            raise TypeError("auto_save should be a boolean")
        self._auto_save = val

    @auto_save.setter
    def auto_save(self, val: bool):
        self.set_auto_save(val)

    def perform_auto_save(self):
        """
        Perform an auto-save if the attribute is set to True.
        """
        if self.auto_save:
            self.save()

    @staticmethod
    def auto_save_after():
        """
        Wrapper that will auto-save if the self passed to `method`
        has an auto_save attribute set to True.
        """

        def outer_wrapper(method):

            @wraps(method)
            def wrapper_method(self: AbstractCacher, *args, **kwargs):
                ret = method(self, *args, **kwargs)
                self.perform_auto_save()
                return ret

            return wrapper_method

        return outer_wrapper

    @contextmanager
    def temp_auto_save(self, temp_value):
        """
        Context manager for temporarily setting the value of
        `auto_save`.
        """
        old_value = self.auto_save
        try:
            yield temp_value
        finally:
            self.auto_save = old_value

    def create_save_path(self, path: Path | None = None, file_suffix=""):

        filename = "cache" if len(file_suffix) == 0 else f"cache.{file_suffix}"
        save_path = (
            Path() / self.name_as_snake / filename
            if path is None
            else path / self.name_as_snake / filename
        )
        return save_path

    def metadata(self) -> CacherMetadata:
        """
        Get metadata about this cacher.
        """

        return {"hash_algorithm": self.hasher().name}

    @abc.abstractmethod
    def cache_to_state_cache(self) -> StateCacheObject:
        """
        Get the cache such that it is suitable for saving.
        """
        return self.cache

    @abc.abstractmethod
    def state_cache_to_cache(
        self, state_cache: StateCacheObject, *args, **kwargs
    ) -> CacheObject:
        """
        Get the proper cache from the state cache.
        """
        return state_cache

    def get_state(self) -> CacherState[StateCacheObject]:
        """
        Get all data (the state) relevant to the cacher. State
        should be saveable as-is using `.save`.
        """

        return {"metadata": self.metadata(), "cache": self.cache_to_state_cache()}

    @classmethod
    @abc.abstractmethod
    def new_cache(cls) -> CacheObject:
        """
        Return a new cache object.
        """

    @abc.abstractmethod
    def save(self, path: Path | None = None) -> Self:
        """
        Save the state.

        If `path` is None, defaults to self.save_path.
        """

    @abc.abstractmethod
    def load(self, path: Path | None = None) -> CacherState[StateCacheObject]:
        """
        Load the state as saved by `save()`.

        If `path` is None, defaults to self.save_path.

        Raises:
            StateNotFoundError:
        """

    def overwrite_cache(self, loaded_cache: CacheObject, overwrite_loaded=False):
        """
        Overwrite either the loaded cache's attributes or self.cache's
        attributes. Will be called in `.load_cache`, unless loading
        is not in-place and overwrite of loaded is not wanted.

        Arguments:
            loaded_cache:
                The cache that has been loaded in.
            overwrite_loaded:
                Whether to overwrite the loaded cache's attributes.
                If False, overwrite the attributes of `self.cache`.
        """
        # nothing to do, so just return here
        return loaded_cache

    def load_cache(
        self,
        path: Path | None = None,
        *args,
        inplace=False,
        overwrite_loaded_cache_attributes=False,
        **kwargs,
    ):
        """
        Load the cache.

        Arguments:
            path:
                Passed to `.load`.
            inplace:
                Whether to return cache or set it in the Cacher.
            args:
                Passed to `.cache_from_state_cache`.
            kwargs:
                Passed to `.cache_from_state_cache`.
            overwrite_loaded_cache_attributes:
                Whether to overwrite the attributes of the loaded
                cache with the current attributes or vice versa.

                By default, the loaded cache's attributes replace
                if the operation is performed
                in place. if not `inplace`, the loaded cache's
                attributes are replaced if `overwrite_loaded_cache_attributes` is
                True, but if False, the cacher's (`self`'s)
                attributes do not change (i.e. this argument has
                no effect).

        Raises:
            StateNotFoundError:
                The state to load the cache from was not found.
        """
        path = self.save_path if path is None else path
        state = self.load(path)
        cache = self.state_cache_to_cache(state["cache"], *args, **kwargs)

        if inplace:
            cache = self.overwrite_cache(cache, overwrite_loaded_cache_attributes)
            self.cache = cache
            return self
        else:
            if overwrite_loaded_cache_attributes:
                cache = self.overwrite_cache(cache, True)
            return cache

    @abc.abstractmethod
    def clear_file_cache(self, path: Path | None = None):
        """
        Clear the file cache.
        """
        path = self.save_path if path is None else path
        path.unlink(missing_ok=True)
        return self

    def clear_memory_cache(self):
        """
        Clear `self.cache`.
        """
        self.cache = self.new_cache()
        return self

    def clear(self, path: Path | None = None):
        """
        Clear cache on file and in memory.

        Arguments:
            path:
                Path of cache file.
        """

        path = self.save_path if path is None else path
        self.clear_file_cache(path)
        self.clear_memory_cache()
        return self
