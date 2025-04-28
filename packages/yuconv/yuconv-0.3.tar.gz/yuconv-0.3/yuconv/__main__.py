#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#    Copyright (C) 2024  Darko Milosevic

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.


from .yu_converter import YuConverter, TransliterationMode
import argparse

yu_converter = YuConverter()
trans_mode = TransliterationMode()
arg_parser = argparse.ArgumentParser(description='YuConverter terminal app')
arg_parser.add_argument('-t', help='Transliterates text using one of the transliteration modes cyr-to-lat, or lat-to-cyr')
arg_parser.add_argument('-m', help='Transliteration mode, cyr-to-lat, or lat-to-cyr')
arg_parser.add_argument('-i', help='Input file or Word document')
arg_parser.add_argument('-o', help='Output file or Word document')

def process_transliteration():
    arguments = arg_parser.parse_args()
    if arguments.m is None:
        raise ValueError('Invalid transliteration mode')
    if arguments.t is not None:
        text = yu_converter.transliterate_text(arguments.t, arguments.m)
        print(text)
    else:
        if arguments.i is not None and arguments.o is not None:
            if arguments.i.endswith('.docx'):
                yu_converter.transliterate_word_document(arguments.i, arguments.o, arguments.m)
                print('Transliteration complete')
            else:
                yu_converter.transliterate_text_file(arguments.i, arguments.o, arguments.m)
                print('Transliteration complete')

def main():
    process_transliteration()

