# coding=utf-8
# email:  xgao85@gmail.com
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

from . import get_logger
from typing import Dict, List


class Procession(object):

    def __init__(self, processors, request_property):
        # type: (List, Dict) -> None
        self._processors = processors
        if 'run_info' in request_property:
            raise RuntimeError('run_info in request_property is used by the framework, please assign another key!')
        request_property['run_info'] = {
            'current_index': 0,
            'run_flag_dict': {},
            'global_variance_dict': {},
        }
        self._request_property = request_property

    def run(self, tmp_result):
        # type: (Dict) -> Dict
        output = {}
        cur_idx = 0
        while cur_idx >= 0:
            if cur_idx < len(self._processors):
                cur_processor = self._processors[cur_idx]
                self._request_property['run_info']['current_index'] = cur_idx
                direction = cur_processor.process(tmp_result, output, self._request_property)
                if direction == 'up':
                    cur_idx -= 1
                elif direction == 'down':
                    cur_idx += 1
                else:
                    raise Exception('processor: {} should return direction'.format(cur_processor.name))
            else:
                cur_idx -= 1
        return output
