from abc import ABC, abstractmethod

class Defaultable(ABC):
    """Public-facing ABC requiring a `default()` method."""

    @classmethod
    @abstractmethod
    def default(cls):
        """Return a default instance."""
        pass

    def __call__(self):
        """Allow calling the class to get the default instance."""
        return self.default()

    @classmethod
    def is_default(cls, obj):
        """Check if the given object is in its default state."""
        return obj == cls.default()


class InternalDefaultable(ABC):
    """Internal-use ABC requiring a `_default()` method."""

    @classmethod
    @abstractmethod
    def _default(cls):
        """Return a default instance (internal use only)."""
        pass

    @classmethod
    def _is_default(cls, obj):
        """Internal method to check if the given object is in its default state."""
        return obj == cls._default()
