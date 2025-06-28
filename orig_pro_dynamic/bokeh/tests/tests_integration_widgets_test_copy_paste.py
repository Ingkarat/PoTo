import pytest
pytest
from time import sleep
from bokeh._testing.util.selenium import copy_table_rows, enter_text_in_cell_with_click_enter, get_page_element, paste_values
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, DataTable, Div, TableColumn
pytest_plugins = ('bokeh._testing.plugins.project',)

def Test_CopyPaste_test_copy_paste_to_textarea(self, bokeh_model_page) -> None:
    source = ColumnDataSource(dict(x=[1, 2], y=[1, 1]))
    columns = [TableColumn(field='x', title='x'), TableColumn(field='y', title='y')]
    table = DataTable(source=source, columns=columns, editable=False, width=600)
    text_area = Div(text='<textarea id="T1"></textarea>')
    page = bokeh_model_page(column(table, text_area))
    copy_table_rows(page.driver, [2, 1])
    sleep(0.1)
    element = get_page_element(page.driver, '#T1')
    enter_text_in_cell_with_click_enter(page.driver, element, 'PASTED:')
    paste_values(page.driver, element)
    result = element.get_attribute('value')
    assert result == '\nPASTED:\n0\t1\t1\n1\t2\t1\n'
    assert page.has_no_console_errors()