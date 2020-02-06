# coding: utf-8
from __future__ import unicode_literals

pos_dict = {
    'a': ['Ag', 'a', 'ad', 'an'],
    'd': ['dg', 'Dg', 'd'],
    'v': ['v', 'vg', 'Vg'],
    'oth': [
        'b', 'c', 'e', 'f', 'g', 'h', 'o', 'p', 'r', 's', 'u', 'x', 'y', 'k',
        'z', 'un', 'j'
    ]
}


def norm_pos(pos):
    for key, values in pos_dict.iteritems():
        if pos in values:
            return key
    return pos
