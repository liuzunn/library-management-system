package com.library.dao;

import com.library.entity.Borrow;
import com.library.util.DBUtil;

import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.Date;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.time.LocalDate;
import java.util.ArrayList;
import java.util.List;

/**
 * 借阅数据访问对象。
 *
 * <p>借书、还书调用存储过程 sp_borrow_book / sp_return_book；
 * 查询直接使用实验一建立的视图 v_borrow_detail。</p>
 */
public class BorrowDao {

    private static final String DETAIL_COLS =
            "书号, 书名, 作者, 出版社, 卡号, 姓名, 读者类型, 级别, 借书时间, 还书时间, 状态, 借阅天数";

    /** 借书。 */
    public void borrow(String bookNo, String cardNo, LocalDate date) throws SQLException {
        try (Connection conn = DBUtil.getConnection();
             CallableStatement cs = conn.prepareCall("{call sp_borrow_book(?,?,?)}")) {
            cs.setString(1, bookNo);
            cs.setString(2, cardNo);
            cs.setDate(3, Date.valueOf(date));
            cs.execute();
        }
    }

    /** 还书。 */
    public void giveBack(String bookNo, String cardNo, LocalDate date) throws SQLException {
        try (Connection conn = DBUtil.getConnection();
             CallableStatement cs = conn.prepareCall("{call sp_return_book(?,?,?)}")) {
            cs.setString(1, bookNo);
            cs.setString(2, cardNo);
            cs.setDate(3, Date.valueOf(date));
            cs.execute();
        }
    }

    /** 全部借阅明细（借用视图 v_borrow_detail）。 */
    public List<Borrow> findDetails() throws SQLException {
        return query("SELECT " + DETAIL_COLS + " FROM v_borrow_detail ORDER BY 借书时间 DESC", null);
    }

    /** 按书号 / 卡号 / 姓名模糊查询借阅明细。 */
    public List<Borrow> searchDetails(String keyword) throws SQLException {
        if (keyword == null || keyword.isBlank()) {
            return findDetails();
        }
        return query("SELECT " + DETAIL_COLS + " FROM v_borrow_detail"
                        + " WHERE 书号 LIKE ? OR 书名 LIKE ? OR 卡号 LIKE ? OR 姓名 LIKE ?"
                        + " ORDER BY 借书时间 DESC",
                "%" + keyword.trim() + "%");
    }

    /** 尚未归还的借阅记录。 */
    public List<Borrow> findOpenLoans() throws SQLException {
        return query("SELECT " + DETAIL_COLS + " FROM v_borrow_detail"
                + " WHERE 还书时间 IS NULL ORDER BY 借书时间", null);
    }

    public int countAll() throws SQLException {
        return count("SELECT COUNT(*) FROM borrow");
    }

    public int countOpen() throws SQLException {
        return count("SELECT COUNT(*) FROM borrow WHERE return_date IS NULL");
    }

    private int count(String sql) throws SQLException {
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            return rs.next() ? rs.getInt(1) : 0;
        }
    }

    private List<Borrow> query(String sql, String like) throws SQLException {
        List<Borrow> list = new ArrayList<>();
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            if (like != null) {
                for (int i = 1; i <= 4; i++) {
                    ps.setString(i, like);
                }
            }
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    Borrow b = new Borrow();
                    b.setBookNo(rs.getString("书号"));
                    b.setTitle(rs.getString("书名"));
                    b.setAuthor(rs.getString("作者"));
                    b.setPublisher(rs.getString("出版社"));
                    b.setCardNo(rs.getString("卡号"));
                    b.setName(rs.getString("姓名"));
                    b.setReaderType(rs.getString("读者类型"));
                    b.setGrade(rs.getString("级别"));
                    Date bd = rs.getDate("借书时间");
                    Date rd = rs.getDate("还书时间");
                    b.setBorrowDate(bd == null ? null : bd.toLocalDate());
                    b.setReturnDate(rd == null ? null : rd.toLocalDate());
                    b.setStatus(rs.getString("状态"));
                    b.setDays(rs.getInt("借阅天数"));
                    list.add(b);
                }
            }
        }
        return list;
    }
}
