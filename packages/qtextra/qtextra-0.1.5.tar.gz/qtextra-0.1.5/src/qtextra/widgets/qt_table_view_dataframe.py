"""
Defines the DataFrameViewer class to display DataFrames as a table. The DataFrameViewer is made up of three separate
QTableWidgets... DataTableView for the DataFrame's contents, and two HeaderView widgets for the column and index
 headers.
"""

import numpy as np
import pandas as pd
import qtpy.QtCore as Qc
import qtpy.QtGui as Qg
import qtpy.QtWidgets as Qw
from qtpy.QtCore import Qt


class QtDataFrameWidget(Qw.QWidget):
    """
    Displays a DataFrame as a table.

    Args:
    ----
        df (DataFrame): The DataFrame to display
    """

    def __init__(
        self, parent: Qw.QWidget, df: pd.DataFrame, inplace: bool = True, editable: bool = False, stretch: bool = False
    ):
        super().__init__(parent)
        if df is None:
            df = pd.DataFrame()
        if not inplace:
            df = df.copy()

        # Indicates whether the widget has been shown yet. Set to True in
        self._loaded = False
        self.editable = editable

        # Set up DataFrame TableView and Model
        self.dataView = DataTableView(df, parent=self)
        if not editable:
            self.dataView.setEditTriggers(Qw.QAbstractItemView.EditTrigger.NoEditTriggers)

        # Create headers
        self.columnHeader = HeaderView(self, df, Qt.Orientation.Horizontal)
        self.indexHeader = HeaderView(self, df, Qt.Orientation.Vertical)

        # Link scrollbars
        # Scrolling in data table also scrolls the headers
        self.dataView.horizontalScrollBar().valueChanged.connect(self.columnHeader.horizontalScrollBar().setValue)
        self.dataView.verticalScrollBar().valueChanged.connect(self.indexHeader.verticalScrollBar().setValue)
        # Scrolling in headers also scrolls the data table
        self.columnHeader.horizontalScrollBar().valueChanged.connect(self.dataView.horizontalScrollBar().setValue)
        self.indexHeader.verticalScrollBar().valueChanged.connect(self.dataView.verticalScrollBar().setValue)

        self.dataView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.dataView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Disable scrolling on the headers. Even though the scrollbars are hidden, scrolling by dragging desyncs them
        self.indexHeader.horizontalScrollBar().valueChanged.connect(lambda: None)

        # Toggle level names
        if not (any(df.columns.names) or df.columns.name):
            self.columnHeader.verticalHeader().setFixedWidth(0)
        if not (any(df.index.names) or df.index.name):
            self.indexHeader.horizontalHeader().setFixedHeight(0)

        # Set up layout
        self.gridLayout = Qw.QGridLayout(self)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)

        # Add items to layout
        self.gridLayout.addWidget(self.columnHeader, 0, 1, 1, 2)
        self.gridLayout.addWidget(self.indexHeader, 1, 0, 2, 2)
        self.gridLayout.addWidget(self.dataView, 2, 2, 1, 1)
        self.gridLayout.addWidget(self.dataView.horizontalScrollBar(), 3, 2, 1, 1)
        self.gridLayout.addWidget(self.dataView.verticalScrollBar(), 2, 3, 1, 1)

        # These expand when the window is enlarged instead of having the grid squares spread out
        self.gridLayout.setColumnStretch(4, 1)
        self.gridLayout.setRowStretch(4, 1)

        # These placeholders will ensure the size of the blank spaces beside our headers
        self.gridLayout.addWidget(TrackingSpacer(ref_x=self.columnHeader.verticalHeader()), 3, 1, 1, 1)
        self.gridLayout.addWidget(TrackingSpacer(ref_y=self.indexHeader.horizontalHeader()), 1, 2, 1, 1)
        self.gridLayout.addItem(
            Qw.QSpacerItem(0, 0, Qw.QSizePolicy.Policy.Expanding, Qw.QSizePolicy.Policy.Expanding), 0, 0, 1, 1
        )

        # Styling
        for header in [self.indexHeader, self.columnHeader]:
            header.setStyleSheet("background-color: white;selection-color: black;selection-background-color: #EAEAEA;")

        self.dataView.setStyleSheet(
            "background-color: white;"
            "alternate-background-color: #F4F6F6;"
            "selection-color: black;"
            "selection-background-color: #BBDEFB;"
        )

        for item in [self.dataView, self.columnHeader, self.indexHeader]:
            item.setContentsMargins(0, 0, 0, 0)
            item.setStyleSheet(item.styleSheet() + "border: 0px solid black;")
            item.setItemDelegate(NoFocusDelegate())

    def showEvent(self, event: Qg.QShowEvent):
        """Initialize column and row sizes on the first time the widget is shown."""
        if not self._loaded:
            # Set column widths
            for column_index in range(self.columnHeader.model().columnCount()):
                self.auto_size_column(column_index)

            # Set row heights
            # Just sets a single uniform row height based on the first N rows for performance.
            N = 100
            default_row_height = 30
            for row_index in range(self.indexHeader.model().rowCount())[:N]:
                self.auto_size_row(row_index)
                height = self.indexHeader.rowHeight(row_index)
                default_row_height = max(default_row_height, height)

            # Set limit for default row height
            default_row_height = min(default_row_height, 100)

            self.indexHeader.verticalHeader().setDefaultSectionSize(default_row_height)
            self.dataView.verticalHeader().setDefaultSectionSize(default_row_height)

        self._loaded = True
        event.accept()

    def set_data(self, df):
        """Set data header."""
        self.dataView.set_data(df)
        self.columnHeader.set_data(df)
        self.indexHeader.set_data(df)

    def auto_size_column(self, column_index):
        """Set the size of column at column_index to fit its contents."""
        padding = 20

        self.columnHeader.resizeColumnToContents(column_index)
        width = self.columnHeader.columnWidth(column_index)

        # Iterate over the column's rows and check the width of each to determine the max width for the column
        # Only check the first N rows for performance. If there is larger content in cells below it will be cut off
        N = 100
        for i in range(self.dataView.model().rowCount())[:N]:
            mi = self.dataView.model().index(i, column_index)
            text = self.dataView.model().data(mi)
            w = self.dataView.fontMetrics().boundingRect(text).width()

            width = max(width, w)

        width += padding

        # add maximum allowable column width so column is never too big.
        max_allowable_width = 500
        width = min(width, max_allowable_width)

        self.columnHeader.setColumnWidth(column_index, width)
        self.dataView.setColumnWidth(column_index, width)

        self.dataView.updateGeometry()
        self.columnHeader.updateGeometry()

    def auto_size_row(self, row_index):
        """Set the size of row at row_index to fix its contents."""
        padding = 20

        self.indexHeader.resizeRowToContents(row_index)
        height = self.indexHeader.rowHeight(row_index)

        # Iterate over the row's columns and check the width of each to determine the max height for the row
        # Only check the first N columns for performance.
        N = 100
        for i in range(min(N, self.dataView.model().columnCount())):
            mi = self.dataView.model().index(row_index, i)
            cell_width = self.columnHeader.columnWidth(i)
            text = self.dataView.model().data(mi)
            # Gets row height at a constrained width (the column width).
            # This constrained width, with the flag of Qt.TextWordWrap
            # gets the height the cell would have to be to fit the text.
            constrained_rect = Qc.QRect(0, 0, cell_width, 0)
            h = self.dataView.fontMetrics().boundingRect(constrained_rect, Qt.TextWordWrap, text).height()

            height = max(height, h)

        height += padding

        self.indexHeader.setRowHeight(row_index, height)
        self.dataView.setRowHeight(row_index, height)

        self.dataView.updateGeometry()
        self.indexHeader.updateGeometry()

    def keyPressEvent(self, event):
        """Handle key presses."""
        Qw.QWidget.keyPressEvent(self, event)

        if event.matches(Qg.QKeySequence.Copy):
            print("Ctrl + C")
            self.dataView.copy()
        if event.matches(Qg.QKeySequence.Paste):
            self.dataView.paste()
            print("Ctrl + V")
        if event.key() == Qt.Key_P and (event.modifiers() & Qt.ControlModifier):
            self.dataView.print()
            print("Ctrl + P")
        if event.key() == Qt.Key_D and (event.modifiers() & Qt.ControlModifier):
            self.debug()
            print("Ctrl + D")

    def debug(self):
        """Debug."""
        print(self.columnHeader.sizeHint())
        print(self.dataView.sizeHint())
        print(self.dataView.horizontalScrollBar().sizeHint())


