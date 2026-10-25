# -*- coding: utf-8 -*-
import os
"""在 library_db 上做功能与完整性测试, 记录真实执行结果供实验报告引用。"""
import io, json, sys
from pathlib import Path
import pymysql

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(r"C:\Users\LZ\Desktop\软工")
OUT = ROOT / "_work" / "verify.json"

conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", password=os.environ.get("LIBRARY_DB_PASSWORD", ""),
                       database="library_db", charset="utf8mb4", autocommit=True)
results = []


def demo(title, sql, params=None, fetch=True, note=None):
    rec = {"title": title, "sql": sql.strip(), "cols": [], "rows": [], "error": None,
           "note": note}
    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            if fetch and cur.description:
                rec["cols"] = [d[0] for d in cur.description]
                rec["rows"] = [[str(v) if v is not None else "NULL" for v in r]
                               for r in cur.fetchall()]
            else:
                rec["rows"] = [["受影响行数: %d" % cur.rowcount]]
    except Exception as e:
        rec["error"] = "%s: %s" % (type(e).__name__, e)
    results.append(rec)
    print("==", title)
    if rec["error"]:
        print("   ERROR:", rec["error"])
    else:
        print("   ", rec["cols"])
        for r in rec["rows"][:8]:
            print("   ", r)
    return rec


demo("1. 查看数据库中已建立的对象", "SHOW TABLES")
demo("2. 图书表结构", "DESCRIBE book")
demo("3. 读者表结构", "DESCRIBE reader")
demo("4. 借阅表结构", "DESCRIBE borrow")
demo("5. 借阅明细视图查询（前 6 行）",
     "SELECT 书号,书名,姓名,读者类型,借书时间,还书时间,状态 FROM v_borrow_detail LIMIT 6")
demo("6. 外键约束定义", """SELECT TABLE_NAME, COLUMN_NAME, CONSTRAINT_NAME,
       REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
FROM information_schema.KEY_COLUMN_USAGE
WHERE TABLE_SCHEMA='library_db' AND REFERENCED_TABLE_NAME IS NOT NULL""")

# ---- 功能测试：录入 ----
demo("7. 功能测试·录入图书（调用 sp_book_insert）",
     "CALL sp_book_insert('B0025','软件测试技术','朱少民',49.00,'人民邮电出版社','系统讲解软件测试方法与用例设计。')",
     fetch=False)
demo("8. 录入结果确认", "SELECT * FROM book WHERE book_no='B0025'")

# ---- 功能测试：修改 ----
demo("9. 功能测试·修改图书（调用 sp_book_update）",
     "CALL sp_book_update('B0025','软件测试技术（第2版）','朱少民',55.00,'人民邮电出版社','第2版新增自动化测试与持续集成内容。')",
     fetch=False)
demo("10. 修改结果确认", "SELECT book_no,title,author,price,publisher FROM book WHERE book_no='B0025'")

# ---- 完整性测试 ----
demo("11. 完整性测试·主键重复（插入已存在的书号）",
     "INSERT INTO book(book_no,title,author,price) VALUES ('B0001','重复书号测试','测试',1.00)",
     fetch=False)
demo("12. 完整性测试·外键约束（借阅不存在的图书）",
     "INSERT INTO borrow(book_no,card_no,borrow_date) VALUES ('B9999','R0001',CURDATE())",
     fetch=False)
demo("13. 完整性测试·ENUM 取值约束（性别填非法值）",
     "INSERT INTO reader(card_no,name,gender) VALUES ('R9999','测试','未知')",
     fetch=False)

# ---- 触发器测试 ----
open_row = None
with conn.cursor() as cur:
    cur.execute("SELECT book_no, card_no, title FROM borrow br JOIN book b USING(book_no) "
                "WHERE return_date IS NULL LIMIT 1")
    open_row = cur.fetchone()
if open_row:
    demo("14. 触发器测试·把尚未归还的图书再次借出（书号 %s）" % open_row[0],
         "CALL sp_borrow_book('%s','R0002',CURDATE())" % open_row[0], fetch=False,
         note="预期被 trg_borrow_before_insert 拒绝")
    demo("15. 触发器测试·还书时间早于借书时间",
         "INSERT INTO borrow(book_no,card_no,borrow_date,return_date) "
         "VALUES ('B0001','R0001','2026-09-10','2026-09-01')", fetch=False,
         note="预期被触发器拒绝")

# ---- 功能测试：删除 ----
demo("16. 功能测试·删除图书（调用 sp_book_delete）",
     "CALL sp_book_delete('B0025')", fetch=False)
demo("17. 删除结果确认（记录数应为 0）",
     "SELECT COUNT(*) AS 剩余记录数 FROM book WHERE book_no='B0025'")

# ---- 统计 ----
demo("18. 数据总量统计", """SELECT (SELECT COUNT(*) FROM book) AS 图书数,
       (SELECT COUNT(*) FROM reader) AS 读者数,
       (SELECT COUNT(*) FROM borrow) AS 借阅记录数,
       (SELECT COUNT(*) FROM borrow WHERE return_date IS NULL) AS 未归还数""")
demo("19. 图书借阅排行（前 8 名）",
     "SELECT 书名, 出版社, 借阅次数, 在借数量 FROM v_book_stat ORDER BY 借阅次数 DESC LIMIT 8")
demo("20. 读者借阅统计",
     "SELECT * FROM v_reader_stat ORDER BY 借阅总次数 DESC")

conn.close()
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
print("saved", OUT)
