"""
抖音评论可视化分析平台
"""
# 导入库
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from PIL import ImageFont

# 导入自定义函数
from utility.data_loader import load_data
from utility.data_prase import *
from view import *

def run_view(file_path):
    # 初始化Dash应用
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.title = "抖音评论可视化分析平台"
    server = app.server

    # 载入数据
    df = load_data(file_path)

    # 数据处理
    time_df = get_time_comments(df) # 时间与评论数量
    local_df = get_local_comments(df) # 地理与评论数量
    hot_df = get_hot_comments(df) # 点赞量最高的10条评论

    emo_df = get_emotion_comments(df).sort_values(by='评论点赞数', ascending=False) # 情绪
    df_grouped = emo_df.groupby('情绪', as_index=False).agg(
        评论数量=('情绪', 'count'),
        总点赞数=('评论点赞数', 'sum'),
        平均点赞=('评论点赞数', 'mean')
    )


    # 在现有可视化数据部分添加
    wordcloud_img = get_wordcloud_figure(df['评论内容'].tolist())

    # 可视化数据
    local_fig = create_local_figure(local_df)
    hot_fig = create_hot_figure(hot_df)
    emo_pie = create_emotion_pie(df_grouped)
    emo_bar = create_emotion_bar(df_grouped)

    # 时间与评论数量
    date_options = [{'label': str(date), 'value': date} for date in time_df['日期'].unique()]

    # 定义列颜色配置
    COLOR_SCHEME = {
        'time-series': '#e6f7ff',    # 淡蓝色
        'emotion-pie': '#fff7e6',    # 米色
        'emotion-bar': '#f0ffe6',    # 淡绿色
        'map': '#f9f2ff',            # 淡紫色
        'top-comments': '#fff0f0',   # 淡粉色
        'word-cloud': '#e6ffff',     # 淡青色
        'search': '#fff5e6'          # 浅橙色
    }

    # 测试字体是否可用
    try:
        ImageFont.truetype('C:/Windows/Fonts/msyh.ttc', 12)
        print("字体加载成功")
    except Exception as e:
        print(f"字体加载失败: {str(e)}")

    # 应用布局
    app.layout = dbc.Container([
        # 标题优化（增加响应式字体）
        html.H1("抖音评论可视化分析仪表盘", 
            className="text-center my-4 p-3 shadow-sm rounded-3",
            style={
                'color': '#2c3e50', 
                'fontSize': 'clamp(1.8rem, 3vw, 2.5rem)',  # 响应式字体
                'background': 'linear-gradient(145deg, #ffffff, #f8f9fa)',
                'border': '1px solid rgba(0,0,0,0.1)'
            }),
        
        # 第一排布局调整
        dbc.Row([
            # 时间序列图表（2/5宽度）
            dbc.Col(
                html.Div([
                    # 新增标题
                    html.H4("评论数量随时间变化的趋势",
                        className="mb-2",
                        style={
                            'color': '#2c3e50',
                            'fontSize': '24px',
                            'fontWeight': '600',
                            'textAlign': 'center'
                        }),
                    dcc.Dropdown(
                        id='date-selector',
                        options=date_options,
                        value=time_df['日期'].max(),
                        clearable=False,
                        className='mb-3 shadow-sm'
                    ),
                    dcc.Graph(
                        id='time-series-chart',
                        style={'height': 'calc(50vh - 90px)'}  # 调整高度计算
                    )
                ], style={
                    'backgroundColor': COLOR_SCHEME['time-series'], 
                    'height': '60vh',
                    'minHeight': '500px',
                    'borderRadius': '12px',
                    'padding': '15px'  # 增加内边距
                }),
                width=5,
                className="h-100"
            ),

            # 情绪分析图表（3/5宽度）
            dbc.Col(
                html.Div([
                    html.H4("评论情绪分布",
                        className="mb-3",
                        style={'color': '#2c3e50', 
                               'fontSize': '24px',
                               'fontWeight': '600', 
                               'textAlign': 'center'}),
                    dbc.Row([
                        dbc.Col(
                            dcc.Graph(
                                id='emotion-pie',
                                figure=emo_pie,
                                style={'height': '90%'}  # 微调高度
                            ),
                            width=6,
                            className='p-1 h-100'  # 减少内边距
                        ),
                        dbc.Col(
                            dcc.Graph(
                                id='emotion-bar',
                                figure=emo_bar,
                                style={'height': '90%'}
                            ),
                            width=6,
                            className='p-1 h-100'
                        )
                    ], className='h-100 g-2')  # 添加列间距
                ], style={
                    'backgroundColor': COLOR_SCHEME['emotion-pie'],
                    'height': '60vh',  # 同步增加高度
                    'padding': '15px',  # 增加内边距
                    'minHeight': '500px'
                }),
                width=7,  # 3/5比例 (7/12 ≈ 58.3%)
                className="h-100"
            )
        ], className='g-3', style={'minHeight': '55vh'}),

        # 第二排最终调整
        dbc.Row([
            dbc.Col(
                html.Div(
                    dcc.Graph(
                        id='choropleth-map',
                        figure=local_fig,
                        style={
                            'height': '100%',
                            'width': '95%',  # 增加宽度限制
                            'margin': '0 auto'  # 水平居中
                        }
                    ),
                    className='chart-container p-3 shadow rounded-3',
                    style={
                        'backgroundColor': COLOR_SCHEME['map'], # 地图背景颜色
                        'height': '75vh', # 增加高度
                        'display': 'flex',  # 启用弹性布局
                        'justifyContent': 'center',  # 水平居中
                        'alignItems': 'center'  # 垂直居中
                    }
                ),
                width=7,
                className="h-100 ps-0"
            ),
            dbc.Col(
                html.Div(
                    dcc.Graph(
                        id='top-comments-bar',
                        figure=hot_fig,
                        style={
                            'height': '95%',  # 增加高度限制
                            'width': '98%'  # 增加宽度限制
                        }
                    ),
                    className='chart-container p-3 shadow rounded-3',
                    style={
                        'backgroundColor': COLOR_SCHEME['top-comments'],
                        'height': '75vh',
                        'justifyContent': 'center',  # 水平居中
                        'alignItems': 'center',  # 垂直居中
                    }
                ),
                width=5,
                className="h-100 pe-0"
            )
        ], className='g-3', style={
            'minHeight': '70vh',  # 恢复原始高度
            'margin': '1rem 0',  # 外边距减半
            'borderTop': '1px solid #eee',  # 减细分割线
            'borderBottom': '1px solid #eee',
            'padding': '1rem 0'  # 内边距减少
        }),
            
        # 第三排最终调整
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H4("评论关键词云图", 
                        className="mb-3",
                        style={'color': '#2c3e50', 'fontSize': '24px'}),
                    html.Img(
                        id='wordcloud-image',
                        src=wordcloud_img,
                        style={
                            'height': '92%',  # 增加图片占比
                            'objectFit': 'cover',  # 改为cover填充
                            'width': '100%'  # 增加宽度限制
                        }
                    )
                ], style={
                    'backgroundColor': COLOR_SCHEME['word-cloud'],
                    'height': '60vh',  # 增加总高度
                    'minHeight': '450px',
                    'padding': '15px'  # 减少内边距
                }),
                width=6,
                className="h-100 d-flex flex-column"
            ),
            
            dbc.Col(
                html.Div([
                    html.H4("评论搜索分析", 
                        className="mb-3",
                        style={'color': '#2c3e50', 'fontSize': '24px'}),
                    html.P("输入关键词搜索含有关键词的评论", className="text-muted"),
                    dcc.Input(
                        id='comment-search',
                        type='text',
                        placeholder='输入关键词搜索...',
                        className='form-control mb-3',
                        style={'height': '45px'}  # 增加输入框高度
                    ),
                    html.Div(
                        id='comment-list',
                        style={
                            'height': 'calc(100% - 100px)',  # 动态计算高度
                            'overflowY': 'auto',
                            'paddingRight': '10px'
                        }
                    )
                ], style={
                    'backgroundColor': COLOR_SCHEME['search'],
                    'height': '60vh',
                    'minHeight': '450px',
                    'padding': '15px'
                }),
                width=6,
                className="h-100 d-flex flex-column"
            )
        ], className='g-3', style={'minHeight': '60vh'}),  # 增加行高
    ], fluid=True, style={
        'padding': '1.5rem',  # 容器边距减少
        'background': 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
        'minHeight': '100vh'
    })


    # 回调函数组
    # 时间与评论数量的折线图
    @app.callback(
        Output('time-series-chart', 'figure'),
        [Input('date-selector', 'value')]
    )
    def update_time_series(selected_date):
        """
        输入：selected_date (str)
        DATA PROCESSING: 需要实现按日期过滤时间序列数据
        输出：反映该日期各小时评论数量的折线图
        """
        return create_time_figure(time_df, selected_date)

    # 评论内容搜索
    @app.callback(
        Output('comment-list', 'children'),
        [Input('comment-search', 'value')]
    )
    def update_search_results(search_text):
        if not search_text:
            return html.Div([
                html.Img(src='assets/search_icon.png', height=30),
                html.P("输入关键词搜索精彩评论...", className="text-muted")
            ], className="text-center")
        
        try:
            filtered = df[df['评论内容'].str.contains(search_text, case=False, na=False)]
            if filtered.empty:
                return html.Div([
                    html.Img(src='assets/no_results.png', height=100),
                    html.P("没有找到相关评论", className="text-danger mt-2")
                ], className="text-center")
                
            return [
                html.Div([
                    html.P([
                        html.Span(f"{row['用户名']}: ", className="fw-bold"),
                        row['评论内容']
                    ], className="mb-1"),
                    html.Small(f"❤️ {row['评论点赞数']} | 📅 {row['评论时间']}"),
                    html.Hr(className="my-2")
                ], className="comment-item p-2 hover-bg") 
                for _, row in filtered.head(20).iterrows()
            ]
        except Exception as e:
            return html.Div([
                html.Img(src='assets/error.png', height=50),
                html.P("搜索服务暂时不可用", className="text-danger mt-2")
            ], className="text-center")

    # 样式配置
    app.css.append_css({
    'external_url': 'assets/styles.css'
})

    app.run_server(debug=True) 

""" if __name__ == '__main__':
        # 从URL中提取视频ID
    url = "https://www.douyin.com/discover?modal_id=7441458537089338643"
    aweme_id = url.split("modal_id=")[1].split("&")[0]
    run_view(f'data/csv/{aweme_id}.csv')
 """