# coding: utf-8
from __future__ import unicode_literals

import re
import copy

from base_normalize import BaseNormalize


IGNORED_CHARS = {'\n', '\t', '\r', '　', ' ', '_', '\3', '\4', '\u2028', '\xa0'}
REPLACED_CHARS = {
    '[0-9]': 'n',
    '[〇一二三四五六七八九十]': 'N',
    '[壹贰叁肆伍陆柒捌玖零拾佰仟萬]': 'M'
}


class Normalize(BaseNormalize):

    """
    对样本进行归一化处理
    """

    def __init__(self, content, sbc2dbc=True, ignored_chars=IGNORED_CHARS, replaced_chars=REPLACED_CHARS,
                 is_english=False):
        super(Normalize, self).__init__(content)
        self._sbc2dbc = sbc2dbc
        self._ignored_chars = copy.deepcopy(ignored_chars)
        self._replaced_chars = copy.deepcopy(replaced_chars)
        self._is_english = is_english
        if self._is_english:
            self._ignored_chars.remove(' ')

    def normalize(self):
        normed_content = self._content
        if self._sbc2dbc:
            normed_content = self.sbc2dbc(normed_content)  # sbc 2 dbc
        for k, v in self._replaced_chars.iteritems():  # replace char
            normed_content = re.sub(k, v, normed_content)
        tmp_content = normed_content
        normed_content = re.sub('|'.join(self._ignored_chars), '', normed_content)  # delete ignore chars
        self._gen_index_map(tmp_content, normed_content)
        if self._is_english:
            normed_content = normed_content.lower()
        return normed_content

    @staticmethod
    def sbc2dbc(string):
        n = []
        for char in string:
            num = ord(char)
            if num == 0x3000:
                num = 32
            elif 0xFF01 <= num <= 0xFF5E:
                num -= 0xfee0
            num = unichr(num)
            n.append(num)
        return ''.join(n)
