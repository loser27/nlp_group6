import random
import pickle
question_tilda_dict = pickle.load(open("question_tilda_d100.pkl","rb"))
data_dict = pickle.load(open("data_full.pkl","rb"))
tag_set = []
for id in data_dict:
    for tag in data_dict[id]:
        if tag not in tag_set:
            tag_set.append(tag)
print len(tag_set)
print tag_set

qid_set = set(data_dict.keys())
print len(qid_set)
testing_set = random.sample(qid_set,4768)
training_set = qid_set.difference(testing_set)
training_set = sorted(list(training_set))
testing_set = sorted(list(testing_set))
question_tilda_train_matrix = []
question_tilda_test_matrix = []
rating_matrix = []
for id in training_set:
    rating_matrix.append([1 if tag in data_dict[id] else 0 for tag in tag_set])
    question_tilda_train_matrix.append(question_tilda_dict[id])

for id in testing_set:
    question_tilda_test_matrix.append(question_tilda_dict[id])
pickle.dump(question_tilda_train_matrix,open("q_tilda_train_d100.pkl","wb"))
pickle.dump(question_tilda_test_matrix,open("q_tilda_test_d100.pkl","wb"))
pickle.dump(testing_set,open("qid_test.pkl","wb"))
pickle.dump(training_set,open("qid_train.pkl","wb"))
pickle.dump(rating_matrix,open("rating_matrix.pkl","wb"))
pickle.dump(tag_set,open("tag_set.pkl","wb"))
