import sys

###reading true labels###
labelfile = sys.argv[1]
f=open(labelfile)
truelabels =[]
l = f.readline()
while(l!=''):
	a=l.split()
	truelabels.append(int(a[0]))
	l=f.readline()

###reading predicted labels###
labelfile = sys.argv[2]
f=open(labelfile)
predictedlabels =[]
l = f.readline()
while(l!=''):
        a=l.split()
        predictedlabels.append(int(a[0]))
        l=f.readline()
print(len(truelabels))
###identify true/false positives/negtives###
TP=0
FP=0
TN=0
FN=0
print("datapoint","truelabels","predictedlabels")
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


###calculation###

Error =float(FP+FN)/float(TP+TN+FP+FN)

BER =(0.5)*((float(FN)/float(TP+FN))+(float(FP)/float(TN+FP)))

#Precision = TP /(TP+FP)

#Recall = TN/(TN+FN)

acc=(1-Error)*100

print("Error =",Error)
print("Accuracy=",acc)
print("Balanced Error Rate =",BER)
#print("Precision =",Precision)
#print("Recall =",Recall)



