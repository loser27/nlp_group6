try:
    import numpy
    import pickle
    import timeit

except:
    print "This implementation requires the numpy module."
    exit(0)

###############################################################################

"""
@INPUT:
    R     : a matrix to be factorized, dimension N x M
    P     : an initial matrix of dimension N x K
    Q     : an initial matrix of dimension M x K
    K     : the number of latent features
    steps : the maximum number of steps to perform the optimisation
    alpha : the learning rate
    beta  : the regularization parameter
@OUTPUT:
    the final matrices P and Q
"""
def matrix_factorization(R, P,P_tilda, Q, K, steps=4, alpha=0.05, beta=0.0001, gamma=0.0002):
    Q = Q.T
    for step in xrange(steps):
        start = timeit.default_timer()

        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k]-gamma*(P[i][k]-P_tilda[i][k]))
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = numpy.dot(P,Q)
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * ( pow(P[i][k],2) + pow(Q[k][j],2) )
        if e < 0.001:
            break
        stop = timeit.default_timer()
        print "iteration_"+str(step) + str(stop - start)
    return P, Q.T

###############################################################################

def test_recall(question_train_matrix,tag_matrix):
    question_test_matrix = pickle.load(open("q_tilda_test_d100.pkl", "rb"))
    data_dict = pickle.load(open("data_full.pkl", "rb"))
    tag_set = pickle.load(open("tag_set.pkl", "rb"))
    qid_test = pickle.load(open("qid_test.pkl", "rb"))

    rating_tag_test = {}
    iter = 0
    for q_test_vec in question_test_matrix:
        rating_tag_test[qid_test[iter]] = []
        iter_tag = 0
        for tag_vec in tag_matrix:
            cos_product = numpy.dot(q_test_vec,tag_vec)
            rating_tag_test[qid_test[iter]].append((cos_product,tag_set[iter_tag]))
            iter_tag+=1
        iter += 1
    print "rating tag matrix"
    print len(rating_tag_test.keys())
    print len(rating_tag_test[qid_test[0]])
    for qid in rating_tag_test:
        rating_tag_test[qid] = sorted(rating_tag_test[qid],reverse=True)
        rating_tag_test[qid] = [x[1] for x in rating_tag_test[qid]]

    recall_at_1 = 0
    for qid in qid_test:
        if len(set(rating_tag_test[qid][:30]).intersection(data_dict[qid])) > 0:
            recall_at_1 += 1
    print "for 30 recmmd recall at 1 : " +str(recall_at_1)

    recall_at_1 = 0
    for qid in qid_test:
        if len(set(rating_tag_test[qid][:20]).intersection(data_dict[qid])) > 0:
            recall_at_1 += 1
    print "for 20 recmmd recall at 1 : " +str(recall_at_1)

    recall_at_1 = 0
    for qid in qid_test:
        if len(set(rating_tag_test[qid][:15]).intersection(data_dict[qid])) > 0:
            recall_at_1 += 1
    print "for 15 recmmd recall at 1 : " +str(recall_at_1)

    recall_at_1 = 0
    for qid in qid_test:
        if len(set(rating_tag_test[qid][:10]).intersection(data_dict[qid])) > 0:
            recall_at_1 += 1
    print "for 10 recmmd recall at 1 : " + str(recall_at_1)

    len_qid = 0.75*len(qid_test)
    recall_at_1 = 0
    for qid in qid_test:
        if len(set(rating_tag_test[qid][:5]).intersection(data_dict[qid])) > 0:
            recall_at_1 += 1
    print "for 5 recmmd recall at 1 : " + str(recall_at_1)
    pool_of_value = [1,3,5,10]
    for k in pool_of_value:
        recall = 0.0
        precision = 0.0
        recall_temp = 0.0
        for qid in qid_test:
            matched_tag = len(set(rating_tag_test[qid][:k]).intersection(data_dict[qid]))
            recall += matched_tag/float((len(data_dict[qid])))
            #recall_temp += len(data_dict[qid])
            precision += (matched_tag/float(k))
        precision = precision/float(len(qid_test))
        recall = recall/len_qid
        print 'recall at '+str(k)
        print recall
        print 'precision at '+str(k)
        print precision


###########################################################
if __name__ == "__main__":
    R = [
         [5,3,0,1],
         [4,0,0,1],
         [1,1,0,5],
         [1,0,0,4],
         [0,1,5,4],
        ]

    R = numpy.array(R)

    R = pickle.load(open("rating_matrix.pkl","rb"))
    R = numpy.array(R)

    N = len(R)
    M = len(R[0])
    print N
    print M
    K = 100
    
    P_tilda = [
                [2,1],
                [0,2],
                [3,3],
                [1,2],
                [2,1]
                ]

    P_tilda = pickle.load(open("q_tilda_train_d100.pkl","rb"))
    P_tilda = numpy.array(P_tilda)
    print len(P_tilda)
    print len(P_tilda[0])

    P = numpy.random.rand(N,K)
    Q = numpy.random.rand(M,K)
    p1 = P
    q1 = Q
    start = timeit.default_timer()

    #nP, nQ = matrix_factorization(R, P,P_tilda, Q, K)
    #pickle.dump(nP,open("question_trained_vec.pkl","wb"))
    #pickle.dump(nQ,open("tag_trained_vec.pkl","wb"))
    nP = pickle.load(open("question_trained_vec.pkl","rb"))
    nQ = pickle.load(open("tag_trained_vec.pkl","rb"))
    print len(nQ)
    print len(nQ[1])
    nR = numpy.dot(nP, nQ.T)
    print nP
    print nQ
    print nR
    test_recall(nP,nQ)

    #nP, nQ = matrix_factorization(R, p1,P_tilda, q1, K,4,0.05,0.0001,0)
    #test_recall(nP, nQ)

    stop = timeit.default_timer()
    print "total_time" + str(stop - start)



