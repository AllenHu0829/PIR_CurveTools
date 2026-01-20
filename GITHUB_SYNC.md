# GitHub 同步指南

## 当前状态

代码已经提交到本地Git仓库，现在需要推送到GitHub。

## 步骤1：在GitHub上创建新仓库

1. 访问 [GitHub](https://github.com)
2. 点击右上角的 "+" 按钮，选择 "New repository"
3. 填写仓库信息：
   - Repository name: `PIRADC` (或你喜欢的名称)
   - Description: `Streamlit数据图表生成器 - 支持CSV/Excel文件批量生成折线图、柱状图、散点图`
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"（因为我们已经有了）
4. 点击 "Create repository"

## 步骤2：添加远程仓库并推送

在项目目录中执行以下命令（将 `YOUR_USERNAME` 替换为你的GitHub用户名）：

```bash
# 添加远程仓库
git remote add origin https://github.com/YOUR_USERNAME/PIRADC.git

# 或者使用SSH（如果你配置了SSH密钥）
# git remote add origin git@github.com:YOUR_USERNAME/PIRADC.git

# 推送代码到GitHub
git branch -M main
git push -u origin main
```

## 步骤3：验证

访问你的GitHub仓库页面，应该能看到所有文件已经上传。

## 后续更新

以后如果有代码更新，使用以下命令：

```bash
# 添加更改的文件
git add .

# 提交更改
git commit -m "描述你的更改"

# 推送到GitHub
git push
```

## 注意事项

- 确保 `.gitignore` 文件已正确配置，避免上传不必要的文件
- 不要上传包含敏感信息的文件
- 大文件（如CSV/Excel数据文件）建议不要上传到GitHub
