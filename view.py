"""
定义可视化图表
"""

### 导入依赖库
import plotly.express as px
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
# 导入自定义配置
from utility.config import config


def create_time_figure(df, selected_date):
    """
    获取时间序列图
    """
    try:
        # 确保日期格式统一
        df['日期'] = pd.to_datetime(df['日期']).dt.date
        selected_date = pd.to_datetime(selected_date).date()
        
        # 添加时间格式校验
        filtered_df = df[df['日期'] == selected_date].sort_values('时间')
        
        # 添加空数据提示
        if filtered_df.empty:
            return go.Figure().add_annotation(
                text="当日无评论数据", 
                showarrow=False,
                font=dict(size=20)
            )
        
        # 创建图表
        fig = go.Figure()
        
        # 添加折线
        fig.add_trace(go.Scatter(
            x=filtered_df['时间'],
            y=filtered_df['评论数量'],
            mode='lines+markers',
            name='评论数量',
            line=dict(color='#3498db', width=2),
            marker=dict(size=6, color='#2980b9'),
            hovertemplate='<b>时间</b>: %{x}<br>'
                        '<b>评论数</b>: %{y}<extra></extra>'
        ))
        
        # 设置布局
        fig.update_layout(
            title={
                'text': f"{selected_date} 评论数量时间分布",
                'x': 0.5,
                'xanchor': 'center'
            },
            xaxis=dict(
                title='时间',
                tickformat='%H:%M',
                gridcolor='#eee',
                showline=True,
                linecolor='#ccc'
            ),
            yaxis=dict(
                title='评论数量',
                gridcolor='#eee',
                showline=True,
                linecolor='#ccc'
            ),
            plot_bgcolor='white',
            hoverlabel=dict(
                bgcolor='white',
                font_size=12,
                font_family="Arial"
            ),
            margin=dict(l=50, r=50, t=50, b=40),
            height=500
        )
        
        # 添加平均线
        avg = filtered_df['评论数量'].mean()
        fig.add_hline(
            y=avg,
            line_dash="dot",
            line_color="#e74c3c",
            annotation_text=f"平均值: {avg:.1f}",
            annotation_position="bottom right"
        )
        
        return fig
    except Exception as e:
        return go.Figure().add_annotation(text="数据加载失败", showarrow=False)


def create_emotion_pie(df):
    fig = px.pie(
        df,
        names='情绪',
        values='评论数量',
        color='情绪',
        color_discrete_map={'积极': '#2ecc71', '消极': '#e74c3c'},
        hole=0.3,
        title='情绪分布占比'
    )
    fig.update_traces(
        textinfo='percent+label', # 设置文本信息为百分比和标签
        hovertemplate="<b>%{label}</b><br>数量: %{value}", # 设置悬停模板
        hoverlabel=dict(font_size=14) # 设置悬停标签字体大小
    )
    fig.update_layout(
        title_font=dict(size=18),  # 缩小标题
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.15,  # 上移图例
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=40, b=30, l=20, r=20)  # 减少边距
    )
    return fig

def create_emotion_bar(df):
    fig = px.bar(
        df,
        x='情绪',
        y=['总点赞数', '平均点赞'],
        barmode='group',
        title='情绪与点赞关联分析',
        color_discrete_sequence=['#3498db', '#9b59b6'],
        labels={'value': '数值', 'variable': '指标'}
    )
    fig.update_layout(
        hovermode='x unified',
        xaxis_title="情绪类型",
        yaxis=dict(
            title_font=dict(size=12),  # 缩小字体
            tickfont=dict(size=10)
        ),
        margin=dict(t=40, l=60, r=10, b=30),  # 优化边距
        legend=dict(
            font=dict(size=10),
            title_font=dict(size=11)
        )
    )
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>%{data.name}: %{y:,.0f}",
        hoverlabel=dict(font_size=14)
    )
    return fig


