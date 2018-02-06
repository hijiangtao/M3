#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# tripFlow 计算
# 
# python tripFlowCal.py -d /home/joe/Documents/git/fake -p /home/joe/Documents/git/fake -e 0.01 -m 40

import sys
import time
import logging
import getopt
from util.tripFlow.extractGridEdges import ExtractGridEdges
from util.tripFlow.dbscanTFIntersections import DBScanTFIntersections
from util.tripFlow.mergeClusterEdges import MergeClusterEdges

			
def processTask(x, eps, min_samples, stdindir, stdoutdir): 
	PROP = {
		'index': x, 
		'IDIRECTORY': stdindir, 
		'ODIRECTORY': stdoutdir
	}
	task = ExtractGridEdges(PROP)
	res = task.run()

	clusterofilename = ''
	while (True):
		clusterPROP = {
			'index': x, 
			'ODIRECTORY': stdoutdir,
			'res': res,
			'eps': eps,
			'min_samples': min_samples
		}
		print '''
===	Cluster Opts	===
index	= %d
stdindir	= %s
stdoutdir	= %s
eps		= %f
min_samples	= %d
===	Cluster Opts	===
''' % (x, stdindir, stdoutdir, eps, min_samples)

		clusterTask = DBScanTFIntersections(clusterPROP)
		noiseRate, clusterofilename = clusterTask.run()

		if noiseRate <= 0.5:
			break
		else:
			eps += 0.001

	mergePROP = {
		'index': x, 
		'IDIRECTORY': stdindir, 
		'ODIRECTORY': stdoutdir
	}
	mergeTask = MergeClusterEdges(mergePROP)
	mergeTask.run()


def usage():
	# /datahouse/zhtan/datasets/VIS-rawdata-region/
	print "python tripFlowCal.py -d /datasets -p /datasets -e 0.01 -m 10 -x 18"


def main(argv):
	try:
		argsArray = ["help", 'stdindir=', 'stdoutdir', "eps", "min_samples", "index="]
		opts, args = getopt.getopt(argv, "hd:p:e:m:x:", argsArray)
	except getopt.GetoptError as err:
		print str(err)
		usage()
		sys.exit(2)

	stdindir = '/home/tao.jiang/datasets/JingJinJi/records'
	stdoutdir = '/home/tao.jiang/datasets/JingJinJi/records'
	eps, min_samples = 0.01, 10
	x = 9

	for opt, arg in opts:
		if opt == '-h':
			usage()
			sys.exit()
		elif opt in ("-d", "--stdindir"):
			stdindir = arg
		elif opt in ('-p', '--stdoutdir'):
			stdoutdir = arg
		elif opt in ("-e", "--eps"):
			eps = float(arg)
		elif opt in ('-m', '--min_samples'):
			min_samples = int(arg)
		elif opt in ('-x', '--index'):
			x = int(arg)

	STARTTIME = time.time()
	print "Start approach at %s" % STARTTIME

	# print '''
	# ===	Cluster Opts	===
	# stdindir	= %s
	# stdoutdir	= %s
	# eps		= %f
	# min_samples	= %d
	# ===	Cluster Opts	===
	# ''' % (stdindir, stdoutdir, eps, min_samples)

	processTask(x, eps, min_samples, stdindir, stdoutdir)

	# @多进程运行程序 END
	ENDTIME = time.time()
	print "END TIME: %s" % ENDTIME
	print "Total minutes: %f" % ((ENDTIME-STARTTIME)/60.0)


if __name__ == '__main__':
	logging.basicConfig(filename='logger-tripflowcal.log', level=logging.DEBUG)
	main(sys.argv[1:])