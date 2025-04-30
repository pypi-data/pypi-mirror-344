from collections import deque
from typing import Any, Self, Generator, override
from collections.abc import Callable
from contextlib import contextmanager
import datetime as dt

from .invalidation_dict import InvalidationDict


def maxlen(value: int | None) -> int | None:

    if value is None or value < 1:
        return None
    else:
        return int(value)


def _compare_deque_objects(one, two):
    return one == two


type ComparisonFunc[one, two] = Callable[[one, two], bool]


class DequeCache[T](InvalidationDict[str, deque[T]]):
    """
    Dictionary that holds cached items in deques. Allows deques'
    max length to be changed dynamically. In the deques, most recently
    used item should be on the left.
    """

    def __init__(
        self,
        max_size: int | None = None,
        compare_deque_obj: ComparisonFunc | None = None,
        *args,
        **kwargs,
    ):
        """
        Arguments:
            max_size:
                The max size of the deques.
            compare_deque_obj:
                Function to compare objects in deque with. For None,
                defaults to equality comparison. Second passed value
                will be the object in the deque, first value is up
                to the user, whatever is needed in the comparison
                function.
        """

        super().__init__(*args, **kwargs)

        self._max_size = maxlen(max_size)
        self.compare_deque_objects: ComparisonFunc[Any, T] = (
            _compare_deque_objects if compare_deque_obj is None else compare_deque_obj
        )
        self._move_newest_to_front = True

    @property
    def max_size(self) -> int | None:
        return self._max_size

    def _deque_factory(self) -> deque[T]:
        return deque(maxlen=self._max_size)

    @max_size.setter
    def max_size(self, value: int | None):

        if value is None or value < 1:
            self._max_size = None
        else:
            self._max_size = int(value)

        for key in self:
            new_deque = self._deque_factory()
            # Maintain order by reversing, extending from left
            new_deque.extendleft(reversed(self[key]))
            self[key] = new_deque

    @contextmanager
    def no_moving_recent_to_front(self) -> Generator[Self, None, None]:
        """
        Stop moving the most recently accessed item to the front
        of the deque.
        """

        try:
            self._move_newest_to_front = False
            yield self
        finally:
            self._move_newest_to_front = True

    def find_cached_item[one, two](
        self,
        key,
        comp_value: one,
        comp_function: ComparisonFunc[one, two] | None = None,
    ) -> T:
        """
        Find the cached item in the deque pointed to by `key`.
        Arguments:
            key:
                Key to use to get the relevant deque.
            comp_value:
                Value to be used in `comp_function` as the first
                argument.
            comp_function:
                Function that compares `comp_value` against an
                object in the relevant deque. First argument
                will be `comp_value`, second will be the deque
                object. Returns True for a match, otherwise False.

                Defaults to `self.compare_deque_objects` if None.

        Raises:
            LookupError:
                When no deque value matching the passed data
                is found.
        """

        comp_function = (
            comp_function if not (comp_function is None) else self.compare_deque_objects
        )
        for i, deq_ob in enumerate(self[key]):
            if comp_function(comp_value, deq_ob):
                # move the accessed object to the front
                if self._move_newest_to_front:
                    del self[key][i]
                    self.get_and_update(key).appendleft(deq_ob)
                return deq_ob

        raise LookupError("No matching deque value found")

    def __getitem__(self, key) -> deque[T]:
        if not key in self:
            super().__setitem__(key, self._deque_factory())
        return super().__getitem__(key)

    @override
    def invalidate(self, key):
        self[key].clear()
        return self
