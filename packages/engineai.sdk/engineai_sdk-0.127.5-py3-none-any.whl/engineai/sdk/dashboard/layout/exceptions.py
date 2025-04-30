"""Layout Exceptions specs."""

from engineai.sdk.dashboard.exceptions import EngineAIDashboardError


class RowMaximumItemsError(EngineAIDashboardError):
    """Dashboard Layout Row Maximum Items Exception."""

    def __init__(self) -> None:
        """Constructor for RowMaximumItemsError class."""
        super().__init__()
        self.error_strings.append("The maximum allowed items per row is 6.")


class RowMinimumItemsError(EngineAIDashboardError):
    """Dashboard Layout Row Minimum Items Exception."""

    def __init__(self) -> None:
        """Constructor for RowMinimumItemsError class."""
        super().__init__()
        self.error_strings.append("The minimum allowed items per row is 1.")


class RowMaximumAutoWidthItemsError(EngineAIDashboardError):
    """Dashboard Layout Row Maximum Auto Width Items Exception."""

    def __init__(self) -> None:
        """Constructor for RowMaximumAutoWidthItemsError class."""
        super().__init__()
        self.error_strings.append(
            "The row has 5 columns with auto width. "
            "The total columns allowed in this mode are 1, 2, 3, 4 and 6."
        )


class RowColumnsAutoWidthError(EngineAIDashboardError):
    """Dashboard Layout Rows Columns Auto Width Exception."""

    def __init__(self) -> None:
        """Constructor for RowColumnsAutoWidthError class."""
        super().__init__()
        self.error_strings.append(
            "Cannot add to the row a column without custom `width` when "
            "all the other columns have custom width."
        )


class RowColumnsCustomWidthError(EngineAIDashboardError):
    """Dashboard Layout Rows Columns Custom Width Exception."""

    def __init__(self) -> None:
        """Constructor for RowColumnsCustomWidthError class."""
        super().__init__()
        self.error_strings.append(
            "Cannot add to the row a column with custom `width` when "
            "all the other columns don't have custom width."
        )


class RowColumnsMaximumWidthError(EngineAIDashboardError):
    """Dashboard Layout Rows Columns Maximum Width Exception."""

    def __init__(
        self, overflow_width: int, total_width: int, new_width: int, *args: object
    ) -> None:
        """Constructor for RowColumnsMaximumWidthError class.

        Args:
            overflow_width (int): overflow width.
            total_width (int): total width.
            new_width (int): new width.
        """
        super().__init__(overflow_width, total_width, new_width, *args)
        self.error_strings.append(
            f"Adding column would result in width overflow: "
            f"{overflow_width} = "
            f"{total_width} + {new_width} (new column)"
        )


class ColumnWrongWidthSizeError(EngineAIDashboardError):
    """Dashboard Layout Column Limits Width Exception."""

    def __init__(self) -> None:
        """Constructor for ColumnLimitsWidthError class."""
        super().__init__()
        self.error_strings.append(
            "Column `width` must have one of the following values: "
            "2, 3, 4, 6, 8, 10 or 12."
        )


class ColumnLimitsWidthError(EngineAIDashboardError):
    """Dashboard Layout Column Limits Width Exception."""

    def __init__(self) -> None:
        """Constructor for ColumnLimitsWidthError class."""
        super().__init__()
        self.error_strings.append(
            "If `width` is set the values must be between 2 and 12."
        )
