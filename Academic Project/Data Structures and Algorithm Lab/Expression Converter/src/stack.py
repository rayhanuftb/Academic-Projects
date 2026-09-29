from typing import Any, List, Optional


class Stack:
    """LIFO (Last-In-First-Out) Stack data structure implementation."""

    def __init__(self):
        self._items: List[Any] = []

    def push(self, item: Any) -> None:
        """Pushes an element onto the top of the stack. O(1) time complexity."""
        self._items.append(item)

    def pop(self) -> Any:
        """Removes and returns the top element of the stack. O(1) time complexity."""
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> Optional[Any]:
        """Returns the top element without removing it. O(1) time complexity."""
        if self.is_empty():
            return None
        return self._items[-1]

    def is_empty(self) -> bool:
        """Checks if the stack contains zero elements. O(1) time complexity."""
        return len(self._items) == 0

    def size(self) -> int:
        """Returns the number of elements in the stack. O(1) time complexity."""
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items})"
