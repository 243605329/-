"""
1. 定义评论容器类和回复容器类
2. 实现抽象类，用于获取数据和解析数据
"""

from typing import List


class ReplyContainer():
    """
    回复容器类
    包含回复发布者cid、reply_id、用户名、回复内容、点赞数量
    """
    def __init__(self):
        self.cid : str = ""
        self.reply_id : str = ""
        self.user_name : str = ""
        self.reply_content : str = ""
        self.likes : int = 0

    def __str__(self) -> str:
        return f"""用户名: {self.user_name},
回复内容: {self.reply_content}, 
点赞数量: {self.likes}"""



class CommentContainer():
    """
    评论容器类
    包含评论发布者cid、用户名、评论发布时间、评论发布地点、评论内容、评论回复、点赞数量
    """
    def __init__(self):
        self.cid: str = "" 
        self.user_name: str = ""
        self.comment_time: str = ""
        self.comment_ip: str = ""
        self.comment_content: str = ""
        self.comment_reply: List[ReplyContainer] = []
        self.likes: int = 0

    def __str__(self) -> str:
        return f"""用户名: {self.user_name}, 
评论时间: {self.comment_time}, 
评论地点: {self.comment_ip}, 
评论内容: {self.comment_content}, 
评论回复: 
{'\n'.join(str(reply.user_name) + " : " + str(reply.reply_content) for reply in self.comment_reply)}, 
点赞数量: {self.likes}"""
    

