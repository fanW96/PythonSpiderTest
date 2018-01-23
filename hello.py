#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# name = input('please input your name:')
# print('hello 韦璠：',name)


# r = 13/72*100
# print('%01.1f%%' %r)


height = 1.75
weight = 80.5
bmi = weight/(height**2)
print('体重指数=',bmi)
a=18.5
b=25
c=28
d=32
if bmi<a:

    print('判定结果为：过轻')
elif bmi<b:
    print('恭喜你，判定结果为正常')
elif bmi<c:
    print('判定结果为：过重')
elif bmi<d:
    print('判定结果为：肥胖')
    print('判定结果为：严重肥胖')