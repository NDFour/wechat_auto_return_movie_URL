import MySQLdb

def to_mysql():
    conn=MySQLdb.Connection(host='127.0.0.1',port=3306,user='root',passwd='cqmygpython2',db='test',charset='utf8')
    cursor=conn.cursor()
    sql_insert="insert into test2 (name) values('hello')"
    cursor.execute(sql_insert)
    conn.commit()

    cursor.close()
    conn.close()

def main():
    to_mysql()

main()