def create_local_figure(df):
    """
    获取地理分布图
    """
    # 获取GeoJSON数据
    geojson_data = requests.get(config.GEOJSON_URL).json()

    # 获取所有省份列表
    provinces_in_geojson = [f['properties']['name'] for f in geojson_data['features']]
    df_merged = (
        pd.DataFrame({'省份': provinces_in_geojson})
        .merge(df, on='省份', how='left')
        .fillna({'评论数量': 0})
    )

    # 自定义颜色比例（0值对应灰色，渐变色由青绿色到深蓝色）
    max_value = df_merged['评论数量'].max()
    custom_scale = [
        [0.0, 'lightgray'],    # 0值显示为浅灰色
        [0.00001, '#42f5b9'],  # 青绿色
        [1.0, '#1b2cc1']       # 深蓝色
    ]

    # 创建初始地图
    fig = px.choropleth(
        df_merged,
        geojson=geojson_data, # GeoJSON数据
        locations='省份', # 省份名称
        featureidkey='properties.name', # 省份名称
        color='评论数量', # 颜色映射
        color_continuous_scale=custom_scale, # 颜色比例
        range_color=(0, max_value), # 颜色范围
        projection="mercator", # 投影方式
        title="中国各省评论数量色块地图"
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        margin=dict(l=0, r=0, t=30, b=0),
        height=720,  # 微调高度
        width=1080,    # 微调宽度
        title_font=dict(size=24,color='#2c3e50',family='Arial',weight='bold'), # 设置标题字体大小
        title_x=0.5, # 设置标题水平居中
        title_y=0.95, # 设置标题垂直居中
        legend=dict(orientation="h", yanchor="bottom", y=1.02) # 设置图例位置
    )
    fig.update_geos(
        projection_scale=1.5,  # 放大地图比例
        center={"lat": 35, "lon": 105}  # 调整地图中心点
    )
    return fig

def create_hot_figure(df):
    """
    获取点赞量最高的评论
    输入：df
    输出：点赞量最高的评论的柱状图
    """
    # ... existing code ...

    # 在hot_comments分析之后添加可视化代码
    # 创建横向柱状图（优化配色和样式）
    fig = px.bar(df,
                x='评论点赞数',
                y='用户名',
                orientation='h',
                hover_data={'评论内容': True},
                title='<b>🔥 热门评论点赞排行</b>',
                text='评论点赞数',
                color='评论点赞数',  # 新增颜色映射
                color_continuous_scale='Viridis',  # 使用现代配色方案
                height=780)  # 增加高度

    # 优化视觉样式
    fig.update_layout(
        margin=dict(l=100, r=30, t=80, b=40),  # 减少右侧边距
        height=720,
        width=800,
        title_font=dict(size=24,color='#2c3e50',family='Arial',weight='bold'), # 设置标题字体大小
        title_x=0.5, # 设置标题水平居中
        title_y=0.95, # 设置标题垂直居中
        legend=dict(orientation="h", 
                    yanchor="top", xanchor="center", 
                    y=-0.15,x=0.5,
                    bgcolor='rgba(255,255,255,0.5)'  # 半透明背景
                    ) # 设置图例位置居中
    )
    fig.update_yaxes(automargin=True)  # 确保Y轴标签完整

    # 优化柱状图样式
    fig.update_traces(
        marker=dict(
            line=dict(width=1, color='rgba(0,0,0,0.1)')  # 添加细边框
        ),
        hovertemplate=
        '<b>%{y}</b><br>' +
        '<i>%{customdata[0]}</i><br>' +
        '点赞数: %{x:,}<extra></extra>',  # 添加千位分隔符
        texttemplate='%{text:,} 👍',  # 添加表情符号
        textposition='outside', # 文本位置
        textfont={'color': '#2c3e50', 'size': 10},
        width=0.7  # 调整柱宽
    )




    return fig

def get_wordcloud_figure(contents):
    """
    生成评论词云
    输入：评论内容列表
    输出：词云图像路径
    """
    from wordcloud import WordCloud
    import jieba
    from collections import Counter
    import base64
    from io import BytesIO

    # 中文分词处理
    words = []
    for text in contents:
        words.extend(jieba.lcut_for_search(text))
    
    # 统计词频（过滤单字和停用词）
    word_counts = Counter([w for w in words if len(w) > 1])
    
    # 生成词云
    wc = WordCloud(
        width=1200,  # 增大画布宽度
        height=800,  # 增大画布高度
        font_path='C:/Windows/Fonts/msyh.ttc',
        background_color='white',
        colormap='viridis',
        max_words=200,  # 增加最大词数
        max_font_size=150  # 增大最大字号
    ).generate_from_frequencies(word_counts)
    
    # 转换为Base64编码
    img_buffer = BytesIO()
    wc.to_image().save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    
    return f'data:image/png;base64,{img_str}'

