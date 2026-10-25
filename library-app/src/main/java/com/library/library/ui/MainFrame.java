package com.library.library.ui;

import com.library.library.service.LibraryService;
import com.library.library.util.DBUtil;

import javax.swing.BorderFactory;
import javax.swing.Box;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTabbedPane;
import javax.swing.SwingUtilities;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Font;

/** 主窗口：上方标题栏 + 中间四个功能选项卡 + 下方状态栏。 */
public class MainFrame extends JFrame {

    private final LibraryService service = new LibraryService();
    private final JLabel status = new JLabel("正在连接数据库 …");
    private final BookPanel bookPanel;
    private final ReaderPanel readerPanel;
    private final BorrowPanel borrowPanel;
    private final StatPanel statPanel;

    public MainFrame() {
        super("图书管理系统 —— 软件工程实验二");
        setDefaultCloseOperation(EXIT_ON_CLOSE);
        setSize(1250, 810);
        setLocationRelativeTo(null);
        setLayout(new BorderLayout());

        add(buildHeader(), BorderLayout.NORTH);

        bookPanel = new BookPanel(this);
        readerPanel = new ReaderPanel(this);
        borrowPanel = new BorrowPanel(this);
        statPanel = new StatPanel(this);

        JTabbedPane tabs = new JTabbedPane();
        tabs.addTab("  图书管理  ", bookPanel);
        tabs.addTab("  读者管理  ", readerPanel);
        tabs.addTab("  借阅管理  ", borrowPanel);
        tabs.addTab("  统计查询  ", statPanel);
        tabs.addChangeListener(e -> {
            if (tabs.getSelectedComponent() == statPanel) {
                statPanel.reload();
            }
            refreshStatus();
        });
        add(tabs, BorderLayout.CENTER);
        add(buildStatusBar(), BorderLayout.SOUTH);

        SwingUtilities.invokeLater(() -> {
            bookPanel.reload();
            refreshStatus();
        });
    }

    private JPanel buildHeader() {
        JPanel head = new JPanel(new BorderLayout());
        head.setBackground(UIUtil.PRIMARY);
        head.setBorder(BorderFactory.createEmptyBorder(10, 18, 10, 18));

        JLabel title = new JLabel("图书管理系统");
        title.setForeground(Color.WHITE);
        title.setFont(new Font("Microsoft YaHei", Font.BOLD, 21));

        JLabel sub = new JLabel("软件工程实验二 · Java 21 + JDBC + Swing · 数据库 library_db（MySQL 8.0.44）");
        sub.setForeground(new Color(0xD8E4F5));
        sub.setFont(new Font("Microsoft YaHei", Font.PLAIN, 12));

        JPanel left = new JPanel();
        left.setOpaque(false);
        left.setLayout(new javax.swing.BoxLayout(left, javax.swing.BoxLayout.Y_AXIS));
        left.add(title);
        left.add(Box.createVerticalStrut(4));
        left.add(sub);

        head.add(left, BorderLayout.WEST);
        return head;
    }

    private JPanel buildStatusBar() {
        JPanel bar = new JPanel(new BorderLayout());
        bar.setBackground(new Color(0xF1F4F9));
        bar.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createMatteBorder(1, 0, 0, 0, new Color(0xD5DCE6)),
                BorderFactory.createEmptyBorder(5, 14, 5, 14)));
        status.setFont(new Font("Microsoft YaHei", Font.PLAIN, 12));
        status.setForeground(new Color(0x33475B));
        bar.add(status, BorderLayout.WEST);
        return bar;
    }

    /** 重新统计并刷新状态栏。 */
    public void refreshStatus() {
        new Thread(() -> {
            try {
                int[] t = service.totals();
                String text = "数据库 library_db 已连接（" + DBUtil.getUsername() + "@127.0.0.1:3306）"
                        + "    图书 " + t[0] + " 种    读者 " + t[1] + " 人    借阅记录 " + t[2]
                        + " 条（其中未归还 " + t[3] + " 条）";
                SwingUtilities.invokeLater(() -> status.setText(text));
            } catch (Exception e) {
                SwingUtilities.invokeLater(() -> status.setText("数据库连接失败：" + e.getMessage()));
            }
        }, "status-refresh").start();
    }
}
