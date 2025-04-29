import copy
import numbers
import pandas as pd
import numpy as np
import statstables as st
from abc import ABC, abstractmethod
from scipy import stats
from typing import Union, Callable
from collections import defaultdict, ChainMap
from pathlib import Path
from .renderers import LatexRenderer, HTMLRenderer, ASCIIRenderer
from .utils import pstars, validate_line_location, VALID_LINE_LOCATIONS, latex_preamble
from .parameters import TableParams, MeanDiffsTableParams, ModelTableParams
from .cellformatting import DEFAULT_FORMATS, validate_format_dict


class Table(ABC):
    """
    Abstract class for defining common characteristics/methods of all tables
    """

    VALID_ALIGNMENTS = ["l", "r", "c", "left", "right", "center"]

    def __init__(
        self,
        *,
        caption_location: str | None = None,
        sig_digits: int | None = None,
        thousands_sep: str | None = None,
        show_columns: bool | None = None,
        include_index: bool | None = None,
        column_labels: dict | None = None,
        index_labels: dict | None = None,
        notes: list[tuple] | None = None,
        label: str | None = None,
        caption: str | None = None,
        index_name: str = "",
        formatters: dict | None = None,
        default_formatter: Callable | None = None,
        longtable: bool = False,
        **kwargs,
    ):
        user_params = {
            k: v
            for k, v in {
                "caption_location": caption_location,
                "sig_digits": sig_digits,
                "thousands_sep": thousands_sep,
                "show_columns": show_columns,
                "include_index": include_index,
            }.items()
            if v is not None
        } | kwargs

        self.table_params = TableParams(user_params)
        self.reset_custom_features()
        self.rename_columns(column_labels)
        self.rename_index(index_labels)
        self.add_notes(notes)
        self.label = label
        self.caption = caption
        self.index_name = index_name
        self.default_formatter = self._default_formatter
        if default_formatter is not None:
            self.default_formatter = default_formatter
        self.custom_formatters(formatters)
        self.longtable = longtable
        self.panel_label = None
        self.panel_label_alignment = "l"

    def reset_params(self, restore_to_defaults=False) -> None:
        """
        Resets all parameters to their default values
        """
        self.table_params.reset_params(restore_to_defaults)

    def reset_custom_features(self):
        self._multicolumns = []
        self._index_labels = dict()
        self._column_labels = dict()
        self.notes = []
        self._formatters = dict()
        self.custom_lines = defaultdict(list)
        self.custom_tex_lines = defaultdict(list)
        self.custom_html_lines = defaultdict(list)

    def reset_all(self, restore_to_defaults=False):
        self.reset_params(restore_to_defaults)
        self.reset_custom_features()

    def update_parameter(self, param, value):
        """
        Helper method for updating a parameter
        """
        self.table_params[param] = value

    def rename_columns(self, column_labels: dict | None) -> None:
        """
        Rename the columns in the table. The keys of the column_labels should be the
        current column labels and the values should be the new labels.

        Parameters
        ----------
        column_labels : dict
            _description_
        """
        if column_labels is None:
            return None
        assert isinstance(column_labels, dict), "column_labels must be a dictionary"
        self._column_labels.update(column_labels)

    def rename_index(self, index_labels: dict | None) -> None:
        """
        Rename the index labels in the table. The keys of the index_labels should
        be the current index labels and the values should be the new labels.

        Parameters
        ----------
        index_labels : dict
            Dictionary where the keys are the current index labels and the values
            are the new labels.
        """
        if index_labels is None:
            return None
        assert isinstance(index_labels, dict), "index_labels must be a dictionary"
        self._index_labels.update(index_labels)

    # TODO: Add method for creating index labels that span multiple rows
    def add_multicolumns(
        self,
        columns: str | list[str],
        spans: list[int] | None = None,
        formats: list[str] | None = None,
        position: int | None = None,
        underline: bool = True,
    ) -> None:
        """
        All columns that span multiple columns in the table. These will be placed
        above the individual column labels. The sum of the spans must equal the
        number of columns in the table, not including the index.

        Parameters
        ----------
        columns : Union[str, list[str]]
            If a single string is provided, it will span the entire table. If a list
            is provided, each will span the number of columns in the corresponding
            index of the spans list.
        spans : list[int]
            List of how many columns each multicolumn should span.
        formats : list[str], optional
            Not implemented yet. Will eventually allow for text formatting (bold,
            underline, etc.), by default None
        """
        # TODO: implement formats (underline, bold, etc.)
        # TODO: Allow for placing the multicolumns below the table body
        if not spans:
            spans = [self.ncolumns]
        assert len(columns) == len(
            spans
        ), "A column label must be provided for each column in the table"
        assert (
            sum(spans) == self.ncolumns
        ), f"The sum of spans must equal the number of columns. There are {self.ncolumns} columns, but spans sum to {sum(spans)}"
        _position = len(self._multicolumns) if position is None else position
        self._multicolumns.insert(_position, (columns, spans, underline))

    def remove_multicolumn(self, column=None, index=None, all=False) -> None:
        """
        Remove a multicolumn from the table. The column can be specified using
        either the column itself or its index in the multicolumns list.

        Parameters
        ----------
        column : str, optional
            The column to remove, by default None
        index : int, optional
            The index of the column to remove, by default None
        all : bool, optional
            If true, remove all multicolumn previously provided
        """
        if all:
            self._multicolumns.clear()
            return None
        if column is None and index is None:
            raise ValueError("Either 'column' or 'index' must be provided")
        if column is not None:
            self._multicolumns.remove(column)
        elif index is not None:
            self._multicolumns.pop(index)

    # def add_multiindex(self, index: list[str], spans: list[tuple]) -> None:
    #     """
    #     Add a multiindex to the table. This will be placed above the index column
    #     in the table. The sum of the spans must equal the number of rows in the table.

    #     Parameters
    #     ----------
    #     index : list[str]
    #         List of labels for the multiindex
    #     spans : list[tuple]
    #         List of tuples that indicate where the index should start and how many
    #         rows it should span. The first element of the tuple should be the row
    #         it starts and the second should be the number of rows it spans.
    #     """
    #     assert len(index) == len(spans), "index and spans must be the same length"
    #     self._multiindex.append((index, spans))
    #     for i, s in zip(index, spans):
    #         self._multiindex[s[0]] = {"index": i, "end": s[1]}

    def custom_formatters(self, formatters: dict | None) -> None:
        """
        Method to set custom formatters either along the columns or index. Each
        key in the formatters dict must be a function that returns a string.

        You cannot set both column and index formatters at this time. Whichever
        is set last will be the one used.

        Parameters
        ----------
        formatters : dict
            Dictionary of fuctions to format the values. The keys should correspond
            to either a column or index label in the table. If you want to format
            along both axis, the key should be a tuple of the form: (index, column)
        axis : str, optional
            Which axis to format along, by default "columns"

        Raises
        ------
        ValueError
            Error is raised if the values in the formatters dict are not functions
        """
        if formatters is None:
            return None
        assert all(
            callable(f) for f in formatters.values()
        ), "Values in the formatters dict must be functions"
        self._formatters.update(formatters)

    def add_note(
        self,
        note: str,
        alignment: str = "r",
        escape: bool = True,
        position: int | None = None,
    ) -> None:
        """
        Adds a single line note to the bottom on the table, under the bottom line.

        Parameters
        ----------
        note : str
            The text of the note
        alignment : str, optional
            Which side of the table to align the note, by default "l"
        escape : bool, optional
            If true, a "\" is added LaTeX characters that must be escaped, by default True
        position : int, optional
            The position in the notes list to insert the note. Inserts note at the
            end of the list by default.
        """
        assert isinstance(note, str), "Note must be a string"
        assert alignment in ["l", "c", "r"], "alignment must be 'l', 'c', or 'r'"
        _position = len(self.notes) if position is None else position
        self.notes.insert(_position, (note, alignment, escape))

    def add_notes(self, notes: list[tuple] | None) -> None:
        """
        Adds multiple notes to the table. Each element of notes should be a tuple
        where the first element is the text of the note, the second is the alignment
        parameter and the third is the escape parameter.
        """
        if notes is None:
            return None
        for i, note in enumerate(notes):
            try:
                self.add_note(note=note[0], alignment=note[1], escape=note[2])
            except Exception as e:
                raise ValueError(f"Note {i} yields error {e}")

    def remove_note(
        self, note: str | None = None, index: int | None = None, all: bool = False
    ) -> None:
        """
        Removes a note that has been added to the table. To specify which note,
        either pass the text of the note as the 'note' parameter or the index of
        the note as the 'index' parameter.

        Parameters
        ----------
        note : str, optional
            Text of note to remove, by default None
        index : int, optional
            Index of the note to be removed, by default None
        all : bool, optional
            If true, remove all notes from the table

        Raises
        ------
        ValueError
            Raises and error if neither 'note' or 'index' are provided
        """
        if all:
            self.notes.clear()
            return None
        if note is None and index is None:
            raise ValueError("Either 'note' or 'index' must be provided")
        if note is not None:
            self.notes.remove(note)
        elif index is not None:
            self.notes.pop(index)

    def add_line(
        self,
        line: list[str],
        location: str = "after-body",
        label: str = "",
        deliminate: bool = False,
        position: int | None = None,
    ) -> None:
        """
        Add a line to the table that will be rendered at the specified location.
        The line will be formatted to fit the table and the number of elements in
        the list should equal the number of columns in the table. The index label
        for the line is an empty string by default, but can be specified with the
        label parameter.

        Parameters
        ----------
        line : list[str]
            A list with each element that will comprise the line. the number of
            elements of this list should equal the number of columns in the table
        location : str, optional
            Where on the table to place the line, by default "after-body"
        label : str, optional:
            The index label for the line, by default ""
        deliminate: bool, optional
            If true, a horizontal line will be placed above the line
        position : int, optional:
            The position in the order of lines to insert this line
        """
        validate_line_location(location)
        assert (
            len(line) == self.ncolumns
        ), f"Line must have the same number of columns. There are {self.ncolumns} but only {len(line)} line entries"
        _position = len(self.custom_lines[location]) if position is None else position
        self.custom_lines[location].insert(
            _position, {"line": line, "label": label, "deliminate": deliminate}
        )

    def remove_line(
        self,
        location: str | None = None,
        line: list | None = None,
        index: int | None = None,
        all: bool = False,
    ) -> None:
        """
        Remove a custom line. To specify which line to remove, either pass the list
        containing the line as the 'line' parameter or the index of the line as the
        'index' parameter.

        Parameters
        ----------
        location : str | None
            Where in the table the line is located. If not provided and `all`
            is true, all lines in every location will be removed.
        line : list, optional
            List containing the line elements, by default None
        index : int, optional
            Index of the line in the custom line list for the specified location, by default None
        all : bool, optional
            Remove all custom lines. If true and `location` = None, all custom
            lines in every position will be removed. Otherwise only the lines
            in the provided location are removed.

        Raises
        ------
        ValueError
            Raises an error if neither 'line' or 'index' are provided, or if the
            line cannot be found in the custom lines list.
        """
        if location is None and all:
            for loc in VALID_LINE_LOCATIONS:
                self.custom_lines[loc].clear()
            return None
        if location is None and not all:
            raise ValueError("Either a location must be provided or all must be true")
        validate_line_location(location)
        if line is None and index is None:
            raise ValueError("Either 'line' or 'index' must be provided")

        if all:
            self.custom_lines[location].clear()
            return None
        if line is not None:
            self.custom_lines[location].remove(line)
        elif index is not None:
            self.custom_lines[location].pop(index)

    def add_latex_line(self, line: str, location: str = "after-body") -> None:
        """
        Add line that will only be rendered in the LaTeX output. This method
        assumes the line is formatted as needed, including escape characters and
        line breaks. The provided line will be rendered as is. Note that this is
        different from the generic add_line method, which will format the line
        to fit in either LaTeX or HTML output.

        Parameters
        ----------
        line : str
            The line to add to the table
        location : str, optional
            Where in the table to place the line, by default "bottom"
        """
        validate_line_location(location)
        self.custom_tex_lines[location].append(line)

    def remove_latex_line(
        self,
        location: str | None = None,
        line: str | None = None,
        index: int | None = None,
        all: bool = False,
    ) -> None:
        """
        Remove a custom LaTex line. To specify which line to remove, either pass the list
        containing the line as the 'line' parameter or the index of the line as the
        'index' parameter.

        Parameters
        ----------
        location : str
            Where in the table the line is located.
        line : list, optional
            List containing the line elements.
        index : int, optional
            Index of the line in the custom line list for the specified location.
        all : bool, optional
            Remove all custom LaTex lines. If true and `location` = None, all custom
            lines in every position will be removed. Otherwise only the lines
            in the provided location are removed.

        Raises
        ------
        ValueError
            Raises an error if neither 'line' or 'index' are provided, or if the
            line cannot be found in the custom lines list.
        """
        if location is None and all:
            for loc in VALID_LINE_LOCATIONS:
                self.custom_tex_lines[loc].clear()
            return None
        if location is None and not all:
            raise ValueError("Either a location must be provided or all must be true")
        validate_line_location(location)
        if line is None and index is None:
            raise ValueError("Either 'line' or 'index' must be provided")

        if line is not None:
            self.custom_tex_lines[location].remove(line)
        elif index is not None:
            self.custom_tex_lines[location].pop(index)

    def add_html_line(self, line: str, location: str = "bottom") -> None:
        """
        Add line that will only be rendered in the HTML output. This method
        assumes the line is formatted as needed, including line breaks. The
        provided line will be rendered as is. Note that this is different from
        the generic add_line method, which will format the line to fit in either
        LaTeX or HTML output.

        Parameters
        ----------
        line : str
            The line to add to the table
        location : str, optional
            Where in the table to place the line. By default "bottom", other options
            are: 'top', 'after-multicolumns', 'after-columns', 'after-body', 'after-footer'.
            Note: not all of these are implemented yet.
        """
        validate_line_location(location)
        self.custom_html_lines[location].append(line)

    def remove_html_line(
        self,
        location: str | None = None,
        line: str | None = None,
        index: int | None = None,
        all: bool = False,
    ):
        """
        Remove a custom HTML line. To specify which line to remove, either pass the list
        containing the line as the 'line' parameter or the index of the line as the
        'index' parameter.

        Parameters
        ----------
        location : str
            Where in the table the line is located.
        line : list, optional
            List containing the line elements.
        index : int, optional
            Index of the line in the custom line list for the specified location.
        all : bool, optional
            Remove all custom LaTex lines. If true and `location` = None, all custom
            lines in every position will be removed. Otherwise only the lines
            in the provided location are removed.

        Raises
        ------
        ValueError
            Raises an error if neither 'line' or 'index' are provided, or if the
            line cannot be found in the custom lines list.
        """
        if location is None and all:
            for loc in VALID_LINE_LOCATIONS:
                self.custom_html_lines[loc].clear()
            return None
        if location is None and not all:
            raise ValueError("Either a location must be provided or all must be true")
        validate_line_location(location)
        if line is None and index is None:
            raise ValueError("Either 'line' or 'index' must be provided")

        if line is not None:
            self.custom_html_lines[location].remove(line)
        elif index is not None:
            self.custom_html_lines[location].pop(index)

    def render_latex(
        self,
        outfile: Union[str, Path, None] = None,
        only_tabular=False,
        *args,
        **kwargs,
    ) -> str | None:
        """
        Render the table in LaTeX. Note that you will need to include the booktabs
        package in your LaTeX document. If no outfile is provided, the LaTeX
        string will be returned, otherwise the text will be written to the specified
        file.

        Parameters
        ----------
        outfile : str, Path, optional
            File to write the text to, by default None.
        only_tabular : bool, optional
            If True, the text will only be wrapped in a tabular enviroment. If
            false, the text will also be wrapped in a table enviroment. It is
            False by default.

        Returns
        -------
        Union[str, None]
            If an outfile is not specified, the LaTeX string will be returned.
            Otherwise None will be returned.
        """
        # longtable environments are their own thing. They don't go in table environments
        if self.longtable:
            only_tabular = True
        tex_str = LatexRenderer(self).render(only_tabular=only_tabular)
        if not outfile:
            return tex_str
        preamble = latex_preamble()
        tex_str = preamble + tex_str
        Path(outfile).write_text(tex_str)
        return None

    def render_html(
        self,
        outfile: Union[str, Path, None] = None,
        table_class="",
        convert_latex=True,
        *args,
        **kwargs,
    ) -> str | None:
        """
        Render the table in HTML. Note that you will need to include the booktabs
        package in your LaTeX document. If no outfile is provided, the LaTeX
        string will be returned, otherwise the text will be written to the specified
        file.

        This is also used in the _repr_html_ method to render the tables in
        Jupyter notebooks.

        Parameters
        ----------
        outfile : str, Path, optional
            File to write the text to, by default None.

        Returns
        -------
        Union[str, None]
            If an outfile is not specified, the HTML string will be returned.
            Otherwise None will be returned.
        """
        html_str = HTMLRenderer(self, _class=table_class).render(
            convert_latex=convert_latex
        )
        if not outfile:
            return html_str
        Path(outfile).write_text(html_str)
        return None

    def render_ascii(self, convert_latex=True) -> str:
        return ASCIIRenderer(self).render(convert_latex=convert_latex)

    def __str__(self) -> str:
        return self.render_ascii()

    def __repr__(self) -> str:
        return self.render_ascii()

    def _repr_html_(self):
        return self.render_html()

    def _default_formatter(self, value: Union[int, float, str], **kwargs) -> str:
        thousands_sep = self.table_params["thousands_sep"]
        sig_digits = self.table_params["sig_digits"]
        # format the numbers, otherwise just return a string
        if isinstance(value, numbers.Number):
            if float(value).is_integer():
                return f"{value:{thousands_sep}.0f}"
            return f"{value:{thousands_sep}.{sig_digits}f}"
        return str(value)

    def _format_value(
        self,
        _index: str | int | None,
        col: str | int | None,
        value: Union[int, float, str],
        **kwargs,
    ) -> ChainMap:
        if (_index, col) in self._formatters.keys():
            formatter = self._formatters[(_index, col)]
        elif _index in self._formatters.keys():
            formatter = self._formatters.get(_index, self._default_formatter)
        elif col in self._formatters.keys():
            formatter = self._formatters.get(col, self._default_formatter)
        else:
            formatter = self.default_formatter
        # for if the row is blank
        if value == "":
            return ChainMap({"value": ""}, DEFAULT_FORMATS)
        # attempting to pass in the kwargs allows users to define formatter
        # functions that take in additonal arguments. If their function doesn't,
        # just pass in the value.
        try:
            formatted_value = formatter(value, **kwargs)
        except TypeError:
            formatted_value = formatter(value)

        if isinstance(formatted_value, str):
            return ChainMap({"value": formatted_value}, DEFAULT_FORMATS)
        elif isinstance(formatted_value, dict):
            validate_format_dict(formatted_value)
            return ChainMap(formatted_value, DEFAULT_FORMATS)
        else:
            raise ValueError(
                f"Formatter must return a dictionary or string. Returns {type(formatted_value)}"
            )

    @abstractmethod
    def _create_rows(self) -> list[list[ChainMap]]:
        """
        This method should return a list of lists, where each inner list is a
        row in the body of the table. Each element of those inner lists should
        be one cell in the table.
        """
        # TODO: Make it return a list of dictionaries instead of strings.
        # Dictionaries will contain information on formatting (bold, italic, color, etc.)
        pass

    @staticmethod
    def _validate_input_type(value, dtype):
        if not isinstance(value, dtype):
            raise TypeError(f"{value} must be a {dtype}")

    ##### Properties #####

    @property
    def ncolumns(self) -> int:
        return self._ncolumns

    @ncolumns.setter
    def ncolumns(self, ncolumns: int) -> None:
        self._ncolumns = ncolumns

    @property
    def caption_location(self) -> str:
        """
        Location of the caption in the table. Can be either 'top' or 'bottom'.
        """
        return self.table_params["caption_location"]

    @property
    def caption(self) -> str | None:
        """
        Caption for the table. This will be placed above or below the table,
        depending on the caption_location parameter.
        """
        return self._caption

    @caption.setter
    def caption(self, caption: str | None = None) -> None:
        assert isinstance(caption, (str, type(None))), "Caption must be a string"
        self._caption = caption

    @property
    def label(self) -> str | None:
        """
        Label for the table. This will be used to reference the table in LaTeX.
        """
        return self._label

    @label.setter
    def label(self, label: str | None = None) -> None:
        assert isinstance(label, (str, type(None))), "Label must be a string"
        self._label = label

    @property
    def index_name(self) -> str:
        """
        Name of the index column in the table
        """
        return self._index_name

    @index_name.setter
    def index_name(self, name: str) -> None:
        assert isinstance(name, str), "index_name must be a string"
        self._index_name = name

    @property
    def panel_label(self) -> str | None:
        """
        Labeled used if the table is part of a panel
        """
        return self._panel_label

    @panel_label.setter
    def panel_label(self, label: str | None):
        assert isinstance(label, str) or label is None
        self._panel_label = label