# Remove dotted border on cell focus.  https://stackoverflow.com/a/55252650/3620725
class NoFocusDelegate(Qw.QStyledItemDelegate):
    def paint(self, QPainter, QStyleOptionViewItem, QModelIndex):
        """Paint event."""
        if QStyleOptionViewItem.state & Qw.QStyle.State_HasFocus:
            QStyleOptionViewItem.state = QStyleOptionViewItem.state ^ Qw.QStyle.State_HasFocus
        super().paint(QPainter, QStyleOptionViewItem, QModelIndex)


class DataTableModel(Qc.QAbstractTableModel):
    """Model for DataTableView to connect for DataFrame data."""

    def __init__(self, df, parent=None):
        super().__init__(parent)
        self.df = df

    def headerData(self, section, orientation, role=None):
        # Headers for DataTableView are hidden. Header data is shown in HeaderView
        pass

    def columnCount(self, parent=None):
        """Return the number of columns in the DataFrame."""
        if type(self.df) == pd.Series:
            return 1
        else:
            return self.df.columns.shape[0]

    def rowCount(self, parent=None):
        """Return the number of rows in the DataFrame."""
        return len(self.df)

    # Returns the data from the DataFrame
    def data(self, index, role=Qc.Qt.DisplayRole):
        """Return the data to display in the table."""
        if role == Qc.Qt.DisplayRole or role == Qc.Qt.EditRole or role == Qc.Qt.ToolTipRole:
            row = index.row()
            col = index.column()
            cell = self.df.iloc[row, col]

            # NaN case
            if pd.isnull(cell):
                return ""

            # Float formatting
            if isinstance(cell, (float, np.floating)):
                if not role == Qc.Qt.ToolTipRole:
                    return f"{cell:.4f}"

            return str(cell)

        elif role == Qc.Qt.ToolTipRole:
            row = index.row()
            col = index.column()
            cell = self.df.iloc[row, col]

            # NaN case
            if pd.isnull(cell):
                return "NaN"

            return str(cell)

    def flags(self, index):
        """Set the item flags at the given index."""
        # Set the table to be editable
        return Qc.Qt.ItemIsEditable | Qc.Qt.ItemIsEnabled | Qc.Qt.ItemIsSelectable

    # Set data in the DataFrame. Required if table is editable
    def setData(self, index, value, role=None):
        """Set the data at the given index."""
        if role == Qc.Qt.EditRole:
            row = index.row()
            col = index.column()
            try:
                self.df.iat[row, col] = value
            except Exception as e:
                print(e)
                return False
            self.dataChanged.emit(index, index)

            return True


