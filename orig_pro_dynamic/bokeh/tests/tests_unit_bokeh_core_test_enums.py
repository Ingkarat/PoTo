import pytest
pytest
from bokeh._testing.util.api import verify_all
from bokeh.colors import named
from bokeh.palettes import __palettes__
import bokeh.core.enums as bce
ALL = ('Align', 'Anchor', 'AngleUnits', 'AutosizeMode', 'ButtonType', 'CalendarPosition', 'DashPattern', 'DateFormat', 'DatetimeUnits', 'Dimension', 'Dimensions', 'Direction', 'Enumeration', 'enumeration', 'FontStyle', 'HatchPattern', 'HatchPatternAbbreviation', 'HoldPolicy', 'HorizontalLocation', 'JitterRandomDistribution', 'LatLon', 'LegendClickPolicy', 'LegendLocation', 'LineCap', 'LineDash', 'LineJoin', 'Location', 'MapType', 'MarkerType', 'NamedColor', 'NumeralLanguage', 'Orientation', 'OutputBackend', 'PaddingUnits', 'Palette', 'RenderLevel', 'RenderMode', 'ResetPolicy', 'RoundingFunction', 'SelectionMode', 'SizingMode', 'SizingPolicy', 'SortDirection', 'SpatialUnits', 'StartEnd', 'StepMode', 'TextAlign', 'TextBaseline', 'TextureRepetition', 'TickLabelOrientation', 'TooltipAttachment', 'TooltipFieldFormatter', 'TrackPolicy', 'VerticalAlign', 'VerticalLocation')

def test_Enumeration_default() -> None:
    e = bce.Enumeration()
    assert e.__slots__ == ()

def test_enums_contents() -> None:
    assert [x for x in dir(bce) if x[0].isupper()] == ['Align', 'Anchor', 'AngleUnits', 'AutosizeMode', 'ButtonType', 'CalendarPosition', 'DashPattern', 'DateFormat', 'DatetimeUnits', 'Dimension', 'Dimensions', 'Direction', 'Enumeration', 'FontStyle', 'HatchPattern', 'HatchPatternAbbreviation', 'HoldPolicy', 'HorizontalLocation', 'JitterRandomDistribution', 'LatLon', 'LegendClickPolicy', 'LegendLocation', 'LineCap', 'LineDash', 'LineJoin', 'Location', 'MapType', 'MarkerType', 'NamedColor', 'NumeralLanguage', 'Orientation', 'OutputBackend', 'PaddingUnits', 'Palette', 'RenderLevel', 'RenderMode', 'ResetPolicy', 'RoundingFunction', 'SelectionMode', 'SizingMode', 'SizingPolicy', 'SortDirection', 'SpatialUnits', 'StartEnd', 'StepMode', 'TextAlign', 'TextBaseline', 'TextureRepetition', 'TickLabelOrientation', 'TooltipAttachment', 'TooltipFieldFormatter', 'TrackPolicy', 'VerticalAlign', 'VerticalLocation']
Test___all__ = verify_all(bce, ALL)

def Test_enumeration_test_basic(self) -> None:
    e = bce.enumeration('foo', 'bar', 'baz')
    assert isinstance(e, bce.Enumeration)
    assert str(e) == 'Enumeration(foo, bar, baz)'
    assert [x for x in e] == ['foo', 'bar', 'baz']
    for x in ['foo', 'bar', 'baz']:
        assert x in e
    assert 'junk' not in e

def Test_enumeration_test_case(self) -> None:
    e = bce.enumeration('foo', 'bar', 'baz', case_sensitive=False)
    assert isinstance(e, bce.Enumeration)
    assert str(e) == 'Enumeration(foo, bar, baz)'
    assert [x for x in e] == ['foo', 'bar', 'baz']
    for x in ['foo', 'FOO', 'bar', 'bAr', 'baz', 'BAZ']:
        assert x in e
    assert 'junk' not in e

def Test_enumeration_test_quote(self) -> None:
    e = bce.enumeration('foo', 'bar', 'baz', quote=True)
    assert isinstance(e, bce.Enumeration)
    assert str(e) == 'Enumeration("foo", "bar", "baz")' or str(e) == "Enumeration('foo', 'bar', 'baz')"
    assert [x for x in e] == ['foo', 'bar', 'baz']
    for x in ['foo', 'bar', 'baz']:
        assert x in e
    assert 'junk' not in e

def Test_enumeration_test_default(self) -> None:
    e = bce.enumeration('foo', 'bar', 'baz')
    assert e._default == 'foo'

