"""
存储类的实现
1. csv存储类
2. json存储类
3. 数据库存储类
"""
import csv
import os
import pathlib
import json
from typing import Optional
from datetime import datetime


from utility.abstract_class import AbstractStore
from utility.asyn_db import AsyncMysqlDB, MysqlConnect
from utility.data_container import CommentContainer



class StoreFactory:
    """
    存储工厂类
    根据不同的存储类型，返回不同的存储实现类
    支持CSV、JSON、数据库三种存储方式
    """

    @staticmethod
    def get_store(data_save_type: str) -> AbstractStore:
        if data_save_type == "csv":
            return CsvStore()
        elif data_save_type == "json":
            return JsonStore()
        elif data_save_type == "database":
            return DatabaseStore()
        else:
            raise ValueError(f"不支持的存储类型: {data_save_type}")



class CsvStore(AbstractStore):
    """
    csv存储类
    """

    def __init__(self):
        """
        初始化
        """
        self.file_path = "data/csv"

    def make_file_path(self,aweme_id:str):
        """
        创建文件路径
        """
        return f"{self.file_path}/{aweme_id}.csv"

    def save_data(self,save_item:CommentContainer,aweme_id:str):
        """
        保存数据
        :param save_item: 保存的评论数据
        :param aweme_id: 视频id
        :return: 
        """
        # 创建目录
        pathlib.Path(self.make_file_path(aweme_id)).parent.mkdir(parents=True,exist_ok=True)
        file_name = self.make_file_path(aweme_id)
        
        # 判断文件是否存在，如果不存在则写入表头
        file_exists = os.path.exists(file_name)
        

        # 准备评论数据
        comment_data = [
            save_item.cid,
            save_item.user_name,
            save_item.comment_time,
            save_item.comment_ip,
            save_item.comment_content,
            save_item.likes,
            len(save_item.comment_reply)
        ]
        
            
        # 写入CSV文件
        with open(file_name, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # 如果文件不存在，写入表头
            if not file_exists:
                headers = ['CID', '用户名', '评论时间', 
                           '评论地点', '评论内容', '评论点赞数','评论数量']
                writer.writerow(headers)

            # 写入数据行
            writer.writerow(comment_data)

        # 准备回复数据
"""         reply_data = []
        for reply in save_item.comment_reply:
            reply_data.append([
                reply.cid,
                reply.reply_id,
                reply.user_name,
                reply.reply_content,
                reply.likes
            ])
            
        with open(file_name.replace(".csv","_reply.csv"), mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            # 如果文件不存在，写入表头
            if not file_exists:
                headers = ['CID', '回复的评论CID', '用户名', '回复内容', '回复点赞数']
                writer.writerow(headers)
            # 写入数据行
            writer.writerows(reply_data)
            print(reply_data) """



class JsonStore(AbstractStore):
    """
    json存储类
    """
    def __init__(self):
        """
        初始化
        """
        self.file_path = "data/json"

    def make_file_path(self,aweme_id:str):
        """
        创建文件路径
        """
        return f"{self.file_path}/{aweme_id}.json"
    
    def save_data(self,save_item:CommentContainer,aweme_id:str):
        """
        保存数据
        :param save_item: 保存的评论数据
        :param aweme_id: 视频id
        :return: 
        """
        # 创建目录
        pathlib.Path(self.make_file_path(aweme_id)).parent.mkdir(parents=True,exist_ok=True)
        file_name = self.make_file_path(aweme_id)
        
        # 将评论数据转换为字典格式
        comment_dict = {
            "cid": save_item.cid,
            "user_name": save_item.user_name,
            "comment_time": save_item.comment_time,
            "comment_ip": save_item.comment_ip,
            "comment_content": save_item.comment_content,
            "likes": save_item.likes,
            "replies": []
        }
        
        # 将回复数据转换为字典格式
        for reply in save_item.comment_reply:
            reply_dict = {
                "reply_id": reply.reply_id,
                "user_name": reply.user_name,
                "reply_content": reply.reply_content,
                "likes": reply.likes
            }
            comment_dict["replies"].append(reply_dict)
        
        save_item_list = []
        # 如果文件存在，则读取文件中的数据
        if os.path.exists(file_name):
            with open(file_name, mode="r", encoding="utf-8") as file:
                try:
                    save_item_list = json.load(file)
                except json.JSONDecodeError:
                    save_item_list = []
        
        # 将新的评论数据添加到列表中
        save_item_list.append(comment_dict)
        
        # 将数据保存到文件中
        with open(file_name, mode="w", encoding="utf-8") as file:
            json.dump(save_item_list, file, ensure_ascii=False, indent=2)




class DatabaseStore(AbstractStore):
    """
    数据库存储类
    """
    def __init__(self):
        """
        初始化
        """
        self.db: Optional[AsyncMysqlDB] = None
        self.mysql_connect = None
        
    async def init_db(self):
        if not self.mysql_connect:
            self.mysql_connect = MysqlConnect()
            self.db = (await self.mysql_connect.async_init()).get_db()
            
    async def save_data(self,save_item:CommentContainer,aweme_id:str):
        """
        保存数据
        """
        try:
            await self.init_db()
            from utility.utility import insert_comment,update_comment,query_comment_by_cid
            
            comment = await query_comment_by_cid(self.db,"douyin_comment",save_item.cid)
            if comment.cid:  # 修改判断条件
                print(f"更新评论: {save_item.cid}")
                await update_comment(self.db,"douyin_comment",save_item)
            else:
                print(f"插入评论: {save_item.cid}")
                await insert_comment(self.db,"douyin_comment",save_item)
                
        except Exception as e:
            print(f"保存数据失败: {e}")
            raise e
        
