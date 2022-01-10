#!/usr/bin/python3
# -*- coding: UTF-8 -*-


# use itertool.permutations, better than product
# permutations('ABCD', 2)
# AB AC AD BA BC BD CA CB CD DA DB DC


import sys
from os.path import dirname, basename, isfile, join
import inspect
import glob
import types
import copy
from typing import List, Any
import numpy

modules = glob.glob(join(dirname(__file__), "*.py"))
mods = [basename(f)[:-3] for f in modules if
		isfile(f) and not f.endswith('__init__.py') and not f.endswith('metadata.py') and not f.endswith(
			basename(__file__))]

print("loading module:")
for mod in mods:
	print("[load module] " + mod)
	try:
		module_obj = __import__(mod)
		globals()[mod] = module_obj
	except ImportError:
		sys.stderr.write("ERROR: missing python module: " + mod + "\n")
		sys.exit(1)

### version 1: overwrite funciton by same name
# calmod={}
# for mod in mods:
# 	for fun in dir(globals()[mod]):
# 		if not fun.startswith("cal_"):
# 			continue
# 		dtr=fun.replace("cal_","")
# 		dtr=dtr.lower()
# 		if len(dtr.split("_"))!=2:
# 			print("[IGNORE] {}.{}: can not identify cal_src_des".format(mod, fun))
# 			continue
# 		if dtr in calmod:
# 			print("[IGNORE] {}:  overwrite by  {}.{}".format(
# 				calmod[dtr],
# 				mod, fun
# 			))
# 		calmod[dtr]=mod+'.'+fun

# print(calmod)


### build funs
# print("\nbuild funs:")
# funs=[]   # [{f: fun point, name: "", src:"", des""}]
# for mod in mods:
# 	fstmp = [obj for name,obj in inspect.getmembers(sys.modules[mod])
#					  if (inspect.isfunction(obj))]
# 	for fun in fstmp:
# 		# print(fun)
# 		# print(type(fun))
# 		if type(fun)!=types.FunctionType:
# 			continue
# 		# print(type(fun))
# 		# print(mod+"."+fname)
# 		fname=fun.__name__
# 		if not fname.startswith("cal_"):
# 			print("[IGNORE] {0}.{1} is not meta function like cal_src_des".format(mod, fname))
# 			continue
# 		# print(fname)
# 		dtr=fname.replace("cal_","")
# 		dtr=dtr.lower()
# 		srcdes=dtr.split("_")
# 		# print(srcdes)
# 		if len(srcdes)!=2:
# 			print("[IGNORE] {}.{}: is not meta function like cal_src_des".format(mod, fname))
# 			continue
# 		# print(type(srcdes))
# 		# print(fun)
# 		# print(type(fun))
# 		funs.append({
# 			"f":fun, "name":mod+"."+fname,
# 			"src":srcdes[0], "des":srcdes[1]
# 			})
# 		# print("added 1: "+str(len(funs)))
# 		# print(funs)
# print("total funs: "+str(len(funs)))


# build fun (class version)
print("\nbuild funs:")
class Fun:
	def __init__(self, mod: str, f):
		self.fun = None
		self.src = ""
		self.des = ""
		self.name = ""
		if type(f) != types.FunctionType:
			print("[IGNORE] should init with function")
			return None
		self.fun = f
		fname = f.__name__
		if not fname.startswith("cal_"):
			print("[IGNORE] {0}.{1} is not meta function like cal_src_des".format(mod, fname))
			raise
		dtr = fname.replace("cal_", "")
		dtr = dtr.lower()
		srcdes = dtr.split("_")
		if len(srcdes) != 2:
			print("[IGNORE] {}.{}: is not meta function like cal_src_des".format(mod, fname))
			raise
		self.src = srcdes[0]
		self.des = srcdes[1]
		self.name = mod + "." + fname

	def dump(self):
		print("{} -> {}: {}".format(
			self.src,
			self.des,
			self.name
		))

