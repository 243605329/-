# 抖音评论数据可视化

## 项目框架

```mermaid
graph TD
    A[Main入口] --> B[爬虫模块]
    A --> C[可视化模块]
    B --> D[数据获取]
    B --> E[数据解析]
    B --> F[数据存储]
    C --> G[数据加载]
    C --> H[数据处理]
    C --> I[Dash可视化]
    D --> J[抖音API请求]
    E --> K[评论/回复解析]
    F --> L[CSV/JSON/DB存储]
    H --> M[情感分析]
    H --> N[数据聚合]
    I --> O[交互式图表]
```

```mermaid
graph TD
    A[main.py] --> B[run_crawler.py]
    A --> C[douyin_comment_view.py]
    
    B --> D[store.py]
    B --> E[utility/data_acquire_parse.py]
    
    D --> F[StoreFactory]
    D --> G[CsvStore]
    D --> H[JsonStore]
    D --> I[DatabaseStore]
    D --> J[utility/abstract_class.py]
    D --> K[utility/asyn_db.py]
    
    C --> L[view.py]
    C --> M[utility/data_loader.py]
    C --> N[utility/data_prase.py]
    C --> O[assets/china_provinces.geojson]
    C --> P[assets/styles.css]
    
    L --> Q[utility/config.py]
    L --> R[wordcloud生成逻辑]
    L --> S[Plotly图表生成]
    
    style A fill:#f9f,stroke:#333
    style B fill:#cff,stroke:#333
    style C fill:#cff,stroke:#333
    style D fill:#ff9,stroke:#333
    style L fill:#ff9,stroke:#333
```

主要模块关系说明：

1. 入口文件main.py协调整个流程
2. 爬虫模块run_crawler.py负责数据采集和存储
3. 可视化模块douyin_comment_view.py负责数据分析展示
4. 存储系统store.py提供多种存储方式
5. view.py包含所有可视化图表生成逻辑
6. utility包包含数据处理、配置等工具函数
7. assets包含地理数据和样式资源
箭头表示模块间的依赖调用关系，黄色背景的是核心功能模块，青色背景的是主要流程控制器，粉色背景的是程序入口。

## 爬虫框架

```mermaid
graph TD
%% 爬虫模块结构
subgraph 爬虫模块
    B[run_crawler.py] --> B1[AcquireParseComment]
    B1 -->|数据获取| B1a[acquire_data]
    B1 -->|数据解析| B1b[parse_data]
    B --> B2[StoreFactory]
    B2 --> B2a[CsvStore]
    B2 --> B2b[JsonStore]
    B2 --> B2c[DatabaseStore]
    B2a -->|依赖| B3[CommentContainer]
    B2b -->|依赖| B3
    B2c -->|依赖| B3
    B2c -->|异步操作| B4[AsyncMysqlDB]
    B4 -->|连接池| B5[MysqlConnect]
end

style B fill:#cff,stroke:#333
style B1 fill:#9f9,stroke:#333
style B2 fill:#ff9,stroke:#333
style B2a fill:#f99,stroke:#333
style B2b fill:#f99,stroke:#333
style B2c fill:#f99,stroke:#333
```

## 可视化框架

```mermaid
graph TD
%% 可视化模块结构
subgraph 可视化模块
    C[douyin_comment_view.py] --> C1[view.py]
    C1 --> C1a[create_time_figure]
    C1 --> C1b[create_emotion_pie]
    C1 --> C1c[create_local_figure]
    C1 --> C1d[create_hot_figure]
    C1 --> C1e[get_wordcloud_figure]
    C --> C2[data_loader.py]
    C --> C3[data_prase.py]
    C --> C4[Dash组件]
    C4 --> C4a[布局系统]
    C4 --> C4b[回调函数]
    C --> C5[assets资源]
    C5 --> C5a[china_provinces.geojson]
    C5 --> C5b[styles.css]
    C1c -->|地理数据| C5a
    C1e -->|字体配置| C6[msyh.ttc]
    C -->|配置| C7[config.py]
end

style C fill:#cff,stroke:#333
style C1 fill:#ff9,stroke:#333
style C4 fill:#9f9,stroke:#333
style C5 fill:#f99,stroke:#333
```

模块结构说明：

1. 爬虫模块：

- 核心控制器：run_crawler.py
- 数据获取解析：AcquireParseComment类实现API请求和响应解析
- 存储系统：工厂模式支持CSV/JSON/DB三种存储方式
- 数据容器：CommentContainer统一数据结构
- 数据库连接：通过AsyncMysqlDB实现异步操作

2. 可视化模块：

- 主控制器：douyin_comment_view.py
- 图表引擎：view.py包含5种可视化图表生成器
- Dash框架：实现交互式Web仪表盘
- 数据处理：data_loader和data_prase进行数据清洗
- 资源依赖：地理数据、样式表、中文字体等
- 配置系统：config.py管理API密钥等参数

箭头表示数据流向和依赖关系，绿色背景的是数据处理组件，黄色背景的是核心逻辑，红色背景的是基础设施组件。


### 页面布局

```mermaid
graph TD
    A[用户界面] --> B[布局容器]
    B --> C[第一排布局]
    B --> D[第二排布局]
    B --> E[第三排布局]
    
    C --> C1[时间选择器]
    C --> C2[折线图]
    C --> C3[情绪饼图]
    C --> C4[情绪柱状图]
    
    D --> D1[地理分布图]
    D --> D2[热门评论柱状图]
    
    E --> E1[关键词云]
    E --> E2[搜索输入框]
    E --> E3[评论列表]
    
    C1 -->|选择日期| C2
    C4 -->|悬停事件| D2
    E2 -->|输入关键词| E3
    
    style A fill:#f0f0ff,stroke:#333
    style B fill:#e6f3ff,stroke:#3399ff
    style C fill:#e6ffe6,stroke:#00cc66
    style D fill:#fff0e6,stroke:#ff9933
    style E fill:#ffe6ff,stroke:#cc00cc
    style C1 fill:#cce6ff,stroke:#0066cc
    style C2 fill:#ccffcc,stroke:#009933
    style C3 fill:#ffcccc,stroke:#cc0000
    style C4 fill:#ffffcc,stroke:#cccc00
    style D1 fill:#e6ccff,stroke:#6600cc
    style D2 fill:#ccffff,stroke:#006666
    style E1 fill:#ffd9b3,stroke:#cc6600
    style E2 fill:#b3d9ff,stroke:#004080
    style E3 fill:#d9ffb3,stroke:#408000
```