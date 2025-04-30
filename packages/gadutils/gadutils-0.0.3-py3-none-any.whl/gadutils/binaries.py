from gadutils import strings

from gadutils.strings import const


def tostring(string: bytes) -> str:
    return strings.strip(string.decode(const.ENCODING_UTF).replace(const.SYMBOL_NEWLINE, const.SYMBOL_EMPTY))
