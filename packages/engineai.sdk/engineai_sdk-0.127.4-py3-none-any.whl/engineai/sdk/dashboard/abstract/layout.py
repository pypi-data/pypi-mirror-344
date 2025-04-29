"""Abstract Class implemented by main Dashboard Items."""

import dataclasses
import inspect
from abc import abstractmethod
from typing import Any
from typing import List
from typing import Optional

import networkx as nx
from typing_extensions import Unpack

from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.base import AbstractFactory

graph = nx.DiGraph()


@dataclasses.dataclass
class CompatibilityItem:
    supported: List[Any]
    default: Any


class AbstractLayoutItem(AbstractFactory):
    """Abstract Class implemented by main Dashboard Items."""

    _INPUT_KEY: Optional[str] = None
    _SINGLE_RESULT = False
    compatibilities: CompatibilityItem

    def __init__(self) -> None:
        """Creates a generic Vertical GridItem."""
        super().__init__()
        self.__dashboard_slug = ""

    @abstractmethod
    def prepare(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Prepare tab.

        Args:
            **kwargs (Unpack[PrepareParams]): keyword arguments
        """

    @property
    def dashboard_slug(self) -> str:
        """Returns items dashboard slug.

        Returns:
            str: dashboard slug
        """
        return self.__dashboard_slug

    @dashboard_slug.setter
    def dashboard_slug(self, dashboard_slug: str) -> None:
        """Sets the item's dashboard slug."""
        self.__dashboard_slug = dashboard_slug

    @property
    def input_key(self) -> str:
        """Return input type argument value.

        All Select Layout Items must now have the _INPUT_KEY defined.
        """
        if self._INPUT_KEY is None:
            msg = f"Class {self.__class__.__name__}._INPUT_KEY not defined."
            raise NotImplementedError(msg)
        return self._INPUT_KEY

    def __str__(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return self.__str__()

    @abstractmethod
    def height(self) -> float: ...

    @abstractmethod
    def items(self) -> List["AbstractLayoutItem"]:
        return [self]

    def __setattr__(self, key: str, value: Any) -> None:
        if isinstance(value, AbstractLayoutItem):
            self._add_to_graph(key, value)
        elif (
            isinstance(value, (tuple, list))
            and len(value) > 0
            and all(isinstance(item, AbstractLayoutItem) for item in value)
        ):
            for item in value:
                self._add_to_graph(key, item)
        else:
            super().__setattr__(key, value)

    def _add_to_graph(self, key: str, value: Any) -> None:
        if isinstance(value, tuple(self.compatibilities.supported)):
            graph.add_edge(self, value)
        else:
            default_class = self.compatibilities.default
            default_parameters = inspect.signature(default_class.__init__).parameters
            layout_parameter = next(
                name
                for name in default_parameters
                if name in ("content", "items", "tabs")
            )
            graph.add_edge(
                self,
                (
                    default_class(*value if isinstance(value, list) else [value])
                    if layout_parameter != "content"
                    else default_class(**{layout_parameter: value})
                ),
            )
        successors = list(graph.successors(self))
        super().__setattr__(
            key,
            (successors[0] if self._SINGLE_RESULT else successors),
        )