class GenericTable(Table):
    """
    A generic table will take in any DataFrame and allow for easy formating and
    column/index naming
    """

    def __init__(self, df: pd.DataFrame | pd.Series, **kwargs):
        self.df = df
        self.ncolumns = df.shape[1]
        self.columns = df.columns
        self.nrows = df.shape[0]
        super().__init__(**kwargs)

    def reset_params(self, restore_to_defaults=False):
        super().reset_params(restore_to_defaults)

    def reset_custom_features(self):
        super().reset_custom_features()

    def _create_rows(self):
        rows = []
        for _index, row in self.df.iterrows():
            _row = [
                self._format_value(
                    f"{_index}_label", "_index", self._index_labels.get(_index, _index)
                )
            ]
            for col, value in zip(row.index, row.values):
                formated_val = self._format_value(_index, col, value)
                # TODO: return a dictionary with all of the formatting options
                _row.append(formated_val)
            if not self.table_params["include_index"]:
                _row.pop(0)
            # if _index in self._multiindex.keys():
            #     _row.insert(0, self._multiindex[_index]["index"])
            rows.append(_row)
        return rows


class MeanDifferenceTable(Table):
    def __init__(
        self,
        df: pd.DataFrame,
        var_list: list,
        group_var: str,
        diff_pairs: list[tuple] | None = None,
        alternative: str = "two-sided",
        *,
        caption_location: str | None = None,
        sig_digits: int = 3,
        thousands_sep: str = ",",
        show_columns: bool = True,
        show_n: bool | None = None,
        show_standard_errors: bool | None = None,
        p_values: list | None = None,
        show_stars: bool | None = None,
        show_significance_levels: bool | None = None,
        column_labels: dict | None = None,
        index_labels: dict | None = None,
        notes: list[tuple] | None = None,
        label: str | None = None,
        caption: str | None = None,
        index_name: str = "",
        formatters: dict | None = None,
        default_formatter: Callable | None = None,
        longtable: bool = False,
        **kwargs,
    ):
        """
        Table that shows the difference in means between the specified groups in
        the data. If there are only two groups, the table will show the difference
        between the two.

        Parameters
        ----------
        df : pd.DataFrame
            DataFrame containing the raw data to be compared
        var_list : list
            List of variables to compare means to between the groups
        group_var : str
            The variable in the data to group by
        diff_pairs : list[tuple], optional
            A list containing all of the pairs to take difference between. The
            order they are listed in the tuple will be how they are subtracted.
            If not specified, the difference between the two groups will be taken.
            This must be specified when there are more than two groups.
        alternative : str, optional
            The alternative hypothesis for the t-test. It is a two-sided test
            by default, but can be set to 'greater' or 'less' for a one-sided test.
            For now, the same test is applied to each variable.
        """
        user_params = {
            k: v
            for k, v in {
                "caption_location": caption_location,
                "sig_digits": sig_digits,
                "thousands_sep": thousands_sep,
                "show_columns": show_columns,
                "show_n": show_n,
                "show_standard_errors": show_standard_errors,
                "p_values": p_values,
                "show_stars": show_stars,
                "show_significance_levels": show_significance_levels,
            }.items()
            if v is not None
        }
        self.table_params = MeanDiffsTableParams(user_params)
        # TODO: allow for grouping on multiple variables
        self.groups = df[group_var].unique()
        self.ngroups = len(self.groups)
        self.var_list = var_list
        if self.ngroups > 2 and not diff_pairs:
            raise ValueError(
                "`diff_pairs` argument must be provided if there are more than 2 groups"
            )
        if self.ngroups < 2:
            raise ValueError("There must be at least two groups")
        self.alternative = alternative
        self.type_gdf = df.groupby(group_var)
        # adjust these to only count non-null values
        self.grp_sizes = self.type_gdf.size()
        self.grp_sizes["Overall Mean"] = df.shape[0]
        self.means = self.type_gdf[var_list].mean().T
        # add toal means column to means
        self.means["Overall Mean"] = df[var_list].mean()
        total_sem = df[var_list].sem()
        total_sem.name = "Overall Mean"
        self.sem = pd.merge(
            self.type_gdf[var_list].sem().T,
            total_sem,
            left_index=True,
            right_index=True,
        )
        self.diff_pairs = diff_pairs
        self.ndiffs = len(self.diff_pairs) if self.diff_pairs else 1
        self.t_stats = {}
        self.pvalues = {}
        self.reset_params()
        self._get_diffs()
        self.ncolumns = self.means.shape[1]
        # convert columns to strings to avoid issues with numerical groups
        self.columns = self.means.columns.astype(str)
        self.reset_custom_features()
        self.rename_columns(column_labels)
        self.rename_index(index_labels)
        self.add_notes(notes)
        self.label = label
        self.caption = caption
        self.index_name = index_name
        self.default_formatter = self._default_formatter
        if default_formatter is not None:
            self.default_formatter = default_formatter
        self.custom_formatters(formatters)
        self.longtable = longtable
        self.panel_label = None
        self.panel_label_alignment = "l"

    def reset_params(self, restore_to_defaults=False):
        super().reset_params(restore_to_defaults)

    def reset_param(self, param: str, to_default: bool = False) -> None:
        """
        Reset a single parameter to its default value. If `to_default` is True,
        resets back to the built in default value. If it is false, it resets to
        whatever the user has set as the default value when initializing the table

        Parameters
        ----------
        param : str
            The parameter to reset
        to_default : bool, optional
            If True, resets to the built in default value. If False, resets to the
            user specified default value, by default False

        Returns
        -------
        None
        """
        self.table_params[0].pop(param)
        # if to default, remove parameter from user provided defaults
        if to_default:
            self.table_params[1].pop(param)

    def reset_custom_features(self):
        super().reset_custom_features()
        diff_word = "Differences" if len(self.var_list) > 1 else "Difference"
        self.add_multicolumns(
            ["Means", "", diff_word], [self.ngroups, 1, self.ndiffs]
        )  # may need to move this later if we make including the total mean optional

    @staticmethod
    def _render(render_func):
        def wrapper(self, **kwargs):
            if self.table_params["show_n"]:
                self.add_line(
                    [
                        f"N={self.grp_sizes[c]:,}" if c in self.grp_sizes.index else ""
                        for c in self.means.columns
                    ],
                    location="after-columns",
                )
            if self.table_params["show_significance_levels"]:
                _p = "p<"
                if render_func.__name__ == "render_latex":
                    _p = "p$<$"
                stars = ", ".join(
                    [
                        f"{'*' * i} {_p} {p}"
                        for i, p in enumerate(
                            sorted(self.table_params["p_values"], reverse=True), start=1
                        )
                    ]
                )
                note = f"{stars}"
                self.add_note(note, alignment="l", escape=False)
            output = render_func(self, **kwargs)
            # remove all the supurflous lines that may not be needed in future renders
            if self.table_params["show_n"]:
                self.remove_line(location="after-columns", index=-1)
            if self.table_params["show_significance_levels"]:
                self.remove_note(index=-1)
                print("Note: Standard errors assume samples are drawn independently.")
            return output

        return wrapper

    @_render
    def render_latex(self, outfile=None, only_tabular=False) -> str | None:
        return super().render_latex(outfile, only_tabular)

    @_render
    def render_html(self, outfile=None, convert_latex=True) -> str | None:
        return super().render_html(outfile=outfile, convert_latex=convert_latex)

    @_render
    def render_ascii(self, convert_latex=True) -> str:
        return super().render_ascii(convert_latex=convert_latex)

    def _get_diffs(self):
        # TODO: allow for standard errors caluclated under dependent samples
        def sig_test(grp0, grp1, col):
            se_list = []
            for var in self.var_list:
                _stat, pval = stats.ttest_ind(
                    grp0[var], grp1[var], equal_var=False, alternative=self.alternative
                )
                self.t_stats[f"{col}_{var}"] = _stat
                self.pvalues[f"{col}_{var}"] = pval
                s1 = grp0[var].std() ** 2
                s2 = grp1[var].std() ** 2
                n1 = grp0.shape[0]
                n2 = grp1.shape[0]
                se_list.append(np.sqrt(s1 / n1 + s2 / n2))

            return pd.Series(se_list, index=self.var_list)

        if self.diff_pairs is None:
            self.means["Difference"] = (
                self.means[self.groups[0]] - self.means[self.groups[1]]
            )
            grp0 = self.type_gdf.get_group(self.groups[0])
            grp1 = self.type_gdf.get_group(self.groups[1])
            ses = sig_test(grp0, grp1, "Difference")
            ses.name = "Difference"
            self.sem = self.sem.merge(ses, left_index=True, right_index=True)
        else:
            for pair in self.diff_pairs:
                _col = f"{pair[0]} - {pair[1]}"
                self.means[_col] = self.means[pair[0]] - self.means[pair[1]]
                ses = sig_test(
                    self.type_gdf.get_group(pair[0]),
                    self.type_gdf.get_group(pair[1]),
                    _col,
                )
                ses.name = _col
                self.sem = self.sem.merge(ses, left_index=True, right_index=True)

    def _create_rows(self):
        rows = []
        for _index, row in self.means.iterrows():
            sem_row = [self._format_value(f"{_index}_label", "_index", "")]
            _row = [
                self._format_value(
                    f"{_index}_label", "_index", self._index_labels.get(_index, _index)
                )
            ]
            for col, value in zip(row.index, row.values):
                # pull standard error and p-value
                try:
                    se = self.sem.loc[_index, col]
                except KeyError:
                    se = None
                try:
                    pval = self.pvalues[f"{col}_{_index}"]
                except KeyError:
                    pval = None
                formatted_val = self._format_value(
                    _index, col, value, p_value=pval, se=se
                )
                if self.table_params["show_standard_errors"]:
                    try:
                        se = self.sem.loc[_index, col]
                        formatted_se = copy.copy(formatted_val)
                        # formatted_se = self._format_value(_index, col, se)
                        formatted_se["value"] = (
                            f"({se:,.{self.table_params['sig_digits']}f})"
                        )
                        sem_row.append(formatted_se)
                    except KeyError:
                        sem_row.append(self._format_value(_index, col, ""))
                if self.table_params["show_stars"]:
                    try:
                        stars = pstars(pval, self.table_params["p_values"])
                    except TypeError:
                        stars = ""
                    formatted_val["value"] = f"{formatted_val['value']}{stars}"
                _row.append(formatted_val)
            rows.append(_row)
            if self.table_params["show_standard_errors"]:
                rows.append(sem_row)
        return rows


