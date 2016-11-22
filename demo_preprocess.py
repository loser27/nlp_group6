import pickle
doc1 = (open('data.csv','rb')).readlines()
data = {}
docs = []
ch = 0
print len(doc1)
for i in range(0,len(doc1)):
    elements = doc1[i].lower().split('|')
    qid = elements[0]
    words = list(set(elements[1].lower().split()))
    data[int(qid)] = (elements[1].lower(),elements[2])

pickle.dump(data,open("data_question.pkl","wb"))
