"""
    通过Table对象来实现找图找色、识别点击的插件
"""
from plugin.tablerEx import TABLE_ITEM_TYPE_COLOR, TABLE_ITEM_TYPE_IMAGE


def _findColor(finder, start_x, start_y, end_x, end_y, match_color_str):
    """
        多点找色，支持偏色
    """
    x, y = finder.findMultiColor(start_x, start_y, end_x, end_y, match_color_str)
    return x, y


def _findImage(finder, start_x, start_y, end_x, end_y, template_path, threshold):
    """
        多尺寸找图
    """
    x, y = finder.findImage(start_x, start_y, end_x, end_y, template_path, threshold)
    return x, y


class FinderEx:
    def __init__(self, finder, toucher, phone, logger, timer, tabler_ex):
        self.finder = finder
        self.toucher = toucher
        self.phone = phone
        self.logger = logger
        self.timer = timer
        self.table = tabler_ex.table

    def tap(self, table_name, table_item_name):
        """
            点击操作主函数
            :param table_name: 表名
            :param table_item_name: 字段名
            :return: 点击结果
        """
        item = self.table[table_name][table_item_name]
        self.logger.info("正在点击[", table_name, "][", table_item_name, "]", "->点击坐标[",
                         ",".join([str(item.position_x), str(item.position_y)]), "]")
        return self.toucher.tapSingle(item.position_x, item.position_y)

    def longTouch(self, table_name, table_item_name, time_cost):
        """
            长按操作主函数
            :param table_name: 表名
            :param table_item_name: 字段名
            :param time_cost: 长按时长
            :return: 点击结果
        """
        item = self.table[table_name][table_item_name]
        self.logger.info("正在长按[", table_name, "][", table_item_name, "]", "->长按坐标[",
                         ",".join([str(item.position_x), str(item.position_y)]), "]->长按时长[", time_cost, "s]")
        return self.toucher.longTouchSingle(item.position_x, item.position_y, time_cost)

    def swipe(self, table_name, table_item_name, time_cost):
        """
            滑动操作主函数
            :param table_name: 表名
            :param table_item_name: 字段名
            :param time_cost: 滑动时长
            :return: 点击结果
        """
        item = self.table[table_name][table_item_name]
        self.logger.info("正在滑动[", table_name, "][", table_item_name, "]", "->滑动起点坐标[",
                         ",".join([str(item.start_x), str(item.start_y)]), "]", "->滑动终点坐标[",
                         ",".join([str(item.end_x), str(item.end_y)]), "]", "->滑动时长[", time_cost, "s]")
        return self.toucher.swipeSingle(item.start_x, item.start_y, item.end_x, item.end_y, time_cost)

    def find(self, table_name, table_item_name, isReturnLoc=False):
        """
            查找操作主函数
            :param table_name: 表名
            :param table_item_name: 字段名
            :param isReturnLoc: 是否返回坐标
            :return: 查找结果
        """
        item = self.table[table_name][table_item_name]
        self.logger.debug("正在查找[", table_name, "][", table_item_name, "]", "->查找范围[",
                          ",".join([str(item.start_x), str(item.start_y), str(item.end_x), str(item.end_y)]), "]")
        x, y = -1, -1
        if item.table_item_type == TABLE_ITEM_TYPE_COLOR:
            x, y = _findColor(self.finder, item.start_x, item.start_y, item.end_x, item.end_y, item.match_color_str)
        elif item.table_item_type == TABLE_ITEM_TYPE_IMAGE:
            x, y = _findImage(self.finder, item.start_x, item.start_y, item.end_x, item.end_y, item.template_path,
                              item.threshold)
        if x != -1 and y != -1:
            self.logger.info("查找成功[", table_name, "][", table_item_name, "]->坐标[", ",".join([str(x), str(y)]), "]")
            return (x, y) if isReturnLoc else True
        self.logger.warning("未找到[", table_name, "][", table_item_name, "]")
        return (x, y) if isReturnLoc else False

    def findTap(self, table_name, table_item_name, py_x=0, py_y=0):
        """
            查找通过则点击
            :param table_name: 表名
            :param table_item_name: 字段名
            :param py_x: x坐标偏移点击数值
            :param py_y: y坐标偏移点击数值
            :return: 是否点击成功
        """
        x, y = self.find(table_name, table_item_name, isReturnLoc=True)
        if x != -1 and y != -1:
            self.logger.info("查找成功[", table_name, "][", table_item_name, "]->坐标[", ",".join([str(x), str(y)]),
                             "]->执行操作[", "点击]")
            self.toucher.tapSingle(x + py_x, y + py_y)
            return True
        return False

    def findLongTouch(self, table_name, table_item_name, time_cost, py_x=0, py_y=0):
        """
            查找通过则长按
            :param table_name: 表名
            :param table_item_name: 字段名
            :param time_cost: 长按时长
            :param py_x: x坐标偏移点击数值
            :param py_y: y坐标偏移点击数值
            :return: 是否长按成功
        """
        x, y = self.find(table_name, table_item_name, isReturnLoc=True)
        if x != -1 and y != -1:
            self.logger.info("查找成功[", table_name, "][", table_item_name, "]->坐标[", ",".join([str(x), str(y)]),
                             "]->执行操作[", "长按]->长按时长[", time_cost, "ms]")
            self.toucher.longTouchSingle(x + py_x, y + py_y, time_cost)
            return True
        return False

    def findRepeat(self, table_name, table_item_name, time_out=30):
        """ 循环直到找到 """
        while True:
            if not self.find(table_name, table_item_name):
                self.timer.sleep(1000)
                time_out -= 1
                if time_out == 0:
                    break
            else:
                return True
        return False

    def findTapRepeat(self, table_name, table_item_name, time_out=30, py_x=0, py_y=0):
        """ 循环直到找到并点击成功 """
        while True:
            if not self.findTap(table_name, table_item_name, py_x, py_y):
                self.timer.sleep(1000)
                time_out -= 1
                if time_out == 0:
                    break
            else:
                return True
        return False

    def findLongTouchRepeat(self, table_name, table_item_name, time_cost, time_out=30, py_x=0, py_y=0):
        """ 循环直到找到并长按成功 """
        while True:
            if not self.findLongTouch(table_name, table_item_name, time_cost, py_x, py_y):
                self.timer.sleep(1000)
                time_out -= 1
                if time_out == 0:
                    break
            else:
                return True
        return False