class SummaryTable(GenericTable):
    def __init__(self, df: pd.DataFrame, var_list: list[str] | None = None, **kwargs):
        if var_list is None:
            var_list = df.columns
        summary_df = df[var_list].describe()
        super().__init__(summary_df, **kwargs)
        # self.reset_custom_features()

    def reset_custom_features(self):
        super().reset_custom_features()
        self.rename_index(
            {
                "count": "Observations",
                "mean": "Mean",
                "std": "Std. Dev.",
                "min": "Min.",
                "max": "Max.",
            }
        )
        self.custom_formatters({"count": lambda x: f"{int(x):,}"})


class ModelTable(Table):
    # stats that get included in the table footer
    # configuration  is (name of the attribute, label, whether it has a p-value)
    model_stats = [
        ("observations", "Observations", False),
        ("ngroups", "N. Groups", False),
        ("r2", {"latex": "$R^2$", "html": "R<sup>2</sup>", "ascii": "R^2"}, False),
        (
            "adjusted_r2",
            {
                "latex": "Adjusted $R^2$",
                "html": "Adjusted R<sup>2</sup>",
                "ascii": "Adjusted R^2",
            },
            False,
        ),
        (
            "pseudo_r2",
            {
                "latex": "Pseudo $R^2$",
                "html": "Pseudo R<sup>2</sup>",
                "ascii": "Pseudo R^2",
            },
            False,
        ),
        ("fstat", "F Statistic", True),
        ("dof", "DoF", False),
        ("model_type", "Model", False),
    ]

    def __init__(
        self,
        models: list,
        *,
        caption_location: str | None = None,
        sig_digits: int = 3,
        thousands_sep: str = ",",
        show_columns: bool = True,
        show_r2: bool | None = None,
        show_adjusted_r2: bool | None = None,
        show_pseudo_r2: bool | None = None,
        show_dof: bool | None = None,
        show_ses: bool | None = None,
        show_cis: bool | None = None,
        show_fstat: bool | None = None,
        single_row: bool | None = None,
        show_observations: bool | None = None,
        show_ngroups: bool | None = None,
        show_model_numbers: bool | None = None,
        p_values: list | None = None,
        show_stars: bool | None = None,
        show_model_type: bool | None = None,
        show_significance_levels: bool | None = None,
        column_labels: dict | None = None,
        index_labels: dict | None = None,
        covariate_labels: dict | None = None,
        covariate_order: list | None = None,
        notes: list[tuple] | None = None,
        label: str | None = None,
        caption: str | None = None,
        index_name: str = "",
        formatters: dict | None = None,
        default_formatter: Callable | None = None,
        dependent_variable_name: str | None = None,
        longtable: bool = False,
        **kwargs,
    ):
        """
        Initialize an instance of the ModelsTable class.

        Parameters
        ----------
        models : list
            List of the models to include in the table. Each item in the list should
            be a fitted model of one of the supported types (see `st.SupportedModels`).
            If a type is not natively supported, it can be added to the `st.SupportedModels`
            dictionary to still work with this table.

        Raises
        ------
        KeyError
            Raised if a model is not supported. To use custom models, add them to the
            `st.SupportedModels` dictionary.
        """
        user_params = {
            k: v
            for k, v in {
                "caption_location": caption_location,
                "sig_digits": sig_digits,
                "thousands_sep": thousands_sep,
                "show_columns": show_columns,
                "show_r2": show_r2,
                "show_adjusted_r2": show_adjusted_r2,
                "show_pseudo_r2": show_pseudo_r2,
                "show_dof": show_dof,
                "show_ses": show_ses,
                "show_cis": show_cis,
                "show_fstat": show_fstat,
                "single_row": single_row,
                "show_observations": show_observations,
                "show_ngroups": show_ngroups,
                "show_model_numbers": show_model_numbers,
                "p_values": p_values,
                "show_stars": show_stars,
                "show_model_type": show_model_type,
                "show_significance_levels": show_significance_levels,
            }.items()
            if v is not None
        } | kwargs
        self.models = []
        self.params = set()
        self.ncolumns = len(models)
        dep_vars = []
        # pull the parameters from each model
        for mod in models:
            try:
                mod_obj = st.SupportedModels[type(mod)](mod)
                self.models.append(mod_obj)
            except KeyError as e:
                msg = (
                    f"{type(mod)} is unsupported. To use custom models, "
                    "add them to the `st.SupportedModels` dictionary."
                )
                raise KeyError(msg) from e
            self.params.update(mod_obj.param_labels)
            dep_vars.append(mod_obj.dependent_variable)

        self.all_param_labels = sorted(self.params)
        self.table_params = ModelTableParams(user_params)
        self.reset_custom_features()
        self.rename_columns(column_labels)
        self.rename_covariates(index_labels)
        self.rename_covariates(covariate_labels)
        self.covariate_order(covariate_order)
        self.add_notes(notes)
        self.label = label
        self.caption = caption
        self.index_name = index_name
        self.longtable = longtable
        self.panel_label = None
        self.panel_label_alignment = "l"
        self.default_formatter = self._default_formatter
        if default_formatter is not None:
            self.default_formatter = default_formatter
        self.custom_formatters(formatters)
        # check whether all dep_vars are the same. If they are, display the variable
        # name by default.
        if all(var == dep_vars[0] for var in dep_vars):
            self.dependent_variable_name = dep_vars[0]
            if dependent_variable_name is not None:
                self.dependent_variable_name = dependent_variable_name

    def reset_custom_features(self):
        super().reset_custom_features()
        self.dependent_variable = ""
        self._model_nums = [f"({i})" for i in range(1, len(self.models) + 1)]
        self.columns = self._model_nums
        self.param_labels = self.all_param_labels
        self.custom_formatters(
            {
                "r2_index": self._stats_index_formatter,
                "pseudo_r2_index": self._stats_index_formatter,
            }
        )

    def _stats_index_formatter(self, stat_name: str) -> dict:
        return {"value": stat_name, "escape": False}

    def rename_covariates(self, names: dict | None) -> None:
        """
        Dictionary renaming the covariate labels in the table. The format should be:
        {parameter_name: desired_label}. If a covariate is not in the dictionary,
        the parameter name will be used.

        Parameters
        ----------
        names : dict
            Dictionary containing the new names for the covariates
        """
        if names is None:
            return None
        self._index_labels = names

    def covariate_order(self, order: list | None) -> None:
        """
        Set order of covariates in the table. Wraps the `parameter_order` method
        """
        self.parameter_order(order)

    def parameter_order(self, order: list | None) -> None:
        """
        Set the order of the parameters in the table. An error will be raised if
        the parameter is not in any of the models.

        Parameters
        ----------
        order : list
            List of the parameters in the order you want them to appear in the table.
        """
        if order is None:
            return None
        assert isinstance(order, list), "`order` must be a list"
        missing = ""
        for p in order:
            if p not in self.all_param_labels:
                missing += f"{p}\n"
        if missing:
            raise ValueError(
                f"The following parameters are not in the models:\n{missing}"
            )
        self.param_labels = order

    def _create_rows(self):
        rows = []
        sig_digits = self.table_params["sig_digits"]
        for param in self.param_labels:
            row = [
                self._format_value(
                    f"{param}_label", "index", self._index_labels.get(param, param)
                )
            ]
            se_row = [self._format_value(f"{param}_label", "se", "")]
            ci_row = [self._format_value(f"{param}_label", "ci", "")]
            for i, mod in enumerate(self.models):
                if param not in mod.param_labels:
                    row.append(self._format_value(param, i, ""))
                    se_row.append(self._format_value(param, i, ""))
                    ci_row.append(self._format_value(param, i, ""))
                    continue
                param_val = mod.params[param]
                pvalue = mod.pvalues[param]
                row_val = self._format_value(
                    param,
                    i,
                    param_val,
                    p_value=pvalue,
                    se=mod.sterrs[param],
                    ci=(mod.cis_low[param], mod.cis_high[param]),
                )
                se = f"({mod.sterrs[param]:.{sig_digits}f})"
                # make formatting for the standard error the same as the parameter
                se_dict = copy.copy(row_val)
                se_dict["value"] = se
                se_row.append(se_dict)
                ci_low = f"{mod.cis_low[param]:.{sig_digits}f}"
                ci_high = f"{mod.cis_high[param]:.{sig_digits}f}"
                ci = f"({ci_low}, {ci_high})"
                ci_dict = copy.copy(row_val)
                ci_dict["value"] = ci
                ci_row.append(ci_dict)
                stars = pstars(pvalue, self.table_params["p_values"])
                # update value to include significance stars and SE and CI if needed
                row_val["value"] += (
                    stars * self.table_params["show_stars"]
                    + f" {se}"
                    * self.table_params["single_row"]
                    * self.table_params["show_ses"]
                    + f" {ci}"
                    * self.table_params["single_row"]
                    * self.table_params["show_cis"]
                )

                row.append(row_val)
            rows.append(row)
            if self.table_params["show_ses"] and not self.table_params["single_row"]:
                rows.append(se_row)
            if self.table_params["show_cis"] and not self.table_params["single_row"]:
                rows.append(ci_row)
        return rows

    def _create_stats_rows(self, renderer: str) -> list:
        """
        Internal method to create rows for model statistics.

        Parameters
        ----------
        renderer : str
            The type of renderer being used. Should be 'latex', 'html', or 'ascii'

        Returns
        -------
        list
            List containing each row of statistics
        """
        rows = []
        for stat, name, pvalue in self.model_stats:
            _name = name
            if isinstance(name, dict):
                _name = name[renderer]
            if not getattr(self.table_params, f"show_{stat}"):
                continue
            row = [self._format_value(f"{stat}_index", None, _name)]
            for i, mod in enumerate(self.models):
                # try to get all of the model stats. will throw an error if the
                # model doesn't have that attribute
                try:
                    val = mod.get_formatted_value(stat, self.table_params["sig_digits"])
                    if pvalue and self.table_params["show_stars"]:
                        stars = pstars(
                            getattr(mod, f"{stat}_pvalue"),
                            self.table_params["p_values"],
                        )
                        val = f"{val}{stars}"
                except AttributeError:
                    val = ""
                row.append(self._format_value(stat, i, val))
            # only add the stat if at least one model has it
            if not all(r["value"] == "" for r in row[1:]):
                rows.append(row)
        return rows

    @staticmethod
    def _render(render_func: Callable):
        """
        Wrapper for the render function to add a p-value note formatted to fit
        the type of renderer being used.

        Parameters
        ----------
        render_func : Callable
            The rendering function being wrapped
        """

        def wrapper(self, **kwargs):
            if self.table_params["show_significance_levels"]:
                _p = "p<"
                if render_func.__name__ == "render_latex":
                    _p = "p$<$"
                stars = ", ".join(
                    [
                        f"{'*' * i}{_p}{p}"
                        for i, p in enumerate(
                            sorted(self.table_params["p_values"], reverse=True), start=1
                        )
                    ]
                )
                stars_note = f"{stars}"
                self.add_note(stars_note, alignment="l", escape=False, position=0)
                _stars_note = (stars_note, "l", False)
            output = render_func(self, **kwargs)
            if self.table_params["show_significance_levels"]:
                self.remove_note(note=_stars_note)

            return output

        return wrapper

    @_render
    def render_latex(self, outfile=None, only_tabular=False) -> Union[str, None]:
        return super().render_latex(outfile, only_tabular)

    @_render
    def render_html(self, outfile=None, convert_latex: bool = True) -> Union[str, None]:
        return super().render_html(outfile=outfile, convert_latex=convert_latex)

    @_render
    def render_ascii(self, convert_latex=True) -> str:
        return super().render_ascii(convert_latex=convert_latex)

    ##### Properties #####
    @property
    def dependent_variable_name(self) -> str:
        return self._dependent_variable_name

    @dependent_variable_name.setter
    def dependent_variable_name(self, name: str) -> None:
        # remove current dependent variable from multicolumns to update later
        if len(self._multicolumns) > 0:
            try:
                col = (
                    [f"Dependent Variable: {self.dependent_variable_name}"],
                    [self.ncolumns],
                    True,
                )
                self.remove_multicolumn(col)
            except ValueError:
                pass
        self._dependent_variable_name = name
        if name != "":
            self.add_multicolumns(
                [f"Dependent Variable: {name}"], [self.ncolumns], position=0
            )


