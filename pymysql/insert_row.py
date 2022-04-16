import pymysql

con = pymysql.connect(host='localhost',
                        port=3306,
                        user='social',
                        passwd='socialpassword',
                        db='socialdb')

city = (9, 'Kiev', 2887000)

try:

    with con.cursor() as cur:
        
        cur.execute('INSERT INTO cities VALUES(%s, %s, %s)',
        (city[0], city[1], city[2]))
        con.commit()

        print('new city inserted')

finally:
    
    con.close()