package com.library.util;

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
            if (in != null) {
                CFG.load(new java.io.InputStreamReader(in, java.nio.charset.StandardCharsets.UTF_8));
            }
            Class.forName(prop("jdbc.driver", "LIBRARY_DB_DRIVER", "com.mysql.cj.jdbc.Driver"));
        } catch (Exception e) {
            throw new ExceptionInInitializerError("数据库驱动初始化失败：" + e.getMessage());
        }
    }

    private DBUtil() {
    }

    /**
     * 取值优先级：环境变量 &gt; db.properties &gt; 内置默认值。
     *
     * <p>口令等敏感项建议通过环境变量注入，不要把真实口令写进 db.properties
     * 并提交到版本库。需要本地文件配置时，复制 db.properties.example 为
     * db.properties（该文件已被 .gitignore 忽略）。</p>
     */
    private static String prop(String key, String envName, String fallback) {
        String v = System.getenv(envName);
        if (v != null && !v.isBlank()) {
            return v;
        }
        v = CFG.getProperty(key);
        return (v != null && !v.isBlank()) ? v : fallback;
    }

    private static String url() {
        return prop("jdbc.url", "LIBRARY_DB_URL",
                "jdbc:mysql://127.0.0.1:3306/library_db?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai");
    }

    private static String username() {
        return prop("jdbc.username", "LIBRARY_DB_USER", "root");
    }

    private static String password() {
        return prop("jdbc.password", "LIBRARY_DB_PASSWORD", "");
    }

    /** 取得一个数据库连接。 */
    public static Connection getConnection() throws SQLException {
        return DriverManager.getConnection(url(), username(), password());
    }

    /** 连接串（不含口令），用于界面状态栏显示。 */
    public static String getUrl() {
        return url();
    }

    public static String getUsername() {
        return username();
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
