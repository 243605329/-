
from abc import abstractmethod
from datetime import datetime
import json
import random
import time
from typing import Dict, List

import requests

from utility.abstract_class import AcquireParseClass
from utility.data_container import CommentContainer, ReplyContainer


class AcquireParseComment(AcquireParseClass):
    """
    继承抽象类，用于获取评论数据，并解析评论数据
    """
    @abstractmethod
    def acquire_data(aweme_id:str) -> List:
        """
        获取评论数据
        :param aweme_id: 视频id
        :return: 评论数据
        """
        from utility.config_c import params,cookies,headers

        response_list: List[Dict] = []
        cursor = 0
        while True:
            print(f"正在请求第{cursor}页评论数据")
            params['aweme_id'] = aweme_id
            params['cursor'] = str(cursor)
            response = requests.get('https://www-hj.douyin.com/aweme/v1/web/comment/list/',params=params,cookies=cookies,headers=headers)
        
            if response.status_code != 200:
                print(f"请求失败，状态码：{response.status_code}")
                print(f"响应内容：{response.text}")
                print(f"请求URL：{response.url}")
                print(f"请求头：{response.request.headers}")
                print(f"请求cookies：{response.request._cookies}")
                print("完整请求信息：")
                print(response.request.__dict__)
                print("完整响应信息：")
                print(response.__dict__)
            else:
                print("请求成功")
            
            data = response.json()
            response_list.append(data)
            if not data.get('has_more',False):
                break
            cursor = data.get('cursor',cursor + 20)

        print(f"获取评论数据完成，共获取{len(response_list)}页评论数据")
        
        return response_list


    @abstractmethod
    def parse_data(response_list) -> List:
        """
        解析评论数据
        :param response: 评论数据
        :return: 评论数据容器列表
        """

        print("开始解析评论数据")
        comment_list: List[CommentContainer] = []

        for response in response_list:
            print(f"正在解析第{response_list.index(response)}页评论数据")
            comments:Dict = response['comments']
            for comment in comments:
                comment_container = CommentContainer()
                comment_container.cid = comment['cid'].strip()
                comment_container.user_name = comment['user']['nickname'].strip()
                comment_container.comment_time = datetime.fromtimestamp(comment['create_time']).strftime("%Y-%m-%d %H:%M:%S")
                comment_container.comment_ip = comment['ip_label']
                comment_container.comment_content = comment['text'].strip()
                comment_container.likes = comment['digg_count']
                comment_container.reply_comment_total = comment['reply_comment_total']
        
        return comment_list

                
"""                 # 如果存在回复，则将回复数据添加到容器中
                if comment['reply_comment_total'] > 0:
                    reply_response_list = AcquireParseReply.acquire_data(comment['aweme_id'],comment['cid'])
                    reply_list = AcquireParseReply.parse_data(reply_response_list)
                    print(f"成功获取并解析{comment['cid']}共{len(reply_list)}条回复数据")
                    comment_container.comment_reply = reply_list
                # 将数据容器添加到列表中
                comment_list.append(comment_container)

        print(f"解析完成，共解析{len(comment_list)}条评论数据") """

        


class AcquireParseReply(AcquireParseClass):
    """
    继承抽象类，用于获取回复数据，并解析回复数据
    """
    @abstractmethod
    def acquire_data(aweme_id:str,cid:str) -> List:
        """
        获取回复数据
        :param aweme_id: 视频id
        :return: 回复数据
        """
        from utility.config_c import cookies,headers
        from utility.config_r import params
        reply_response_list: List[Dict] = []
        cursor = 0
        params['item_id'] = aweme_id
        params['comment_id'] = cid
        
        while True:
            try:
                params['cursor'] = str(cursor)
                
                # 增加随机延时
                delay = random.uniform(1, 3)
                time.sleep(delay)
                
                # 随机更新一些请求参数
                params['_signature'] = str(int(time.time() * 1000))
                
                response = requests.get('https://www-hj.douyin.com/aweme/v1/web/comment/list/reply/',
                                     params=params,
                                     cookies=cookies,
                                     headers=headers,
                                     timeout=3)
                
                # 如果触发反爬，等待更长时间后重试
                if 'Bd-Ticket-Guard-Result' in response.headers and response.headers['Bd-Ticket-Guard-Result'] == '1205':
                    print("检测到反爬限制，等待重试...")
                    time.sleep(3)  # 等待10秒后重试
                    continue
                    
                # 检查响应内容是否为空
                if not response.text.strip():
                    print("收到空响应，尝试重试...")
                    time.sleep(1)  # 等待5秒后重试
                    continue
                    
                data = response.json()
                if not data:
                    break
                    
                reply_response_list.append(data)
                if not data.get('has_more',False):
                    break
                cursor = data.get('cursor',cursor + 3)
                
            except requests.exceptions.RequestException as e:
                print(f"请求异常: {e}")
                time.sleep(1)  # 出错后等待5秒
                continue
            except json.JSONDecodeError as e:
                print(f"JSON解析错误: {e}")
                time.sleep(1)  # 出错后等待5秒
                continue
            
        return reply_response_list

    @abstractmethod
    def parse_data(response_list) -> List:
        """
        解析回复数据
        :param response_list: 回复数据
        :return: 回复数据容器列表
        """
        reply_list: List[ReplyContainer] = []
        for response in response_list:
            # 添加检查确保 comments 字段存在且不为 None
            reply_data = response.get('comments')
            if not reply_data:  # 如果 reply_data 为 None 或空列表
                print("该页回复数据为空")
                continue
            
            for reply in reply_data:
                reply_container = ReplyContainer()
                reply_container.cid = reply['cid'].strip()
                reply_container.reply_id = reply['reply_id'].strip()
                reply_container.user_name = reply['user']['nickname'].strip()
                reply_container.reply_content = reply['text'].strip()
                reply_container.likes = reply['digg_count']
                reply_list.append(reply_container)
        
        return reply_list