class Config:
    GEOJSON_URL = "https://geojson.cn/api/china/china.json"
    COLOR_SCALE = [
        [0.0, 'lightgray'],
        [0.00001, '#42f5b9'],
        [1.0, '#1b2cc1']
    ]
    DASH_LAYOUT = {
        'height': 500,
        'margin': dict(l=50, r=50, t=60, b=50)
    }

config = Config() 