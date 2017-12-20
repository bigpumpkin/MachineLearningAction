import logRegres
from numpy import *
dataArr,labelMat = logRegres.loadDataSet()
weights = logRegres.stocGradAscent1(array(dataArr), labelMat)
logRegres.plotBestFit(mat(weights).transpose())
