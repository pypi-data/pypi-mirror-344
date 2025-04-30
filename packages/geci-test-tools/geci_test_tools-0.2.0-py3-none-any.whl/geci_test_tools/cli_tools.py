import re


def strip_ansi_sequences(text):
    ansi_escape = re.compile(r"\x1b\[([0-9;]*[mGKF])")
    return ansi_escape.sub("", text)