def Test_enumeration_test_len(self) -> None:
    e = bce.enumeration('foo', 'bar', 'baz')
    assert len(e) == 3

def Test_bce_test_Anchor(self) -> None:
    assert tuple(bce.Anchor) == ('top_left', 'top_center', 'top_right', 'center_left', 'center', 'center_right', 'bottom_left', 'bottom_center', 'bottom_right')

def Test_bce_test_AngleUnits(self) -> None:
    assert tuple(bce.AngleUnits) == ('deg', 'rad')

def Test_bce_test_ButtonType(self) -> None:
    assert tuple(bce.ButtonType) == ('default', 'primary', 'success', 'warning', 'danger')

def Test_bce_test_CalendarPosition(self) -> None:
    assert tuple(bce.CalendarPosition) == ('auto', 'above', 'below')

def Test_bce_test_DashPattern(self) -> None:
    assert tuple(bce.DashPattern) == ('solid', 'dashed', 'dotted', 'dotdash', 'dashdot')

def Test_bce_test_DateFormat(self) -> None:
    assert tuple(bce.DateFormat) == ('ATOM', 'W3C', 'RFC-3339', 'ISO-8601', 'COOKIE', 'RFC-822', 'RFC-850', 'RFC-1036', 'RFC-1123', 'RFC-2822', 'RSS', 'TIMESTAMP')

def Test_bce_test_DatetimeUnits(self) -> None:
    assert tuple(bce.DatetimeUnits) == ('microseconds', 'milliseconds', 'seconds', 'minsec', 'minutes', 'hourmin', 'hours', 'days', 'months', 'years')

def Test_bce_test_Dimension(self) -> None:
    assert tuple(bce.Dimension) == ('width', 'height')

def Test_bce_test_Dimensions(self) -> None:
    assert tuple(bce.Dimensions) == ('width', 'height', 'both')

def Test_bce_test_Direction(self) -> None:
    assert tuple(bce.Direction) == ('clock', 'anticlock')

def Test_bce_test_FontStyle(self) -> None:
    assert tuple(bce.FontStyle) == ('normal', 'italic', 'bold', 'bold italic')

def Test_bce_test_HatchPattern(self) -> None:
    assert tuple(bce.HatchPattern) == ('blank', 'dot', 'ring', 'horizontal_line', 'vertical_line', 'cross', 'horizontal_dash', 'vertical_dash', 'spiral', 'right_diagonal_line', 'left_diagonal_line', 'diagonal_cross', 'right_diagonal_dash', 'left_diagonal_dash', 'horizontal_wave', 'vertical_wave', 'criss_cross')

def Test_bce_test_HatchPatternAbbreviation(self) -> None:
    assert tuple(bce.HatchPatternAbbreviation) == (' ', '.', 'o', '-', '|', '+', '"', ':', '@', '/', '\\', 'x', ',', '`', 'v', '>', '*')

def Test_bce_test_HoldPolicy(self) -> None:
    assert tuple(bce.HoldPolicy) == ('combine', 'collect')

def Test_bce_test_HorizontalLocation(self) -> None:
    assert tuple(bce.HorizontalLocation) == ('left', 'right')

def Test_bce_test_JitterRandomDistribution(self) -> None:
    assert tuple(bce.JitterRandomDistribution) == ('uniform', 'normal')

def Test_bce_test_LatLon(self) -> None:
    assert tuple(bce.LatLon) == ('lat', 'lon')

def Test_bce_test_LegendClickPolicy(self) -> None:
    assert tuple(bce.LegendClickPolicy) == ('none', 'hide', 'mute')

def Test_bce_test_LegendLocation(self) -> None:
    assert tuple(bce.LegendLocation) == ('top_left', 'top_center', 'top_right', 'center_left', 'center', 'center_right', 'bottom_left', 'bottom_center', 'bottom_right')

def Test_bce_test_LineCap(self) -> None:
    assert tuple(bce.LineCap) == ('butt', 'round', 'square')

def Test_bce_test_LineDash(self) -> None:
    assert tuple(bce.LineDash) == ('solid', 'dashed', 'dotted', 'dotdash', 'dashdot')

def Test_bce_test_LineJoin(self) -> None:
    assert tuple(bce.LineJoin) == ('miter', 'round', 'bevel')

def Test_bce_test_Location(self) -> None:
    assert tuple(bce.Location) == ('above', 'below', 'left', 'right')

def Test_bce_test_MapType(self) -> None:
    assert tuple(bce.MapType) == ('satellite', 'roadmap', 'terrain', 'hybrid')

