import pickle
import re
from functools import partial
from math import log
from multiprocessing.pool import Pool
from sqlite3 import connect
from statistics import stdev, mean

from enchant import Dict
from nltk import word_tokenize, pos_tag, WordNetLemmatizer, BigramTagger, DefaultTagger, \
    RegexpTagger, TrigramTagger, UnigramTagger
from nltk.corpus import stopwords, brown
from nltk.corpus import wordnet


def prepare_toolset():
    toolset = {}
    patterns = [(r'^[\.1-9]+$', 'NUM'),
                (r'^[^a-zA-Z]+$', '.'),
                (r'^[^a-zA-Z]*[a-zA-Z]+[-\'][a-zA-Z]+[^a-zA-Z]*$', 'NOUN'),
                (r'^.*[a-zA-Z]+[^-a-zA-Z]+[a-zA-Z]+.*$', '.')]
    train_set = brown.tagged_sents(categories='learned', tagset='universal') + brown.tagged_sents(categories='news',
                                                                                                  tagset='universal') + brown.tagged_sents(
        categories='reviews', tagset='universal')
    utgr = UnigramTagger(train=train_set, backoff=DefaultTagger('NN'))
    btgr = BigramTagger(train=train_set, backoff=utgr)
    ttgr = TrigramTagger(train=train_set, backoff=btgr)
    toolset['tgr'] = RegexpTagger(regexps=patterns, backoff=ttgr)
    toolset['sw'] = stopwords.words('english')
    toolset['lr'] = WordNetLemmatizer()
    toolset['wntg'] = {'NOUN': wordnet.NOUN, 'VERB': wordnet.VERB, 'ADJ': wordnet.ADJ, 'ADV': wordnet.ADV,
                       'X': wordnet.NOUN}
    print('Tools Ready')
    return toolset


def bow_creator(toolset: dict, inp):
    tagged_words = toolset['tgr'].tag(word_tokenize(inp[1]))
    keywords = [(toolset['lr'].lemmatize(re.sub("[ \t\r\n]+", " ", re.sub("[^a-zA-Z]", ' ', w)).strip().lower(),
                                         toolset['wntg'][t]), t) for w, t in tagged_words if
                t in ['NOUN', 'VERB', 'ADJ', 'ADV', 'X'] and w not in toolset['sw']]
    keywords_frequency = dict((keyw, keywords.count(keyw)) for keyw in keywords)
    return tuple((inp[0], keywords_frequency))


def create_tables():
    with connect('../Dumps/db.db') as con:
        cur = con.cursor()
        cur.execute('''DROP TABLE IF EXISTS dictionary''')
        cur.execute('''DROP TABLE IF EXISTS q2keyw''')
        cur.execute('''DROP TABLE IF EXISTS q2tag''')
        cur.execute('''CREATE TABLE IF NOT EXISTS dictionary(
            type TEXT NOT NULL,
            pos TEXT NOT NULL,
            df INTEGER NOT NULL,
            ttf INTEGER NOT NULL,
            code INTEGER DEFAULT 0,
            PRIMARY KEY(type, pos));''')
        cur.execute('''CREATE TABLE IF  NOT EXISTS q2keyw(
            qid INTEGER NOT NULL,
            keyw TEXT NOT NULL,
            pos TEXT NOT NULL,
            tf INTEGER NOT NULL,
            tfidf REAL DEFAULT 0,
            PRIMARY KEY(qid, keyw, pos),
            FOREIGN KEY(keyw, pos) REFERENCES dictionary(type, pos));''')
        cur.execute('''CREATE TABLE IF NOT EXISTS q2tag(
            qid INTEGER NOT NULL,
            tag TEXT NOT NULL,
            PRIMARY KEY(qid, tag));''')


def q2keyw(sow_dict: dict):
    l = []
    with connect('../Dumps/db.db') as con:
        cur = con.cursor()
        cur.execute('''SELECT type, pos, df FROM dictionary ''')
        df = dict(((data[0], data[1]),data[2]) for data in cur.fetchall())
    for q in sow_dict.keys():
        for w, t in sow_dict[q].keys():
            l.append((q, w, t, sow_dict[q][(w, t)], sow_dict[q][(w, t)] * log(len(sow_dict.keys()) / df[(w, t)])))

    with connect('../Dumps/db.db') as con:
        cur = con.cursor()
        cur.executemany('''INSERT INTO q2keyw(qid, keyw, pos, tf, tfidf) VALUES(?, ?, ?, ?, ?);''', l)
    print('Question to Keyword Mapping Created')


