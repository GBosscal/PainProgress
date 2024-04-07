import os


def get_mime_type_and_name(file_path):
    # 定义更多的文件扩展名及其对应的 MIME 类型
    mime_types = {
        '.txt': 'text/plain',
        '.html': 'text/html',
        '.css': 'text/css',
        '.js': 'application/javascript',
        '.json': 'application/json',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.pdf': 'application/pdf',
        '.doc': 'application/msword',
        '.docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        '.xls': 'application/vnd.ms-excel',
        '.xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg',
        '.m4a': 'audio/x-m4a',
        # 添加更多的扩展名和对应的 MIME 类型
    }

    # 获取文件扩展名
    file_extension = os.path.splitext(file_path)[1]

    # 根据扩展名查找对应的 MIME 类型
    mime_type = mime_types.get(file_extension.lower())

    # 如果无法匹配扩展名，返回默认值
    if not mime_type:
        mime_type = 'application/octet-stream'

    # 获取文件名
    file_name = os.path.basename(file_path)

    return mime_type, file_name
