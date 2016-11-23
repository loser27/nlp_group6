import csv
import sqlite3 as sq
writ = csv.writer(open('../Dumps/fnl_data.csv', 'w'), delimiter='|')
with sq.connect('''../Dumps/db.db''') as con:
    cur = con.cursor()
    cur.execute('''SELECT qid from q2keyw GROUP BY qid''')
    qids = [a[0] for a in cur.fetchall()]

    for i, qid in enumerate(qids):
        cur.execute(
            '''SELECT keyw FROM (SELECT * from q2keyw  where qid = %d) NATURAL JOIN dictionary WHERE df < 2400 GROUP BY keyw''' % qid)
        keywords = ' '.join([a[0] for a in cur.fetchall()])

        cur.execute('''SELECT tag  from q2tag  where qid = %d''' % qid)
        tags = ','.join([a[0] for a in cur.fetchall()])
        print([i, qid, keywords, tags])
        writ.writerow([qid, keywords, tags])
writ.close()