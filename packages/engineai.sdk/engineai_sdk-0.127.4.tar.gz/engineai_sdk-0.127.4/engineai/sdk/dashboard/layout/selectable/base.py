"""Specs for selectable layouts in a dashboard vertical grid."""

import logging
from abc import abstractmethod
from typing import Any
from typing import Dict
from typing import List
from typing import Set
from typing import Union

from typing_extensions import Unpack

from engineai.sdk.dashboard.abstract.layout import AbstractLayoutItem
from engineai.sdk.dashboard.abstract.typing import PrepareParams
from engineai.sdk.dashboard.decorator import type_check
from engineai.sdk.dashboard.interface import SelectableInterface
from engineai.sdk.dashboard.interface import SelectableItemInterface
from engineai.sdk.dashboard.layout.typings import LayoutItem
from engineai.sdk.dashboard.templated_string import TemplatedStringItem

from .exceptions import SelectableDuplicatedLabelError
from .exceptions import SelectableHasNoItemsError
from .exceptions import SelectableWithDefaultSelectionError

logger = logging.getLogger(__name__)


class SelectableItem(SelectableItemInterface):
    """Spec for item for a selectable section in a dashboard vertical grid layout."""

    _SINGLE_RESULT = True

    @type_check
    def __init__(
        self,
        *,
        label: TemplatedStringItem,
        content: Union[LayoutItem, List[LayoutItem]],
        default_selected: bool = False,
    ) -> None:
        """Construct tab for tab section dashboard vertical grid layout.

        Args:
            label: label to be displayed in dashboard
            content: item to be added in selectable
                layout.
            default_selected: set item as default selected.
        """
        super().__init__()
        self.__label = label
        self.__content = content
        self.__default_selected = default_selected

    def height(self) -> float:
        return self.__content.height()

    def items(self) -> List[AbstractLayoutItem]:
        """Returns list of grid items that need to be inserted individually."""
        return self.__content.items()

    @property
    def default_selected(self) -> bool:
        """Returns whether tab is default selected.

        Returns:
            bool: whether tab is default selected
        """
        return self.__default_selected

    @default_selected.setter
    def default_selected(self, value: bool) -> None:
        """Set tab as default selected.

        Args:
            value (bool): set tab as default selected
        """
        self.__default_selected = value

    def prepare(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Prepare tab.

        Args:
            **kwargs (Unpack[PrepareParams]): keyword arguments
        """
        self.__content.prepare(**kwargs)

    @property
    def item(self) -> LayoutItem:
        """Returns the underlying item."""
        return self.__content

    @property
    def label(self) -> TemplatedStringItem:
        """Returns label.

        Returns:
            str: label
        """
        return self.__label

    @abstractmethod
    def build(self) -> Dict[str, Any]:
        """Method implemented by all factories to generate Input spec.

        Returns:
            Input object for Dashboard API
        """


class SelectableSection(SelectableInterface):
    """Spec for section in a dashboard vertical grid layout."""

    _HEIGHT_TITLE = 0.48

    @type_check
    def __init__(
        self,
        *items: SelectableItem,
    ) -> None:
        """Construct Selectable Section for dashboard vertical grid layout."""
        super().__init__()
        self._items = []
        self.__has_default_selection: bool = False
        self.__item_labels: Set[TemplatedStringItem] = set()
        self._items = self._add_items(*items)

    def height(self) -> float:
        return max(item.height() for item in self._items) + self._HEIGHT_TITLE

    def items(self) -> List[AbstractLayoutItem]:
        """Returns list of grid items that need to be inserted individually."""
        items: List[AbstractLayoutItem] = [self]
        for selectable in self._items:
            items += selectable.items()
        return items

    def prepare(self, **kwargs: Unpack[PrepareParams]) -> None:
        """Prepare Selectable Section.

        Args:
            **kwargs (Unpack[PrepareParams]): keyword arguments
        """

        # At this level the user already added the items to the SelectableSection
        # so we can assume that there's no other element that will be added.
        # If there's a default selection, we will set the first item as default selected.
        if self.__has_default_selection is False:
            self._items[0].default_selected = True
            self.__has_default_selection = True

        for item in self._items:
            item.prepare(**kwargs)

    def _add_items(self, *items: SelectableItem) -> List[SelectableItem]:
        if len(items) == 0:
            raise SelectableHasNoItemsError(selectable_class=self.__class__.__name__)

        return [self.__add_item(item=item) for item in items]

    def __add_item(
        self,
        *,
        item: SelectableItem,
    ) -> SelectableItem:
        """Add select to select section.

        Args:
            item (SelectableItem): select to be added

        Raises:
            - if select section already has a default selection select
            - if select section already has a select with the same id or label
        """
        if item.default_selected is True and self.__has_default_selection is True:
            raise SelectableWithDefaultSelectionError(
                selectable_class=self.__class__.__name__
            )
        if item.default_selected:
            self.__has_default_selection = item.default_selected

        if item.label in self.__item_labels:
            raise SelectableDuplicatedLabelError(
                selectable_class=self.__class__.__name__,
                selectable_item_label=str(item.label),
            )

        self.__item_labels.add(item.label)
        return item
