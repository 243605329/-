"""
数据处理函数
定义处理数据的函数
"""
import pandas as pd


def get_time_comments(df) -> pd.DataFrame:
    """
    提取时间与评论量的数据
    """
    time_comments = pd.to_datetime(df['评论时间'], errors='coerce')
    time_comments = pd.DataFrame(pd.to_datetime(df['评论时间'], errors='coerce').reset_index(),columns=['评论时间'])
    time_comments = time_comments.resample('h', on='评论时间').size().reset_index(name='评论数量')
    time_comments['日期'] = time_comments['评论时间'].dt.date
    time_comments['时间'] = time_comments['评论时间'].dt.time
    return time_comments


def get_local_comments(df) -> pd.DataFrame:
    """
    提取评论地点与评论量的数据
    """
    local_comments = df.groupby('省份').size().reset_index(name='评论数量')
    local_comments['省份'] = local_comments['省份'].str.replace('中国', '').str.strip()
    local_comments['省份'] = local_comments['省份'].replace({
        '内蒙古': '内蒙古自治区',
        '黑龙江': '黑龙江省',
        '香港': '香港特别行政区'  # 保持与GeoJSON匹配
    })
    return local_comments


def get_hot_comments(df) -> pd.DataFrame:
    """
    提取热度与评论量的数据
    """
    hot_comments = df[['用户名','评论内容', '评论点赞数']].copy()
    hot_comments = hot_comments.sort_values(by='评论点赞数', ascending=False).head(10)
    return hot_comments


def get_emotion_comments(df) -> pd.DataFrame:
    """
    提取评论情绪与评论量的数据
    """
    from .analyze_emo import get_emotion_df
    try:
        return df[['评论内容', '评论点赞数']].pipe(get_emotion_df) # 返回情绪分析后的数据
    except Exception as e:
        print(f"情绪分析出错: {str(e)}")
        print("问题数据样本:", df[['评论内容', '评论点赞数']].head(2))
        raise



