def format_timestamp(timestamp):
    # 将时间戳转换为整数分钟和秒
    minutes, seconds = divmod(timestamp / 1000, 60)
    # 格式化为字符串，保留两位小数
    formatted_time = f"{minutes * 60 + seconds:05.2f}s"
    return formatted_time

# 示例使用
timestamp = 15845  # 以秒为单位的时间戳
formatted_time = format_timestamp(timestamp)
print(formatted_time)  # 输出：320分55秒
