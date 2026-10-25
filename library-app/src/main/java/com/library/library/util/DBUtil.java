package com.library.library.util;

import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Properties;

/**
 * JDBC 连接管理工具类。
 *
 * <p>从 classpath 下的 db.properties 读取连接参数，加载驱动并对外提供
 * {@link #getConnection()}。所有 DAO 都通过它取得数据库连接。</p>
 */
public final class DBUtil {

    private static final Properties CFG = new Properties();

    static {
        try (InputStream in = DBUtil.class.getClassLoader().getResourceAsStream("db.properties")) {
            if (in == null) {
                throw new IllegalStateException("找不到配置文件 db.properties");
            }
            CFG.load(new java.io.InputStreamReader(in, java.nio.charset.StandardCharsets.UTF_8));
            Class.forName(CFG.getProperty("jdbc.driver"));
        } catch (Exception e) {
            throw new ExceptionInInitializerError("数据库驱动初始化失败：" + e.getMessage());
        }
    }

    private DBUtil() {
    }

    /** 取得一个数据库连接。 */
    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(
                CFG.getProperty("jdbc.url"),
                CFG.getProperty("jdbc.username"),
                CFG.getProperty("jdbc.password"));
    }

    /** 连接串（不含口令），用于界面状态栏显示。 */
    public static String getUrl() {
        return CFG.getProperty("jdbc.url");
    }

    public static String getUsername() {
        return CFG.getProperty("jdbc.username");
    }

    /** 静默关闭资源。 */
    public static void close(ResultSet rs, Statement st, Connection conn) {
        if (rs != null) {
            try {
                rs.close();
            } catch (SQLException ignored) {
            }
        }
        if (st != null) {
            try {
                st.close();
            } catch (SQLException ignored) {
            }
        }
        if (conn != null) {
            try {
                conn.close();
            } catch (SQLException ignored) {
            }
        }
    }

    public static void close(Statement st, Connection conn) {
        close(null, st, conn);
    }
}
