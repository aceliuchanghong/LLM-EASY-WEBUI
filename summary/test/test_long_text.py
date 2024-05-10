from smain import crack_long_text, SummaryPrompt
from summary.mp4_sum.stepSummaryWorker import stepSummaryWorker

text = """
[0.46s -> 1.36s] 哈喽 大家好

[1.36s -> 4.40s] 欢迎各位加入格莱美这个大家庭

[4.40s -> 6.86s] 在此呢 我代表集团 代表学院

[6.86s -> 9.74s] 对大家的加入表示由衷的感谢

[9.74s -> 13.06s] 在此呢 也希望大家能够在这个频道当中

[13.06s -> 15.54s] 都能够学有所成 更进一步

[15.54s -> 19.18s] 在成就格莱美的同时 也成就我们自己

[19.18s -> 23.44s] 那很荣幸 能够作为第一堂课的主讲师

[23.44s -> 26.74s] 我是赵晨 也是我们学院的负责人

[26.74s -> 30.56s] 那今天呢 就由我来给大家讲解

[30.56s -> 32.76s] 我们格莱美的企业文化

[32.76s -> 35.56s] 那在讲解之前 也希望呢

[35.56s -> 37.66s] 大家能够带着以下几个问题

[37.66s -> 40.44s] 来学习今天的整个课程

[40.44s -> 44.50s] 首先第一个 是我们格莱美是做什么的

[44.50s -> 48.08s] 第二个 是我们格莱美的整个发展历程

[48.08s -> 49.52s] 是什么样的

[49.52s -> 52.52s] 那第三个 是我们格莱美拥有着

[52.52s -> 56.02s] 一个什么样的企业使命 愿景 价值观
[56.02s -> 56.72s] 啊
[56.72s -> 61.16s] 那第四个 是我们的行动准则是什么
[61.16s -> 63.50s] 那第五个呢 是我们格莱美
[63.50s -> 67.16s] 在从业十年的这样一个从业时间
[67.16s -> 69.24s] 我们获得了哪些荣誉
[69.24s -> 73.04s] 那希望呢 大家能够带着以下的问题
[73.04s -> 76.26s] 来开始我们今天的整个课程的学习
[76.26s -> 78.80s] 我们开始整个企业文化的讲解
[78.80s -> 81.24s] 我们今天会从四个大板块
[81.24s -> 83.90s] 来给大家诠释我们格莱美的企业文化
[83.90s -> 86.54s] 第一个 是关于我们格莱美
[86.72s -> 90.98s] 第二个 也是我们企业文化当中最核心的部分
[90.98s -> 93.14s] 企业文化的介绍
[93.14s -> 94.46s] 第三个 是学院风采
[94.46s -> 95.74s] 第四个 是荣誉基地
[95.74s -> 100.70s] 也是我们从业近十年所获得的荣誉的展示
[102.14s -> 104.94s] 首先第一个 是关于我们格莱美
[104.94s -> 107.42s] 那这张的重点内容呢
[107.42s -> 109.84s] 大家很清楚的知道我们是做什么的
[111.30s -> 113.12s] 首先我们格莱美呢
[113.12s -> 115.82s] 是一站式婚礼宴会中心
[116.72s -> 119.22s] 那什么是一站式
[119.22s -> 121.48s] 大家要很清晰的知道这个概念
[121.48s -> 123.54s] 一站式通俗点来讲
[123.54s -> 125.90s] 就是客户选择我们格莱美
[125.90s -> 128.74s] 到她整个的前期的备婚
[128.74s -> 130.54s] 以及婚礼的执行
[130.54s -> 132.94s] 以及婚礼宴会的结束
[132.94s -> 135.40s] 那这期间所产生的服务
[135.40s -> 138.24s] 都是由我们格莱美人
[138.24s -> 141.14s] 所提供的一条龙的服务
[141.14s -> 145.32s] 就是不需要客户再进行自己去联系婚庆啊
[145.32s -> 146.52s] 或者自己去联系大家的婚礼啊
[146.52s -> 148.52s] 自己搭建啊 等等
[148.52s -> 150.52s] 就不需要客户再操心了
[150.52s -> 152.52s] 那所有的这种服务细项
[152.52s -> 154.52s] 都是由我们来完成的
[154.52s -> 156.52s] 那再一个呢
[156.52s -> 158.52s] 我们大家要很清楚的知道
[158.52s -> 160.52s] 那我们格莱美区别于
[160.52s -> 163.52s] 市场上同竞品的这种酒店
[163.52s -> 166.52s] 也就是我们所讲到的心理酒店
[166.52s -> 167.52s] 这种传统的酒店
[167.52s -> 169.52s] 一个区别是什么
[169.52s -> 171.52s] 那像传统的酒店
[171.52s -> 173.52s] 它的整个婚庆现场的布置搭建
[173.52s -> 175.52s] 可能都是需要客户来找到
[176.52s -> 180.52s] 婚庆公司来进行一个搭建的
[180.52s -> 182.52s] 那我们跟同市场上
[182.52s -> 184.52s] 所标榜的一站是
[184.52s -> 185.52s] 婚礼宴会堂
[185.52s -> 186.52s] 婚礼宴会中心
[186.52s -> 188.52s] 它们的区别是什么呢
[188.52s -> 190.52s] 就是
[190.52s -> 192.52s] 你像市场上所标榜的
[192.52s -> 193.52s] 一站是婚礼宴会中心
[193.52s -> 195.52s] 那我们就要看它的执行团队
[195.52s -> 198.52s] 是不是隶属于它们自己的团队
[198.52s -> 200.52s] 你像市场上所
[200.52s -> 204.52s] 大家所熟知的婚礼堂
[204.52s -> 206.52s] 你像这个格洛雅或者是
[206.52s -> 207.52s] 宫廷山羊等等
[207.52s -> 209.52s] 那么它的整个执行团队
[209.52s -> 211.52s] 像宴会执行团队
[211.52s -> 213.52s] 包括婚礼策划团队
[213.52s -> 215.52s] 以及它的整个除证
[215.52s -> 216.52s] 出品团队
[216.52s -> 218.52s] 都是嫁接在第三方
[218.52s -> 221.52s] 这样的一个合作的这种形式
[221.52s -> 223.52s] 那你像我们格莱美
[223.52s -> 226.52s] 它就是真正意义上的一站是
[226.52s -> 227.52s] 婚礼宴会中心
[227.52s -> 229.52s] 因为所有的执行团队
[229.52s -> 231.52s] 都是我们格莱美人
[231.52s -> 233.52s] 都是我们自己的团队
[233.52s -> 235.52s] 所以这一块也是我们
[235.52s -> 237.52s] 整个区别于
[237.52s -> 240.52s] 同市场上的一些同竞品
[240.52s -> 242.52s] 那再一个也是我们的
[242.52s -> 244.52s] 最大的一个优势
[244.52s -> 246.52s] 所以这一块大家要很清楚
[246.52s -> 248.52s] 什么是一站式
[248.52s -> 250.52s] 那再一个大家要很清楚的知道
[250.52s -> 253.52s] 我们品牌成立的时间
[253.52s -> 255.52s] 早在我们2013年
[255.52s -> 257.52s] 我们的品牌是在香港
[257.52s -> 259.52s] 已经完成了注册
[259.52s -> 261.52s] 那在2014年
[261.52s -> 263.52s] 我们选择了具有
[263.52s -> 267.52s] 深厚的文化底蕴的城市苏州
[267.52s -> 271.52s] 同时我们苏州也拥有着苏氏浪漫
[271.52s -> 274.52s] 这样的一座历史名城
[274.52s -> 276.52s] 那么我们的第一家店
[276.52s -> 279.52s] 东泰湖店坐落于苏州的吴江
[279.52s -> 282.52s] 这部分我们在讲到
[282.52s -> 284.52s] 企业的发展历程的时候
[284.52s -> 287.52s] 我们会给大家进行着重的讲解
[287.52s -> 288.52s] 所以这一章里面
[288.52s -> 290.52s] 大家清楚的两个点
[290.52s -> 292.52s] 第一个是成立的时间
[292.52s -> 296.52s] 第二个就是我们是做什么的
[296.52s -> 299.52s] 第三是一站式的概念
[299.52s -> 301.52s] 以及我们区别于
[301.52s -> 304.52s] 同市场上传统的酒店
[304.52s -> 307.52s] 以及同竞品的这种标榜的
[307.52s -> 310.52s] 一站式婚礼堂的区别的这些知识点
[310.52s -> 312.52s] 大家一定要很清晰的知道
[312.52s -> 314.52s] 再一个接下来往下讲
[314.52s -> 317.52s] 就是讲到我们格兰美品牌的
[317.52s -> 320.52s] 创始人高宾高总
[320.52s -> 321.52s] 为什么要讲
[321.52s -> 323.52s] 为什么要讲我们董事长呢
[323.52s -> 325.52s] 其实企业文化
"""
if __name__ == '__main__':
    file_name = r'C:\Users\lawrence\Videos\yunyin.mp4'
    fileInfo = "格莱美"
    Summary = stepSummaryWorker(file_name)
    sumText = crack_long_text(text, Summary, file_name, fileInfo)

