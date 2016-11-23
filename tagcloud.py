from sqlite3 import connect
from matplotlib.pyplot import figure, imshow, axis, show
from wordcloud import WordCloud

with connect('../Dumps/db.db') as con:
    cur = con.cursor()
    cur.execute('''SELECT type, ttf FROM dictionary GROUP BY type ORDER BY ttf DESC LIMIT 400''')
    data = cur.fetchall()
    counts = [(d[0], d[1]) for d in data]
    wc = WordCloud().generate_from_frequencies(counts)
    figure(figsize=(15, 10))
    imshow(wc)
    axis('off')
    show()

    cur.execute('''SELECT type, ttf FROM dictionary WHERE df < 2400 GROUP BY type ORDER BY ttf DESC LIMIT 400''')
    data = cur.fetchall()
    counts = [(d[0], d[1]) for d in data]
    wc = WordCloud().generate_from_frequencies(counts)
    figure(figsize=(15, 10))
    imshow(wc)
    axis('off')
    show()

    cur.execute(
        '''SELECT type, ttf FROM dictionary WHERE df < 2400 AND pos = 'NOUN' ORDER BY ttf DESC LIMIT 400''')
    data = cur.fetchall()
    counts = [(d[0], d[1]) for d in data]
    wc = WordCloud().generate_from_frequencies(counts)
    figure(figsize=(15, 10))
    imshow(wc)
    axis('off')
    show()

    cur.execute(
        '''SELECT type, ttf FROM dictionary WHERE df < 2400 AND pos = 'VERB' ORDER BY ttf DESC LIMIT 400''')
    data = cur.fetchall()
    counts = [(d[0], d[1]) for d in data]
    wc = WordCloud().generate_from_frequencies(counts)
    figure(figsize=(15, 10))
    imshow(wc)
    axis('off')
    show()

    cur.execute(
        '''SELECT type, ttf FROM dictionary WHERE df < 2400 AND pos = 'ADJ' ORDER BY ttf DESC LIMIT 400''')
    data = cur.fetchall()
    counts = [(d[0], d[1]) for d in data]
    wc = WordCloud().generate_from_frequencies(counts)
    figure(figsize=(15, 10))
    imshow(wc)
    axis('off')
    show()

    cur.execute(
        '''SELECT type, ttf FROM dictionary WHERE df < 2400 AND pos = 'ADV' ORDER BY ttf DESC LIMIT 400''')
    data = cur.fetchall()
    counts = [(d[0], d[1]) for d in data]
    wc = WordCloud().generate_from_frequencies(counts)
    figure(figsize=(15,10))
    imshow(wc)
    axis('off')
    show()
