# PIR CurveTools - 数据图表生成器

一个基于 Flask 的 Web 应用，用于从 CSV / Excel 文件中批量生成折线图、柱状图、散点图。可直接部署到公网访问。

## 功能特点

- **多格式支持** — CSV / XLSX / XLS 文件上传
- **多种图表** — 折线图、柱状图、散点图一键切换
- **列选择** — 通过下拉菜单选择数据列和行名列
- **智能命名** — 按行名自动命名，也可按行号命名
- **批量处理** — 一次处理数百行数据
- **一键下载** — ZIP 打包下载所有图表
- **数据预览** — 上传后即时预览表格
- **统计信息** — 数据点数、最值、均值
- **颜色自选** — 6 种预设颜色

## 快速开始

### 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
python app.py
```

浏览器打开 `http://localhost:5000`

### Docker 运行

```bash
docker build -t pir-curvetools .
docker run -p 5000:5000 pir-curvetools
```

## 公网部署

### 方法 1：Render（推荐，免费）

1. Fork 本仓库或推送到你的 GitHub
2. 访问 [render.com](https://render.com)，使用 GitHub 登录
3. New → Web Service → 选择本仓库
4. 自动识别 `render.yaml`，点击 Deploy
5. 等待 2-3 分钟，获得 `https://pir-curvetools.onrender.com`

### 方法 2：Railway

1. 访问 [railway.app](https://railway.app)，使用 GitHub 登录
2. New Project → Deploy from GitHub repo → 选择本仓库
3. 自动识别 `Procfile`，一键部署
4. 获得 `https://xxx.up.railway.app`

### 方法 3：Docker 部署到任意服务器

```bash
# 构建
docker build -t pir-curvetools .

# 运行（后台）
docker run -d -p 80:5000 --name curvetools pir-curvetools
```

用服务器公网 IP 即可访问。

## 项目结构

```
├── app.py              # Flask 后端
├── templates/
│   └── index.html      # 前端页面
├── requirements.txt    # Python 依赖
├── Procfile            # Heroku / Railway
├── Dockerfile          # Docker 镜像
├── render.yaml         # Render.com 配置
└── README.md
```

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Flask + Gunicorn |
| 前端 | Bootstrap 5 + Vanilla JS |
| 图表 | Matplotlib |
| 数据 | Pandas / NumPy |

## License

MIT
