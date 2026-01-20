import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import zipfile
import io
from pathlib import Path

# 设置页面配置
st.set_page_config(
    page_title="数据图表生成器",
    page_icon="📊",
    layout="wide"
)

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def parse_data(data_string):
    """解析逗号分隔的数字字符串为浮点数列表"""
    if not data_string or not isinstance(data_string, str):
        return []
    
    # 移除可能的引号
    data_string = str(data_string).strip().strip('"').strip("'")
    
    parts = data_string.split(',')
    values = []
    for p in parts:
        p = p.strip()
        if p:
            try:
                values.append(float(p))
            except ValueError:
                continue
    return values

def plot_chart(data_values, row_name, chart_type='line', figsize=(12, 6), color='blue'):
    """生成图表（折线图/柱状图/散点图）"""
    if not data_values:
        return None
    
    data_array = np.array(data_values)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # 根据图表类型绘制
    if chart_type == 'line':
        ax.plot(data_array, linewidth=1.5, color=color, marker='', linestyle='-')
        chart_title = f'{row_name} - 折线图'
    elif chart_type == 'bar':
        ax.bar(range(len(data_array)), data_array, color=color, alpha=0.7)
        chart_title = f'{row_name} - 柱状图'
    elif chart_type == 'scatter':
        ax.scatter(range(len(data_array)), data_array, color=color, s=20, alpha=0.6)
        chart_title = f'{row_name} - 散点图'
    else:
        ax.plot(data_array, linewidth=1.5, color=color, marker='', linestyle='-')
        chart_title = f'{row_name} - 折线图'
    
    ax.set_title(chart_title, fontsize=12, fontweight='bold')
    ax.set_xlabel('Sample Index', fontsize=10)
    ax.set_ylabel('Value', fontsize=10)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def sanitize_filename(filename):
    """清理文件名，移除非法字符"""
    # 移除或替换Windows文件名中的非法字符
    illegal_chars = '<>:"/\\|?*'
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    # 限制文件名长度
    if len(filename) > 200:
        filename = filename[:200]
    return filename

