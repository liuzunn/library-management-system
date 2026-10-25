package com.library.library.dao;

import com.library.library.entity.Reader;
import com.library.library.util.DBUtil;

import java.sql.CallableStatement;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;

/**
 * 读者数据访问对象，录入 / 修改 / 删除分别调用存储过程
 * sp_reader_insert、sp_reader_update、sp_reader_delete。
 */
public class ReaderDao {

    private static final String COLS = "card_no, name, gender, unit, type, grade";

    public List<Reader> findAll() throws SQLException {
        return search(null);
    }

    /** 按卡号 / 姓名 / 单位 / 类型模糊查询。 */
    public List<Reader> search(String keyword) throws SQLException {
        boolean has = keyword != null && !keyword.isBlank();
        String sql = "SELECT " + COLS + " FROM reader"
                + (has ? " WHERE card_no LIKE ? OR name LIKE ? OR unit LIKE ? OR type LIKE ?" : "")
                + " ORDER BY card_no";
        List<Reader> list = new ArrayList<>();
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

    public void insert(Reader r) throws SQLException {
        try (Connection conn = DBUtil.getConnection();
             CallableStatement cs = conn.prepareCall("{call sp_reader_insert(?,?,?,?,?,?)}")) {
            bind(cs, r);
            cs.execute();
        }
    }

    public void update(Reader r) throws SQLException {
        try (Connection conn = DBUtil.getConnection();
             CallableStatement cs = conn.prepareCall("{call sp_reader_update(?,?,?,?,?,?)}")) {
            bind(cs, r);
            cs.execute();
        }
    }

    public void delete(String cardNo) throws SQLException {
        try (Connection conn = DBUtil.getConnection();
             CallableStatement cs = conn.prepareCall("{call sp_reader_delete(?)}")) {
            cs.setString(1, cardNo);
            cs.execute();
        }
    }

    public int count() throws SQLException {
        try (Connection conn = DBUtil.getConnection();
             PreparedStatement ps = conn.prepareStatement("SELECT COUNT(*) FROM reader");
             ResultSet rs = ps.executeQuery()) {
            return rs.next() ? rs.getInt(1) : 0;
        }
    }

    private void bind(CallableStatement cs, Reader r) throws SQLException {
        cs.setString(1, r.getCardNo());
        cs.setString(2, r.getName());
        cs.setString(3, r.getGender());
        cs.setString(4, r.getUnit());
        cs.setString(5, r.getType());
        cs.setString(6, r.getGrade());
    }

    private Reader map(ResultSet rs) throws SQLException {
        return new Reader(rs.getString("card_no"), rs.getString("name"), rs.getString("gender"),
                rs.getString("unit"), rs.getString("type"), rs.getString("grade"));
    }
}
