import sqlite3
import os

TABLE_CREATIION_DICT = {"Date": """CREATE TABLE Date (image_file nvarchar primart key)""",
                        "Place": """CREATE TABLE Place (image_file nvarchar primary key)""",
                        "Thing": """CREATE TABLE Thing (image_file nvarchar primary key)""",
                        "People": """CREATE TABLE People (image_file nvarchar primary key)""",
                        "Summary": """CREATE TABLE Summary (image_file nvarchar primary key, 
                        md5 char(32), 
                        create_date date, 
                        image_name_date nvarchar, 
                        create_week char(22), 
                        image_name_week nvarchar, 
                        gps_latitude_d char(1), 
                        gps_latitude decimal(3,6), 
                        gps_longitude_d char(1), 
                        gps_longitude decimal(3,6), 
                        nation nvarchar, 
                        province nvarchar, 
                        city nvarchar,
                        district nvarchar, 
                        street nvarchar, 
                        street_number nvarchar, 
                        image_name_address nvarchar, 
                        top5 nvarchar, 
                        image_name_thing text, 
                        bbox text, 
                        feature text, 
                        person text, 
                        image_name_person text)"""}
# 表格集合
# set of table
TABLES = set(["Date", "Place", "Thing", "People", "Summary","Top5"])  # for table name checking

# 数据库路径
db_path = os.path.join("record", "info.db")

# 确保 record 目录存在
if not os.path.exists("record"):
    os.makedirs("record")

# 连接数据库
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 插入示例数据
def initialize_data(cursor):
    # 插入数据到 People 表
    cursor.execute("""
    INSERT OR IGNORE INTO People (image_file) VALUES
    ("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\image\\Alice.jpg"),
    ("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\image\\bob.jpg")
    """)

    # 插入数据到 Summary 表
    cursor.execute("""
    INSERT INTO Summary (image_file, md5, create_date, person, province, city, district, image_name_thing, feature)
    VALUES
    ("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\image\\Alice.jpg", "md5hash1", "2024-12-01", "Alice", "California", "Los Angeles", "Downtown",  "image_thing_1", "feature_1"),
    ("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\image\\bob.jpg", "md5hash2", "2024-12-02", "Bob", "Texas", "Austin", "North Austin",  "image_thing_2", "feature_2")
    """)

    # 插入数据到 Thing 表
    cursor.execute("""
    INSERT OR IGNORE INTO Thing (image_file) VALUES
    ("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\image\\Alice.jpg"),
    ("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\image\\bob.jpg")
    """)

    # 插入数据到 Place 表
    cursor.execute("""
    INSERT OR IGNORE INTO Place (image_file) VALUES
    ("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\image\\Alice.jpg"),
    ("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\image\\bob.jpg")
    """)

    # 插入数据到 Date 表
    cursor.execute("""
    INSERT OR IGNORE INTO Date (image_file) VALUES
    ("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\image\\Alice.jpg"),
    ("C:\\Users\\86178\\Desktop\\Personal_Moments-master\\image\\bob.jpg")
    """)

    # 提交更改
    cursor.connection.commit()


initialize_data(cursor)

# 提交更改并关闭连接
conn.commit()
conn.close()

print("Database initialized successfully with sample data.")
