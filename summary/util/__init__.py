"""
  // 我希望你是一名专业的视频内容编辑，帮我用${language}总结视频的内容精华。请你将视频字幕文本进行总结（字幕中可能有错别字，如果你发现了错别字请改正），然后以无序列表的方式返回，不要超过5条。记得不要重复句子，确保所有的句子都足够精简，清晰完整，祝你好运！
  const betterPrompt = `I want you to act as an educational content creator. You will help students summarize the essence of the video in ${enLanguage}. Please summarize the video subtitles (there may be typos in the subtitles, please correct them) and return them in an unordered list format. Please do not exceed ${sentenceCount} items, and make sure not to repeat any sentences and all sentences are concise, clear, and complete. Good luck!`
  const timestamp = ' ' //`（类似 10:24）`;
  // 我希望你是一名专业的视频内容编辑，帮我用${language}总结视频的内容精华。请先用一句简短的话总结视频梗概。然后再请你将视频字幕文本进行总结（字幕中可能有错别字，如果你发现了错别字请改正），在每句话的最前面加上时间戳${timestamp}，每句话开头只需要一个开始时间。请你以无序列表的方式返回，请注意不要超过5条哦，确保所有的句子都足够精简，清晰完整，祝你好运！
  const promptWithTimestamp = `I would like you to act as a professional video content editor. You will help students summarize the essence of the video in ${enLanguage}. Please start by summarizing the whole video in one short sentence (there may be typos in the subtitles, please correct them). Then, please summarize the video subtitles, each subtitle should has the start timestamp (e.g. 12.4 -) so that students can select the video part. Please return in an unordered list format, make sure not to exceed ${sentenceCount} items and all sentences are concise, clear, and complete. Good luck!`
"""
prompt_all_summary_zh = "我希望你是一名专业的视频内容编辑，帮我用总结视频的内容精华。请先用一句简短的话总结视频梗概。然后再请你将视频字幕文本进行总结（字幕中可能有错别字，如果你发现了错别字请改正），在每句话的最前面加上时间戳，每句话开头只需要一个开始时间。请你以无序列表的方式返回，请注意不要超过5条哦，确保所有的句子都足够精简，清晰完整，祝你好运！"
prompt_step_summary_zh = ""
active_prompt_zh = "如果做的好,我会支付十美元小费"
language_dict = {"ZH": "中文", "EN": "English"}
