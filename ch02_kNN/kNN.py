# -*- coding: utf-8 -*-

from numpy import *
import operator
from os import listdir

def createDataSet():
	group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
	labels = ['A','A','B','B']
	return group, labels

def classify0(inX, dataSet, labels, k):
	#读取dataSet的第一维度长度
	dataSetSize = dataSet.shape[0]  
	# tile函数，构造dataSetSize x 1个inX的copy。在行方向上重复dataSetSize次，列方向上重复1次
	diffMat = tile(inX ,(dataSetSize,1)) - dataSet

	sqDiffMat = diffMat**2
	#将矩阵的每一行向量的元素相加（按列相加）
	sqDistances= sqDiffMat.sum(axis = 1)
	distances = sqDistances**0.5

	#argsort函数返回数组distances值从小到大的索引值,数组的索引最小为0   
	sortedDisIndicies = distances.argsort()
	#dict，用于存储不同标签出现的次数
	classCount = {}

	for i in range(k):      #range(k)=[0,1,...,k-1]
		voteIlabel = labels[sortedDisIndicies[i]]
		#依次查询classCount中是否有该key，有则将取出value再+1，没有则返回添加该key并置value为0，再+1
		classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
	#根据classCount.iteritems()生成的tuple的第一个域（第二个元素）进行排序，reverse=True代表降序
	sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True) 
	return sortedClassCount[0][0]

def file2matrix(filename):
	fr = open(filename)
	arrayOLines = fr.readlines()
	numberOfLines  = len(arrayOLines)
	returnMat = zeros((numberOfLines,3)) 
	classLabelVector = []
	index = 0
	for line in arrayOLines:
		line = line.strip()                     #strip() 方法用于移除字符串头尾指定的字符（默认为空格）
		listFromLine = line.split('\t')         #split()通过指定分隔符对字符串进行切片 
		returnMat[index,:] = listFromLine[0:3]  
		classLabelVector.append(int(listFromLine[-1]))
		index += 1
	return returnMat,classLabelVector


#数据归一化处理  
#newvalue = (oldvalue - min)/(max - min)  
def autoNorm(dataSet):
	minVals = dataSet.min(0)
	maxVals = dataSet.max(0)
	ranges = maxVals - minVals
	normDataSet = zeros(shape(dataSet))
	#读取dataSet的第一维度长度(行数)
	m = dataSet.shape[0]
	#构造mX1个copy
	normDataSet = dataSet - tile(minVals, (m,1))
	#element wise divide   
	normDataSet = normDataSet/tile(ranges, (m,1))   
	return normDataSet, ranges, minVals

def datingClassTest():
	hoRatio = 0.10
	datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
	normMat, ranges, minVals = autoNorm(datingDataMat)
	m = normMat.shape[0]
	numTestVecs = int(m*hoRatio)
	errorCount = 0.0
	for i in range(numTestVecs):
		classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
		print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
		if (classifierResult != datingLabels[i]):
			errorCount += 1.0
	print "the total error rate is: %f"	%(errorCount/float(numTestVecs))

def classifyPerson():
	resultList = ['not at all','in small doses','in large doses']
	precentTats = float(raw_input("percentage of time spent playing video game?"))
	ffMiles = float(raw_input("frequent filer miles earned per year?"))
	iceCream = float(raw_input("liters of ice-cream cosumed per year?"))
	datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
	normMat, ranges, minVals = autoNorm(datingDataMat)
	inArr = array([ffMiles, precentTats, iceCream])
	#inArr need be normalized
	classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
	print "You will probably like this person: ",resultList[classifierResult-1]
