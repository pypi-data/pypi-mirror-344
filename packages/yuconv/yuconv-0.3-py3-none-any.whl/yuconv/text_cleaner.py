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

from .transliteration import transliterate_file, transliterate_text, transliterate_word_document

class TransliterationMode:
    CyrillicToLatin = ""
    LatinToCyrillic = ""

    def __init__(self):
        self.CyrillicToLatin = "cyr-to-lat"
        self.LatinToCyrillic = "lat-to-cyr"

class YuConverter:
    def __init__(self, file_name:str=None):
        """
        YuConverter class
        Args:
        file_name (str): Path of a file to be read. You can specify a text file, or a word document
        """
        self.file_name = file_name
    
    def transliterate_text(self, text:str, transliteration_mode:str) ->str:
        """
        Transliterate text using one of the transliteration modes
        args:
        text (str): Input text
        transliteration_mode (str): Transliteration mode Cyrillic, or Latin. You can use the TransliterationMode class to choose the transliteration mode.
        Examples:
        >>> from yuconv import YuConverter
        >>> yu_converter = YuConverter()
        >>> transliterated_text = yu_converter.transliterate_text('Konji su pasli na livadi.', TransliterationMode.LatinToCyrillic)
        Returns:
        str: Transliterated text
        """
        return transliterate_text(text, transliteration_mode)
    
    def transliterate_text_file(self, input_file=None, output_file=None, transliteration_mode=str):
        """
        Transliterates text file, and saves the transliteration to the output file
        Args:
        input_file (str): a File to be transliterated
        output_file (str): a File where transliteration should be saved
        transliteration_mode (str): Mode for transliteration (Cyrillic, or Latin). You can use the TransliterationMode class to choose the transliteration mode.
        """
        input_transliteration_file = input_file if input_file is not None else self.file_name
        if input_transliteration_file is None:
            raise ValueError('input_file must be a valid file name.')
        transliterate_file(input_transliteration_file, output_file, transliteration_mode)
    
    def transliterate_word_document(self, input_document=None, output_document=None, transliteration_mode=str):
        """
        Transliterates Word documents using TransliterationMode (Cyrillic, or Latin)
        args:
        input_document (str): Document to be transliterated
        output_document (str): Transliterated document (Document to be saved after transliteration)
        transliteration_mode (str): Transliteration mode (CyrillicToLatin, or LatinToCyrillic). You can use the TransliterationMode class to choose the transliteration mode.
        """
        input_transliteration_file = input_document if input_document is not None else self.file_name
        if input_transliteration_file is None:
            raise ValueError('Input Word document cannot be a blank value.')
        transliterate_word_document(input_document, output_document, transliteration_mode)

