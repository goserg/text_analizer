from typing import Dict, List, Union

from bokeh.plotting import figure, output_file, show, ColumnDataSource

TOOLS = "pan,wheel_zoom,reset,hover,save"


class BokehPlot:
    def __init__(self, file_name: str) -> None:
        output_file(file_name, mode="inline")
        self.p = figure(title="Распределение слов по длине",
                        x_axis_label='длина слова (букв)',
                        y_axis_label='количество слов (%)',
                        tools=TOOLS,
                        tooltips=[("Текст", "@book"), ("Длина слова", "@x"), ("Частота", "@y%")],
                        )
        self.p.toolbar.autohide = True

    def add_plot(self,
                 name: str,
                 data: Dict[str, Union[range, List[Union[float, int]]]],
                 color: str,
                 ) -> None:
        source = ColumnDataSource(data=data)
        self.p.square("x", "y", legend_label=name, line_width=1, fill_color=None, color=color, source=source)
        self.p.line("x", "y", legend_label=name, line_width=1, color=color, source=source)

    def show(self) -> None:
        show(self.p)