def Test_bce_test_MarkerType(self) -> None:
    assert tuple(bce.MarkerType) == ('asterisk', 'circle', 'circle_cross', 'circle_dot', 'circle_x', 'circle_y', 'cross', 'dash', 'diamond', 'diamond_cross', 'diamond_dot', 'dot', 'hex', 'hex_dot', 'inverted_triangle', 'plus', 'square', 'square_cross', 'square_dot', 'square_pin', 'square_x', 'triangle', 'triangle_dot', 'triangle_pin', 'x', 'y')

def Test_bce_test_NamedColor(self) -> None:
    assert len(tuple(bce.NamedColor)) == 147
    assert tuple(bce.NamedColor) == tuple(named.__all__)

def Test_bce_test_NumeralLanguage(self) -> None:
    assert tuple(bce.NumeralLanguage) == ('be-nl', 'chs', 'cs', 'da-dk', 'de-ch', 'de', 'en', 'en-gb', 'es-ES', 'es', 'et', 'fi', 'fr-CA', 'fr-ch', 'fr', 'hu', 'it', 'ja', 'nl-nl', 'pl', 'pt-br', 'pt-pt', 'ru', 'ru-UA', 'sk', 'th', 'tr', 'uk-UA')

def Test_bce_test_Orientation(self) -> None:
    assert tuple(bce.Orientation) == ('horizontal', 'vertical')

def Test_bce_test_OutputBackend(self) -> None:
    assert tuple(bce.OutputBackend) == ('canvas', 'svg', 'webgl')

def Test_bce_test_PaddingUnits(self) -> None:
    assert tuple(bce.PaddingUnits) == ('percent', 'absolute')

def Test_bce_test_Palette(self) -> None:
    assert tuple(bce.Palette) == tuple(__palettes__)

def Test_bce_test_RenderLevel(self) -> None:
    assert tuple(bce.RenderLevel) == ('image', 'underlay', 'glyph', 'guide', 'annotation', 'overlay')

def Test_bce_test_RenderMode(self) -> None:
    assert tuple(bce.RenderMode) == ('canvas', 'css')

def Test_bce_test_ResetPolicy(self) -> None:
    assert tuple(bce.ResetPolicy) == ('standard', 'event_only')

def Test_bce_test_RoundingFunction(self) -> None:
    assert tuple(bce.RoundingFunction) == ('round', 'nearest', 'floor', 'rounddown', 'ceil', 'roundup')

def Test_bce_test_SelectionMode(self) -> None:
    assert tuple(bce.SelectionMode) == ('replace', 'append', 'intersect', 'subtract')

def Test_bce_test_SizingMode(self) -> None:
    assert tuple(bce.SizingMode) == ('stretch_width', 'stretch_height', 'stretch_both', 'scale_width', 'scale_height', 'scale_both', 'fixed')

def Test_bce_test_SortDirection(self) -> None:
    assert tuple(bce.SortDirection) == ('ascending', 'descending')

def Test_bce_test_SpatialUnits(self) -> None:
    assert tuple(bce.SpatialUnits) == ('screen', 'data')

def Test_bce_test_StartEnd(self) -> None:
    assert tuple(bce.StartEnd) == ('start', 'end')

def Test_bce_test_StepMode(self) -> None:
    assert tuple(bce.StepMode) == ('before', 'after', 'center')

def Test_bce_test_TextAlign(self) -> None:
    assert tuple(bce.TextAlign) == ('left', 'right', 'center')

def Test_bce_test_TextBaseline(self) -> None:
    assert tuple(bce.TextBaseline) == ('top', 'middle', 'bottom', 'alphabetic', 'hanging', 'ideographic')

def Test_bce_test_TextureRepetition(self) -> None:
    assert tuple(bce.TextureRepetition) == ('repeat', 'repeat_x', 'repeat_y', 'no_repeat')

def Test_bce_test_TickLabelOrientation(self) -> None:
    assert tuple(bce.TickLabelOrientation) == ('horizontal', 'vertical', 'parallel', 'normal')

def Test_bce_test_TooltipAttachment(self) -> None:
    assert tuple(bce.TooltipAttachment) == ('horizontal', 'vertical', 'left', 'right', 'above', 'below')

def Test_bce_test_TooltipFieldFormatter(self) -> None:
    assert tuple(bce.TooltipFieldFormatter) == ('numeral', 'datetime', 'printf')

def Test_bce_test_VerticalAlign(self) -> None:
    assert tuple(bce.VerticalAlign) == ('top', 'middle', 'bottom')

def Test_bce_test_VerticalLocation(self) -> None:
    assert tuple(bce.VerticalLocation) == ('above', 'below')