"""
Author: Big Panda
Created Time: 25.04.2025 14:09
Modified Time: 25.04.2025 14:09
Description:
    
"""
# class Logger:
#     def __init__(self, func):
#         self.func = func
#
#     def __call__(self, *args, **kwargs):
#         print(args)
#         print(kwargs)
#         print(f"调用函数 {self.func.__name__}")
#         result = self.func(*args, **kwargs)
#         print(f"函数 {self.func.__name__} 执行完毕")
#         return result
#
#
# @Logger
# def add(a, b):
#     return a + b
#
#
# print(add(2, 3))

# class Repeat:
#     def __init__(self, times):
#         self.times = times
#
#     def __call__(self, func):
#         def hhhh(*args, **kwargs):
#             for _ in range(self.times):
#                 result = func(*args, **kwargs)
#             return result
#
#         return hhhh
#
#
# @Repeat(times=3)
# def greet(name):
#     print(f"Hello, {name}!")


# greet("World")
# 输出:
# from DataRestriction import *


# x = RealProperty(1)
# print(x)
# print(x < 2)
# 调用函数 add
# 函数 add 执行完毕
# 5

# 这里的示例也可以写成一个教程！！！！
# x, y = [1, 3]
# print(x)
# print(y)

# class Parent:
#     def __init__(self):
#         self.data = "Parent Data"  # 父类的属性
#
#
# class Child(Parent):
#     def __init__(self):
#         self.data = "Child Data"  # 子类无意中覆盖了父类的 data
#
#
# obj = Child()
# print(obj.data)  # 输出 "Child Data"（父类的 data 被覆盖）
# print(Parent().data)


# class Parent:
#     def __init__(self):
#         self.__data = "Parent Data"  # 名称修饰后变为 _Parent__data
#
#
# class Child(Parent):
#     def __init__(self):
#         super().__init__()  # 先调用父类初始化
#         self.__data = "Child Data"  # 名称修饰后变为 _Child__data
#
#
# obj = Child()
# print(obj._Parent__data)  # 输出 "Parent Data"（父类数据未被覆盖）
# print(obj._Child__data)  # 输出 "Child Data"
