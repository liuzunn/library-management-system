/* =====================================================================
   实验一  建立相关数据库 —— 图书管理系统
   文件: 01_create_database.sql        数据库: MySQL 8.0.44
   内容: 建立数据库 library_db 及 图书 / 读者 / 借阅 三张基本表,
         并建立索引、外键约束、视图与存储过程。
   ===================================================================== */

DROP DATABASE IF EXISTS library_db;
CREATE DATABASE library_db
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;
USE library_db;

/* ---------------------------------------------------------------------
   1. 图书表  book —— 对应 E-R 图中的实体"图书"
      属性: 书号(主键) 书名 作者 价格 出版社 摘要
   --------------------------------------------------------------------- */
CREATE TABLE book (
    book_no    VARCHAR(20)   NOT NULL                  COMMENT '书号，主键',
    title      VARCHAR(120)  NOT NULL                  COMMENT '书名',
    author     VARCHAR(60)   NOT NULL                  COMMENT '作者',
    price      DECIMAL(8, 2) NOT NULL DEFAULT 0.00     COMMENT '价格(元)',
    publisher  VARCHAR(80)       NULL                  COMMENT '出版社',
    summary    VARCHAR(500)      NULL                  COMMENT '摘要',
    PRIMARY KEY (book_no),
    KEY idx_book_title (title),
    KEY idx_book_publisher (publisher)
) ENGINE = InnoDB COMMENT = '图书(书号,书名,作者,价格,出版社,摘要)';

/* ---------------------------------------------------------------------
   2. 读者表  reader —— 对应 E-R 图中的实体"读者"
      属性: 卡号(主键) 姓名 性别 单位 类型 级别
   --------------------------------------------------------------------- */
CREATE TABLE reader (
    card_no  VARCHAR(20) NOT NULL              COMMENT '卡号，主键',
    name     VARCHAR(30) NOT NULL              COMMENT '姓名',
    gender   ENUM('男','女') NOT NULL DEFAULT '男' COMMENT '性别',
    unit     VARCHAR(80)     NULL              COMMENT '单位',
    type     VARCHAR(20)     NULL              COMMENT '类型(学生/教师/职工)',
    grade    VARCHAR(20)     NULL              COMMENT '级别(本科/硕士/博士/教职工)',
    PRIMARY KEY (card_no),
    KEY idx_reader_name (name),
    KEY idx_reader_type (type)
) ENGINE = InnoDB COMMENT = '读者(卡号,姓名,性别,单位,类型,级别)';

/* ---------------------------------------------------------------------
   3. 借阅表  borrow —— 对应 E-R 图中的联系"借阅"
      属性: 借书时间 还书时间;  外码: 书号 -> book, 卡号 -> reader
      以 (书号,卡号,借书时间) 为联合主键, 既可表达"当前借阅"状态,
      又可完整保留历史借阅记录。
   --------------------------------------------------------------------- */
