from gensim.models import doc2vec
import pickle
import time
from collections import namedtuple
list_of_doc_ids = []
doc1 = (open('data.csv','rb')).readlines()
analyzedDocument = namedtuple('AnalyzedDocument', 'words tags')
data = {}
docs = []
ch = 0
print len(doc1)
for i in range(0,len(doc1)):
    elements = doc1[i].lower().split('|')
    qid = elements[0]
    words = list(set(elements[1].lower().split()))
    if ch<len(words):
        ch = len(words)
    tags = ['LABEL_'+str(qid)]
    data[int(qid)] = elements[2].lower().split(",")
    data[int(qid)][-1] = data[int(qid)][-1][:-1]
    #print data[int(qid)]
    #time.sleep(1)
    list_of_doc_ids.append('LABEL_'+str(qid))
    #print words
    #print tags
    docs.append(analyzedDocument(words, tags))

#print ch # maximum length of keyword

model100 = doc2vec.Doc2Vec(docs, size = 100, window = ch, min_count = 1, workers = 4)
print len(model100.docvecs)
print model100.docvecs.count
print model100.docvecs['LABEL_4'][:5] ##just need to iterate using all the "LABEL_"+qid to get the vectors of all labels ie questions
question_tilda_matrix = {} #the required matrix
for doc_id in list_of_doc_ids:
    id = int(doc_id[6:])
    question_tilda_matrix[id]=(model100.docvecs[doc_id])
print "rating_matrix"
print len(question_tilda_matrix)
print question_tilda_matrix[4][:5]

print (model100.most_similar(positive=['c']))
print model100.docvecs.most_similar(positive=['LABEL_4'])
pickle.dump(question_tilda_matrix,open("question_tilda_d100.pkl","wb"))
pickle.dump(data,open("data_full.pkl","wb"))


model150 = doc2vec.Doc2Vec(docs, size = 150, window = ch, min_count = 1, workers = 4)
print len(model150.docvecs)
question_tilda_matrix = {} #the required matrix
for doc_id in list_of_doc_ids:
    id = int(doc_id[6:])
    question_tilda_matrix[id]=(model150.docvecs[doc_id])
pickle.dump(question_tilda_matrix,open("question_tilda_d150.pkl","wb"))


model200 = doc2vec.Doc2Vec(docs, size = 200, window = ch, min_count = 1, workers = 4)
print len(model200.docvecs)
question_tilda_matrix = {} #the required matrix
for doc_id in list_of_doc_ids:
    id = int(doc_id[6:])
    question_tilda_matrix[id]=(model200.docvecs[doc_id])
pickle.dump(question_tilda_matrix,open("question_tilda_d200.pkl","wb"))
