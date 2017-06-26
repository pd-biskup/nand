from asciimatics.screen import Screen
from asciimatics.widgets import Widget, Frame, ListBox, Layout, Button, TextBox
from asciimatics.scene import Scene
from scripts.chip_parser import Parser


def main(screen):
    chips = Parser.chips()
    list = ChipsListView(screen, chips)
    effects = [list]
    scene = Scene(effects, -1)
    screen.play([scene])


class ChipsListView(Frame):

    def __init__(self, screen, model):
        super(ChipsListView, self).__init__(screen, screen.height, screen.width, has_border=False)
        self._screen = screen
        self._model = model
        self._list_options = []
        for index, chip in enumerate(model):
            self._list_options.append((model[chip][0], index))
        self._list_view = ListBox(Widget.FILL_FRAME, self._list_options, on_change=self._on_list_change)
        self._button_exit = Button('Exit', self._on_button_exit)
        self._text_info = TextBox(Widget.FILL_FRAME)
        self._text_info.disabled = True
        layout = Layout([1, 3], fill_frame=True)
        self._layout = layout
        self.add_layout(layout)
        layout.add_widget(self._list_view, 0)
        layout.add_widget(self._button_exit, 0)
        layout.add_widget(self._text_info, 1)
        self.fix()

    def _on_button_exit(self):
        self._screen.close()

    def _on_list_change(self):
        self._text_info.value = [(self._model[self._list_options[self._list_view.value][0]][1])]

if __name__ == '__main__':
    Screen.wrapper(main)
