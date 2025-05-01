"""
inner/outer elliptic/square reliefs for any kivy widget
=======================================================

the :class:`ReliefCanvas` mixin class of this ae namespace portion can be added to any square or elliptic Kivy widget
to draw an inner and/or outer relief, in order to convert your widget to have an outstanding or sunken 3D-appearance.
"""
from typing import Any, Callable, Tuple, Union

from kivy.app import App                                                                    # type: ignore
from kivy.graphics import Color, Line                                                       # type: ignore
from kivy.factory import Factory                                                            # type: ignore
# pylint: disable=no-name-in-module
from kivy.graphics.instructions import InstructionGroup                                     # type: ignore # noqa: E0611
from kivy.properties import ListProperty, NumericProperty, ObjectProperty                   # type: ignore # noqa: E0611

from ae.gui.utils import ColorRGB, ColorOrInk                                               # type: ignore


__version__ = '0.3.13'


ANGLE_BEG = 87                                          #: beginning angle for ellipse drawings
ANGLE_END = 267                                         #: ending angle for ellipse drawings
DEF_INK = (0, 0, 0)                                     #: default value of :paramref:`relief_colors.color_or_ink`

ReliefColors = Union[Tuple[ColorRGB, ColorRGB], Tuple]  #: tuple of (top, bottom) relief colors or empty tuple
ReliefBrightness = Tuple[float, float]                  #: top and bottom brightness/darken factor


def relief_colors(color_or_ink: ColorOrInk = DEF_INK, darken_factors: ReliefBrightness = (0.6, 0.3)) -> ReliefColors:
    """ calculate the (top and bottom) colors used for the relief lines/drawings.

    :param color_or_ink:        optional color used to calculate the relief colors from, which will first be lightened
                                until one of the color parts (R, G or B) reaches the value 1.0; then
                                :paramref:`~relief_colors.darken factors` will be applied to the color parts. If not
                                passed or passed the value of :data:`DEF_INK`, then the framework
                                :attr:`~ae.kivy.apps.FrameworkApp.font_color` will be used.

                                .. note::
                                    if the alpha value of the argument :paramref:`~relief_colors.color_or_ink` is zero,
                                    then no relief colors will be calculated and an empty tuple will be returned
                                    (which is disabling the relief effect).

    :param darken_factors:      two factors to darken (1) the top and (2) the bottom relief color parts.

    :return:                    tuple with darkened colors calculated from :paramref:`~relief_colors.color_or_ink` and
                                :paramref:`~relief_colors.darken_factors` or an empty tuple if the alpha value of
                                :paramref:`~relief_colors.color_or_ink` has a zero value.
    """
    if color_or_ink == DEF_INK:
        fw_app = App.get_running_app()      # results in None in unit tests
        color_or_ink = fw_app and fw_app.font_color or DEF_INK
    elif len(color_or_ink) > 3 and not color_or_ink[3]:
        return ()

    max_col_part = max(color_or_ink[:3])
    if max_col_part == 0:                   # prevent zero division if color_or_ink is black/default
        lightened_color = [1.0, 1.0, 1.0]
    else:
        brighten_factor = 1 / max_col_part
        lightened_color = [(col * brighten_factor) for col in color_or_ink[:3]]

    return tuple([col_part * darken for col_part in lightened_color] for darken in darken_factors)


