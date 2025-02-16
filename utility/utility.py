"""
定义一些爬虫代码的工具函数
"""



from utility.data_container import CommentContainer, ReplyContainer

from asyn_db import AsyncMysqlDB

from datetime import datetime


async def insert_comment(db: AsyncMysqlDB, table_name:str,comment: CommentContainer) -> int:
    """
    插入数据
    :param db:
    :param comment:
    :return:
    """
    # 将时间戳转换为datetime格式
    comment_time = datetime.fromtimestamp(int(comment.comment_time))
    
    item = {
        "cid": comment.cid,
        "user_name": comment.user_name,
        "comment_time": comment_time,  # 使用转换后的datetime
        "comment_ip": comment.comment_ip,
        "comment_content": comment.comment_content,
        "reply_num": len(comment.comment_reply),
        "likes": comment.likes
    }
    print(f"准备插入数据: {item}")
    result = await db.item_to_table(table_name, item)
    print(f"插入结果: {result}")
    return result


async def update_comment(db: AsyncMysqlDB, table_name:str,comment: CommentContainer) -> int:
    """
    更新数据
    :param db:
    :param comment:
    :return:
    """
    # 将时间戳转换为datetime格式
    comment_time = datetime.fromtimestamp(int(comment.comment_time))
    
    item = {
        "user_name": comment.user_name,
        "comment_time": comment_time,  # 使用转换后的datetime
        "comment_ip": comment.comment_ip,
        "comment_content": comment.comment_content,
        "reply_num": len(comment.comment_reply),
        "likes": comment.likes
    }
    print(f"Updating item: {item}")
    return await db.update_table(table_name, item, "cid", comment.cid)


async def query_comment_by_cid(db: AsyncMysqlDB, table_name:str, cid: str) -> CommentContainer:
    """
    查询数据
    :param db:
    :param table_name:
    :param cid:
    :return:
    """
    sql = f"select * from {table_name} where cid = '{cid}'"
    rows = await db.query(sql)
    if len(rows) > 0:
        return CommentContainer(**rows[0])
    return CommentContainer()


async def insert_reply(db: AsyncMysqlDB, table_name: str, reply: ReplyContainer) -> int:
    """
    插入回复数据
    :param db: 数据库连接
    :param table_name: 表名
    :param reply: 回复数据容器
    :return: 插入的行ID
    """
    item = {
        'cid': reply.cid,
        'reply_id': reply.reply_id,
        'user_name': reply.user_name,
        'reply_content': reply.reply_content,
        'likes': reply.likes
    }
    print(f"Inserting reply: {item}")
    return await db.item_to_table(table_name, item)

async def update_reply(db: AsyncMysqlDB, table_name: str, reply: ReplyContainer) -> int:
    """
    更新回复数据
    :param db: 数据库连接
    :param table_name: 表名
    :param reply: 回复数据容器
    :return: 更新的行数
    """
    item = {
        'reply_id': reply.reply_id,
        'user_name': reply.user_name,
        'reply_content': reply.reply_content,
        'likes': reply.likes
    }
    print(f"Updating reply: {item}")
    return await db.update_table(table_name, item, "cid", reply.cid)



async def query_reply_by_cid(db: AsyncMysqlDB, table_name: str, cid: str) -> ReplyContainer:
    """
    根据cid查询回复数据
    :param db: 数据库连接
    :param table_name: 表名
    :param cid: 回复ID
    :return: 回复数据容器
    """
    sql = f"select * from {table_name} where cid = %s"
    rows = await db.query(sql, cid)
    if len(rows) > 0:
        reply = ReplyContainer()
        reply.cid = rows[0]['cid']
        reply.reply_id = rows[0]['reply_id']
        reply.user_name = rows[0]['user_name']
        reply.reply_content = rows[0]['reply_content']
        reply.likes = rows[0]['likes']
        return reply
    return ReplyContainer()