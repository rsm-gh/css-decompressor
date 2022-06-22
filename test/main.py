#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

#  Copyright (C) 2018 Rafael Senties Martinelli
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


import sys
sys.path.append('../')

from css_min import cssmin
from css_decompressor import decompress_css



def test1():

    with open('./input.css', 'r') as f:
        css = f.read()
    
    css = cssmin(css)
    css = decompress_css(css)
    
    with open('./output1.css', 'w') as f:
        css = f.write(css)
    

    print("Test 1, done.")



def test2():

    with open('./input.css', 'r') as f:
        css = f.read()
    
    css = cssmin(css)
    css = decompress_css(css)
    
    with open('./output2.css', 'w') as f:
        css = f.write(css)
    

    print("Test 2, done.")


if __name__ == "__main__":
    test1()
    test2()
        
        
