llm_model_name = "gpt-4-turbo"
openai_api_base = "https://api.xty.app/v1"

file_default_path = r'C:\Users\lawrence\Videos'
model_size_or_path = r'C:\Users\lawrence\Documents\large_v3'

company_name = 'sotawork'
allSummaryPromptStart = """
我希望你是一名专业的视频内容编辑,帮我用中文总结内容精华.请用一句简短的话总结梗概,大概100-150字左右,内容如下:

"""
allSummaryPromptEnd = """

.第一遍一定不完美,请反复考虑斟酌一下,如果你做的够完美,我愿意支付$10小费!
"""
stepSummaryPromptStart = """
你是一名专业的杂志社编辑,我将给出带时间戳的文本,首先去除和视频完全不相关的内容,然后帮我按照不同章节(chapter)总结该内容,大概3-8段即可,并且给出该章节起始时间,格式如下:
mm:ss:{内容梗概} (eg:14:60 项目进度同步与问题解决策略)
每个章节梗概大概15-30个字,
待总结的内容如下:

"""
stepSummaryPromptEnd = """

.第一遍一定不完美,请反复考虑斟酌一下,如果你做的够完美,我愿意支付$10小费!
"""

LOG_LEVEL = "INFO"
# sqlite
db_path = "summary/media_sum.db"

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
