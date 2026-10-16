package com.library.dao;

import com.library.entity.BookStat;
import com.library.entity.ReaderStat;
import com.library.util.DBUtil;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * 统计查询对象，数据来源为实验一建立的视图
 * v_book_stat、v_reader_stat 以及借阅表的聚合查询。
 */
public class StatDao {

    /** 图书借阅排行（前 n 名）。 */
    public List<BookStat> bookRank(int limit) throws SQLException {
        List<BookStat> list = new ArrayList<>();
        String sql = "SELECT 书号, 书名, 出版社, 借阅次数, 在借数量 FROM v_book_stat"
                + " ORDER BY 借阅次数 DESC, 书号 LIMIT ?";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql)) {
            ps.setInt(1, limit);
            try (ResultSet rs = ps.executeQuery()) {
                while (rs.next()) {
                    BookStat s = new BookStat();
                    s.setBookNo(rs.getString("书号"));
                    s.setTitle(rs.getString("书名"));
                    s.setPublisher(rs.getString("出版社"));
                    s.setBorrowCount(rs.getInt("借阅次数"));
                    s.setOpenCount(rs.getInt("在借数量"));
                    list.add(s);
                }
            }
        }
        return list;
    }

    /** 读者借阅统计（按类型 / 级别）。 */
    public List<ReaderStat> readerStat() throws SQLException {
        List<ReaderStat> list = new ArrayList<>();
        String sql = "SELECT 读者类型, 级别, 读者人数, 借阅总次数, 人均借阅次数"
                + " FROM v_reader_stat ORDER BY 借阅总次数 DESC";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                ReaderStat s = new ReaderStat();
                s.setType(rs.getString("读者类型"));
                s.setGrade(rs.getString("级别"));
                s.setReaderCount(rs.getInt("读者人数"));
                s.setBorrowCount(rs.getInt("借阅总次数"));
                s.setAvgCount(rs.getDouble("人均借阅次数"));
                list.add(s);
            }
        }
        return list;
    }

    /** 各出版社借阅次数。 */
    public Map<String, Integer> publisherStat() throws SQLException {
        Map<String, Integer> map = new LinkedHashMap<>();
        String sql = "SELECT b.publisher AS k, COUNT(*) AS v FROM borrow br"
                + " JOIN book b ON br.book_no = b.book_no"
                + " GROUP BY b.publisher ORDER BY v DESC";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                map.put(rs.getString("k"), rs.getInt("v"));
            }
        }
        return map;
    }

    /** 月度借阅量。 */
    public Map<String, Integer> monthlyStat() throws SQLException {
        Map<String, Integer> map = new LinkedHashMap<>();
        String sql = "SELECT DATE_FORMAT(borrow_date,'%Y-%m') AS k, COUNT(*) AS v"
                + " FROM borrow GROUP BY k ORDER BY k";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                map.put(rs.getString("k"), rs.getInt("v"));
            }
        }
        return map;
    }

    /** 汇总数据量：图书种数、读者人数、借阅记录数、未归还数。 */
    public int[] totals() throws SQLException {
        String sql = "SELECT (SELECT COUNT(*) FROM book), (SELECT COUNT(*) FROM reader),"
                + " (SELECT COUNT(*) FROM borrow), (SELECT COUNT(*) FROM borrow WHERE return_date IS NULL)";
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            if (rs.next()) {
                return new int[]{rs.getInt(1), rs.getInt(2), rs.getInt(3), rs.getInt(4)};
            }
        }
        return new int[]{0, 0, 0, 0};
    }
}
