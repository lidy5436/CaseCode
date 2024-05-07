from options.options import insertData, connectToDatabase, queryData

if __name__ == '__main__':
    # 连接数据库
    connection = connectToDatabase('127.0.0.1', 'root', '123456', 'website_template')
    if connection:
        # 列名称
        columns = ['id', 'role_code', 'role_name', 'description']
        # 数据
        data = [
            ('1001', '1001', '10001', '10001')
        ]
        # 插入数据
        insertData(connection, "base_role", columns, data)

        # 查询数据
        dataList = queryData(connection, 'base_role')
        print("查询到数据:\n{}".format(dataList))
