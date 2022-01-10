#!/usr/bin/python3
# -*- coding: UTF-8 -*-

class Metadata:
	def __init__(self, t, d):
		self.t=t
		self.d=d
		self.history=[{"init": "ok"}]    # [ {"mod.fun": "cal log msg"} ]
		self.t0=t
		self.d0=d


# import Exception
# from Exception import *

# try:
# 	1/0
# except Expression as e:
# 	print(e)


# try:
#     1/0
# except Exception as e: # work on python 3.x
#     print('Failed to upload to ftp: '+ str(e))