class ReliefCanvas:                                                                             # pragma: no cover
    """ relief canvas mixin class.

    to activate the drawing of a relief, you have to specify two colors, one for the top part and another one
    for the bottom part of the relief, which are both stored in a single kivy property. the function
    :func:`relief_colors` can be used to calculate lightened and darkened values of the surface color of the widget::

        MySquareRaisedWidgetWithColoredSurface:
            surface_color: 0.9, 0.6, 0.3, 1.0
            relief_square_outer_colors: relief_colors(color_or_ink=self.surface_color)

    this will result in a raised widget with a square outer relief where the top/left relief color gets a lightened
    value and the bottom/right relief a darkened value of the color specified by `surface_color`.

    using the default values will result in raised widgets with the inner part sunken, simulating the light source in
    the top left window border/corner. to make a sunken widget for the same light source position, you simply have
    to flip the items of the :paramref:`~relief_colors.darken_factors` argument of the :func:`relief_colors` function.

    the following example shows this for a round/elliptic button widget::

        MyRoundSunkenButton:
            relief_ellipse_outer_colors: relief_colors(darken_factors=(0.3, 0.6))

    the other color attributes of this mixin class control the relief colors for the inner part of a square-shaped
    widget (:attr:`.relief_square_inner_colors`) and for the inner part of an elliptic shape widget
    (:attr:`.relief_ellipse_inner_colors`).

    the depth of the outer raise/sunk effect can be controlled with the :attr:`.relief_square_outer_lines`
    property/attribute. :attr:`.relief_square_inner_lines` controls the raise/sunk depth of the inner surface of a
    square widget. :attr:`.relief_ellipse_inner_lines` and :attr:`.relief_ellipse_outer_lines` are doing the same for
    widgets with a round/elliptic shape.

    the properties :attr:`.relief_square_inner_offset` and :attr:`.relief_ellipse_inner_offset` are specifying the width
    of the widget border (the part between the outer and the inner relief) in pixels.

    .. note::
        at least one of the classes that is mixing in this class has to inherit from Widget (or EventDispatcher) to get
        the widgets `pos`, `size`, `canvas` properties and the `bind` method.
    """

    relief_pos_size = ListProperty([])
    """ list/tuple of optional relief position and size (x, y, width, height) in pixels.

    if not specified or empty list/tuple, than the pos/size values of the mixing-in widget will be used instead.

    :attr:`relief_pos_size` is a :class:`~kivy.properties.ListProperty` and defaults to an empty list.
    """

    relief_ellipse_inner_colors: ReliefColors = ObjectProperty(())
    """ list/tuple of ellipse inner (top, bottom) rgb colors.

    :attr:`relief_ellipse_inner_colors` is a :class:`~kivy.properties.ObjectProperty` and defaults to an empty tuple.
    """

    relief_ellipse_inner_lines = NumericProperty('3sp')
    """ number of ellipse inner lines/pixels to be drawn.

    :attr:`relief_ellipse_inner_lines` is a :class:`~kivy.properties.NumericProperty` and defaults to '3sp'.
    """

    relief_ellipse_inner_offset = NumericProperty('1sp')
    """ number of pixels left unchanged at the border of the inner elliptic surface before the inner relief starts.

    :attr:`relief_ellipse_inner_offset` is a :class:`~kivy.properties.NumericProperty` and defaults to '1sp'.
    """

    relief_ellipse_outer_colors: ReliefColors = ObjectProperty(())
    """ list/tuple of ellipse outer (top, bottom) rgb colors.

    :attr:`relief_ellipse_outer_colors` is a :class:`~kivy.properties.ObjectProperty` and defaults to an empty tuple.
    """

    relief_ellipse_outer_lines = NumericProperty('3sp')
    """ number of ellipse outer lines/pixels to be drawn.

    :attr:`relief_ellipse_outer_lines` is a :class:`~kivy.properties.NumericProperty` and defaults to '3sp'.
    """

    relief_square_inner_colors = ObjectProperty(())
    """ list/tuple of square inner (top, bottom) rgb colors.

    :attr:`relief_square_inner_colors` is a :class:`~kivy.properties.ObjectProperty` and defaults to an empty tuple.
    """

    relief_square_inner_lines = NumericProperty('3sp')
    """ number of square inner lines/pixels to be drawn.

    :attr:`relief_square_inner_lines` is a :class:`~kivy.properties.NumericProperty` and defaults to '3sp'.
    """

    relief_square_inner_offset = NumericProperty('1sp')
    """ number of pixels left unchanged at the border of the square inner surface before the inner relief starts.

    :attr:`relief_square_inner_offset` is a :class:`~kivy.properties.NumericProperty` and defaults to '1sp'.
    """

    relief_square_outer_colors: ReliefColors = ObjectProperty(())
    """ list/tuple of square outer (top, bottom) rgb colors.

    :attr:`relief_square_outer_colors` is a :class:`~kivy.properties.ObjectProperty` and defaults to an empty tuple.
    """

    relief_square_outer_lines: NumericProperty = NumericProperty('3sp')
    """ number of square outer lines/pixels to be drawn.

    :attr:`relief_square_outer_lines` is a :class:`~kivy.properties.NumericProperty` and defaults to '3sp'.
    """

    # attributes provided by the class to be mixed into
    bind: Any
    canvas: Any
    pos: list
    size: list

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        bind_func, bound_func = self.bind, self._relief_refresh
        bind_func(pos=bound_func)
        bind_func(size=bound_func)
        bind_func(relief_pos_size=bound_func)
        bind_func(relief_ellipse_inner_colors=bound_func)
        bind_func(relief_ellipse_inner_lines=bound_func)
        bind_func(relief_ellipse_inner_offset=bound_func)
        bind_func(relief_ellipse_outer_colors=bound_func)
        bind_func(relief_ellipse_outer_lines=bound_func)
        bind_func(relief_square_inner_colors=bound_func)
        bind_func(relief_square_inner_lines=bound_func)
        bind_func(relief_square_inner_offset=bound_func)
        bind_func(relief_square_outer_colors=bound_func)
        bind_func(relief_square_outer_lines=bound_func)

        self._relief_graphic_instructions = InstructionGroup()

    def _relief_refresh(self, *_args):
        """ pos/size or color changed event handler. """
        if self._relief_graphic_instructions.length():
            self.canvas.after.remove(self._relief_graphic_instructions)
            self._relief_graphic_instructions.clear()

        add = self._relief_graphic_instructions.add
        pos_size = self.relief_pos_size or (*self.pos, *self.size)
        if self.relief_ellipse_inner_colors and self.relief_ellipse_inner_lines:
            self._relief_ellipse_inner_refresh(add, *self.relief_ellipse_inner_colors, *pos_size)
        if self.relief_ellipse_outer_colors and self.relief_ellipse_outer_lines:
            self._relief_ellipse_outer_refresh(add, *self.relief_ellipse_outer_colors, *pos_size)
        if self.relief_square_inner_colors and self.relief_square_inner_lines:
            self._relief_square_inner_refresh(add, *self.relief_square_inner_colors, *pos_size)
        if self.relief_square_outer_colors and self.relief_square_outer_lines:
            self._relief_square_outer_refresh(add, *self.relief_square_outer_colors, *pos_size)

        if self._relief_graphic_instructions.length():
            self.canvas.after.add(self._relief_graphic_instructions)

    def _relief_ellipse_inner_refresh(self, add_instruction: Callable,
                                      top_color: ColorRGB, bottom_color: ColorRGB,
                                      wid_x: float, wid_y: float, wid_width: float, wid_height: float):
        """ ellipse pos/size or color-changed event handler. """
        lines = int(self.relief_ellipse_inner_lines)
        offset = int(self.relief_ellipse_inner_offset)
        for line in range(1, lines + 1):
            alpha = 0.9 - (line / lines) * 0.8997
            line += offset
            line2 = 2 * line

            in_x1 = wid_x + line
            in_y1 = wid_y + line
            in_width = wid_width - line2
            in_height = wid_height - line2

            add_instruction(Color(*top_color, alpha))                   # inside top left
            add_instruction(Line(ellipse=[in_x1, in_y1, in_width, in_height, ANGLE_END, 360 + ANGLE_BEG]))
            add_instruction(Color(*bottom_color, alpha))                # inside bottom right
            add_instruction(Line(ellipse=[in_x1, in_y1, in_width, in_height, ANGLE_BEG, ANGLE_END]))

    def _relief_ellipse_outer_refresh(self, add_instruction: Callable,
                                      top_color: ColorRGB, bottom_color: ColorRGB,
                                      wid_x: float, wid_y: float, wid_width: float, wid_height: float):
        """ ellipse pos/size or color-changed event handler. """
        lines = int(self.relief_ellipse_outer_lines)
        for line in range(1, lines + 1):
            alpha = 0.9 - (line / lines) * 0.8997
            line2 = 2 * line

            out_x1 = wid_x - line
            out_y1 = wid_y - line
            out_width = wid_width + line2
            out_height = wid_height + line2

            add_instruction(Color(*top_color, alpha))                   # outside top left
            add_instruction(Line(ellipse=[out_x1, out_y1, out_width, out_height, ANGLE_END, 360 + ANGLE_BEG]))
            add_instruction(Color(*bottom_color, alpha))                # outside bottom right
            add_instruction(Line(ellipse=[out_x1, out_y1, out_width, out_height, ANGLE_BEG, ANGLE_END]))

    def _relief_square_inner_refresh(self, add_instruction: Callable,
                                     top_color: ColorRGB, bottom_color: ColorRGB,
                                     wid_x: float, wid_y: float, wid_width: float, wid_height: float):
        """ square pos/size or color changed event handler. """
        lines = int(self.relief_square_inner_lines)
        offset = int(self.relief_square_inner_offset)
        for line in range(1, lines + 1):
            alpha = 0.9 - (line / lines) * 0.8997
            line += offset
            line2 = 2 * line

            in_x1 = wid_x + line
            in_x2 = in_x1 + wid_width - line2
            in_y1 = wid_y + line
            in_y2 = in_y1 + wid_height - line2

            add_instruction(Color(*top_color, alpha))                   # inside top left
            add_instruction(Line(points=[in_x1, in_y1, in_x1, in_y2, in_x2, in_y2]))
            add_instruction(Color(*bottom_color, alpha))                # inside bottom right
            add_instruction(Line(points=[in_x1, in_y1, in_x2, in_y1, in_x2, in_y2]))

    def _relief_square_outer_refresh(self, add_instruction: Callable,
                                     top_color: ColorRGB, bottom_color: ColorRGB,
                                     wid_x: float, wid_y: float, wid_width: float, wid_height: float):
        """ square pos/size or color changed event handler. """
        lines = int(self.relief_square_outer_lines)
        for line in range(1, lines + 1):
            alpha = 0.9 - (line / lines) * 0.8997
            line2 = 2 * line

            out_x1 = wid_x - line
            out_x2 = out_x1 + wid_width + line2
            out_y1 = wid_y - line
            out_y2 = out_y1 + wid_height + line2

            add_instruction(Color(*top_color, alpha))                   # outside upper left
            add_instruction(Line(points=[out_x1, out_y1, out_x1, out_y2, out_x2, out_y2]))
            add_instruction(Color(*bottom_color, alpha))                # outside bottom right
            add_instruction(Line(points=[out_x1, out_y1, out_x2, out_y1, out_x2, out_y2]))


Factory.register('ReliefCanvas', cls=ReliefCanvas)
