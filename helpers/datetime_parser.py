#!/usr/bin/python
# -*- coding: utf-8 -*-
import dateparser


def parse_datetime(s):
    return dateparser.parse(s, settings={'PREFER_DATES_FROM': 'future', 'FUZZY': True}, languages=['en', 'vi'])


def main():
    print(parse_datetime('tháng mười'))


if __name__ == '__main__':
    main()
