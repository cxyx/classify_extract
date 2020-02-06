# -*- coding: utf-8 -*-
# email: qianyixin@datagrand.com
# date: 2019-07-02 15:06

import re
import traceback
import sys
from ..common.extract_tools import cut_head
from ..common.extract_tools import start_extract
from classify_extract.conf import conf
from u_shape_framework.processors.processor_base import ProcessorBase
from ..driver import logger_offline as logger


class ProcessorContentToText(ProcessorBase):
    '''
    func:将线上的配置文件与本地合并,线上优先
    后期版本可能增加更新部分配置,较多代码,所以单独processor,目前更新所有的
    '''

    def load(self, args):
        self._args = args

    def up(self, tmp_result, output, request_property):
        pass

    def down(self,tmp_result, output, request_property):
        print('ProcessorExtractPre')
        text = request_property.get('content')
        # text = tmp_result.get('content')
        mapper = [i for i in range(len(text))]
        opontions = []
        prerequisite = []
        requirement = []
        all_list = list()
        re_opontions = re.search(r'审批意见[:：]', text)
        all_list.extend([re_opontions.span()] if re_opontions else [None])
        re_prerequisite = re.search(
            r'((?:贷款)?前提(?:落实)?条件[: ：]|([一二三四]、)(?:贷款)?前提(?:落实)?条件[:：]?)(.{,5}(?:贷款)?前提(?:落实)?条件[: ：]|([一二三四]、)(?:贷款)?前提(?:落实)?条件[:：]?)?',
            text)
        all_list.extend([re_prerequisite.span()] if re_prerequisite else [None])
        re_requirement = re.search(
            r'((?:补充融资|融资|贷后|贷款|保兑业务|业务)?管理(?:要求|条件)[: ：]|[一二三四]、?(?:补充融资|融资|贷后|贷款|保兑业务|业务)?管理(?:要求|条件)[: ：]?)(.{,5}(?:补充融资|融资|贷后|贷款|保兑业务|业务)?管理(?:要求|条件)[: ：]|[一二三四]、?(?:补充融资|融资|贷后|贷款|保兑业务|业务)?管理(?:要求|条件)[: ：]?)?',
            text)

        all_list.extend([re_requirement.span()] if re_requirement else [None])

        if all_list[0]:
            end_index = all_list[1][0] if all_list[1] else all_list[2][0] if all_list[2] else None
            start_index = all_list[0][1]
            head_len = cut_head(text[start_index:end_index], r'^.{,5}审批意见[:：]')
            opontions.append(text[start_index + head_len:end_index])
            opontions.append(mapper[start_index + head_len:end_index])
            # print 'opontions',opontions
        if all_list[1]:
            end_index = all_list[2][0] if all_list[2] else None
            start_index = all_list[1][1]
            head_len = cut_head(text[start_index:end_index], r'^.{,5}前提(?:落实)?条件[::]')
            print('text', text)
            prerequisite.append(text[start_index + head_len:end_index])
            prerequisite.append(mapper[start_index + head_len:end_index])
            print('prerequisite', prerequisite)
        if all_list[2]:
            end_index = None
            start_index = all_list[2][1]
            head_len = cut_head(text[start_index:end_index], r'^.{,5}管理(条件|要求)[::]')
            requirement.append(text[start_index + head_len:end_index])
            requirement.append(mapper[start_index + head_len:end_index])

        print("**审批意见:**")
        print("{},{}".format(opontions[1][0] if opontions[1] else "NULL", opontions[0] if opontions else "NULL"))
        print("**前提条件:**")
        # print 'prerequisite',prerequisite
        print("{},{}".format(prerequisite[1][0] if prerequisite[1] else "NULL",
                              prerequisite[0] if prerequisite else "NULL"))
        print("**管理要求:**")
        print("{},{}".format(requirement[1][0] if requirement[1] else "NULL",
                              requirement[0] if requirement else "NULL"))
        logger.info('安装审批意见,审批意见,管理要求三者不同类型提取信息成功!!!!')
        tmp_result.update({'opontions': opontions, 'prerequisite': prerequisite, 'requirement': requirement})
        print('tmp_resulttmp_result',tmp_result)

