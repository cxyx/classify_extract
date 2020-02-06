# coding: utf-8
from __future__ import unicode_literals

import re


"""
当content太长时，以字段为中心，切除无用的content
"""


def cut_off_content(content, tags, context_len=10, step=5, max_len=100):
    """
    tags标签体系：BMESO
    """

    assert len(content) == len(tags)

    # norm
    normed_tags = ''.join([tag[0] for tag in tags])

    # find all values
    values = [(m.start(), m.start() + len(m.group())) for m in re.finditer('BM*E|S', normed_tags)]

    # gen sequence
    seq_start = seq_end = -1
    for value_start, value_end in values:
        if value_end <= seq_end:
            continue
        # 根据context_len获得序列开始、结束位置
        seq_start = value_start - context_len if value_start - context_len > 0 else 0
        seq_end = value_end + context_len if value_end + context_len < len(normed_tags) else len(normed_tags)
        # 禁止起止位置出现value
        while seq_start >= 0 and normed_tags[seq_start] != 'O':
            seq_start -= step
        while seq_end <= len(normed_tags) and normed_tags[seq_end-1] != 'O':
            seq_end += step
        seq_start = seq_start if seq_start > 0 else 0
        seq_end = seq_end if seq_end < len(normed_tags) else len(normed_tags)
        # 设置最大长度
        if seq_end - seq_start <= max_len:
            yield content[seq_start:seq_end], tags[seq_start:seq_end]
        else:
            seq_start = value_start - max_len / 2 if value_start - max_len / 2 > 0 else 0
            seq_end = value_start + max_len / 2 if value_start + max_len / 2 < len(normed_tags) else len(normed_tags)
            yield content[seq_start:seq_end], tags[seq_start:seq_end]

