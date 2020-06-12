import random
from typing import List

from bokeh.palettes import Dark2_5 as Palette
from bok import BokehPlot


def generate_name_distribution_plot(book_list, colors: List[str] = None) -> None:
    if colors:
        colors = iter(colors)
    p = BokehPlot("output/name_distribution.html")
    x = range(1, 21)
    for book in book_list:
        y = []
        t = [book.title]*len(x)
        for i in x:
            try:
                y.append(book.letters_in_words[i] * 100 / sum(book.letters_in_words.values()))
            except KeyError:
                y.append(0)
        data = {"x": x, "y": y, "book": t}
        if colors:
            try:
                p.add_plot(book.title, data, next(colors))
            except StopIteration:
                p.add_plot(book.title, data, random.choice(Palette))
        else:
            p.add_plot(book.title, data, random.choice(Palette))
    p.show()
