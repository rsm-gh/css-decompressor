#!/usr/bin/python
# -*- coding: utf-8 -*-
#

#  Copyright (C) 2015-2016, 2018 Rafael Senties Martinelli
#
#  This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License 3 as published by
#   the Free Software Foundation.
#
#  This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
#   along with this program; if not, write to the Free Software Foundation,
#   Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA.


__version__ = "2018.10.28"

_MESUREMENT_2DIGIT_UNITS = ('em','ex','px','cm','mm','in','pt','pc','ch','vh','vw')
_TAB_CHARACTER="    "

def replace_multiple_spaces(text):
    return ' '.join(text.split())


def inside_closing_brace(start_index, text, end_index=-1):
    
    if end_index == -1:
        end_index = len(text)
    
    reserch_text = text[start_index:end_index]
    
    if "}" in reserch_text and not "{" in reserch_text.split("}",1)[0]:
        return True
        
    return False

def format_line_with_left_code_and_right_comment(original_line, coment_separator):

    code_block = original_line.split(coment_separator,1)[0]
    comment_block = original_line.split(coment_separator,1)[1]
    
    code_block = replace_multiple_spaces(code_block)
    new_line = code_block + coment_separator + comment_block + '\n'
    new_line = new_line.replace(';'+coment_separator,'; '+coment_separator)
            
    return new_line


def format_line_with_left_comment_and_right_code(original_line, coment_separator):

    comment_block = original_line.split(coment_separator,1)[0]
    code_block = original_line.split(coment_separator,1)[1]
    
    code_block = replace_multiple_spaces(code_block)
    new_line = comment_block + coment_separator + '\n' + code_block
            
    return new_line


def format_coments_and_spaces(original_text):
    
    new_text = ""
    inside_comment = False
    
    for original_line in original_text.split('\n'):
        
        if '/*' in original_line and '*/' in original_line: # this will fail if the comment tags are inverted. To be improved.
            
            if original_line.rsplit('*/', 1)[1].strip() != '':
                new_text += format_line_with_left_comment_and_right_code(original_line, '*/')
            else:
                new_text += format_line_with_left_code_and_right_comment(original_line, '/*')
            
        elif '/*' in original_line:
            inside_comment = True
            
            code_text = original_line.split('/*',1)[0].strip()
            comment_text = original_line.split('/*',1)[1]
            
            if code_text == '':
            
                if new_text[-1:] != '\n':
                    new_text += '\n'
                
                new_text += original_line + '\n'
            else:
                new_text += code_text + '\n/*' + comment_text + '\n'
            
            
        elif inside_comment:
            
            if '*/' in original_line:
                inside_comment = False
                
                comment_text = original_line.rsplit('*/',1)[0]
                code_text = original_line.rsplit('*/',1)[1].strip()
                
                if code_text == '':
                    new_text += original_line + '\n\n'
                else:
                    new_text += comment_text+ '*/\n' + code_text
            else:
                new_text += original_line + '\n'
        
        elif '//' in original_line:
            new_text += format_line_with_left_code_and_right_comment(original_line, '//')
        
        else:
            
            new_line = original_line
            
            for char in ('\t','\n'):
                new_line=new_line.replace(char,'')
                
            new_line = replace_multiple_spaces(new_line)
            
            new_text += new_line
        
    return new_text


def needs_space_before(new_text_last_char, char, chars):

    if new_text_last_char in (' ',':'):
        return False
    
    elif char == '#' and chars[-1] == ':':
        return True
    
    elif char == '.' and not chars[-1].isdigit() and chars[1].isdigit():
        return True
    
    elif char == '!' and ''.join(chars[x] for x in range(1,4)) == 'imp':
        return True
    
    return False

def needs_space_after(char, char_index, chars, text):

    if chars[1] in (';',' '):
        return False

    elif char in (',',')'):
        return True

    elif char == ':' and inside_closing_brace(char_index, text):
        return True
    
    elif char == 's' and chars[-1].isdigit() and not chars[1]+chars[2]=='ol':
        return True
        
    elif chars[-1]+char in _MESUREMENT_2DIGIT_UNITS and chars[-2].isdigit():
        return True

    elif char == 'm' and chars[-3].isdigit() and ''.join(chars[x] for x in range(-2,1)) == 'rem':
        return True
        
    elif char in ('n','x') and chars[-4].isdigit() and ''.join(chars[x] for x in range(-3,1)) in ('vmin','vmax'):
        return True
        
    return False
    
    
def decompress_css(original_css):
    
    converted_css = format_coments_and_spaces(original_css)
    
    new_text=""
    indent_level=0
    inside_commented_block = False
    

    for i, char in enumerate(converted_css):
        
        #
        #
        #
        chars={k:'' for k in range(-4,4)}
        for k in range(-4,4):
            try:
                chars[k]=converted_css[i+k]
            except:
                pass
        
        new_text_last_char=new_text[-1:]
        
        
        #
        #
        #
        if (char == '/' and chars[1] == '*') or inside_commented_block:
            inside_commented_block = True
             
            if char == '/' and chars[-1] == '*':
                inside_commented_block = False
                
        elif char in ('>', '+'):
            
            if chars[-1] != ' ':
                char = ' '+char
            
            if chars[1] != ' ':
                char = char + ' '
        
        elif needs_space_after(char, i, chars, converted_css):
            char+=' '
        
        elif needs_space_before(new_text_last_char, char, chars):
            char = ' '+char
    
        elif char == '{':
            
            indent_level+=1
            
            if new_text_last_char != ' ':
                char =' {\n'
            else:
                char ='{\n'
            
            
        elif char == '}':
            
            indent_level-=1
            
            if new_text_last_char != '\n':
                new_text += '\n'
                new_text_last_char='\n'
            
            if chars[1] == '}':
                char = '}\n'
            else:
                char = '}\n\n'
            
            
        elif char == ';':
            
            if chars[2] == '/' and chars[3] == '*':  #     code; /* comment */
                pass
            elif chars[2] == '/' and chars[3] == '/': #    code; // comment
                pass
            else:   
                char = ';\n'
        
        
        if new_text_last_char == '\n':
            new_text += _TAB_CHARACTER*indent_level
            
        new_text+=char

    return new_text


if __name__ == '__main__':
    
    import sys
     
    css=sys.stdin.read()
    css=decompress_css(css)
    sys.stdout.write(css)

