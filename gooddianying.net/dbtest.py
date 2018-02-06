import MySQLdb

def main():
    conn=MySQLdb.Connection(host='127.0.0.1',port=3306,user='root',passwd='cqmygpython2',db='test',charset='utf8')
    cursor=conn.cursor()

    try:
        sql_insert="insert into fortable (id,name) values(1001,'my_name')"
        print(sql_dinsert)
        cursor.execute(sql_insert)
        conn.commit()
        print('-> SAVE info of %s to MySQL success !!'%i[0])
    except:
        conn.rollback()
        print('-> SAVE info of %s to MySQL failed !!'%i[0])

    cursor.close()
    conn.close()

main()
