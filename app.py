import matplotlib
matplotlib.use('Agg')

from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import uuid
import zipfile
import io
import shutil
import base64

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 * 1024  # 200MB
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')
app.config['OUTPUT_FOLDER'] = os.path.join(os.path.dirname(__file__), 'output')

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 确保目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)


# ── 工具函数 ──────────────────────────────────────────────

def parse_data(data_string):
    """解析逗号分隔的数字字符串为浮点数列表"""
    if not data_string or not isinstance(data_string, str):
        return []
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


def sanitize_filename(filename):
    """清理文件名，移除非法字符"""
    illegal_chars = '<>:"/\\|?*'
    for char in illegal_chars:
        filename = filename.replace(char, '_')
    if len(filename) > 200:
        filename = filename[:200]
    return filename


def plot_chart(data_values, row_name, chart_type='line', color='#3b82f6'):
    """生成图表并返回 fig 对象"""
    if not data_values:
        return None
    data_array = np.array(data_values)
    fig, ax = plt.subplots(figsize=(12, 5))

    chart_labels = {'line': '折线图', 'bar': '柱状图', 'scatter': '散点图'}
    label = chart_labels.get(chart_type, '折线图')

    if chart_type == 'line':
        ax.plot(data_array, linewidth=1.5, color=color)
    elif chart_type == 'bar':
        ax.bar(range(len(data_array)), data_array, color=color, alpha=0.7)
    elif chart_type == 'scatter':
        ax.scatter(range(len(data_array)), data_array, color=color, s=20, alpha=0.6)
    else:
        ax.plot(data_array, linewidth=1.5, color=color)

    ax.set_title(f'{row_name} - {label}', fontsize=12, fontweight='bold')
    ax.set_xlabel('Sample Index', fontsize=10)
    ax.set_ylabel('Value', fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    return fig


def fig_to_base64(fig):
    """将 matplotlib fig 转为 base64 字符串"""
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=120, bbox_inches='tight')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')


# ── 路由 ──────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """上传文件并返回列名列表"""
    if 'file' not in request.files:
        return jsonify({'error': '未找到文件'}), 400

    f = request.files['file']
    if f.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    ext = f.filename.rsplit('.', 1)[-1].lower()
    if ext not in ('csv', 'xlsx', 'xls'):
        return jsonify({'error': '仅支持 CSV / XLSX / XLS 文件'}), 400

    # 保存到临时目录
    session_id = uuid.uuid4().hex
    session_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    os.makedirs(session_dir, exist_ok=True)
    filepath = os.path.join(session_dir, f.filename)
    f.save(filepath)

    # 读取文件
    try:
        if ext == 'csv':
            df = pd.read_csv(filepath, encoding='utf-8')
        else:
            df = pd.read_excel(filepath)
    except Exception as e:
        return jsonify({'error': f'读取文件失败: {str(e)}'}), 400

    columns = df.columns.tolist()
    preview = df.head(5).to_dict(orient='records')
    total_rows = len(df)

    return jsonify({
        'session_id': session_id,
        'filename': f.filename,
        'columns': columns,
        'total_rows': total_rows,
        'preview': preview
    })


@app.route('/process', methods=['POST'])
def process():
    """处理数据并生成图表"""
    data = request.get_json()
    session_id = data.get('session_id')
    data_column = data.get('data_column')
    name_column = data.get('name_column')  # 可为 None
    chart_type = data.get('chart_type', 'line')
    color = data.get('color', '#3b82f6')

    if not session_id or not data_column:
        return jsonify({'error': '缺少参数'}), 400

    # 查找上传的文件
    session_dir = os.path.join(app.config['UPLOAD_FOLDER'], session_id)
    if not os.path.exists(session_dir):
        return jsonify({'error': '会话已过期，请重新上传文件'}), 400

    files = os.listdir(session_dir)
    if not files:
        return jsonify({'error': '找不到上传的文件'}), 400

    filepath = os.path.join(session_dir, files[0])
    ext = files[0].rsplit('.', 1)[-1].lower()

    try:
        if ext == 'csv':
            df = pd.read_csv(filepath, encoding='utf-8')
        else:
            df = pd.read_excel(filepath)
    except Exception as e:
        return jsonify({'error': f'读取文件失败: {str(e)}'}), 400

    # 输出目录
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    results = []
    first_preview = None

    for idx, row in df.iterrows():
        if name_column and name_column in df.columns:
            row_name = str(row[name_column])
        else:
            row_name = f"row_{idx + 2}"

        safe_name = sanitize_filename(row_name)

        if data_column not in df.columns:
            continue

        data_values = parse_data(row[data_column])
        if not data_values:
            continue

        fig = plot_chart(data_values, row_name, chart_type, color)
        if fig:
            out_file = os.path.join(output_dir, f'{safe_name}.png')
            fig.savefig(out_file, dpi=150, bbox_inches='tight')

            # 第一张图做预览
            if first_preview is None:
                first_preview = fig_to_base64(fig)
            else:
                plt.close(fig)

            results.append({
                'row_name': row_name,
                'row_number': idx + 2,
                'data_points': len(data_values),
                'min_value': f"{min(data_values):.2f}",
                'max_value': f"{max(data_values):.2f}",
                'mean_value': f"{np.mean(data_values):.2f}",
                'file_name': f'{safe_name}.png'
            })

    return jsonify({
        'success': True,
        'total': len(results),
        'results': results,
        'preview': first_preview
    })


@app.route('/download/<session_id>')
def download_zip(session_id):
    """打包下载所有图表"""
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
    if not os.path.exists(output_dir):
        return jsonify({'error': '找不到生成的文件'}), 404

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for fname in os.listdir(output_dir):
            fpath = os.path.join(output_dir, fname)
            if os.path.isfile(fpath):
                zf.write(fpath, fname)
    buf.seek(0)

    return send_file(
        buf,
        mimetype='application/zip',
        as_attachment=True,
        download_name='charts.zip'
    )


@app.route('/preview/<session_id>/<filename>')
def preview_image(session_id, filename):
    """预览单张图片"""
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], session_id)
    return send_from_directory(output_dir, filename)


# ── 启动 ──────────────────────────────────────────────────

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
