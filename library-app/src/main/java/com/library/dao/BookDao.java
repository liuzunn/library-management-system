package com.library.dao;

import com.library.entity.Book;
import com.library.util.DBUtil;

import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/**
 * 图书数据访问对象。
 *
 * <p>查询使用 PreparedStatement，录入 / 修改 / 删除直接调用实验一中建立的
 * 存储过程 sp_book_insert、sp_book_update、sp_book_delete，
 * 由数据库层负责主键唯一性、外码等完整性检查。</p>
 */
public class BookDao {

    private static final String COLS = "book_no, title, author, price, publisher, summary";

    /** 查询全部图书。 */
    public List<Book> findAll() throws SQLException {
        return search(null);
    }

    /** 按书号 / 书名 / 作者 / 出版社模糊查询。 */
    public List<Book> search(String keyword) throws SQLException {
        boolean has = keyword != null && !keyword.isBlank();
        String sql = "SELECT " + COLS + " FROM book"
                + (has ? " WHERE book_no LIKE ? OR title LIKE ? OR author LIKE ? OR publisher LIKE ?" : "")
                + " ORDER BY book_no";
        List<Book> list = new ArrayList<>();
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            if (has) {
                String like = "%" + keyword.trim() + "%";
                for (int i = 1; i <= 4; i++) {
                    ps.setString(i, like);
                }
            }
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    list.add(map(rs));
                }
            }
        }
        return list;
    }

    /** 录入图书：调用存储过程 sp_book_insert。 */
    public void insert(Book b) throws SQLException {
        try (Connection conn = DBUtil.getConnection();
             CallableStatement cs = conn.prepareCall("{call sp_book_insert(?,?,?,?,?,?)}")) {
            cs.setString(1, b.getBookNo());
            cs.setString(2, b.getTitle());
            cs.setString(3, b.getAuthor());
            cs.setBigDecimal(4, b.getPrice());
            cs.setString(5, b.getPublisher());
            cs.setString(6, b.getSummary());
            cs.execute();
        }
    }

    /** 修改图书：调用存储过程 sp_book_update。 */
    public void update(Book b) throws SQLException {
        try (Connection conn = DBUtil.getConnection();
             CallableStatement cs = conn.prepareCall("{call sp_book_update(?,?,?,?,?,?)}")) {
            cs.setString(1, b.getBookNo());
            cs.setString(2, b.getTitle());
            cs.setString(3, b.getAuthor());
            cs.setBigDecimal(4, b.getPrice());
            cs.setString(5, b.getPublisher());
            cs.setString(6, b.getSummary());
            cs.execute();
        }
    }

    /** 删除图书：调用存储过程 sp_book_delete（图书仍在借阅中时数据库会拒绝）。 */
    public void delete(String bookNo) throws SQLException {
        try (Connection conn = DBUtil.getConnection();
             CallableStatement cs = conn.prepareCall("{call sp_book_delete(?)}")) {
            cs.setString(1, bookNo);
            cs.execute();
        }
    }

    /** 图书总种数。 */
    public int count() throws SQLException {
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement("SELECT COUNT(*) FROM book");
             ResultSet rs = ps.executeQuery()) {
            return rs.next() ? rs.getInt(1) : 0;
        }
    }

    private Book map(ResultSet rs) throws SQLException {
        return new Book(rs.getString("book_no"), rs.getString("title"), rs.getString("author"),
                rs.getBigDecimal("price"), rs.getString("publisher"), rs.getString("summary"));
    }
}
