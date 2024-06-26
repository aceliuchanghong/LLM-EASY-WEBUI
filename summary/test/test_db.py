from datetime import datetime

from summary.config import table_add_sql, table_select_text_sql
from summary.util.check_db import excute_sqlite_sql

summaryType = "SumMp4Step"
filePath = r"C:\Users\lawrence\Videos\yunyin.mp4"
text = """
[0.00s -> 2.92s] 愿起一剑杀万劫
[2.92s -> 5.92s] 无情换作有情天
[5.92s -> 8.82s] 天子之剑
[8.82s -> 11.04s] 以宴席时成为风
[11.04s -> 12.92s] 席代为恶
[12.92s -> 14.60s] 敬畏为极
[14.60s -> 16.32s] 周颂为禅
[16.32s -> 18.12s] 含畏为家
[18.12s -> 19.82s] 包以四夷
[19.82s -> 21.56s] 国以四十
[21.56s -> 23.40s] 绕以渤海
[23.40s -> 24.78s] 带以长山
[24.78s -> 26.46s] 智以武行
[26.46s -> 28.46s] 论以行德
[28.46s -> 30.34s] 开以阴阳
[30.34s -> 31.92s] 识以春夏
[31.92s -> 33.88s] 行以秋冬
[33.88s -> 35.82s] 此剑直之无前
[35.82s -> 37.60s] 举之无上
[37.60s -> 39.14s] 按之无下
[39.14s -> 40.96s] 应之无旁
[40.96s -> 42.90s] 上结浮云
[42.90s -> 44.98s] 下绝地际
[44.98s -> 46.80s] 此剑以用
[46.80s -> 48.00s] 荒诸侯
[48.00s -> 49.92s] 天下福矣
[49.92s -> 53.20s] 此天子之剑也
[53.20s -> 55.02s] 诸侯之剑
[55.02s -> 56.98s] 以知勇士为风
[56.98s -> 58.44s] 以青年
[58.44s -> 59.84s] 识为恶
[59.84s -> 61.72s] 以贤良事为极
[61.72s -> 63.68s] 以周颂事为禅
[63.68s -> 66.32s] 以豪杰事为家
[66.32s -> 69.06s] 此剑直之亦无前
[69.06s -> 71.02s] 止之亦无上
[71.02s -> 72.84s] 按之亦无下
[72.84s -> 75.36s] 应之亦无旁
[75.36s -> 77.32s] 上法言天
[77.32s -> 78.62s] 以顺三光
[78.62s -> 80.04s] 下法方地
[80.04s -> 81.34s] 以顺四时
[81.34s -> 82.76s] 综合名义
[82.76s -> 84.30s] 以安四乡
[84.30s -> 85.60s] 此剑以用
[85.60s -> 87.60s] 如雷霆之战也
[87.60s -> 88.40s] 四方之阴
[88.40s -> 90.08s] 以吾不兵伏
[90.08s -> 92.18s] 而听从之命者矣
[92.18s -> 94.56s] 此诸侯之剑也
[94.56s -> 96.28s] 此剑以用
[96.28s -> 98.28s] 荒诸侯之剑也
"""
fileInfo = "说剑"

sumText = """
00:00: 描述剑的象征意义及其所代表的权力
23:40: 详述剑的使用场景和效果
53:20: 进一步强调剑的重要性及其在战争中的地位
75:36: 从天、地、人三方面解释剑的含义
94:56: 重复强调剑的使用和其所带来的影响
"""
# excute_sqlite_sql(
#     table_add_sql, (summaryType, filePath, text, fileInfo, sumText, str(datetime.now().strftime('%Y%m%d')), "remark"),
#     False)

# 此文件只能放在项目根目录测试
print("待总结:\n" + excute_sqlite_sql(table_select_text_sql, (summaryType, filePath), False)[0][0])
