from __future__ import annotations


class Author:
    __slots__ = "name", "patronymic", "surname"

    def __init__(self, surname: str, name: str, patronymic: str = None) -> None:
        self.surname: str = surname.capitalize()
        self.name: str = name.capitalize()
        try:
            self.patronymic: str = patronymic.capitalize()
        except AttributeError:
            self.patronymic: str = ""

    @classmethod
    def from_string(cls, name: str):
        try:
            surname, name, patronymic = name.split()
            return Author(surname, name, patronymic)
        except ValueError:
            surname, name = name.split()
            return Author(surname, name)

    def __str__(self):
        if self.patronymic:
            return f"{self.name[0]}.{self.patronymic[0]}. {self.surname}"
        else:
            return f"{self.name[0]}. {self.surname}"

    def __repr__(self):
        return f"{self.__class__.__name__}({self})"

    def __eq__(self, other: Author):
        if self.name == other.name and self.surname == other.surname and self.patronymic == other.patronymic:
            return True