def q2tag(tags: dict):
    l = []
    for q in tags.keys():
        for t in set(tags[q]):
            l.append((q, t))
    with connect('../Dumps/db.db') as con:
        cur = con.cursor()
        cur.executemany('''INSERT INTO q2tag(qid, tag) VALUES(?, ?);''', l)
    print('Question to Tag Mapping Created')


def add_to_dictionary(sow_dict: dict):
    df = {}
    ttf = {}
    for q in sow_dict.keys():
        for w, t in sow_dict[q].keys():
            if (w, t) in df:
                df[(w, t)] += 1
                ttf[(w, t)] += sow_dict[q][(w, t)]
            else:
                df[(w, t)] = 1
                ttf[(w, t)] = sow_dict[q][(w, t)]

    with connect('../Dumps/db.db') as con:
        cur = con.cursor()
        cur.executemany('''INSERT INTO dictionary(type, pos, df, ttf) VALUES(?, ?, ?, ?);''',
                        [(w, t, df[(w, t)], ttf[(w, t)]) for w, t in df.keys()])
        cur.execute('''SELECT type, pos FROM dictionary ORDER BY ttf desc, df desc, length(type)''')
        data = cur.fetchall()
        data = [(i + 1, dat[0], dat[1]) for i, dat in enumerate(data)]
        cur.executemany('''UPDATE dictionary SET  code = ? WHERE type = ?  and pos = ?;''', data)
    print('Dictionay Created')


def spell_corrections(bow_dict):
    speller = Dict('en_US')
    vocab = set()
    incorrect = set()
    corrected = dict()
    [vocab.add(w) for q in bow_dict.keys() for w in bow_dict[q]]
    [incorrect.add(w) for w in vocab if not speller.check(w)]
    print('''Corrections Started''')
    for w in incorrect:
        corrections = speller.suggest(w)
        if len(corrections) > 0:
            corrected[w] = corrections[0]
    with connect('../Dumps/db.db')  as con:
        cur = con.cursor()
        cur.execute('DROP TABLE IF EXISTS spell_corrections')
        cur.execute('''CREATE TABLE IF NOT EXISTS spell_corrections(
            original TEXT NOT NULL,
            corrected TEXT NOT NULL);''')
        cur.executemany('''INSERT INTO spell_corrections(original, corrected) VALUES(? , ?)''',
                        [(w, corrected[w]) for w in corrected.keys()])


def get_stats():
    a = [len(bow) for bow in bow_list]
    v = set()
    [v.add(stemmer.stem(bow)) for bow_l in bow_list for bow in bow_l]
    print(len(v))
    b = {}
    for i, j in enumerate(a):
        if j in b:
            b[j] += 1
        else:
            b[j] = 1
    b_x, b_y = [], []
    b_x = list(b.keys())
    for k in b_x:
        b_y.append(b[k])

    # plot(b_x, b_y)
    # show()

    for y in range(len(b_y) - 1, 0, -1):
        b_y[y - 1] += b_y[y]

    # plot(b_x, b_y)
    # show()

    print(obj[a.index(max(a))]['body'], mean(a), stdev(a))


create_tables()
obj = pickle.load(open("../Dumps/dataset.pickle", "rb"))
print(len(obj), obj[0:10])
bodies = dict((int(ob['Id']), ob['body']) for ob in obj)
print(bodies[70272])
tags = dict((int(ob['Id']), ob['tags']) for ob in obj)
print(tags[70272])

tools = prepare_toolset()
with Pool() as p:
    bow_dict = dict(p.map(partial(bow_creator, tools), [(i, bodies[i]) for i in bodies.keys()]))
print(bow_dict[70272])


add_to_dictionary(bow_dict)
q2keyw(bow_dict)
q2tag(tags)
