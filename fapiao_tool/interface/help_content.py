"""内置帮助文档 HTML。"""

USER_GUIDE_HTML = """
<body style="background:#0c1018; color:#b8c0d0; font-family:'Segoe UI','Microsoft YaHei UI',sans-serif; font-size:12px; line-height:1.6;">
<h2 style="color:#9061ff; margin-top:0; font-size:16px;">发票合并助手 · 使用说明</h2>

<h3 style="color:#dce2ee; font-size:13px;">功能概述</h3>
<p>将多张发票 PDF 或图片按网格排版，合并导出为<strong style="color:#f0f2f8;">单个 PDF</strong>，并在导出前提供<strong style="color:#22b8cf;">高清滚动预览</strong>。</p>

<h3 style="color:#dce2ee; font-size:13px;">界面分区</h3>
<ul>
<li><strong style="color:#c8d0e0;">文件列表</strong> — 管理待合并素材，支持多选删除。</li>
<li><strong style="color:#c8d0e0;">排版设置</strong> — 页面方向、行列数与导出操作。</li>
<li><strong style="color:#c8d0e0;">实时预览</strong> — 自动刷新全部页面的排版效果，可滚动查看。</li>
</ul>

<h3 style="color:#dce2ee; font-size:13px;">操作流程</h3>
<ol>
<li>点击「添加文件」导入 PDF 或图片。</li>
<li>调整行列与方向，右侧预览区同步更新。</li>
<li>确认无误后点击「PDF 合并并导出」，选择保存位置。</li>
</ol>

<h3 style="color:#dce2ee; font-size:13px;">快捷键</h3>
<table cellpadding="4" style="color:#98a0b4;">
<tr><td><strong style="color:#9061ff;">Ctrl+O</strong></td><td>添加文件</td></tr>
<tr><td><strong style="color:#9061ff;">Delete</strong></td><td>移除选中</td></tr>
<tr><td><strong style="color:#9061ff;">Ctrl+M</strong></td><td>合并导出</td></tr>
<tr><td><strong style="color:#9061ff;">F1</strong></td><td>打开说明</td></tr>
</table>

<h3 style="color:#dce2ee; font-size:13px;">格式说明</h3>
<p>支持 PDF / JPG / JPEG / PNG / TIF / BMP。PDF 仅取第一页；图片自动转 PDF 后参与排版。</p>
</body>
"""
