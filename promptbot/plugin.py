from abc import ABC, abstractmethod


class Plugin(ABC):
    """
    A base class for creating plugins.

    Class Attributes:
        EXPLAIN (str): A required explanation of what the plugin does.
        NAME (str): The name of the plugin.

    """

    EXPLAIN: str
    NAME: str

    @abstractmethod
    def run(self, *args, **kwargs):
        """
        Runs the plugin.

        Args:
            *args: Any positional arguments that the plugin needs.
            **kwargs: Any keyword arguments that the plugin needs.

        """
        pass
