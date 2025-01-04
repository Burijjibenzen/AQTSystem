import pandas as pd
import mysql.connector
from mysql.connector import Error

# CSV 文件路径
csv_file_path = 'locationData.csv'

# 数据库连接配置
db_config = {
    'host': 'localhost',      # 数据库主机地址
    'user': 'root',  # 数据库用户名
    'password': '123456',  # 数据库密码
    'database': 'aqt'   # 数据库名称
}

# 目标表名
table_name = 'aqt_location'

def load_csv_to_mysql(csv_file_path, db_config, table_name):
    try:
        # 读取 CSV 文件
        df = pd.read_csv(csv_file_path)
        print("CSV 文件读取成功！")

        # 连接 MySQL 数据库
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(prepared=True)
        print("数据库连接成功！")

        # 将 DataFrame 转换为元组列表，并为第一列的值加上单引号
        data_tuples = [(f'{row[0]}', *row[1:]) for row in df.to_numpy()]
        print(f"处理后的数据: {data_tuples}")

        # 逐行插入数据，并添加自增的 id
        for index, row in enumerate(data_tuples, start=1):
            try:
                # 在每行数据前添加自增的 id
                row_with_id = (index,) + row
                insert_query = f"INSERT INTO {table_name} VALUES {row_with_id};"
                print(f"生成的 SQL 语句: {insert_query}")
                cursor.execute(insert_query)
                conn.commit()
                print(f"插入成功: {row_with_id}")

            except Error as e:
                print(f"插入失败: {row_with_id}, 错误: {e}")

    except Error as e:
        print(f"发生错误: {e}")

    finally:
        # 关闭数据库连接
        if conn.is_connected():
            cursor.close()
            conn.close()
            print("数据库连接已关闭。")

# 调用函数导入数据
load_csv_to_mysql(csv_file_path, db_config, table_name)