funs: List[Fun] = []  # [{f: fun point, name: "", src:"", des""}]


def buildfuns():
	global funs
	for mod in mods:
		fstmp = [obj for name, obj in inspect.getmembers(sys.modules[mod])
				 if (inspect.isfunction(obj))]
		for ftmp in fstmp:
			if type(ftmp) != types.FunctionType:
				print("[IGNORE] {0}.{1} is not meta function".format(mod, ftmp))
				continue
			fname = ftmp.__name__
			if not fname.startswith("cal_"):
				print("[IGNORE] {0}.{1} is not meta function like cal_src_des".format(mod, fname))
				continue
			dtr = fname.replace("cal_", "")
			dtr = dtr.lower()
			srcdes = dtr.split("_")
			if len(srcdes) != 2:
				print("[IGNORE] {}.{}: is not meta function like cal_src_des".format(mod, fname))
				continue
			funs.append(Fun(mod, ftmp))


buildfuns()


### build calpath fast
print("\nbuild metapaths: ")

class Metapath:
	def __init__(self, fun: Fun):
		self.funs = []
		self.src = ""
		self.des = ""
		if not inspect.isfunction(fun.fun):
			print("[IGNORE] add NO fun: " + type(fun))
			return
		# print(type(fun))
		# print(fun.src)
		self.funs.append(fun)
		self.src = fun.src
		self.des = fun.des

	def addfun(self, fun: Fun):
		if not inspect.isfunction(fun.fun):
			print("[IGNORE] add NO fun: " + type(fun.fun))
			return
		self.funs.append(fun)
		self.des = fun.des

	def dump(self):
		s = ""
		s += self.src
		s += " -> "
		s += self.des
		s += ": "
		fnamelist=[]
		for i in self.funs:
			fnamelist.append(i.src + "_" + i.des)
		s+=', '.join(fnamelist)
		print(s)


# metapaths=[]   # [{path: [ fun, fun, ... ], src, des}]
metapaths: List[Metapath] = []



def funsbysrc(src):
	rtn = []
	# funs=[]   # [{f: fun point, name: "", src:"", des""}]
	for fun in funs:
		if fun.src == src:
			rtn.append(fun)
	return rtn



def metapathAppenddOneLevelAndSaveToMetaPaths(metapath: Metapath):
	# print("\nmetapathAppenddOneLevelAndSaveToMetaPaths:")
	for fun in funsbysrc(metapath.des):
		metapathtmp=copy.deepcopy(metapath)
		isnew=True
		for funhas in metapathtmp.funs:
			if funhas.des == fun.des:
				isnew=False
				break
		if isnew:
			metapathtmp.addfun(fun)
			metapaths.append(metapathtmp)

def genpathall(stepdepth:int):
	print("gen path max depth: {}".format(stepdepth))
	roundtmp=1
	print("gen depth: {}".format(roundtmp))
	roundtmp+=1
	for f in funs:
		metapaths.append(Metapath(f))
	# metapaths.append(Metapath(funs[0]))
	metapathscurrentlen=0
	while True:
		print("gen depth: {}".format(roundtmp))
		roundtmp+=1
		for m in copy.deepcopy(metapaths):
			metapathAppenddOneLevelAndSaveToMetaPaths(m)
		if len(metapaths)==metapathscurrentlen:
			break
		if len(metapaths[len(metapaths)-1].funs) >= stepdepth:
			break
		metapathscurrentlen=len(metapaths)
	print("total metapaths count: {}".format(len(metapaths)))


