#!/usr/bin/python
# -*- coding: utf8 -*-


class Normalize(object):
    VIETNAMESE_CHARS = 'àảãáạăằẳẵắặâầẩẫấậòỏõóọôồổỗốộơờởỡớợèẻẽéẹêềểễếệùủũúụưừửữứựìỉĩíịỳỷỹýỵđ'
    LATIN_CHARS = 'aAoOeEuUiIyYdD'

    """
    Hàm xóa stopwords trong tokens
    """

    @classmethod
    def remove_stopwords(cls, tokens, stopwords):
        def in_stopwords(token):
            if isinstance(token, tuple):
                return token[0] in stopwords
            return token in stopwords

        return [token for token in tokens if not in_stopwords(token)]

    """
    Hàm xóa dấu kí tự
    """

    @classmethod
    def delete_tonemark_char(cls, c):
        pos = cls.VIETNAMESE_CHARS.find(c.lower())
        if pos == -1: return c
        if pos <= 16: return cls.LATIN_CHARS[1 - c.islower()]
        if pos <= 33: return cls.LATIN_CHARS[3 - c.islower()]
        if pos <= 44: return cls.LATIN_CHARS[5 - c.islower()]
        if pos <= 55: return cls.LATIN_CHARS[7 - c.islower()]
        if pos <= 60: return cls.LATIN_CHARS[9 - c.islower()]
        if pos <= 65: return cls.LATIN_CHARS[11 - c.islower()]
        if pos <= 66: return cls.LATIN_CHARS[13 - c.islower()]

    """
    Hàm xóa dấu trong chuỗi
    """

    @classmethod
    def delete_tonemark_string(cls, s):
        return ''.join([cls.delete_tonemark_char(c) for c in s])
