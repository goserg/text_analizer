import random
from datetime import date
from typing import List

from bokeh.palettes import Dark2_5 as Palette

from ta_text import TaText
from bok import BokehPlot


class TextManager:
    def __init__(self) -> None:
        self.album = {}

    def add_book(self,
                 file_name: str,
                 author: str,
                 title: str,
                 published: date = date(1, 1, 1),
                 ) -> None:
        if title in self.album.keys():
            raise KeyError(f"a book with title {title} exists in album")
        new_book = TaText.from_file(file_name)
        new_book.author = author
        new_book.published = published
        new_book.title = title
        self.album[title] = new_book

    def generate_name_distribution_plot(self, colors: List[str] = None) -> None:
        if colors:
            colors = iter(colors)
        p = BokehPlot("output/name_distribution.html")
        x = range(1, 21)
        for title, book in self.album.items():
            y = []
            t = [title]*len(x)
            for i in x:
                try:
                    y.append(book.letters_in_words[i] * 100 / sum(book.letters_in_words.values()))
                except KeyError:
                    y.append(0)
            data = {"x": x, "y": y, "book": t}
            if colors:
                try:
                    p.add_plot(title, data, next(colors))
                except StopIteration:
                    p.add_plot(title, data, random.choice(Palette))
            else:
                p.add_plot(title, data, random.choice(Palette))
        p.show()
