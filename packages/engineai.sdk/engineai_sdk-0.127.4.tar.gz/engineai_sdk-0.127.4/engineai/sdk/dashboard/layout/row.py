"""Spec for a row in a dashboard vertical grid layout."""

from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from typing_extensions import Unpack

from engineai.sdk.dashboard.abstract.layout import AbstractLayoutItem
from engineai.sdk.dashboard.abstract.layout import CompatibilityItem
from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.interface import RowInterface

from .column import Column
from .exceptions import RowColumnsAutoWidthError
from .exceptions import RowColumnsCustomWidthError
from .exceptions import RowColumnsMaximumWidthError
from .exceptions import RowMaximumAutoWidthItemsError
from .exceptions import RowMaximumItemsError
from .exceptions import RowMinimumItemsError
from .typings import LayoutItem


class Row(RowInterface):
    """Organize and group content horizontally within a vertical grid layout.

    The Row class represents a row within a vertical grid layout, allowing
    users to organize and group content horizontally.
    """

    compatibilities: CompatibilityItem = CompatibilityItem([Column], Column)

    @type_check
    def __init__(
        self,
        *items: Union[LayoutItem, Column],
        height: Optional[Union[int, float]] = None,
    ) -> None:
        """Constructor for Row.

        Args:
            *items: Content that is going to be added inside the Row,
                if the item is a Column, it will be added to the row, if the item
                is a Widget or a Grid, it will be added to a Column.
            height: Custom height for the row.

        Examples:
            ??? example "Create Row with widget"
                ```py linenums="1"
                import pandas as pd

                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard import layout
                from engineai.sdk.dashboard.widgets import select

                data = pd.DataFrame({"id": [1, 2, 3]})

                dashboard.Dashboard(
                    content=layout.Grid(
                        layout.Row(select.Select(data))
                    )
                )
                ```

            ??? example "Create Row with multiple widgets"
                ```py linenums="1"
                import pandas as pd

                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard import layout
                from engineai.sdk.dashboard.widgets import select
                from engineai.sdk.dashboard.widgets import toggle

                data = pd.DataFrame({"id": [1, 2, 3]})

                dashboard.Dashboard(
                    content=layout.Grid(
                        layout.Row(
                            select.Select(data),
                            toggle.Toggle(data),
                        )
                    )
                )
                ```

            ??? example "Create Row with Tab Section and Card"
                ```py linenums="1"
                import pandas as pd

                from engineai.sdk.dashboard import dashboard
                from engineai.sdk.dashboard import layout
                from engineai.sdk.dashboard.widgets import select
                from engineai.sdk.dashboard.widgets import toggle

                data = pd.DataFrame({"id": [1, 2, 3]})

                dashboard.Dashboard(
                    content=layout.Grid(
                        layout.Row(
                            layout.TabSection(
                                layout.Tab(
                                    label="tab",
                                    content=select.Select(data),
                                )
                            ),
                            layout.Card(
                                header=layout.Header(title="Card"),
                                content=toggle.Toggle(data),
                            ),
                        )
                    )
                )
                ```
        """
        super().__init__()
        self.__total_width: int = 0
        self.__auto_width: bool = True
        self.__custom_height: Optional[Union[int, float]] = height
        self.__height: Optional[Union[int, float]] = None
        self.__columns = []
        self.__columns = self.__set_items(*items)

    @property
    def custom_height(self) -> Optional[Union[int, float]]:
        """Get custom height."""
        return self.__custom_height

    def __set_items(self, *items: Union[LayoutItem, Column]) -> List[Column]:
        """Set columns for row."""
        if len(items) > 6:
            raise RowMaximumItemsError

        if len(items) == 0:
            raise RowMinimumItemsError

        result = []
        for item in items:
            if isinstance(item, Column):
                result.append(self.__add_column(result, item))
            else:
                result.append(self.__add_column(result, Column(content=item)))
        return result

    def __add_column(self, items: List[Column], new_column: Column) -> None:
        """Add column to row."""
        self.__validate_new_column(items, new_column)
        return new_column

    def __validate_new_column(self, items: List[Column], new_column: Column) -> None:
        self.__validate_auto_width(items, new_column)
        self.__validate_custom_width(items, new_column)

    def __validate_auto_width(self, items: List[Column], new_column: Column) -> None:
        if new_column.width is None:
            if items and any(column.width is not None for column in items):
                raise RowColumnsAutoWidthError
            self.__total_width = 12

    def __validate_custom_width(self, items: List[Column], new_column: Column) -> None:
        if new_column.width is not None:
            if items and any(column.width is None for column in items):
                raise RowColumnsCustomWidthError

            if self.__total_width + new_column.width > 12:
                raise RowColumnsMaximumWidthError(
                    overflow_width=self.__total_width + new_column.width,
                    total_width=self.__total_width,
                    new_width=new_column.width,
                )

            self.__total_width += new_column.width
            self.__auto_width = False

    def height(self) -> float:
        """Get row height."""
        self.__height = (
            self.custom_height
            if self.custom_height is not None
            else max(item.height() for item in self.__columns)
        )
        return self.__height

    def items(self) -> List[AbstractLayoutItem]:
        """Returns list of grid items that need to be inserted individually."""
        items: List[AbstractLayoutItem] = []
        for column in self.__columns:
            items += column.items()
        return items

    def prepare(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Prepare row."""
        if self.__auto_width and len(self.__columns) == 5:
            raise RowMaximumAutoWidthItemsError

        auto_width = int(12 / len(self.__columns)) if self.__auto_width else None

        for column in self.__columns:
            column.prepare(auto_width=auto_width, **kwargs)

    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """
        return {
            "height": self.height(),
            "columns": [column.build() for column in self.__columns],
        }
