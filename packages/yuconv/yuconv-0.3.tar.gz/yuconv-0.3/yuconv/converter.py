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

def cir_to_lat(text):
    cyrillic_to_latin = {
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Ђ': 'Đ', 'Е': 'E', 'Ж': 'Ž',
        'З': 'Z', 'И': 'I', 'Ј': 'J', 'К': 'K', 'Л': 'L', 'Љ': 'Lj', 'М': 'M', 'Н': 'N', 
        'Њ': 'Nj', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'Ћ': 'Ć', 'У': 'U',
        'Ф': 'F', 'Х': 'H', 'Ц': 'C', 'Ч': 'Č', 'Џ': 'Dž', 'Ш': 'Š',
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'ђ': 'đ', 'е': 'e', 'ж': 'ž',
        'з': 'z', 'и': 'i', 'ј': 'j', 'к': 'k', 'л': 'l', 'љ': 'lj', 'м': 'm', 'н': 'n',
        'њ': 'nj', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'ћ': 'ć', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'č', 'џ': 'dž', 'ш': 'š'
    }

    result = []
    text_len = len(text)
    i = 0
    
    while i < text_len:
        if text[i:i+2] in ['Љ', 'Њ', 'Џ']:
            result.append(cyrillic_to_latin[text[i]])
            i += 1
        elif text[i] in cyrillic_to_latin:
            result.append(cyrillic_to_latin[text[i]])
        else:
            result.append(text[i])
        i += 1

    return ''.join(result)

def lat_to_cir(text):
    latin_to_cyrillic = {
        'A': 'А', 'B': 'Б', 'V': 'В', 'G': 'Г', 'D': 'Д', 'Đ': 'Ђ', 'E': 'Е', 'Ž': 'Ж',
        'Z': 'З', 'I': 'И', 'J': 'Ј', 'K': 'К', 'L': 'Л', 'Lj': 'Љ', 'M': 'М', 'N': 'Н', 
        'Nj': 'Њ', 'O': 'О', 'P': 'П', 'R': 'Р', 'S': 'С', 'T': 'Т', 'Ć': 'Ћ', 'U': 'У',
        'F': 'Ф', 'H': 'Х', 'C': 'Ц', 'Č': 'Ч', 'Dž': 'Џ', 'Š': 'Ш',
        'a': 'а', 'b': 'б', 'v': 'в', 'g': 'г', 'd': 'д', 'đ': 'ђ', 'e': 'е', 'ž': 'ж',
        'z': 'з', 'i': 'и', 'j': 'ј', 'k': 'к', 'l': 'л', 'lj': 'љ', 'm': 'м', 'n': 'н',
        'nj': 'њ', 'o': 'о', 'p': 'п', 'r': 'р', 's': 'с', 't': 'т', 'ć': 'ћ', 'u': 'у',
        'f': 'ф', 'h': 'х', 'c': 'ц', 'č': 'ч', 'dž': 'џ', 'š': 'ш'
    }

    result = []
    text_len = len(text)
    i = 0

    while i < text_len:
        if i < text_len - 1 and text[i:i+2] in ['Lj', 'Nj', 'Dž', 'lj', 'nj', 'dž']:
            result.append(latin_to_cyrillic[text[i:i+2]])
            i += 2
        elif text[i] in latin_to_cyrillic:
            result.append(latin_to_cyrillic[text[i]])
            i += 1
        else:
            result.append(text[i])
            i += 1

    return ''.join(result)