class PanelTable:
    """
    Merge multiple tables together. Not implemented yet
    """

    VALID_ALIGNMENTS = ["l", "r", "c", "left", "right", "center"]
    ALIGNMENTS = {
        "l": "l",
        "c": "c",
        "r": "r",
        "left": "l",
        "center": "c",
        "right": "r",
    }
    ASCII_ALIGNMENTS = {
        "l": "<",
        "c": "^",
        "r": ">",
        "left": "<",
        "center": "^",
        "right": ">",
    }

    def __init__(
        self,
        panels: list[Table],
        panel_labels: list[str],
        enumerate_type: str | None = "alpha_upper",
        panel_label_alignment: str = "l",
    ):
        for table in panels:
            assert isinstance(table, Table)
        self.npanels = len(panels)
        nlabels = len(panel_labels)
        if len(panels) > len(panel_labels):
            msg = f"There are {self.npanels} but only {nlabels} labels. Each panel must have a lable"
            raise AssertionError(msg)
        elif self.npanels < nlabels:
            msg = f"There are {nlabels} labels but only {self.npanels} panels. Each label must be associated with a panel"
            raise AssertionError(msg)
        valid_enum_types = ["alpha_upper", "alpha_lower", "int", "roman", None]
        assert (
            enumerate_type in valid_enum_types
        ), f"{enumerate_type} is invalid. Must be in {valid_enum_types}"
        self.panels = panels
        self.panel_labels = panel_labels
        self.enumerate_type = enumerate_type
        assert panel_label_alignment in self.VALID_ALIGNMENTS
        self.panel_label_alignment = panel_label_alignment

    def render_latex(self, outfile) -> str | None:
        # assign multicolumns to each table
        match self.enumerate_type:
            case "alpha_upper":
                self.label_char = "A"
            case "alpha_lower":
                self.label_char = "a"
            case "int":
                self.label_char = "1"
            case "roman":
                self.label_char = "i"
            case _:
                self.label_char = ""
        tex_str = ""
        for i, (table, label) in enumerate(zip(self.panels, self.panel_labels)):
            # if it is not the first table, turn off double top rule
            if i != 0:
                table.table_params["double_top_rule"] = False
            # add multicolumn to the table
            label_str = f"Panel {self.label_char}: {label}"
            table.panel_label = label_str
            table.panel_label_alignment = self.ALIGNMENTS[self.panel_label_alignment]
            _tex_str = table.render_latex(only_tabular=True)
            if i < self.npanels - 1:
                # add space between previous panel and label for next one
                # except for the very last panel
                _tex_str = _tex_str.replace(
                    "  \\bottomrule\n\\end{tabularx}\n",
                    "  \\bottomrule\\\\\n\\end{tabularx}\n",
                )
            tex_str += "\n" + _tex_str
            # _tex_str = table.render_latex(only_tabular=True)
            # if self.enumerate_type is not None:
            #     _tex_str = self._modify_latex(table=table, label=lable_str)
            # tex_str += _tex_str
            self._increment_label_char()

        if not outfile:
            return tex_str
        preamble = latex_preamble()
        tex_str = preamble + tex_str
        Path(outfile).write_text(tex_str)
        return None

    def render_ascii(self) -> str:
        # assign multicolumns to each table
        match self.enumerate_type:
            case "alpha_upper":
                self.label_char = "A"
            case "alpha_lower":
                self.label_char = "a"
            case "int":
                self.label_char = "1"
            case "roman":
                self.label_char = "i"
            case _:
                self.label_char = ""
        # get all the table widths to know how large to make panels
        renderers = []
        max_width = 0
        for table in self.panels:
            renderer = ASCIIRenderer(table)
            renderer._get_table_widths()
            table_size = renderer._len + (2 * renderer._border_len)
            max_width = max(max_width, table_size)

        # loop through the tables and actually make them. add all together for panels
        out_str = ""
        for i, (table, label) in enumerate(zip(self.panels, self.panel_labels)):
            # if it is not the first table, turn off double top rule
            if i != 0:
                table.double_top_rule = False
            # add multicolumn to the table
            _label = f"Panel {self.label_char}) {label}"
            label_align = self.ASCII_ALIGNMENTS[self.panel_label_alignment]
            label_str = f"{_label:{label_align}{max_width}}\n"
            table_str = table.render_ascii()
            out_str += label_str + table_str + "\n"
            self._increment_label_char()

        return out_str

    def _modify_latex(self, table: Table, label: str):
        tex_str = table.render_latex(only_tabular=True)
        out_str = tex_str.replace("\\begin{tabular}\n", "")
        new_start = "\\begin{tabular}\n"
        ncols = len(table.columns) + int(table.table_params["include_index"])
        label_alignment = self.ALIGNMENTS[self.panel_label_alignment]
        new_start += (
            "  \\multicolumn{"
            + f"{ncols}"
            + "}"
            + f"{{{label_alignment}}}"
            + f"{{{label}}}"
            + r"\\"
            + "\n"
        )
        return new_start + out_str

    def _increment_label_char(self):
        """
        Increment the label on each panel
        """
        if self.enumerate_type is None:
            pass
        # roman numerals not implemented yet
        elif self.enumerate_type == "roman":
            pass
        else:
            self.label_char = chr(ord(self.label_char) + 1)

    def __str__(self) -> str:
        return self.render_ascii()

    def __repr__(self) -> str:
        return self.render_ascii()
