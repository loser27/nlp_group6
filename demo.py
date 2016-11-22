# -*- coding: utf-8 -*-
"""
Created on Sun Nov 13 23:44:46 2016

@author: sumitk2k15
"""
import random
import pickle
import numpy
data_dict = pickle.load(open("data_full.pkl","rb"))
question_matrix = pickle.load(open("question_trained_vec.pkl","rb"))
tag_matrix = pickle.load(open("tag_trained_vec.pkl","rb"))
tag_set = pickle.load(open("tag_set.pkl", "rb"))
qid_test = pickle.load(open("qid_train.pkl", "rb"))

qid_to_test_index = random.choice([x for x in range(0,len(qid_test))])
qid_to_test = qid_test[qid_to_test_index]
data_question = pickle.load(open("data_question.pkl","rb"))

print "question id is"
print qid_to_test
print data_question[qid_to_test]
rating_tag_test = []
iter_tag = 0
for tag_vec in tag_matrix:
    cos_product = numpy.dot(question_matrix[qid_to_test_index],tag_vec)
    rating_tag_test.append((cos_product,tag_set[iter_tag]))
    iter_tag+=1
    data_dict[qid_to_test]

rating_tag_test = sorted(rating_tag_test,reverse=True)
rating_tag_test = [x[1] for x in rating_tag_test]

recall_at_1 = 0
if len(set(rating_tag_test[:30]).intersection(data_dict[qid_to_test])) > 0:
    recall_at_1 += 1
matched = list(set(rating_tag_test[:30]).intersection(set(data_dict[qid_to_test])))
print "no of correct matches : " +str(len(matched))
print "actual tags"
print data_dict[qid_to_test]
print "recmmd tags"
print rating_tag_test[:30]

print 'the correct recommendation is'
print matched
