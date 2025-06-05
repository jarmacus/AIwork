import os


def load_thing_names(cursor):
    """
    从数据库加载物品标签名称。
    Load thing names from the database.

    :param cursor: sqlite3.Cursor 数据库游标
    :return: 物品标签列表 list of str
    """
    sql_string = "SELECT DISTINCT image_name_thing FROM Summary"  # 查询数据库中的物品标签
    cursor.execute(sql_string)

    # 获取所有物品标签，并去重（确保每个标签只出现一次）
    thing_names = [row[0] for row in cursor.fetchall() if row[0]]  # 过滤空值
    thing_names.sort()  # 可选，按字母顺序排序

    return thing_names


def save_thing_names():
    """
    """