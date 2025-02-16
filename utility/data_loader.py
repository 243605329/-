import pandas as pd


def load_data(file_path):
    df = pd.read_csv(file_path, index_col='CID')
    return (
        df[~df.index.duplicated(keep='first')]
        .dropna(subset=['评论内容'])
        .pipe(clean_location)  # 统一地理位置清洗
        .pipe(parse_datetime)  # 统一时间解析
    ) 

def clean_location(df):
    """清洗地理位置数据"""
    df = df.copy()
    if '评论地点' in df.columns:
        df = df.rename(columns={'评论地点': '省份'})  # 重命名列
        df['省份'] = (
            df['省份']
            .str.replace('中国', '')
            .str.strip()
            .replace({
                '内蒙古': '内蒙古',
                '黑龙江': '黑龙江',
                '香港': '香港'
            })
        )
    return df

def parse_datetime(df):
    """解析时间数据"""
    df = df.copy()
    if '评论时间' in df.columns:
        df['评论时间'] = pd.to_datetime(df['评论时间'], errors='coerce')
    return df 