

"""
实现爬虫的主流程
"""


from utility.data_acquire_parse import AcquireParseComment
from store import StoreFactory


def run_crawler(aweme_id:str):
    """
    爬虫主函数  
    """
    # 1. 发送请求，获取响应的api(comment_api,reply_api)
    comment_response_list = AcquireParseComment.acquire_data(aweme_id)
    # 2. 解析响应的api，获取评论数据,并将评论存储到容器中
    comment_list = AcquireParseComment.parse_data(comment_response_list)
    # 3. 将评论数据存储到本地
    store = StoreFactory.get_store("csv")
    for comment in comment_list:
        store.save_data(comment,aweme_id)



""" if __name__ == "__main__":
    # 从URL中提取视频ID
    url = "https://www.douyin.com/discover?modal_id=7441458537089338643"
    aweme_id = url.split("modal_id=")[1].split("&")[0]
    
    #asyncio.get_event_loop().run_until_complete(run_crawler(aweme_id))
    run_crawler(aweme_id) """

