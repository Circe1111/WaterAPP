# 喝水记录小程序 (WaterAPP)

朋友间共享喝水记录的微信小程序。

## 技术栈

- **前端**: 微信小程序 (WXML + WXSS + JavaScript)
- **后端**: Python FastAPI
- **数据库**: SQLite
- **ORM**: SQLAlchemy

## 功能

- 记录每日喝水量，支持多种杯量选择
- 自定义每日饮水目标
- 喝水提醒通知（微信订阅消息）
- 好友共享与喝水排行榜
- 日/周/月数据统计图表

## 项目结构

```
WaterAPP/
├── miniprogram/          # 微信小程序前端
│   ├── pages/
│   │   ├── index/        # 首页 - 记录喝水
│   │   ├── history/      # 饮水历史
│   │   ├── friends/      # 好友列表 & 排行榜
│   │   ├── stats/        # 统计图表
│   │   └── settings/     # 目标设置 & 提醒
│   ├── components/       # 公共组件
│   ├── utils/            # 工具函数
│   ├── app.js
│   ├── app.json
│   └── app.wxss
├── backend/              # Python 后端
│   ├── app/
│   │   ├── api/          # API 路由
│   │   ├── models/       # 数据模型
│   │   ├── services/     # 业务逻辑
│   │   └── utils/        # 工具函数
│   ├── requirements.txt
│   └── main.py
└── README.md
```

## 快速开始

### 后端

```bash
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
python main.py
```

### 小程序

1. 下载 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)
2. 导入 `miniprogram/` 目录
3. 在 `utils/api.js` 中配置后端 API 地址