def genpathall_src(src, stepdepth:int):
	print("gen path max depth: {}".format(stepdepth))
	roundtmp=1
	print("gen depth: {}".format(roundtmp))
	roundtmp+=1
	for f in funs:
		if f.src==src:
			metapaths.append(Metapath(f))
	metapathscurrentlen=0
	while True:
		print("gen depth: {}".format(roundtmp))
		roundtmp+=1
		for m in copy.deepcopy(metapaths):
			metapathAppenddOneLevelAndSaveToMetaPaths(m)
		if len(metapaths)==metapathscurrentlen:
			break
		if len(metapaths[len(metapaths)-1].funs) >= stepdepth:
			break
		metapathscurrentlen=len(metapaths)
	print("total metapaths count: {}".format(len(metapaths)))



########## cal
def metapath_run(md, metapath:Metapath):
	md=copy.deepcopy(md)
	for f in metapath.funs:
		try:
			# print(">>>>>>")
			# print(md.d, end=" -> ")
			# print(type(p["f"]))
			# print(p["name"])
			md = f.fun(md)
		except Exception as e:
			md.history.append({f.name: str(e)})
			return md
		md.history.append({f.name: "ok"})
	return md



############# main
from metadata import Metadata

roundmax=3
try:
	roundmax=int(sys.argv[1])
except:
	pass

curruni=[]
for i in funs:
	curruni.append(i.src)
curruni=numpy.sort(numpy.unique(curruni)).tolist()


genpathall(roundmax)
totalbestmetadata=Metadata("uninit", 0)
currfriendlyary={}

for curr in curruni:
	print("\n\n-------------------- "+curr)
	print("\nfilter by {}->{}".format(curr,curr))
	metapathswillcal=[]
	for i in metapaths:
		if(i.src==curr and i.des==curr):
			metapathswillcal.append(i)
	print("total metapath: {}".format(len(metapathswillcal)))

	print("\ncal ({},1)".format(curr))
	bestmetadata=Metadata("uninit", 0)
	worstmetadata=Metadata("uninit", 2)
	x=Metadata(curr, 1)
	# y=""
	for m in metapathswillcal:
		y=metapath_run(x, m)
		if y.d>totalbestmetadata.d:
			print(y.d)
			totalbestmetadata=copy.deepcopy(y)
		if y.d>bestmetadata.d:
			print(y.d)
			bestmetadata=copy.deepcopy(y)
		if y.d<worstmetadata.d:
			worstmetadata=copy.deepcopy(y)

	if isinstance(worstmetadata, Metadata):
		print("\nworst answer:")
		print(worstmetadata.d, end="    ")
		print(worstmetadata.history)

	if isinstance(bestmetadata, Metadata):
		print("\nbest answer:")
		print(bestmetadata.d, end="    ")
		print(bestmetadata.history)
		# currfriendlyary[bestmetadata.t]
		for i in bestmetadata.history:
			firstkey=next(iter(i))
			# currEx.cal_hkd_usd
			# s=firstkey.replace("currEx.cal_", "")
			if "_" in firstkey:
				# print("process: "+firstkey)
				try:
					(prefix, src, des)=firstkey.split("_")
					currfriendlyary[src]=currfriendlyary.get(src, 0)+1
					currfriendlyary[des]=currfriendlyary.get(des, 0)+1
				except:
					# not format as prefix_src_des
					pass
				# for i in currfriendlyary:
				# 	print("\t", end="")
				# 	print(i+" "+str(currfriendlyary[i]))

print("\n------------ total best:")
if isinstance(totalbestmetadata, Metadata):
		print("\nbest answer:")
		print(totalbestmetadata.d, end="    ")
		print(totalbestmetadata.history)

currfriendlyary_sorted = sorted(currfriendlyary.items(), key=lambda kv: kv[1])
currfriendlyary_sorted.reverse()
print("\nmost frendly curr (in count): "+ next(iter(currfriendlyary_sorted[0])))
for (cur,cnt) in currfriendlyary_sorted:
	print("{} {}".format(cur, cnt))


# metapathswillcal[0].dump()
# x=Metadata("usd", 1)
# y=metapath_run(x, metapathswillcal[0])
# print(x.history)
# print(x.d)
#
# z=Metadata("usd", 2)
# print(x.history)
# print(x.d)