class DataTableView(Qw.QTableView):
    """Displays the DataFrame data as a table."""

    def __init__(self, df, parent):
        super().__init__(parent)
        self.parent = parent

        # Create and set model
        self.set_data(df)

        # Hide the headers. The DataFrame headers (index & columns) will be displayed in the DataFrameHeaderViews
        self.horizontalHeader().hide()
        self.verticalHeader().hide()

        # Link selection to headers
        self.selectionModel().selectionChanged.connect(self.on_selection_changed)

        # Settings
        # self.setWordWrap(True)
        # self.resizeRowsToContents()
        self.setAlternatingRowColors(True)
        self.setHorizontalScrollMode(Qw.QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(Qw.QAbstractItemView.ScrollPerPixel)

    def set_data(self, df):
        """Set data model."""
        model = DataTableModel(df)
        self.setModel(model)

    def on_selection_changed(self):
        """
        Runs when cells are selected in the main table. This logic highlights the correct cells in the vertical and
        horizontal headers when a data cell is selected.
        """
        columnHeader = self.parent.columnHeader
        indexHeader = self.parent.indexHeader

        # The two blocks below check what columns or rows are selected in the data table and highlights the
        # corresponding ones in the two headers. The if statements check for focus on headers, because if the user
        # clicks a header that will auto-select all cells in that row or column which will trigger this function
        # and cause and infinite loop

        if not columnHeader.hasFocus():
            selection = self.selectionModel().selection()
            columnHeader.selectionModel().select(
                selection, Qc.QItemSelectionModel.Columns | Qc.QItemSelectionModel.ClearAndSelect
            )

        if not indexHeader.hasFocus():
            selection = self.selectionModel().selection()
            indexHeader.selectionModel().select(
                selection, Qc.QItemSelectionModel.Rows | Qc.QItemSelectionModel.ClearAndSelect
            )

    def print(self):
        """Print information."""
        print(self.model().df)

    def copy(self):
        """Copy the selected cells to clipboard in an Excel-pasteable format."""
        # from threading import Thread
        #
        # # Get the bounds using the top left and bottom right selected cells
        # indexes = self.selectionModel().selection().indexes()
        #
        # rows = [ix.row() for ix in indexes]
        # cols = [ix.column() for ix in indexes]
        #
        # df = self.model().df.iloc[min(rows) : max(rows) + 1, min(cols) : max(cols) + 1]
        #
        # # If I try to use Pyperclip without starting new thread large values give access denied error
        # def thread_function(df):
        #     df.to_clipboard(index=False, header=False)
        #
        # Thread(target=thread_function, args=(df,)).start()
        #
        # clipboard = Qg.QGuiApplication.clipboard()
        # clipboard.setText(text)

    def paste(self):
        """Paste data from clipboard."""
        # import sys
        #
        # # Set up clipboard object
        # app = Qw.QApplication.instance()
        # if not app:
        #     app = Qw.QApplication(sys.argv)
        # clipboard = app.clipboard()
        # # TODO
        # print(clipboard.text())

    def sizeHint(self):
        """Get size hint."""
        # Set width and height based on number of columns in model
        # Width
        width = 2 * self.frameWidth()  # Account for border & padding
        # width += self.verticalScrollBar().width()  # Dark theme has scrollbars always shown
        for i in range(self.model().columnCount()):
            width += self.columnWidth(i)

        # Height
        height = 2 * self.frameWidth()  # Account for border & padding
        # height += self.horizontalScrollBar().height()  # Dark theme has scrollbars always shown
        for i in range(self.model().rowCount()):
            height += self.rowHeight(i)
        return Qc.QSize(width, height)


class HeaderModel(Qc.QAbstractTableModel):
    """Model for HeaderView."""

    def __init__(self, df, orientation, parent=None):
        super().__init__(parent)
        self.df = df
        self.orientation = orientation

    def columnCount(self, parent=None):
        """Number of columns."""
        if self.orientation == Qt.Orientation.Horizontal:
            return self.df.columns.shape[0]
        else:  # Vertical
            return self.df.index.nlevels

    def rowCount(self, parent=None):
        """Number of rows."""
        if self.orientation == Qt.Orientation.Horizontal:
            return self.df.columns.nlevels
        elif self.orientation == Qt.Orientation.Vertical:
            return self.df.index.shape[0]

    def data(self, index, role=None):
        """Data."""
        row = index.row()
        col = index.column()

        if role == Qc.Qt.DisplayRole or role == Qc.Qt.ToolTipRole:
            if self.orientation == Qt.Orientation.Horizontal:
                if type(self.df.columns) == pd.MultiIndex:
                    return str(self.df.columns.values[col][row])
                else:
                    return str(self.df.columns.values[col])

            elif self.orientation == Qt.Orientation.Vertical:
                if type(self.df.index) == pd.MultiIndex:
                    return str(self.df.index.values[row][col])
                else:
                    return str(self.df.index.values[row])

    # The headers of this table will show the level names of the MultiIndex
    def headerData(self, section, orientation, role=None):
        """Header data."""
        if role in [Qc.Qt.DisplayRole, Qc.Qt.ToolTipRole]:
            if self.orientation == Qt.Orientation.Horizontal and orientation == Qt.Orientation.Vertical:
                if type(self.df.columns) == pd.MultiIndex:
                    return str(self.df.columns.names[section])
                else:
                    return str(self.df.columns.name)
            elif self.orientation == Qt.Orientation.Vertical and orientation == Qt.Orientation.Horizontal:
                if type(self.df.index) == pd.MultiIndex:
                    return str(self.df.index.names[section])
                else:
                    return str(self.df.index.name)
            else:
                return None  # These cells should be hidden anyways


class HeaderView(Qw.QTableView):
    """Displays the DataFrame index or columns depending on orientation."""

    df = None

    def __init__(self, parent: QtDataFrameWidget, df: pd.DataFrame, orientation: Qt.Orientation):
        super().__init__(parent)

        # Setup
        self.orientation = orientation
        self.parent = parent
        self.table = parent.dataView
        self.set_data(df)

        # These are used during column resizing
        self.header_being_resized = None
        self.resize_start_position = None
        self.initial_header_size = None

        # Handled by self.eventFilter()
        self.setMouseTracking(True)
        self.viewport().setMouseTracking(True)
        self.viewport().installEventFilter(self)

        # Settings
        self.setSizePolicy(Qw.QSizePolicy(Qw.QSizePolicy.Maximum, Qw.QSizePolicy.Maximum))
        self.setWordWrap(False)
        self.setFont(Qg.QFont("Times", weight=Qg.QFont.Bold))
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollMode(Qw.QAbstractItemView.ScrollPerPixel)
        self.setVerticalScrollMode(Qw.QAbstractItemView.ScrollPerPixel)

        # Link selection to DataTable
        self.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.setSpans()
        self.initSize()

        # Orientation specific settings
        if orientation == Qt.Orientation.Horizontal:
            self.setHorizontalScrollBarPolicy(
                Qt.ScrollBarPolicy.ScrollBarAlwaysOff
            )  # Scrollbar is replaced in DataFrameViewer
            self.horizontalHeader().hide()
            self.verticalHeader().setDisabled(True)
            self.verticalHeader().setHighlightSections(False)  # Selection lags a lot without this

        else:
            self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
            self.verticalHeader().hide()
            self.horizontalHeader().setDisabled(True)

            self.horizontalHeader().setHighlightSections(False)  # Selection lags a lot without this

        # Set initial size
        self.resize(self.sizeHint())

    def set_data(self, df):
        """Update dataframe."""
        self.df = df
        self.setModel(HeaderModel(df, self.orientation))

    # Header
    def on_selection_changed(self):
        """Runs when cells are selected in the Header.

        This selects columns in the data table when the header is clicked, and then calls selectAbove().
        """
        # Check focus so we don't get recursive loop, since headers trigger selection of data cells and vice versa
        if self.hasFocus():
            dataView = self.parent.dataView

            # Set selection mode so selecting one row or column at a time adds to selection each time
            if self.orientation == Qt.Orientation.Horizontal:  # This case is for the horizontal header
                # Get the header's selected columns
                selection = self.selectionModel().selection()

                # Removes the higher levels so that only the lowest level of the header affects the data table selection
                last_row_ix = self.df.columns.nlevels - 1
                last_col_ix = self.model().columnCount() - 1
                higher_levels = Qc.QItemSelection(
                    self.model().index(0, 0), self.model().index(last_row_ix - 1, last_col_ix)
                )
                selection.merge(higher_levels, Qc.QItemSelectionModel.SelectionFlag.Deselect)

                # Select the cells in the data view
                dataView.selectionModel().select(
                    selection,
                    Qc.QItemSelectionModel.SelectionFlag.Columns | Qc.QItemSelectionModel.SelectionFlag.ClearAndSelect,
                )
            if self.orientation == Qt.Orientation.Vertical:
                selection = self.selectionModel().selection()

                last_row_ix = self.model().rowCount() - 1
                last_col_ix = self.df.index.nlevels - 1
                higher_levels = Qc.QItemSelection(
                    self.model().index(0, 0), self.model().index(last_row_ix, last_col_ix - 1)
                )
                selection.merge(higher_levels, Qc.QItemSelectionModel.SelectionFlag.Deselect)

                dataView.selectionModel().select(
                    selection,
                    Qc.QItemSelectionModel.SelectionFlag.Rows | Qc.QItemSelectionModel.SelectionFlag.ClearAndSelect,
                )

        self.selectAbove()

    # Take the current set of selected cells and make it so that any spanning cell above a selected cell is selected too
    # This should happen after every selection change
    def selectAbove(self):
        """Select above."""
        if self.orientation == Qt.Orientation.Horizontal:
            if self.df.columns.nlevels == 1:
                return
        else:
            if self.df.index.nlevels == 1:
                return

        for ix in self.selectedIndexes():
            if self.orientation == Qt.Orientation.Horizontal:
                # Loop over the rows above this one
                for row in range(ix.row()):
                    ix2 = self.model().index(row, ix.column())
                    self.setSelection(self.visualRect(ix2), Qc.QItemSelectionModel.SelectionFlag.Select)
            else:
                # Loop over the columns left of this one
                for col in range(ix.column()):
                    ix2 = self.model().index(ix.row(), col)
                    self.setSelection(self.visualRect(ix2), Qc.QItemSelectionModel.SelectionFlag.Select)

    # Fits columns to contents but with a minimum width and added padding
    def initSize(self):
        """Initialize size."""
        padding = 20

        if self.orientation == Qt.Orientation.Horizontal:
            min_size = 100

            self.resizeColumnsToContents()

            for col in range(self.model().columnCount()):
                width = self.columnWidth(col)
                if width + padding < min_size:
                    new_width = min_size
                else:
                    new_width = width + padding

                self.setColumnWidth(col, new_width)
                self.table.setColumnWidth(col, new_width)
        else:
            self.resizeColumnsToContents()
            for col in range(self.model().columnCount()):
                width = self.columnWidth(col)
                self.setColumnWidth(col, width + padding)

    # This sets spans to group together adjacent cells with the same values
    def setSpans(self):
        """Set spans."""
        df = self.model().df

        # Find spans for horizontal HeaderView
        if self.orientation == Qt.Orientation.Horizontal:
            # Find how many levels the MultiIndex has
            if type(df.columns) == pd.MultiIndex:
                N = len(df.columns[0])
            else:
                N = 1

            for level in range(N):  # Iterates over the levels
                # Find how many segments the MultiIndex has
                if type(df.columns) == pd.MultiIndex:
                    arr = [df.columns[i][level] for i in range(len(df.columns))]
                else:
                    arr = df.columns

                # Holds the starting index of a range of equal values.
                # None means it is not currently in a range of equal values.
                match_start = None

                for col in range(1, len(arr)):  # Iterates over cells in row
                    # Check if cell matches cell to its left
                    if arr[col] == arr[col - 1]:
                        if match_start is None:
                            match_start = col - 1
                        # If this is the last cell, need to end it
                        if col == len(arr) - 1:
                            match_end = col
                            span_size = match_end - match_start + 1
                            self.setSpan(level, match_start, 1, span_size)
                    else:
                        if match_start is not None:
                            match_end = col - 1
                            span_size = match_end - match_start + 1
                            self.setSpan(level, match_start, 1, span_size)
                            match_start = None

        # Find spans for vertical HeaderView
        else:
            # Find how many levels the MultiIndex has
            if type(df.index) == pd.MultiIndex:
                N = len(df.index[0])
            else:
                N = 1

            for level in range(N):  # Iterates over the levels
                # Find how many segments the MultiIndex has
                if type(df.index) == pd.MultiIndex:
                    arr = [df.index[i][level] for i in range(len(df.index))]
                else:
                    arr = df.index

                # Holds the starting index of a range of equal values.
                # None means it is not currently in a range of equal values.
                match_start = None

                for row in range(1, len(arr)):  # Iterates over cells in column
                    # Check if cell matches cell above
                    if arr[row] == arr[row - 1]:
                        if match_start is None:
                            match_start = row - 1
                        # If this is the last cell, need to end it
                        if row == len(arr) - 1:
                            match_end = row
                            span_size = match_end - match_start + 1
                            self.setSpan(match_start, level, span_size, 1)
                    else:
                        if match_start is not None:
                            match_end = row - 1
                            span_size = match_end - match_start + 1
                            self.setSpan(match_start, level, span_size, 1)
                            match_start = None

    def over_header_edge(self, mouse_position, margin=3):
        """Return the index of the column or row the mouse is over the edge of, or None if it is not over an edge."""
        # Return the index of the column this x position is on the right edge of
        if self.orientation == Qt.Orientation.Horizontal:
            x = mouse_position
            if self.columnAt(x - margin) != self.columnAt(x + margin):
                if self.columnAt(x + margin) == 0:
                    # We're at the left edge of the first column
                    return None
                else:
                    return self.columnAt(x - margin)
            else:
                return None

        # Return the index of the row this y position is on the top edge of
        elif self.orientation == Qt.Orientation.Vertical:
            y = mouse_position
            if self.rowAt(y - margin) != self.rowAt(y + margin):
                if self.rowAt(y + margin) == 0:
                    # We're at the top edge of the first row
                    return None
                else:
                    return self.rowAt(y - margin)
            else:
                return None

    def eventFilter(self, object: Qc.QObject, event: Qc.QEvent):
        """Event filter."""
        # If mouse is on an edge, start the drag resize process
        if event.type() == Qc.QEvent.Type.MouseButtonPress:
            if self.orientation == Qt.Orientation.Horizontal:
                mouse_position = event.pos().x()
            elif self.orientation == Qt.Orientation.Vertical:
                mouse_position = event.pos().y()

            if self.over_header_edge(mouse_position) is not None:
                self.header_being_resized = self.over_header_edge(mouse_position)
                self.resize_start_position = mouse_position
                if self.orientation == Qt.Orientation.Horizontal:
                    self.initial_header_size = self.columnWidth(self.header_being_resized)
                elif self.orientation == Qt.Orientation.Vertical:
                    self.initial_header_size = self.rowHeight(self.header_being_resized)
                return True
            else:
                self.header_being_resized = None

        # End the drag process
        if event.type() == Qc.QEvent.Type.MouseButtonRelease:
            self.header_being_resized = None

        # Auto size the column that was double clicked
        if event.type() == Qc.QEvent.Type.MouseButtonDblClick:
            if self.orientation == Qt.Orientation.Horizontal:
                mouse_position = event.pos().x()
            elif self.orientation == Qt.Orientation.Vertical:
                mouse_position = event.pos().y()

            # Find which column or row edge the mouse was over and auto size it
            if self.over_header_edge(mouse_position) is not None:
                header_index = self.over_header_edge(mouse_position)
                if self.orientation == Qt.Orientation.Horizontal:
                    self.parent.auto_size_column(header_index)
                elif self.orientation == Qt.Orientation.Vertical:
                    self.parent.auto_size_row(header_index)
                return True

        # Handle active drag resizing
        if event.type() == Qc.QEvent.Type.MouseMove:
            if self.orientation == Qt.Orientation.Horizontal:
                mouse_position = event.pos().x()
            elif self.orientation == Qt.Orientation.Vertical:
                mouse_position = event.pos().y()

            # If this is None, there is no drag resize happening
            if self.header_being_resized is not None:
                size = self.initial_header_size + (mouse_position - self.resize_start_position)
                if size > 10:
                    if self.orientation == Qt.Orientation.Horizontal:
                        self.setColumnWidth(self.header_being_resized, size)
                        self.parent.dataView.setColumnWidth(self.header_being_resized, size)
                    if self.orientation == Qt.Orientation.Vertical:
                        self.setRowHeight(self.header_being_resized, size)
                        self.parent.dataView.setRowHeight(self.header_being_resized, size)

                    self.updateGeometry()
                    self.parent.dataView.updateGeometry()
                return True

            # Set the cursor shape
            if self.over_header_edge(mouse_position) is not None:
                if self.orientation == Qt.Orientation.Horizontal:
                    self.viewport().setCursor(Qg.QCursor(Qt.CursorShape.SplitHCursor))
                elif self.orientation == Qt.Orientation.Vertical:
                    self.viewport().setCursor(Qg.QCursor(Qt.CursorShape.SplitVCursor))
            else:
                self.viewport().setCursor(Qg.QCursor(Qt.CursorShape.ArrowCursor))

        return False

    # Return the size of the header needed to match the corresponding DataTableView
    def sizeHint(self):
        """Size hint."""
        # Horizontal HeaderView
        if self.orientation == Qt.Orientation.Horizontal:
            # Width of DataTableView
            width = self.table.sizeHint().width() + self.verticalHeader().width()
            # Height
            height = 2 * self.frameWidth()  # Account for border & padding
            for i in range(self.model().rowCount()):
                height += self.rowHeight(i)

        # Vertical HeaderView
        else:
            # Height of DataTableView
            height = self.table.sizeHint().height() + self.horizontalHeader().height()
            # Width
            width = 2 * self.frameWidth()  # Account for border & padding
            for i in range(self.model().columnCount()):
                width += self.columnWidth(i)
        return Qc.QSize(width, height)

    # This is needed because otherwise when the horizontal header is a single row it will add whitespace to be bigger
    def minimumSizeHint(self):
        """Minimum size hint."""
        if self.orientation == Qt.Orientation.Horizontal:
            return Qc.QSize(0, self.sizeHint().height())
        else:
            return Qc.QSize(self.sizeHint().width(), 0)


# This is a fixed size widget with a size that tracks some other widget
class TrackingSpacer(Qw.QFrame):
    """Tracking spacer."""

    def __init__(self, ref_x=None, ref_y=None):
        super().__init__()
        self.ref_x = ref_x
        self.ref_y = ref_y

    def minimumSizeHint(self):
        """Minimize size hint."""
        width = 0
        height = 0
        if self.ref_x:
            width = self.ref_x.width()
        if self.ref_y:
            height = self.ref_y.height()

        return Qc.QSize(width, height)


# Examples
if __name__ == "__main__":  # pragma: no cover
    import sys

    from qtextra.utils.dev import qframe

    app, frame, va = qframe(False)
    frame.setMinimumSize(400, 400)

    array = pd.DataFrame(
        {
            ("a", "b"): {("A", "B"): 1, ("A", "C"): 2},
            ("a", "a"): {("A", "C"): 3, ("A", "B"): 4},
            ("a", "c"): {("A", "B"): 5, ("A", "C"): 6},
            ("b", "a"): {("A", "C"): 7, ("A", "B"): 8},
            ("b", "b"): {("A", "D"): 9, ("A", "B"): 10},
        }
    )
    widget = QtDataFrameWidget(None, array)
    va.addWidget(widget, stretch=True)
    btn = Qw.QPushButton("Press me to change data")
    btn.clicked.connect(lambda: widget.set_data(pd.DataFrame(np.random.randint(-255, 255, (10, 10)) / 255)))
    va.addWidget(btn)

    frame.show()
    sys.exit(app.exec_())
