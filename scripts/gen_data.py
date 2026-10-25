# -*- coding: utf-8 -*-
"""生成图书管理系统的初始化数据 (sql/02_sample_data.sql)。

采用固定随机种子, 保证结果可复现; 生成过程遵守以下约束:
  * 同一本书在未归还期间不得再次借出 (与触发器 trg_borrow_before_insert 一致);
  * (书号, 卡号, 借书时间) 联合主键不重复;
  * 还书时间不早于借书时间。
"""
import random
from datetime import date, timedelta

random.seed(20260923)

START = date(2026, 3, 1)
TODAY = date(2026, 9, 20)

BOOKS = [
    ("B0001", "数据库系统概论", "王珊", 45.00, "高等教育出版社", "系统介绍关系数据库原理、SQL语言与数据库设计方法。"),
    ("B0002", "软件工程导论", "张海藩", 39.50, "清华大学出版社", "阐述软件生命周期、结构化分析与面向对象方法。"),
    ("B0003", "数据结构(C语言版)", "严蔚敏", 42.00, "清华大学出版社", "线性表、树、图及其经典算法的C语言实现。"),
    ("B0004", "计算机网络", "谢希仁", 49.00, "电子工业出版社", "自底向上讲解物理层至应用层的协议体系。"),
    ("B0005", "操作系统概念", "郑扣根", 68.00, "机械工业出版社", "进程、内存、文件系统与并发控制的经典教材。"),
    ("B0006", "Java编程思想", "Bruce Eckel", 108.00, "机械工业出版社", "面向对象编程思想与Java语言高级特性。"),
    ("B0007", "Python编程从入门到实践", "Eric Matthes", 89.00, "人民邮电出版社", "以项目驱动方式学习Python基础与数据可视化。"),
    ("B0008", "深入理解计算机系统", "Randal Bryant", 139.00, "机械工业出版社", "从程序员视角剖析计算机系统的底层机制。"),
    ("B0009", "人工智能导论", "李德毅", 56.00, "中国科学技术出版社", "介绍知识表示、搜索策略与机器学习基础。"),
    ("B0010", "编译原理", "陈火旺", 45.00, "国防工业出版社", "词法分析、语法分析、语义分析与代码生成。"),
    ("B0011", "数字信号处理", "丁玉美", 41.00, "西安电子科技大学出版社", "离散信号与系统的时域、频域分析方法。"),
    ("B0012", "离散数学", "屈婉玲", 33.00, "高等教育出版社", "集合论、图论、数理逻辑与组合计数。"),
    ("B0013", "高等数学(上册)", "同济大学数学系", 39.80, "高等教育出版社", "极限、导数、微分与不定积分。"),
    ("B0014", "线性代数", "同济大学数学系", 29.60, "高等教育出版社", "行列式、矩阵、向量组与线性方程组。"),
    ("B0015", "概率论与数理统计", "盛骤", 36.50, "高等教育出版社", "随机变量、参数估计与假设检验。"),
    ("B0016", "大学物理(上册)", "马文蔚", 43.00, "高等教育出版社", "力学、热学与波动光学基础。"),
    ("B0017", "西方经济学", "高鸿业", 52.00, "中国人民大学出版社", "微观与宏观经济学的基本原理与分析框架。"),
    ("B0018", "管理学", "斯蒂芬·罗宾斯", 65.00, "中国人民大学出版社", "计划、组织、领导与控制四大管理职能。"),
    ("B0019", "会计学原理", "葛家澍", 44.00, "中国人民大学出版社", "复式记账、凭证账簿与财务报表编制。"),
    ("B0020", "新概念英语(第二册)", "L.G.亚历山大", 35.90, "外语教学与研究出版社", "英语基础语法与听说读写综合训练。"),
    ("B0021", "大学英语精读(第三册)", "董亚芬", 32.00, "上海外语教育出版社", "大学英语精读课程配套教材。"),
    ("B0022", "红楼梦", "曹雪芹", 59.70, "人民文学出版社", "中国古典四大名著之一, 校注本。"),
    ("B0023", "平凡的世界", "路遥", 98.00, "北京十月文艺出版社", "以孙少安兄弟为主线的当代长篇小说。"),
    ("B0024", "活着", "余华", 28.00, "作家出版社", "讲述福贵一生的当代文学代表作。"),
]

READERS = [
    ("R0001", "张伟", "男", "计算机科学与技术学院", "学生", "本科"),
    ("R0002", "李娜", "女", "计算机科学与技术学院", "学生", "硕士"),
    ("R0003", "王强", "男", "软件学院", "学生", "本科"),
    ("R0004", "刘洋", "男", "软件学院", "学生", "硕士"),
    ("R0005", "陈静", "女", "信息科学与工程学院", "学生", "博士"),
    ("R0006", "杨帆", "男", "经济管理学院", "学生", "本科"),
    ("R0007", "赵敏", "女", "经济管理学院", "学生", "硕士"),
    ("R0008", "孙磊", "男", "外国语学院", "学生", "本科"),
    ("R0009", "周婷", "女", "外国语学院", "学生", "本科"),
    ("R0010", "吴超", "男", "理学院", "学生", "硕士"),
    ("R0011", "郑爽", "女", "理学院", "学生", "本科"),
    ("R0012", "冯军", "男", "计算机科学与技术学院", "教师", "教职工"),
    ("R0013", "蒋丽", "女", "软件学院", "教师", "教职工"),
    ("R0014", "韩雪", "女", "经济管理学院", "教师", "教职工"),
    ("R0015", "曹鹏", "男", "图书馆", "职工", "教职工"),
    ("R0016", "谢兰", "女", "信息科学与工程学院", "学生", "博士"),
    ("R0017", "唐宇", "男", "理学院", "学生", "本科"),
    ("R0018", "邓薇", "女", "外国语学院", "教师", "教职工"),
]

