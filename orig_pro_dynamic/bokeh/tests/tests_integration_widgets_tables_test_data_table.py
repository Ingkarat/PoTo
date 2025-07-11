import pytest
pytest
from bokeh._testing.util.selenium import RECORD, ButtonWrapper, get_table_cell
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, DataTable, TableColumn
pytest_plugins = ('bokeh._testing.plugins.project',)

def Test_CellEditor_Base_setup_method(self):
    source = ColumnDataSource({'values': self.values})
    column = TableColumn(field='values', title='values', editor=self.editor())
    self.table = DataTable(source=source, columns=[column], editable=True, width=600)
    source.selected.js_on_change('indices', CustomJS(args=dict(s=source), code=RECORD('values', 's.data.values')))

def Test_DataTable_test_row_highlights_reflect_no_initial_selection(self, bokeh_model_page) -> None:
    source = ColumnDataSource({'values': [1, 2]})
    column = TableColumn(field='values', title='values')
    table = DataTable(source=source, columns=[column], editable=False, width=600)
    page = bokeh_model_page(table)
    row0 = get_table_cell(page.driver, 1, 1)
    assert 'selected' not in row0.get_attribute('class')
    row1 = get_table_cell(page.driver, 2, 1)
    assert 'selected' not in row1.get_attribute('class')
    assert page.has_no_console_errors()

def Test_DataTable_test_row_highlights_reflect_initial_selection(self, bokeh_model_page) -> None:
    source = ColumnDataSource({'values': [1, 2]})
    source.selected.indices = [1]
    column = TableColumn(field='values', title='values')
    table = DataTable(source=source, columns=[column], editable=False, width=600)
    page = bokeh_model_page(table)
    row0 = get_table_cell(page.driver, 1, 1)
    assert 'selected' not in row0.get_attribute('class')
    row1 = get_table_cell(page.driver, 2, 1)
    assert 'selected' in row1.get_attribute('class')
    assert page.has_no_console_errors()

def Test_DataTable_test_row_highlights_reflect_ui_selection(self, bokeh_model_page) -> None:
    source = ColumnDataSource({'values': [1, 2]})
    column = TableColumn(field='values', title='values')
    table = DataTable(source=source, columns=[column], editable=False, width=600)
    page = bokeh_model_page(table)
    row0 = get_table_cell(page.driver, 1, 1)
    assert 'selected' not in row0.get_attribute('class')
    row1 = get_table_cell(page.driver, 2, 1)
    assert 'selected' not in row1.get_attribute('class')
    cell = get_table_cell(page.driver, 2, 1)
    cell.click()
    row0 = get_table_cell(page.driver, 1, 1)
    assert 'selected' not in row0.get_attribute('class')
    row1 = get_table_cell(page.driver, 2, 1)
    assert 'selected' in row1.get_attribute('class')
    assert page.has_no_console_errors()

def Test_DataTable_test_row_highlights_reflect_js_selection(self, bokeh_model_page) -> None:
    source = ColumnDataSource({'values': [1, 2]})
    col = TableColumn(field='values', title='values')
    table = DataTable(source=source, columns=[col], editable=False, width=600)
    button = ButtonWrapper('Click', callback=CustomJS(args=dict(s=source), code='\n            s.selected.indices = [1]\n        '))
    page = bokeh_model_page(column(button.obj, table))
    row0 = get_table_cell(page.driver, 1, 1)
    assert 'selected' not in row0.get_attribute('class')
    row1 = get_table_cell(page.driver, 2, 1)
    assert 'selected' not in row1.get_attribute('class')
    button.click(page.driver)
    row0 = get_table_cell(page.driver, 1, 1)
    assert 'selected' not in row0.get_attribute('class')
    row1 = get_table_cell(page.driver, 2, 1)
    assert 'selected' in row1.get_attribute('class')
    assert page.has_no_console_errors()