def process_data(df, data_column, name_column=None, chart_type='line', output_dir='output', color='blue'):
    """处理数据并生成图表"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    results = []
    total_rows = len(df)
    
    for idx, row in df.iterrows():
        # 获取行名（用于文件命名）
        if name_column and name_column in df.columns:
            row_name = str(row[name_column])
        else:
            row_name = f"row_{idx + 2}"  # 默认使用行号
        
        # 清理行名作为文件名
        safe_row_name = sanitize_filename(row_name)
        
        # 获取数据列
        if data_column not in df.columns:
            continue
        
        column_data = row[data_column]
        
        # 解析数据
        data_values = parse_data(column_data)
        
        if not data_values:
            continue
        
        # 生成图表
        fig = plot_chart(data_values, row_name, chart_type, color=color)
        
        if fig:
            # 保存图片（使用行名）
            output_file = os.path.join(output_dir, f'{safe_row_name}.png')
            fig.savefig(output_file, dpi=150, bbox_inches='tight')
            plt.close(fig)
            
            results.append({
                'row_name': row_name,
                'row_number': idx + 2,
                'data_points': len(data_values),
                'min_value': f"{min(data_values):.2f}",
                'max_value': f"{max(data_values):.2f}",
                'mean_value': f"{np.mean(data_values):.2f}",
                'file_path': output_file,
                'file_name': f'{safe_row_name}.png'
            })
    
    return results

# 主应用
st.title("📊 数据图表生成器")
st.markdown("---")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置选项")
    
    # 文件上传（支持CSV和Excel）
    uploaded_file = st.file_uploader(
        "上传数据文件",
        type=['csv', 'xlsx', 'xls'],
        help="支持CSV和Excel文件（.csv, .xlsx, .xls）"
    )
    
    st.markdown("---")
    
    # 图表类型选择
    st.subheader("📈 图表类型")
    chart_type = st.radio(
        "选择图表类型",
        ["折线图", "柱状图", "散点图"],
        help="选择要生成的图表类型"
    )
    
    # 图表类型映射
    chart_type_map = {
        "折线图": "line",
        "柱状图": "bar",
        "散点图": "scatter"
    }
    selected_chart_type = chart_type_map[chart_type]
    
    # 颜色选择
    color_options = {
        "蓝色": "blue",
        "红色": "red",
        "绿色": "green",
        "橙色": "orange",
        "紫色": "purple",
        "青色": "cyan"
    }
    selected_color = st.selectbox(
        "图表颜色",
        list(color_options.keys()),
        index=0
    )
    chart_color = color_options[selected_color]
    
    st.markdown("---")
    
    # 输出路径设置
    st.subheader("💾 保存设置")
    output_folder = st.text_input(
        "输出文件夹路径",
        value="output",
        help="生成的图片将保存在此文件夹中（可以是相对路径或绝对路径）"
    )
    
    st.markdown("---")
    st.markdown("### 📝 使用说明")
    st.markdown("""
    1. 上传CSV或Excel文件
    2. 选择数据列和行名列
    3. 选择图表类型和颜色
    4. 设置输出路径
    5. 点击"开始处理"按钮
    6. 下载生成的图表
    """)

# 主内容区
if uploaded_file is not None:
    try:
        # 根据文件类型读取数据
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        elif file_extension in ['xlsx', 'xls']:
            df = pd.read_excel(uploaded_file)
        else:
            st.error("不支持的文件格式")
            st.stop()
        
        st.success(f"✅ 成功读取文件：**{uploaded_file.name}**，共 {len(df)} 行数据")
        
        # 显示数据预览
        with st.expander("📋 数据预览", expanded=False):
            st.dataframe(df.head(10))
            st.caption(f"总列数: {len(df.columns)}")
            st.caption(f"列名: {', '.join(df.columns.tolist())}")
        
        st.markdown("---")
        
        # 列选择
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 数据列选择")
            data_column = st.selectbox(
                "选择数据列（包含逗号分隔的数字）",
                df.columns.tolist(),
                help="选择包含要绘制图表的数据列"
            )
            
            # 显示第一行数据示例
            if len(df) > 0:
                sample_data = df.iloc[0][data_column]
                st.code(f"示例数据（第1行）:\n{str(sample_data)[:150]}...", language="text")
        
        with col2:
            st.subheader("🏷️ 行名列选择（可选）")
            name_column = st.selectbox(
                "选择行名列（用于文件命名）",
                ["不使用行名（使用行号）"] + df.columns.tolist(),
                help="选择用于文件命名的列，如果不选择则使用行号"
            )
            
            if name_column == "不使用行名（使用行号）":
                name_column = None
                st.info("将使用行号命名文件：row_2.png, row_3.png, ...")
            else:
                if len(df) > 0:
                    sample_name = df.iloc[0][name_column]
                    st.info(f"示例行名（第1行）：**{sample_name}**\n\n文件将保存为：**{sanitize_filename(str(sample_name))}.png**")
        
        st.markdown("---")
        
        # 处理按钮
        if st.button("🚀 开始处理", type="primary", use_container_width=True):
            with st.spinner("正在处理数据，请稍候..."):
                # 创建进度条
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # 处理数据
                results = []
                total_rows = len(df)
                
                for idx, row in df.iterrows():
                    # 更新进度
                    progress = (idx + 1) / total_rows
                    progress_bar.progress(progress)
                    status_text.text(f"正在处理第 {idx + 1}/{total_rows} 行...")
                    
                    # 获取行名
                    if name_column and name_column in df.columns:
                        row_name = str(row[name_column])
                    else:
                        row_name = f"row_{idx + 2}"
                    
                    safe_row_name = sanitize_filename(row_name)
                    
                    # 获取数据
                    if data_column not in df.columns:
                        continue
                    
                    column_data = row[data_column]
                    data_values = parse_data(column_data)
                    
                    if not data_values:
                        continue
                    
                    # 创建输出目录
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                    
                    # 生成图表
                    fig = plot_chart(data_values, row_name, selected_chart_type, color=chart_color)
                    
                    if fig:
                        output_file = os.path.join(output_folder, f'{safe_row_name}.png')
                        fig.savefig(output_file, dpi=150, bbox_inches='tight')
                        plt.close(fig)
                        
                        results.append({
                            'row_name': row_name,
                            'row_number': idx + 2,
                            'data_points': len(data_values),
                            'min_value': f"{min(data_values):.2f}",
                            'max_value': f"{max(data_values):.2f}",
                            'mean_value': f"{np.mean(data_values):.2f}",
                            'file_path': output_file,
                            'file_name': f'{safe_row_name}.png'
                        })
                
                progress_bar.progress(1.0)
                status_text.text("处理完成！")
                
                # 显示结果统计
                st.success(f"✅ 成功生成 {len(results)} 个图表！")
                
                # 显示结果表格
                if results:
                    display_results = []
                    for r in results:
                        display_results.append({
                            '行名': r['row_name'],
                            '行号': r['row_number'],
                            '数据点数': r['data_points'],
                            '最小值': r['min_value'],
                            '最大值': r['max_value'],
                            '平均值': r['mean_value'],
                            '文件名': r['file_name']
                        })
                    results_df = pd.DataFrame(display_results)
                    st.dataframe(results_df, use_container_width=True)
                    
                    # 下载功能
                    st.markdown("---")
                    st.subheader("📥 下载选项")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # 创建ZIP文件
                        zip_buffer = io.BytesIO()
                        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                            for result in results:
                                file_path = result['file_path']
                                if os.path.exists(file_path):
                                    zipf.write(file_path, result['file_name'])
                        
                        zip_buffer.seek(0)
                        st.download_button(
                            label="📦 下载所有图片（ZIP）",
                            data=zip_buffer,
                            file_name=f"{output_folder}_charts.zip",
                            mime="application/zip",
                            use_container_width=True
                        )
                    
                    with col2:
                        # 预览第一个图表
                        if results:
                            first_file = results[0]['file_path']
                            if os.path.exists(first_file):
                                st.image(
                                    first_file, 
                                    caption=f"预览：{results[0]['row_name']} ({chart_type})", 
                                    use_container_width=True
                                )
                    
                    # 显示统计信息
                    with st.expander("📊 统计信息", expanded=False):
                        if results:
                            all_data_points = [r['data_points'] for r in results]
                            all_min_values = [float(r['min_value']) for r in results]
                            all_max_values = [float(r['max_value']) for r in results]
                            
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("总图表数", len(results))
                            with col2:
                                st.metric("平均数据点数", f"{np.mean(all_data_points):.1f}")
                            with col3:
                                st.metric("最小值范围", f"{min(all_min_values):.2f}")
                            with col4:
                                st.metric("最大值范围", f"{max(all_max_values):.2f}")
                    
                    # 显示输出路径信息
                    st.info(f"📁 所有图表已保存到：**{os.path.abspath(output_folder)}**")
    
    except Exception as e:
        st.error(f"❌ 处理文件时出错：{str(e)}")
        st.exception(e)

else:
    # 显示欢迎信息
    st.info("👈 请在左侧上传CSV或Excel文件开始使用")
    
    # 显示示例
    with st.expander("📖 使用示例", expanded=True):
        st.markdown("""
        ### 支持的文件格式：
        - ✅ CSV文件（.csv）
        - ✅ Excel文件（.xlsx, .xls）
        
        ### 示例CSV格式：
        ```
        serial_number,adv_algo_d_event,version
        device001,"0,0,-1,0,1,1,1,1",1.16.0
        device002,"0,0,0,0,0,0,0,0",1.16.0
        ```
        
        ### 功能特点：
        - ✅ 支持CSV和Excel文件上传
        - ✅ 多种图表类型（折线图/柱状图/散点图）
        - ✅ 通过列名选择数据列
        - ✅ 可选择行名列用于文件命名
        - ✅ 自定义输出路径
        - ✅ 批量生成和下载
        - ✅ 实时进度显示
        - ✅ 数据统计信息
        """)

# 页脚
st.markdown("---")
st.caption("💡 提示：生成的图片按照行名自动保存，如果未选择行名列则使用行号命名")
