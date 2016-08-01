#coding:utf-8

import GetLastLunarDay
import datetime

testdate = datetime.date(2016,2,28)

print GetLastLunarDay.LunarController(testdate).get_pre_ln_day()