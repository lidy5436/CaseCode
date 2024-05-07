import mysql.connector


# 连接数据库
def connectToDatabase(host, user, password, database):
    try:
        connect = mysql.connector.connect(host=host, user=user, password=password, database=database)
        print("数据库连接成功")
        return connect
    except mysql.connector.Error as error:
        print("连接数据库错误:{}".format(error))
        return None


# 插入数据
def insertData(connect, tableName, columns, data):
    cursor = connect.cursor()
    try:
        # 构建插入语句
        sql = "INSERT INTO {}({}) VALUES ({})".format(
            tableName,
            ','.join(columns),
            ','.join(['%s'] * len(columns))
        )
        cursor.executemany(sql, data)
        connect.commit()
        print("数据插入成功")
    except mysql.connector.Error as error:
        connect.rollback()
        print("数据插入失败:{}".format(error))
    finally:
        cursor.close()


# 查询表数据
def queryData(connect, tableName, columns=None):
    cursor = connect.cursor()
    try:
        if columns:
            # 查询指定列
            sql = "SELECT {} FROM {}".format(','.join(columns), tableName)
        else:
            sql = "SELECT * FROM {}".format(tableName)
        cursor.execute(sql)
        rows = cursor.fetchall()
        return rows
    except mysql.connector.Error as error:
        print('查询出现错误:{}'.format(error))
    finally:
        cursor.close()
