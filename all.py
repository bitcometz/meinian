import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import argparse



def process1(allvalue):

	i = 1
	vid=allvalue[['vid']]
	value_list=[]
	(row_n,column_n) = allvalue.shape
	while i<column_n:
		a = allvalue.iloc[:,i:i+1]
		new=pd.concat([vid,a],axis=1)
		value_list.append(new)
		i += 1
	
	return value_list
	
def process2(feature,value):
	value = value.dropna()
	train = pd.merge(feature,value,on=['vid'])
	predictors = train.iloc[:,1:-1]
	target=train.iloc[:,-1]
	 
	return predictors,target

def cal_error(predictors,target):
	# train(x) and test(y)
	feature_x,feature_y,value_x,value_y = train_test_split(predictors, target,test_size = 0.25, random_state = 0)
	
	rfr=RandomForestRegressor()
	rfr.fit(feature_x,value_x)
	pred_y=rfr.predict(feature_y)
	list_y = value_y.tolist()
	
	#error
	e_sum = 0
	import math
	length=len(pred_y)
	print('length:{}'.format(length))
	for i in range(length):
		#print pred_y[i]
		#print list_y[i]
		e_sum += (math.log(pred_y[i]+1)-math.log(list_y[i]+1))**2
	error = e_sum/length

	return error
	
def idresult(feature,predictors,target,test_csv):	
	rfr1=RandomForestRegressor()
	rfr1.fit(predictors,target)

	#test
	if test_csv != None:
		
		test = pd.read_csv(test_csv)
		test1=test[['vid']]
		test_list=test1['vid'].tolist()
		test_data=pd.merge(test1,feature,on=['vid'])
		test_predictors=test_data.iloc[:,1:]
		print test_data
		print "=="
		print test_predictors
		test_name="value1"
		value_test=rfr1.predict(test_predictors)
		for i in range(len(value_test)):
			value_test[i] =  '%.3f' % value_test[i]
		
		dataset=list(zip(test_list,value_test))
		testdf=pd.DataFrame(data=dataset,columns=['vid',test_name])
	
	return testdf

def filter_none(x):
    try:
        y = float(x)
    except:
        y = None
    return y

		
def main():
	parser = argparse.ArgumentParser(description='Manual to this script')
	parser.add_argument('--feature', required=True,type=str, default=None)
	parser.add_argument('--value', required=True,type=str, default=None)
	parser.add_argument('--test', type=str, default=None)
	parser.add_argument('--o', type=str, default=None)

	args = parser.parse_args()
	feature_csv = args.feature
	value_csv = args.value
	test_csv = args.test
	out_file = args.o
    
	feature = pd.read_csv(feature_csv)
	allvalue = pd.read_csv(value_csv)

	for column in feature.columns:
		if column != 'vid':
			feature[column] = feature[column].apply(filter_none)
			feature[column].fillna(feature[column].mean(), inplace=True)

	value_list = process1(allvalue)

	testdf_list=[]
	error_list=[]

	for value in value_list:
		(predictors,target)=process2(feature,value)
		error_list.append(cal_error(predictors,target))
		if test_csv:
			testdf=idresult(feature,predictors,target,test_csv)
			testdf_list.append(testdf)
	
	for error in error_list:
		print error
	print "average:"+str(float(sum(error_list))/len(error_list))

	if test_csv:
		test = pd.read_csv(test_csv)
		alldf = test[['vid']]
	
		for df in testdf_list:
			alldf=pd.merge(alldf,df,on=['vid'])

		alldf.to_csv(out_file+".csv",index=False,header=False)

if __name__ == '__main__':
	main()



