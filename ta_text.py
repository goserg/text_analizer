from __future__ import annotations
from datetime import date
from typing import List, Dict

from author import Author
from text_parser import ParsedText


def count_letters(words: List[Dict[str, str]]) -> Dict[str: int]:
    letters = {}
    for word in words:
        try:
            letters[len(word["word"])] += 1
        except KeyError:
            letters[len(word["word"])] = 1
    return letters


with open("most_common.txt") as f:
    most_common_words = f.read().split("\n")


def count_common(words: List[Dict[str, str]]) -> Dict[str: float]:
    fingerprint = {}
    for i in words:
        if i["word"] in most_common_words:
            try:
                fingerprint[i["word"]] += 1
            except KeyError:
                fingerprint[i["word"]] = 1
    for key, value in fingerprint.items():
        fingerprint[key] = value / len(words)
    return fingerprint


class TaText:
    __slots__ = ("__text", "author", "title", "published", "hash", "parsed_text", "letters_in_words", "fingerprint")

    def __init__(self,
                 text: str,
                 author: Author = Author("Пушкин", "Александр", "Сергеевич"),
                 title: str = "Unknown title",
                 published: date = date(1, 1, 1),
                 file_name: str = None,
                 ) -> None:
        self.author = author
        self.title = title
        self.published = published
        self.__text = text
        self.hash = hash(self.__text)
        self.parsed_text = ParsedText(file_name)
        self.letters_in_words = count_letters(self.parsed_text.tokens)
        self.fingerprint = count_common(self.parsed_text.tokens)

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, value: str) -> None:
        raise AttributeError("Can not directly modify text")

    @classmethod
    def from_file(cls, file_name: str) -> TaText:
        with open(file_name) as file:
            text = file.read()
            return TaText(text, file_name=file_name)

    def __str__(self) -> str:
        return f"{self.author}: {self.title}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.__str__()})"

    def __eq__(self, other: TaText) -> bool:
        return self.hash == other.hash
