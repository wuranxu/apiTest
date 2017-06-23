__author__ = 'Woody'
'''methods for reading excel files
'''
import xlrd
import os
import logging
from common.function import Operator


class reader(object):
    fileHandle = None

    def __init__(self, filepath):
        # 过滤掉非excel的文件
        if filepath.endswith('.xlsx') or filepath.endswith('.xls'):
            if os.path.exists(filepath):
                try:
                    # 获取xlrd book对象
                    self.fileHandle = xlrd.open_workbook(filepath)
                except Exception as err:
                    logging.error("{} error: 打开本地excel文件失败! 文件目录: {} 错误信息: {}".format(
                        Operator.get_current_func(), filepath, str(err)))
        if not self.fileHandle:
            raise Exception('打开本地excel文件失败! 请检查日志！')

    def get_case_list(self):
        '''
        :return: excel中存放的用例列表
        '''
        case_list = []
        try:
            # 获取excel所有sheet
            sheets = self.fileHandle.sheets()
            # 遍历sheet
            for index in range(len(sheets)):
                sheet = self.fileHandle.sheet_by_index(index)
                # 获取合并的单元格
                merged = self.merge_cell(sheet)
                # 获取sheet的行数（默认每一行就是一条用例）
                rows = sheet.nrows
                # 如果sheet为空，那么rows是0
                if rows:
                    for row in range(rows):
                        case_info = sheet.row_values(row)
                        # 过滤表头, id或method出现在某一行数据里则确认它为表头
                        if not ('id' in case_info or 'test_method' in case_info):
                            for index, content in enumerate(case_info):
                                if merged.get((row, index)):
                                    # 这是合并后的单元格，需要重新取一次数据
                                    case_info[index] = sheet.cell_value(*merged.get((row, index)))
                            # 将用例信息如id，name等组成dict添加到case_list
                            case_list.append(
                                dict(id=case_info[0], name=case_info[1],
                                     params=case_info[2], url=case_info[3],
                                     method=case_info[4], code=case_info[5],
                                     headers=case_info[6], _assert=case_info[7],
                                     expected=case_info[8], enable=case_info[9])
                            )
        # 捕获异常
        except Exception as err:
            print("{} error: {}".format(Operator.get_current_func(), str(err)))
            logging.error("{} error: {}".format(Operator.get_current_func(), str(err)))
        return case_list

    def merge_cell(self, sheet):
        rt = {}
        # 如果存在合并单元格
        if sheet.merged_cells:
            # 遍历合并单元格，sheet.merged_cells会返回元祖
            for item in sheet.merged_cells:
                for row in range(item[0], item[1]):
                    for col in range(item[2], item[3]):
                        rt.update({(row, col): (item[0], item[2])})
        return rt

    def get_addr_status(self):
        # 获取excel所有sheet
        sheets = self.fileHandle.sheets()
        # 遍历sheet
        for index in range(len(sheets)):
            sheet = self.fileHandle.sheet_by_index(index)
            # 获取合并的单元格
            merged = self.merge_cell(sheet)
            # 获取sheet的行数（默认每一行就是一条用例）
            rows = sheet.nrows
            # 如果sheet为空，那么rows是0
            if rows:
                for row in range(rows):
                    case_info = sheet.row_values(row)
                    if case_info[-1].lower() == 'off':
                        yield case_info[0]

    def release_source(self):
        '''
        释放excel资源
        :return:
        '''
        if self.fileHandle:
            self.fileHandle.release_resources()