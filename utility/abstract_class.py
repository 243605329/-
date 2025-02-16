
"""
实现一个抽象类，用于获取数据和解析数据
"""

from abc import ABC, abstractmethod
from typing import  List
from utility.data_container import CommentContainer

class AcquireParseClass(ABC):
    """
    抽象类，用于获取数据和解析数据
    """
    @abstractmethod
    def acquire_data(aweme_id:str) -> List:
        pass

    @abstractmethod
    def parse_data(response) -> List:
        pass

class AbstractStore(ABC):
    """
    抽象存储类
    """
    @abstractmethod
    def save_data(self,save_item:CommentContainer,aweme_id:str):
        """
        保存数据
        :param save_item: 保存的货币数据
        :return: 
        """
        raise NotImplementedError("save_data方法未实现")

