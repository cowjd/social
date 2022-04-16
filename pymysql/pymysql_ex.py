import pymysql
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='social',
                       passwd='socialpassword',
                       db='socialdb')
cur = conn.cursor()

query = '''
select * from news_articles;
'''

n_rows = cur.execute(query)
print(n_rows)

results = list(cur.fetchall())
print(results)

conn.close()