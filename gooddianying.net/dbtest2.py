import pymysql

def main():
    db=pymysql.connect(host='127.0.0.1',user='root',password='cqmygpython2',db='test',port=3306)
    cur=db.cursor()
    sql='insert into fortable (id,name) values(001,"my_name")'
    cur.execute(sql)
    db.commit()
    cur.close()
    db.close()

main()
