import sys
import os

DEBUG = 0


### Read Labels ###
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
#print trainlabels , "trainn"


#l=list(set(trainlabels.values()))
#print("ml=",ml)

'''print('--------------------')
print(n[0])
print(n[1])'''

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
'''
###true class###

labelfile= sys.argv[3]
f=open(labelfile)
trueclass =[]
l=f.readline()
while(l!=''):
	a=l.split()
	trueclass.append(int(a[0]))
	l=f.readline()
'''


###calculate means###

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

#print('testdata= ',testdata)
#print('testdata #=',testdatarows)
print('means =',len(means))
'''
file=open(datafile+'testfile','wb+')
for i in range(0,len(testdatarows),1):
	file.write('{}\n'.format(testdatarows[i]))

file.close()'''
### calculate variance###

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
#print('variance =',variance)


f_m=[]
f_v=[]
f_score=[]
for i in range(len(means[0])):
	#f_m.append((means[0][i]-means[1][i])**2)
	#f_v.append(variance[0][i]+variance[1][i])
	score=((means[0][i]-means[1][i])**2)/(variance[0][i]+variance[1][i])
	f_score.append(score)
	f_m.append(score)
#print(f_m)
#print f_v
#print f_score

#f_m=f_score
#print f_m,"before"
f_score.sort()
f_score.reverse()
#print f_m,"after"

#print f_score[:15]
selected=[]

for i in f_score[:20]:
	for k in range(len(means[0])):
		#print "test",f_m[k],i
		if i==f_m[k]:
			#print "test",f_m[k],i
			selected.append(f_m.index(f_m[k]))
			f_m[k]=-1
selected.sort()
print selected
###############################################
if(os.path.isfile(sys.argv[2]+".selected_data")):
	os.remove(sys.argv[2]+".selected_data")
name=sys.argv[2]+".selected_data"
op = open(name,"w")

for i in trainlabels.keys():
	op.write(str(trainlabels[i]))
	for k in selected:
		#print(data[i][k])

		op.write(" "+str(k+1)+":"+str(data[i][k]))
	op.write("\n")
        #os.system("./train -s 2 -c 1 -B 1 datasets_v1/ionosphere/foo.txt datasets_v1/ionosphere/modelfile.txt")
        #os.system("./predict datasets_v1/ionosphere/testdat.txt datasets_v1/ionosphere/modelfile.txt datasets_v1/ionosphere/outputfile%d.txt"%final_set)

if(os.path.isfile("model_file")):
	os.remove("model_file")	
	print("deleted")
	
os.system("./svm_learn "+name+" model_file")

#os.system("./train -s 2 -c 1 -B 1 "+name+" model_file")
#os.system("./predict datasets_v1/ionosphere/testdat.txt datasets_v1/ionosphere/modelfile.txt datasets_v1/ionosphere/outputfile%d.txt"%final_set)

###############################################


datafile = "snp.test_data"
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

#print i
############################

if(os.path.isfile("output_file")):
	os.remove("output_file")

#os.system("./predict "+name+" model_file output_file")

os.system("./svm_classify "+name+" model_file output_file")

name="output_file"
ch=open(name)

out="check1"
ch1=open(out,"w")

lab =[]
#i=-0

l=ch.readline()
while(l!=''):
	
	if float(l)<0:
		lab.append(-1)
		ch1.write(str(-1)+"\n")
	else:
		lab.append(1)
		ch1.write(str(1)+"\n")
	l=ch.readline()

#rows=len(data)
#cols=len(data[0])
ch.close()
#print lab


