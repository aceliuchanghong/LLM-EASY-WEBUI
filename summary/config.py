llm_model_name = "gpt-4-turbo"
openai_api_base = "https://api.xty.app/v1"
apiKey = 'qwen:14b-gguf'
max_tokens = 8112

file_default_path = r'C:\Users\lawrence\Videos'
model_size_or_path = r'C:\Users\lawrence\Documents\large_v3'

company_name = 'sotawork'

# sqlite
LOG_LEVEL = "ERROR"
db_path = "summary/media_sum.db"
segment_length = 3500

Prompt = """
你是一个专业的秘书，请根据以下会议内容，协助我整理出一份规范的会议纪要。这份纪要应包括会议的基本信息、目的和议题、内容摘要、决议、解决方案、行动事项、附件和参考信息等关键要素。
要求:
1. Markdown格式
2. 不要有多余描述，仅给出结果即可
3. 重点关注以下内容：
   <用户下拉选择,可以多选>
   - 待办事宜
   - 项目金额
   - 解决方案
   - 每人任务
   - 会议目的
   - 会议决议
   - 参会人员
   - 截至时间
   - 会议开始和结束时间
   - 关键讨论点
   <用户下拉选择,可以多选>
会议内容如下:
<内容>
"""

allSummaryPromptStart = """
我希望你是一名专业的视频内容编辑,帮我用中文总结内容精华.请用一句简短的话总结梗概,仅内容即可,不要其他任何修饰词,大概100-150字左右,内容如下:{begin}

"""
allSummaryPromptEnd = """

{end}.注意!第一遍一定不完美,请反复考虑斟酌一下,如果你做的够完美,我愿意支付$10小费!
"""
stepSummaryPromptStart = """
你是一名专业的杂志社编辑,帮我总结内容,我将给出带时间戳的文本,完成以下几点要求
1.去除和视频完全不相关的内容
2.然后帮我按照不同章节(chapter)总结该内容,仅内容即可,不要其他任何修饰词,大概3-6段即可,并且给出该章节起始时间+梗概+描述,格式如下:
```
20:34: 讲述的天子之剑
天子之剑，有恶必杀，对恶有深深的敬畏，说明剑的使命。
```
3.每个章节梗概是15-30个字,描述是30-60个字
待总结的内容如下:{begin}

"""
stepSummaryPromptEnd = """

{end}.注意!第一遍一定不完美,请反复考虑斟酌一下,如果你做的够完美,我愿意支付$10小费!
"""

allSummaryConnStart = """
你是一名专业的杂志社编辑主管,我会给出某一个视频的不同分段总结,
1.帮我合并内容精华,总结梗概,长度大概{待合并的内容}的1/3左右
2.不要有多余描述,仅回答结果即可
待合并的内容如下:{begin}

"""
allSummaryConnEnd = """

{end}.注意!第一遍一定不完美,请反复考虑斟酌一下,如果你做的够完美,我愿意支付$10小费!
"""

stepSummaryConnStart = """
你是一名专业的杂志社编辑主管,我会给出某一个视频的不同章节带时间轴的分段总结,帮我合并其内容精华.
1.{输出结果的章节总数}大概是{待合并的内容}的2/3数目
2.合并之后按照时间顺序给出所有章节起始时间+梗概+描述,输出格式如下:
```
20:34: 讲述的天子之剑
天子之剑，有恶必杀，对恶有深深的敬畏，说明剑的使命。
```
3.不要有多余描述,仅回答结果即可
待合并的内容如下:{begin}

"""
stepSummaryConnEnd = """

{end}.注意!第一遍一定不完美,请反复考虑斟酌一下,如果你做的够完美,我愿意支付$10小费!
"""

textAllSummaryPromptStart = """
我将给你提供一段会议内容，帮我整理成更规范的形式，包括会议的基本信息、目的和议题、内容摘要、决议、解决方案、行动事项、附件和参考信息等会议纪要信息
内容如下:{begin}

"""
textAllSummaryPromptEnd = """

{end}.注意!第一遍一定不完美,请反复考虑斟酌一下
"""

textAllSummaryConnStart = """
我将给你提供一段或多段会议纪要内容,帮我做成一个更加规范的会议纪要
要求:1.markdown格式
2.不要输出任何除了结果的其他话
其内容如下:{begin}

"""
textAllSummaryConnEnd = """

{end}.注意!第一遍一定不完美,请反复考虑斟酌一下
"""

create_table_sql = """
CREATE TABLE IF NOT EXISTS media_sum_info
(summaryType TEXT,filePath TEXT,text_detail TEXT, fileInfo TEXT, sumText TEXT, time_insert TEXT, remark TEXT)
"""
table_select_url_count_sql = """
select count(*) from media_sum_info where summaryType = ? and filePath = ?
"""
table_select_url_sql = """
select * from media_sum_info where summaryType = ? and filePath = ?
"""
table_select_sum_sql = """
select sumText from media_sum_info where summaryType = ? and filePath = ?
"""
table_select_text_sql = """
select text_detail from media_sum_info where summaryType = ? and filePath = ?
"""
table_count_sql = """
select count(*) from media_sum_info
"""
table_all_sql = """
select * from media_sum_info
"""
table_add_sql = """
INSERT INTO media_sum_info (summaryType, filePath, text_detail, fileInfo, sumText, time_insert, remark)
VALUES (?, ?, ?, ?, ?, ?, ?)
"""
table_del_url_sql = """
delete from media_sum_info where summaryType = ? and filePath = ?
"""
table_truncate_sql = """
DELETE FROM media_sum_info
"""
