import os


def load_top5_names(cursor):
    """
    从数据库加载物品标签名称。
    Load thing names from the database.

    :param cursor: sqlite3.Cursor 数据库游标
    :return: 物品标签列表 list of str
    """
    sql_string = "SELECT DISTINCT top5 FROM Summary"  # 查询数据库中的物品标签
    cursor.execute(sql_string)

    # 获取所有物品标签，并去重（确保每个标签只出现一次）
    top5_names = cursor.fetchall()
    return top5_names


def save_top5_names():
    """
    """