CREATE TABLE borrow (
    book_no      VARCHAR(20) NOT NULL          COMMENT '书号，外键',
    card_no      VARCHAR(20) NOT NULL          COMMENT '卡号，外键',
    borrow_date  DATE        NOT NULL          COMMENT '借书时间',
    return_date  DATE            NULL          COMMENT '还书时间，NULL 表示尚未归还',
    PRIMARY KEY (book_no, card_no, borrow_date),
    KEY idx_borrow_card (card_no),
    KEY idx_borrow_date (borrow_date),
    CONSTRAINT fk_borrow_book   FOREIGN KEY (book_no) REFERENCES book (book_no)
        ON UPDATE CASCADE ON DELETE RESTRICT,
    CONSTRAINT fk_borrow_reader FOREIGN KEY (card_no) REFERENCES reader (card_no)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = InnoDB COMMENT = '借阅(书号,卡号,借书时间,还书时间)';

/* ---------------------------------------------------------------------
   4. 视图：借阅明细（三表等值连接，用于日常查询与报表输出）
   --------------------------------------------------------------------- */
CREATE OR REPLACE VIEW v_borrow_detail AS
SELECT b.book_no                          AS 书号,
       b.title                            AS 书名,
       b.author                           AS 作者,
       b.publisher                        AS 出版社,
       r.card_no                          AS 卡号,
       r.name                             AS 姓名,
       r.type                             AS 读者类型,
       r.grade                            AS 级别,
       br.borrow_date                     AS 借书时间,
       br.return_date                     AS 还书时间,
       CASE WHEN br.return_date IS NULL THEN '未归还' ELSE '已归还' END AS 状态,
       DATEDIFF(COALESCE(br.return_date, CURDATE()), br.borrow_date)   AS 借阅天数
FROM borrow br
         JOIN book   b ON br.book_no = b.book_no
         JOIN reader r ON br.card_no = r.card_no;

/* ---------------------------------------------------------------------
   5. 视图：图书借阅统计（按书统计借阅次数与在借数量）
   --------------------------------------------------------------------- */
CREATE OR REPLACE VIEW v_book_stat AS
SELECT b.book_no                                                   AS 书号,
       b.title                                                     AS 书名,
       b.publisher                                                 AS 出版社,
       COUNT(br.borrow_date)                                       AS 借阅次数,
       SUM(CASE WHEN br.return_date IS NULL THEN 1 ELSE 0 END)     AS 在借数量
FROM book b
         LEFT JOIN borrow br ON b.book_no = br.book_no
GROUP BY b.book_no, b.title, b.publisher;

/* ---------------------------------------------------------------------
   6. 视图：读者借阅统计（按类型/级别汇总）
   --------------------------------------------------------------------- */
CREATE OR REPLACE VIEW v_reader_stat AS
SELECT r.type                                                      AS 读者类型,
       r.grade                                                     AS 级别,
       COUNT(DISTINCT r.card_no)                                   AS 读者人数,
       COUNT(br.borrow_date)                                       AS 借阅总次数,
       ROUND(COUNT(br.borrow_date) / COUNT(DISTINCT r.card_no), 2) AS 人均借阅次数
FROM reader r
         LEFT JOIN borrow br ON r.card_no = br.card_no
GROUP BY r.type, r.grade;

/* ---------------------------------------------------------------------
   7. 触发器：借书前校验——同一本书若尚未归还，不允许再次借出
   --------------------------------------------------------------------- */
DROP TRIGGER IF EXISTS trg_borrow_before_insert;
DELIMITER $$
CREATE TRIGGER trg_borrow_before_insert
    BEFORE INSERT ON borrow
    FOR EACH ROW
BEGIN
    DECLARE v_out INT DEFAULT 0;
    IF NEW.return_date IS NOT NULL AND NEW.return_date < NEW.borrow_date THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '还书时间不能早于借书时间';
    END IF;
    IF NEW.return_date IS NULL THEN
        SELECT COUNT(*) INTO v_out
        FROM borrow
        WHERE book_no = NEW.book_no AND return_date IS NULL;
        IF v_out > 0 THEN
            SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '该图书尚未归还，不能重复借出';
        END IF;
    END IF;
END$$
DELIMITER ;

/* ---------------------------------------------------------------------
   8. 存储过程：图书信息的录入 / 修改 / 删除
   --------------------------------------------------------------------- */
DROP PROCEDURE IF EXISTS sp_book_insert;
DELIMITER $$
CREATE PROCEDURE sp_book_insert(IN p_no VARCHAR(20), IN p_title VARCHAR(120),
                                IN p_author VARCHAR(60), IN p_price DECIMAL(8, 2),
                                IN p_pub VARCHAR(80), IN p_summary VARCHAR(500))
BEGIN
    INSERT INTO book (book_no, title, author, price, publisher, summary)
    VALUES (p_no, p_title, p_author, p_price, p_pub, p_summary);
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_book_update;
DELIMITER $$
CREATE PROCEDURE sp_book_update(IN p_no VARCHAR(20), IN p_title VARCHAR(120),
                                IN p_author VARCHAR(60), IN p_price DECIMAL(8, 2),
                                IN p_pub VARCHAR(80), IN p_summary VARCHAR(500))
BEGIN
    UPDATE book
    SET title = p_title, author = p_author, price = p_price,
        publisher = p_pub, summary = p_summary
    WHERE book_no = p_no;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_book_delete;
DELIMITER $$
CREATE PROCEDURE sp_book_delete(IN p_no VARCHAR(20))
BEGIN
    IF EXISTS (SELECT 1 FROM borrow WHERE book_no = p_no AND return_date IS NULL) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '该图书仍在借阅中，不能删除';
    END IF;
    DELETE FROM book WHERE book_no = p_no;
END$$
DELIMITER ;

/* ---------------------------------------------------------------------
   9. 存储过程：读者信息的录入 / 修改 / 删除
   --------------------------------------------------------------------- */
DROP PROCEDURE IF EXISTS sp_reader_insert;
DELIMITER $$
CREATE PROCEDURE sp_reader_insert(IN p_card VARCHAR(20), IN p_name VARCHAR(30),
                                  IN p_gender VARCHAR(2), IN p_unit VARCHAR(80),
                                  IN p_type VARCHAR(20), IN p_grade VARCHAR(20))
BEGIN
    INSERT INTO reader (card_no, name, gender, unit, type, grade)
    VALUES (p_card, p_name, p_gender, p_unit, p_type, p_grade);
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_reader_update;
DELIMITER $$
CREATE PROCEDURE sp_reader_update(IN p_card VARCHAR(20), IN p_name VARCHAR(30),
                                  IN p_gender VARCHAR(2), IN p_unit VARCHAR(80),
                                  IN p_type VARCHAR(20), IN p_grade VARCHAR(20))
BEGIN
    UPDATE reader
    SET name = p_name, gender = p_gender, unit = p_unit,
        type = p_type, grade = p_grade
    WHERE card_no = p_card;
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_reader_delete;
DELIMITER $$
CREATE PROCEDURE sp_reader_delete(IN p_card VARCHAR(20))
BEGIN
    IF EXISTS (SELECT 1 FROM borrow WHERE card_no = p_card AND return_date IS NULL) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = '该读者尚有图书未归还，不能删除';
    END IF;
    DELETE FROM reader WHERE card_no = p_card;
END$$
DELIMITER ;

/* ---------------------------------------------------------------------
   10. 存储过程：借书 / 还书
   --------------------------------------------------------------------- */
DROP PROCEDURE IF EXISTS sp_borrow_book;
DELIMITER $$
CREATE PROCEDURE sp_borrow_book(IN p_no VARCHAR(20), IN p_card VARCHAR(20),
                                IN p_date DATE)
BEGIN
    INSERT INTO borrow (book_no, card_no, borrow_date, return_date)
    VALUES (p_no, p_card, IFNULL(p_date, CURDATE()), NULL);
END$$
DELIMITER ;

DROP PROCEDURE IF EXISTS sp_return_book;
DELIMITER $$
CREATE PROCEDURE sp_return_book(IN p_no VARCHAR(20), IN p_card VARCHAR(20),
                                IN p_date DATE)
BEGIN
    UPDATE borrow
    SET return_date = IFNULL(p_date, CURDATE())
    WHERE book_no = p_no AND card_no = p_card AND return_date IS NULL;
END$$
DELIMITER ;

SELECT '数据库 library_db 及全部对象建立完成' AS 执行结果;
SHOW TABLES;
