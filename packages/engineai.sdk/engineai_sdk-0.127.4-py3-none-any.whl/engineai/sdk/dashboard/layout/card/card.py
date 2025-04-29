"""Spec for a Card in a dashboard  grid layout."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union
from typing import get_args

from typing_extensions import Unpack

from engineai.sdk.dashboard.abstract.layout import AbstractLayoutItem
from engineai.sdk.dashboard.abstract.layout import CompatibilityItem
from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.base import DependencyInterface
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.interface import CardInterface
from engineai.sdk.dashboard.layout.build_item import build_item
from engineai.sdk.dashboard.layout.grid import Grid
from engineai.sdk.dashboard.layout.typings import LayoutItem
from engineai.sdk.dashboard.templated_string import TemplatedStringItem

from .header import CardHeader


class Card(CardInterface):
    """Groups content with widgets, grids, and selectable sections.

    The Card class is a fundamental component in a dashboard layout,
    allowing users to group and organize content. It provides a container
    for various layout items such as widgets, cards, grids, and selectable sections.
    """

    _INPUT_KEY = "card"
    _EXTRA_PADDING = 0.45
    _SINGLE_RESULT = True

    compatibilities: CompatibilityItem = CompatibilityItem(get_args(LayoutItem), Grid)

    @type_check
    def __init__(
        self,
        *,
        content: Union[LayoutItem, List[LayoutItem]],
        header: Optional[Union[TemplatedStringItem, CardHeader]] = None,
    ) -> None:
        """Constructor for Card.

        Args:
            content: content within the Card. One of Widget, Card, Grid,
                SelectableSection.
            header: Header card spec. Defaults to None, i.e. a card without title.

        Examples:
            ??? example "Create a Card layout and add a widget"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import maps
                from engineai.sdk.dashboard.layout import Card

                data = pd.DataFrame(
                   data=[{"region": "PT", "value": 10}, {"region": "GB", "value": 100}]
                )

                Dashboard(content=Card(content=maps.Geo(data=data)))
                ```

            ??? example "Create a Card layout with multiple Widgets"
                ```py linenums="1"
                import pandas as pd
                from engineai.sdk.dashboard.dashboard import Dashboard
                from engineai.sdk.dashboard.widgets import maps
                from engineai.sdk.dashboard.layout import Card

                data = pd.DataFrame(
                   data=[{"region": "PT", "value": 10}, {"region": "GB", "value": 100}]
                )

                Dashboard(
                    content=Card(content=[maps.Geo(data=data), maps.Geo(data=data)])
                )
                ```
        """
        super().__init__()
        self.__header = self._set_header(header)
        self.__content = content

    def height(self) -> float:
        return self.__content.height() + self._EXTRA_PADDING

    def items(self) -> List[AbstractLayoutItem]:
        """Returns list of grid items that need to be inserted individually."""
        return self.__content.items()

    def _set_header(
        self, header: Optional[Union[TemplatedStringItem, CardHeader]]
    ) -> CardHeader:
        if header is None:
            return CardHeader()
        if isinstance(header, CardHeader):
            return header
        return CardHeader(title=header)

    def prepare(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Prepare card.

        Args:
            **kwargs (Unpack[PrepareParams]): keyword arguments
        """
        self.__content.prepare(**kwargs)

    def __build_dependencies(self) -> List[Dict[str, Any]]:
        """Build dependencies for Card."""
        return [
            self.__build_dependency(dependency)
            for dependency in self.__header.dependencies
        ]

    @staticmethod
    def __build_dependency(dependency: DependencyInterface) -> Dict[str, Any]:
        return {
            dependency.input_key: dependency.build(),
        }

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "item": build_item(self.__content),
            "header": self.__header.build(),
            "dependencies": self.__build_dependencies(),
        }
