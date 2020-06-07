import re

import subprocess
EXCEPTIONS = "—", "«", "»", ".."


class ParsedText:
    __slots__ = "tokens"

    def __init__(self, file_name: str) -> None:
        raw_tokens = subprocess.check_output(["mystem.exe", "-n", "-e cp1251", file_name], shell=True)
        raw_tokens = raw_tokens.decode(encoding="cp1251")
        raw_tokens = raw_tokens.split("\n")
        self.tokens = [{"word": i.split("{")[0], "lemma": re.split(r"[}?|]", i.split("{")[1])[0]}
                       for i in raw_tokens if i]
