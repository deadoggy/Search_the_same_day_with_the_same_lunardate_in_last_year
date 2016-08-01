#coding:utf-8
import Lunar
import datetime

class LunarController(object):


    def __init__(self, date):
        self.date = date
        self.Lunar = Lunar.Lunar(date)

    def _compareDateUpToMonth(self, par_1, par_2):
        '''0-same, 1-greater, 2-smaller'''
        if par_1[1] > par_2[1]:
            return 1
        elif par_1[1] < par_2[1]:
            return -1
        else:
            if par_1[2] > par_2[2]:
                return 1
            elif par_1[2] == par_2[2]:
                return 0
            else:
                return -1

    def _search(self, last_date, local_time_ln, gap):#从当前日期向后或向前寻找农历日相同的天
        flag = False
        temp_date = last_date + datetime.timedelta(days=gap)
        while not flag:
            temp_ln = Lunar.Lunar(temp_date).ln_date()
            if local_time_ln[1] == temp_ln[1] and local_time_ln[2] == temp_ln[2] :
                break
            temp_date = temp_date + datetime.timedelta(days=gap)

        return temp_date


    def get_pre_ln_day(self):
        '''
           获取上一个该农历年的阳历日期
           如果去年没有该农历日，返回空元组
        '''
        # 获取当前日期的农历年
        local_time_ln = self.Lunar.ln_date()
        # 获取上一个农历年的月天数信息
        last_lnyear_month = self.Lunar.g_lunar_month_day[local_time_ln[0] - 1 - 1901]
        # 如果当前月是13月而去年没有13月， 返回空
        if 0 != Lunar.Lunar.g_lunar_month_day[local_time_ln[0] - 1901] % 16 and 0 == last_lnyear_month % 16:
            return ()
        # 如果当前日是30号而去年该月是小月，返回空
        if 30 == local_time_ln[2] and 0 == ((last_lnyear_month >> (16 - local_time_ln[1])) % 2):
            return ()
        #获取阳历去年今天
        if 2 == self.date.month and 29 == self.date.day:#如果今年是闰年
            last_date = datetime.date(self.date.year - 1, 3, 1)
        else:
            last_date = datetime.date(self.date.year - 1, self.date.month, self.date.day)

        #获取去年今天的阴历
        last_time_ln = Lunar.Lunar(last_date).ln_date()

        #比较两个的农历日期
        ln_compare = self._compareDateUpToMonth(local_time_ln, last_time_ln)

        if 0 == ln_compare:
            return last_date
        elif 1 == ln_compare:
            return self._search(last_date,local_time_ln,1)
        else:
            return self._search(last_date,local_time_ln,-1)
