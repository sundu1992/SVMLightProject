import sys
import os
import random


		
labelfile= sys.argv[2]
f=open(labelfile)
trueclass =[]
l=f.readline()
while(l!=''):
	a=l.split()
	if(int(a[0])==0):
		trueclass.append(-1)
	else:
		trueclass.append(int(a[0]))
	l=f.readline()


##choose 90% data
nums=[x for x in range(len(trueclass))]
random.shuffle(nums)

k = len(trueclass)*0.90
if(os.path.isfile("randomclass")):
	os.remove("randomclass")
op = open("randomclass","w")


for i in range(int(k)):
	if(trueclass[nums[i]]==-1):
		op.write("0 "+str(nums[i])+"\n")	
	else:
		op.write(str(trueclass[nums[i]])+" "+str(nums[i])+"\n")


op.close()
'''		
### Read Labels ###
labelfile= "randomclass"
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
	trainlabels[int(a[1])]=p
	if p not in ml:
		ml.append(p)
         #print(n)
	n[int(a[0])]+=1
	l=f.readline()
#print trainlabels , "trainn"
'''

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
rm=[]
for i in range(int(k),rows,1):
	rm.append(nums[i])

#print(rm)
		

#print(trueclass)
if(os.path.isfile("check2")):
	os.remove("check2")

fi="check2"
op=open(fi,"w")

for k in rm:

	op.write(str(trueclass[k]))
	op.write("\n")
op.close()



if(os.path.isfile("snp.test_data")):
	os.remove("snp.test_data")

		
name="snp.test_data"
op = open(name,"w")

for k in rm:
	#print(data[i][k])
	#op.write(str(0))
	for j in range(cols):
		op.write(str(data[k][j])+" ")
	op.write("\n")
op.close()
