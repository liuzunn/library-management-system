import os
# -*- coding: utf-8 -*-
"""连接 library_db 执行统计查询, 输出 JSON 供绘图脚本使用。"""
import io
import json
import sys
from pathlib import Path

import pymysql

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

OUT = Path(r"C:\Users\LZ\Desktop\软工\_work\stats.json")

QUERIES = {
    # 各出版社借阅次数
    "publisher": """
        SELECT b.publisher AS k, COUNT(*) AS v
        FROM borrow br JOIN book b ON br.book_no = b.book_no
        GROUP BY b.publisher ORDER BY v DESC""",
    # 月度借阅量
    "monthly": """
        SELECT DATE_FORMAT(borrow_date, '%Y-%m') AS k, COUNT(*) AS v
        FROM borrow GROUP BY k ORDER BY k""",
    # 各读者类型借阅量与人次
    "reader_type": """
        SELECT r.type AS k, COUNT(*) AS v, COUNT(DISTINCT r.card_no) AS n
        FROM borrow br JOIN reader r ON br.card_no = r.card_no
        GROUP BY r.type ORDER BY v DESC""",
    # 读者类型 x 月份
    "type_month": """
        SELECT r.type AS t, DATE_FORMAT(br.borrow_date, '%Y-%m') AS m, COUNT(*) AS n
        FROM borrow br JOIN reader r ON br.card_no = r.card_no
        GROUP BY t, m ORDER BY t, m""",
    # 图书借阅排行
    "top_books": """
        SELECT b.title AS k, COUNT(*) AS v
        FROM borrow br JOIN book b ON br.book_no = b.book_no
        GROUP BY b.book_no, b.title ORDER BY v DESC, b.book_no LIMIT 10""",
    # 未归还按读者类型
    "open_by_type": """
        SELECT r.type AS k, COUNT(*) AS v
        FROM borrow br JOIN reader r ON br.card_no = r.card_no
        WHERE br.return_date IS NULL GROUP BY r.type ORDER BY v DESC""",
    # 总体指标
    "totals": """
        SELECT (SELECT COUNT(*) FROM book) AS books,
               (SELECT COUNT(*) FROM reader) AS readers,
               (SELECT COUNT(*) FROM borrow) AS loans,
               (SELECT COUNT(*) FROM borrow WHERE return_date IS NULL) AS open_loans,
               (SELECT ROUND(AVG(DATEDIFF(return_date, borrow_date)), 1)
                  FROM borrow WHERE return_date IS NOT NULL) AS avg_days,
               (SELECT COUNT(DISTINCT book_no) FROM borrow) AS books_borrowed,
               (SELECT COUNT(DISTINCT card_no) FROM borrow) AS active_readers""",
    # 平均借阅天数按读者类型
    "avg_days_type": """
        SELECT r.type AS k, ROUND(AVG(DATEDIFF(br.return_date, br.borrow_date)), 1) AS v
        FROM borrow br JOIN reader r ON br.card_no = r.card_no
        WHERE br.return_date IS NOT NULL GROUP BY r.type ORDER BY v DESC""",
    # 价格区间分布
    "price_band": """
        SELECT CASE WHEN price < 35 THEN '35元以下'
                    WHEN price < 50 THEN '35-50元'
                    WHEN price < 70 THEN '50-70元'
                    ELSE '70元以上' END AS k,
               COUNT(*) AS v
        FROM book GROUP BY k ORDER BY MIN(price)""",
}

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password=os.environ.get("LIBRARY_DB_PASSWORD", ""),
                       database="library_db", charset="utf8mb4",
                       cursorclass=pymysql.cursors.DictCursor)
data = {}
with conn:
    with conn.cursor() as cur:
        for name, sql in QUERIES.items():
            cur.execute(sql)
            data[name] = cur.fetchall()

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")

for k, v in data.items():
    print("==", k)
    for row in v:
        print("   ", row)
print("saved", OUT)
