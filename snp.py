import sys
import os

DEBUG = 0


########################### Reading Labels ##############################
labelfile= sys.argv[2]
f=open(labelfile)
trainlabels ={}
n=[]
ml=[]

n.append(0)
n.append(0)
l=f.readline()
while(l!=''):
	a=l.split()
	p=int(a[0])
	if p==0:
		trainlabels[int(a[1])] = -1
		p=-1
	else:

		trainlabels[int(a[1])] = p
	if p not in ml:
		ml.append(p)
	n[int(a[0])]+=1
	l=f.readline()
########################Reading Train data##################################
datafile = sys.argv[1]
f= open(datafile)
data =[]
i=-0

l=f.readline()
while(l!=''):
	a=l.split()
	l2=[]
	for j in range(0,len(a),1):
		l2.append(float(a[j]))
	data.append(l2)
	l=f.readline()

rows=len(data)
cols=len(data[0])
f.close()

if(DEBUG):
	for i in range(0,len(data),1):
		print(data[i])


if(DEBUG):
	for i in range(0,len(n),1):
		print(n[i])
	print(trainlabels)


###########################Calculating means#################################

m = []
means = []
testdata = []
temp = []
testdatarows = []

for i in range(0,cols,1):
	m.append(0)

for j in range(0,len(ml),1):
	for i in range(0,rows,1):
		if(trainlabels.get(i) != None):
			if(trainlabels.get(i) == ml[j]):
				for k in range(0,cols,1):
					m[k] += data[i][k]
		'''elif j<=0:
			testdata.append(data[i])
			testdatarows.append(trueclass[i])'''
	for p in range(0,cols,1):
		m[p] /=n[j]
		temp.append(m[p])
	means.append(temp)
	temp = []
	m=[]
	for i in range(0,cols,1):
		m.append(0)


############################Calculate variance#############################

variance = []

for j in range(0,len(ml),1):
	for i in range(0,rows,1):
		if(trainlabels.get(i) !=None and trainlabels.get(i) == ml[j]):
			for k in range(0,cols,1):
				#print('means =',means[j][k])
				m[k] += (data[i][k] - means[j][k])**2
	for p in range(0,cols,1):
		m[p] /=n[j]
		temp.append(m[p])
	variance.append(temp)
	temp = []
	m = []
	for i in range(0,cols,1):
		m.append(0)
##########################Calculating fscore ################################
f_m=[]
f_v=[]
f_score=[]
for i in range(len(means[0])):
	score=((means[0][i]-means[1][i])**2)/(variance[0][i]+variance[1][i])
	f_score.append(score)
	f_m.append(score)
f_score.sort()
f_score.reverse()
selected=[]

for i in f_score[:20]:
	for k in range(len(means[0])):
		if i==f_m[k]:
			selected.append(f_m.index(f_m[k]))
			f_m[k]=-1
selected.sort()
print selected
##################Selecting features using fscore values#############################
if(os.path.isfile(sys.argv[2]+".selected_data")):
	os.remove(sys.argv[2]+".select-ed_data")
name=sys.argv[2]+".selected_data"
op = open(name,"w")

for i in trainlabels.keys():
	op.write(str(trainlabels[i]))
	for k in selected:
		op.write(" "+str(k+1)+":"+str(data[i][k]))
	op.write("\n")

if(os.path.isfile("model_file")):
	os.remove("model_file")
	print("deleted")

os.system("./svm_learn "+name+" model_file")

#####################Reading Test_data##########################


datafile = sys.argv[3]
f= open(datafile)
testdata =[]
i=-0

l=f.readline()
while(l!=''):
        a=l.split()
        l2=[]
        for j in range(0,len(a),1):
                l2.append(float(a[j]))
        testdata.append(l2)
        l=f.readline()

rows=len(testdata)
cols=len(testdata[0])
f.close()

if(os.path.isfile("snp.test_data1")):
	os.remove("snp.test_data1")

name="snp.test_data1"

op=open(name,"w")
for i in range(rows):
	op.write("0")
	for k in selected:
		op.write(" "+str(k+1)+":"+str(testdata[i][k]))
	op.write("\n")

op.close()
########################SVM Classification###############################

if(os.path.isfile("output_file")):
	os.remove("output_file")

os.system("./svm_classify "+name+" model_file output_file")

name="output_file"
ch=open(name)

out="prediction_file"
ch1=open(out,"w")

lab =[]

l=ch.readline()
while(l!=''):

	if float(l)<0:
		lab.append(-1)
		ch1.write(str(-1)+"\n")
	else:
		lab.append(1)
		ch1.write(str(1)+"\n")
	l=ch.readline()

ch.close()
###########################ERROR CALCULATION#############################################


###############reading true labels############################
labelfile = "test_labels"
f=open(labelfile)
truelabels =[]
l = f.readline()
while(l!=''):
	a=l.split()
	truelabels.append(int(a[0]))
	l=f.readline()

##################reading predicted labels####################
labelfile = "prediction_file"
f=open(labelfile)
predictedlabels =[]
l = f.readline()
while(l!=''):
        a=l.split()
        predictedlabels.append(int(a[0]))
        l=f.readline()
print(len(truelabels))

TP=0
FP=0
TN=0
FN=0

for i in range(0,len(truelabels),1):
	print(i,"\t\t",truelabels[i],"\t\t",predictedlabels[i])
	if(predictedlabels[i] == truelabels[i]):
		if(predictedlabels[i] == 1):
			TP +=1
		else:
			TN +=1
	elif(predictedlabels[i] < truelabels[i]):
		FN +=1
	else:
		FP +=1

print(TP,TN,FN,FP)


Error =float(FP+FN)/float(TP+TN+FP+FN)
BER =(0.5)*((float(FN)/float(TP+FN))+(float(FP)/float(TN+FP)))
acc=(1-Error)*100

print("Error =",Error)
print("Accuracy=",acc)
print("Balanced Error Rate =",BER)






