# Streamlit Cloud 部署指南

## 前置条件

✅ 代码已推送到GitHub：https://github.com/AllenHu0829/PIR_CurveTools  
✅ requirements.txt 文件已存在  
✅ streamlit_app.py 主文件已存在  

## 部署步骤

### 方法1：通过Streamlit Cloud网站部署（推荐）

1. **访问Streamlit Cloud**
   - 打开 https://share.streamlit.io/
   - 使用GitHub账号登录

2. **授权Streamlit访问GitHub**
   - 如果首次使用，需要授权Streamlit访问你的GitHub仓库

3. **创建新应用**
   - 点击 "New app" 按钮
   - 或者访问：https://share.streamlit.io/deploy

4. **配置应用**
   - **Repository**: 选择 `AllenHu0829/PIR_CurveTools`
   - **Branch**: 选择 `main`
   - **Main file path**: 输入 `streamlit_app.py`
   - **App URL** (可选): 可以自定义URL，例如 `pir-curve-tools`

5. **部署**
   - 点击 "Deploy" 按钮
   - 等待部署完成（通常需要1-2分钟）

6. **查看应用**
   - 部署完成后，你会得到一个类似这样的URL：
     `https://pir-curve-tools.streamlit.app`
   - 点击URL即可访问你的应用

### 方法2：通过GitHub直接部署

1. **在GitHub仓库中添加Streamlit配置**
   - 访问你的仓库：https://github.com/AllenHu0829/PIR_CurveTools
   - 点击 "Settings" → "Secrets and variables" → "Actions"
   - 添加必要的secrets（如果需要）

2. **使用Streamlit Cloud CLI**（可选）
   ```bash
   # 安装Streamlit CLI
   pip install streamlit
   
   # 部署（需要Streamlit Cloud账号）
   streamlit deploy
   ```

## 部署后检查清单

- [ ] 应用可以正常访问
- [ ] 文件上传功能正常
- [ ] 图表生成功能正常
- [ ] 下载功能正常
- [ ] 所有依赖包正确安装

## 常见问题

### 1. 部署失败 - 依赖包问题
- 检查 `requirements.txt` 是否包含所有必要的包
- 确保版本号兼容

### 2. 应用无法启动
- 检查 `streamlit_app.py` 文件名是否正确
- 检查主文件路径配置

### 3. 文件上传限制
- Streamlit Cloud有文件大小限制（通常200MB）
- 大文件建议使用外部存储

### 4. 性能优化
- 如果处理大量数据，考虑添加缓存
- 使用 `@st.cache_data` 装饰器缓存数据

## 更新应用

当你更新代码后：

1. **提交更改到GitHub**
   ```bash
   git add .
   git commit -m "Update app"
   git push
   ```

2. **Streamlit Cloud会自动重新部署**
   - 通常会在几分钟内自动检测到更改并重新部署
   - 你可以在Streamlit Cloud控制台查看部署状态

## 应用URL

部署完成后，你的应用URL格式为：
```
https://[app-name].streamlit.app
```

或者：
```
https://share.streamlit.io/[username]/[repo-name]/[branch]/[main-file]
```

## 支持

如果遇到问题，可以：
- 查看Streamlit Cloud文档：https://docs.streamlit.io/streamlit-community-cloud
- 查看应用日志：在Streamlit Cloud控制台的"Logs"标签页
- 检查GitHub Actions（如果启用了）
