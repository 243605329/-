import run_crawler
import douyin_comment_view
import time


if __name__ == "__main__":

    # 从URL中提取视频ID
    url = "https://www.douyin.com/discover?modal_id=7441458537089338643"
    aweme_id = url.split("modal_id=")[1].split("&")[0]

    # 爬取数据
    run_crawler.run_crawler(aweme_id)
    time.sleep(5)
    # 可视化数据
    douyin_comment_view.run_view(f'data/csv/{aweme_id}.csv')


