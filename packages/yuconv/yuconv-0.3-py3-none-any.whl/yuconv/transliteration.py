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

from .converter import cir_to_lat, lat_to_cir
from docx import Document


def transliterate_text(input_text: str, transliteration_mode:str) -> str:
    """
    Transliterates text using the transliteration mode.
    Args:
    input_text (str): Text to be translated using the transliteration_mode
    transliteration_mode: (str): Transliteration mode, cyrillic, or latin
    Returns:
    str: Transliterated text
    """
    transliterated_text = ''
    if transliteration_mode == "lat-to-cyr":
        transliterated_text = lat_to_cir(input_text)
    elif transliteration_mode == "cyr-to-lat":
        transliterated_text = cir_to_lat(input_text)
    else:
        raise ValueError('Invalid transliteration mode.')
    return transliterated_text

def transliterate_file(input_file:str, output_file:str, transliteration_mode:str):
    """
    Transliterates an input file using the transliteration_mode and saves the transliterated text to an output file.
    Args:
    input_file (str): a File to be transliterated
    transliteration_mode (str): Transliteration mode cyrillic, or latin. If cyrillic, transliterates latin text to cyrillic, and reverse
    output_file (str): a File contains transliterated text
    """
    source_text = ''
    transliterated_text = ''
    with open(input_file, 'r', encoding='utf-8') as f:
        source_text = f.read()
    if transliteration_mode == "lat-to-cyr":
        transliterated_text = lat_to_cir(source_text)
    elif transliteration_mode == "cyr-to-lat":
        transliterated_text = cir_to_lat(source_text)
    else:
        raise ValueError('Invalid transliteration mode')
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(transliterated_text)

def transliterate_word_document(input_document:str, output_document:str, transliteration_mode:str):
    """
    Transliterates Word document using TransliterationMode, and saves transliterated document to a specifyed file.
    Args:
    input_document (str): Word document to be transliterated
    output_document (str): Output Word document file where transliterated document needs to be saved
    transliteration_mode (str): Mode for transliteration Cyrillic, or Latin
    """
    document = Document(input_document)
    for paragraph in document.paragraphs:
        source_text = paragraph.text
        dest_text = ''
        if transliteration_mode == "lat-to-cyr":
            dest_text = lat_to_cir(source_text)
        elif transliteration_mode == "cyr-to-lat":
            dest_text = cir_to_lat(source_text)
        else:
            raise ValueError('Invalid transliteration mode.')
        paragraph.text = dest_text
    document.save(output_document)