# 借阅热度权重: 热门教材/计算机类被借得更多
HOT = {
    "B0001": 5, "B0002": 4, "B0003": 5, "B0004": 4, "B0005": 3, "B0006": 3,
    "B0007": 5, "B0008": 3, "B0009": 4, "B0010": 2, "B0011": 2, "B0012": 3,
    "B0013": 5, "B0014": 5, "B0015": 4, "B0016": 3, "B0017": 4, "B0018": 3,
    "B0019": 2, "B0020": 4, "B0021": 3, "B0022": 2, "B0023": 3, "B0024": 4,
}
book_pool = [b[0] for b in BOOKS for _ in range(HOT[b[0]])]

# 读者活跃度权重: 学生借阅更频繁
READER_W = {
    "学生": 5, "教师": 4, "职工": 3,
}
reader_pool = [r[0] for r in READERS for _ in range(READER_W[r[4]])]
r_type = {r[0]: r[4] for r in READERS}
r_grade = {r[0]: r[5] for r in READERS}

book_free_at = {b[0]: START - timedelta(days=1) for b in BOOKS}  # 该书最早可再借日期
seen = set()
records = []

day = START
while day <= TODAY:
    # 开学季(3月、9月)与考试周(6月)借阅量偏高
    month_factor = {3: 1.45, 4: 1.05, 5: 1.10, 6: 1.40, 7: 0.55, 8: 0.40, 9: 1.30}[day.month]
    n = 0
    for _ in range(4):
        if random.random() < 0.42 * month_factor:
            n += 1
    for _ in range(n):
        for _try in range(14):
            bno = random.choice(book_pool)
            if book_free_at[bno] >= day:
                continue
            rno = random.choice(reader_pool)
            key = (bno, rno, day)
            if key in seen:
                continue
            seen.add(key)
            base = 30 if r_type[rno] == "学生" else 60
            loan = int(random.gauss(base, 12))
            loan = max(7, min(loan, 90))
            ret = day + timedelta(days=loan)
            if ret > TODAY - timedelta(days=6):
                ret = None          # 近期借出且尚未归还
                book_free_at[bno] = date(2030, 1, 1)
            else:
                book_free_at[bno] = ret
            records.append((bno, rno, day, ret))
            break
    day += timedelta(days=1)

records.sort(key=lambda x: (x[2], x[0], x[1]))

lines = []
lines.append("/* =====================================================================")
lines.append("   实验一  建立相关数据库 —— 图书管理系统")
lines.append("   文件: 02_sample_data.sql")
lines.append("   内容: 图书 24 条、读者 18 条、借阅 " + str(len(records)) + " 条初始数据")
lines.append("   ===================================================================== */")
lines.append("")
lines.append("USE library_db;")
lines.append("")
lines.append("SET FOREIGN_KEY_CHECKS = 0;")
lines.append("TRUNCATE TABLE borrow;")
lines.append("TRUNCATE TABLE book;")
lines.append("TRUNCATE TABLE reader;")
lines.append("SET FOREIGN_KEY_CHECKS = 1;")
lines.append("")
lines.append("/* ---------------- 图书表数据 ---------------- */")
lines.append("INSERT INTO book (book_no, title, author, price, publisher, summary) VALUES")
rows = []
for b in BOOKS:
    rows.append("  ('%s', '%s', '%s', %.2f, '%s', '%s')" % b)
lines.append(",\n".join(rows) + ";")
lines.append("")
lines.append("/* ---------------- 读者表数据 ---------------- */")
lines.append("INSERT INTO reader (card_no, name, gender, unit, type, grade) VALUES")
rows = []
for r in READERS:
    rows.append("  ('%s', '%s', '%s', '%s', '%s', '%s')" % r)
lines.append(",\n".join(rows) + ";")
lines.append("")
lines.append("/* ---------------- 借阅表数据 ---------------- */")
lines.append("INSERT INTO borrow (book_no, card_no, borrow_date, return_date) VALUES")
rows = []
for bno, rno, bd, rd in records:
    rd_s = "NULL" if rd is None else "'%s'" % rd.isoformat()
    rows.append("  ('%s', '%s', '%s', %s)" % (bno, rno, bd.isoformat(), rd_s))
for i in range(0, len(rows), 40):
    chunk = rows[i:i + 40]
    lines.append(",\n".join(chunk) + ";")
    if i + 40 < len(rows):
        lines.append("INSERT INTO borrow (book_no, card_no, borrow_date, return_date) VALUES")
lines.append("")
lines.append("SELECT (SELECT COUNT(*) FROM book)   AS 图书数,")
lines.append("       (SELECT COUNT(*) FROM reader) AS 读者数,")
lines.append("       (SELECT COUNT(*) FROM borrow) AS 借阅记录数;")

out = "\n".join(lines) + "\n"
with open(r"C:\Users\LZ\Desktop\软工\sql\02_sample_data.sql", "w", encoding="utf-8") as f:
    f.write(out)

n_open = sum(1 for r in records if r[3] is None)
print("借阅记录:", len(records), " 其中未归还:", n_open)
print("日期范围:", records[0][2], "->", records[-1][2])
