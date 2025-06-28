import pytest
pytest
from bokeh._testing.util.selenium import RECORD, enter_text_in_cell, enter_text_in_cell_with_click_enter, get_table_cell
from bokeh.models import ColumnDataSource, CustomJS, DataTable, IntEditor, NumberEditor, StringEditor, TableColumn
pytest_plugins = ('bokeh._testing.plugins.project',)

def Test_CellEditor_Base_setup_method(self):
    source = ColumnDataSource({'values': self.values})
    column = TableColumn(field='values', title='values', editor=self.editor())
    self.table = DataTable(source=source, columns=[column], editable=True, width=600)
    source.selected.js_on_change('indices', CustomJS(args=dict(s=source), code=RECORD('values', 's.data.values')))

def Test_IntEditor_test_editing_does_not_update_source_on_noneditable_table(self, bokeh_model_page) -> None:
    self.table.editable = False
    page = bokeh_model_page(self.table)
    cell = get_table_cell(page.driver, 1, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    cell = get_table_cell(page.driver, 1, 1)
    enter_text_in_cell(page.driver, cell, '33')
    cell = get_table_cell(page.driver, 2, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    assert page.has_no_console_errors()

@pytest.mark.parametrize('bad', ['1.1', 'text'])
def Test_IntEditor_test_editing_does_not_update_source_on_bad_values(self, bad, bokeh_model_page) -> None:
    bad = '1.1'
    self.table.editable = False
    page = bokeh_model_page(self.table)
    cell = get_table_cell(page.driver, 1, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    cell = get_table_cell(page.driver, 1, 1)
    enter_text_in_cell(page.driver, cell, bad)
    cell = get_table_cell(page.driver, 2, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    assert page.has_no_console_errors()

def Test_IntEditor_test_editing_updates_source(self, bokeh_model_page) -> None:
    page = bokeh_model_page(self.table)
    cell = get_table_cell(page.driver, 1, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    cell = get_table_cell(page.driver, 1, 1)
    enter_text_in_cell(page.driver, cell, '33')
    cell = get_table_cell(page.driver, 2, 1)
    cell.click()
    results = page.results
    assert results['values'] == [33, 2]
    assert page.has_no_console_errors()

def Test_NumberEditor_test_editing_does_not_update_source_on_noneditable_table(self, bokeh_model_page) -> None:
    self.table.editable = False
    page = bokeh_model_page(self.table)
    cell = get_table_cell(page.driver, 1, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    cell = get_table_cell(page.driver, 1, 1)
    enter_text_in_cell(page.driver, cell, '33.5')
    cell = get_table_cell(page.driver, 2, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    assert page.has_no_console_errors()

@pytest.mark.parametrize('bad', ['text'])
def Test_NumberEditor_test_editing_does_not_update_source_on_bad_values(self, bad, bokeh_model_page) -> None:
    bad = 'text'
    self.table.editable = False
    page = bokeh_model_page(self.table)
    cell = get_table_cell(page.driver, 1, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    cell = get_table_cell(page.driver, 1, 1)
    enter_text_in_cell(page.driver, cell, bad)
    cell = get_table_cell(page.driver, 2, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    assert page.has_no_console_errors()

def Test_NumberEditor_test_editing_updates_source(self, bokeh_model_page) -> None:
    page = bokeh_model_page(self.table)
    cell = get_table_cell(page.driver, 1, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    cell = get_table_cell(page.driver, 1, 1)
    enter_text_in_cell(page.driver, cell, '33.5')
    cell = get_table_cell(page.driver, 2, 1)
    cell.click()
    results = page.results
    assert results['values'] == [33.5, 2.2]
    assert page.has_no_console_errors()

def Test_StringEditor_test_editing_does_not_update_source_on_noneditable_table(self, bokeh_model_page) -> None:
    self.table.editable = False
    page = bokeh_model_page(self.table)
    cell = get_table_cell(page.driver, 1, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    cell = get_table_cell(page.driver, 1, 1)
    enter_text_in_cell(page.driver, cell, 'baz')
    cell = get_table_cell(page.driver, 2, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    assert page.has_no_console_errors()

@pytest.mark.parametrize('bad', ['1', '1.1', '-1'])
def Test_StringEditor_test_editing_does_not_update_source_on_bad_values(self, bad, bokeh_model_page) -> None:
    bad = '1'
    self.table.editable = False
    page = bokeh_model_page(self.table)
    cell = get_table_cell(page.driver, 1, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    cell = get_table_cell(page.driver, 1, 1)
    enter_text_in_cell(page.driver, cell, bad)
    cell = get_table_cell(page.driver, 2, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    assert page.has_no_console_errors()

def Test_StringEditor_test_editing_updates_source(self, bokeh_model_page) -> None:
    page = bokeh_model_page(self.table)
    cell = get_table_cell(page.driver, 1, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    cell = get_table_cell(page.driver, 1, 1)
    enter_text_in_cell(page.driver, cell, 'baz')
    cell = get_table_cell(page.driver, 2, 1)
    cell.click()
    results = page.results
    assert results['values'] == ['baz', 'bar']
    assert page.has_no_console_errors()

def Test_StringEditor_test_editing_updates_source_with_click_enter(self, bokeh_model_page) -> None:
    page = bokeh_model_page(self.table)
    cell = get_table_cell(page.driver, 1, 1)
    cell.click()
    results = page.results
    assert results['values'] == self.values
    cell = get_table_cell(page.driver, 1, 1)
    enter_text_in_cell_with_click_enter(page.driver, cell, 'baz')
    cell = get_table_cell(page.driver, 2, 1)
    cell.click()
    results = page.results
    assert results['values'] == ['baz', 'bar']
    assert page.has_no_console_errors()