import logRegres
from numpy import *
dataArr,labelMat = logRegres.loadDataSet()
weights = logRegres.stocGradAscent0(array(dataArr), labelMat)
logRegres.plotBestFit(mat(weights).transpose())
