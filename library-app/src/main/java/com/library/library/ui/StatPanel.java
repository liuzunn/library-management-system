package com.library.library.ui;

import com.library.library.entity.BookStat;
import com.library.library.entity.ReaderStat;
import com.library.library.service.LibraryService;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JSplitPane;
import javax.swing.JTable;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableModel;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.FlowLayout;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/** 统计查询选项卡：调用实验一建立的视图和聚合查询，输出统计报表与条形图。 */
public class StatPanel extends JPanel {

    private final MainFrame owner;
    private final LibraryService service = new LibraryService();

    private final DefaultTableModel model = UIUtil.model("统计项");
    private final JTable table = new JTable(model);
    private final BarChartPanel chart = new BarChartPanel();
    private final JLabel hint = new JLabel("请选择上方的统计项目。");

    public StatPanel(MainFrame owner) {
        this.owner = owner;
        setLayout(new BorderLayout(0, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 10, 8, 10));

        JPanel bar = new JPanel(new FlowLayout(FlowLayout.LEFT, 8, 4));
        bar.add(UIUtil.sectionLabel("统计查询", UIUtil.PRIMARY));
        bar.add(button("数据总量", e -> showTotals()));
        bar.add(button("图书借阅排行", e -> showBookRank()));
        bar.add(button("读者借阅统计", e -> showReaderStat()));
        bar.add(button("各出版社借阅次数", e -> showPublisher()));
        bar.add(button("月度借阅趋势", e -> showMonthly()));
        bar.add(hint);
        add(bar, BorderLayout.NORTH);

        JSplitPane split = new JSplitPane(JSplitPane.VERTICAL_SPLIT,
                UIUtil.scroll(table), chart);
        split.setResizeWeight(0.46);
        split.setBorder(BorderFactory.createTitledBorder("统计结果"));
        add(split, BorderLayout.CENTER);
    }

    private JButton button(String text, java.awt.event.ActionListener l) {
        JButton b = new JButton(text);
        b.setForeground(UIUtil.PRIMARY);
        b.addActionListener(l);
        return b;
    }

    private void reset(String... columns) {
        model.setColumnCount(0);
        model.setRowCount(0);
        for (String c : columns) {
            model.addColumn(c);
        }
    }

    /** 默认展示图书借阅排行。 */
    public void reload() {
        showBookRank();
    }

    private void showTotals() {
        try {
            int[] t = service.totals();
            reset("统计项", "数值");
            model.addRow(new Object[]{"图书种数", t[0]});
            model.addRow(new Object[]{"读者人数", t[1]});
            model.addRow(new Object[]{"借阅记录数", t[2]});
            model.addRow(new Object[]{"尚未归还数", t[3]});
            Map<String, Integer> m = new LinkedHashMap<>();
            m.put("图书", t[0]);
            m.put("读者", t[1]);
            m.put("借阅", t[2]);
            m.put("未还", t[3]);
            chart.setData("数据总量统计（条）", m, UIUtil.PRIMARY);
            hint.setText("数据来源：book / reader / borrow 三张基本表");
            owner.refreshStatus();
        } catch (Exception ex) {
            UIUtil.error(this, "统计失败：\n" + ex.getMessage());
        }
    }

    private void showBookRank() {
        try {
            List<BookStat> list = service.bookRank(10);
            reset("排名", "书号", "书名", "出版社", "借阅次数", "在借数量");
            Map<String, Integer> m = new LinkedHashMap<>();
            int i = 1;
            for (BookStat s : list) {
                model.addRow(new Object[]{i++, s.getBookNo(), s.getTitle(), s.getPublisher(),
                        s.getBorrowCount(), s.getOpenCount()});
                m.put(s.getTitle(), s.getBorrowCount());
            }
            chart.setData("图书借阅次数排行（前 10 名）", m, UIUtil.PRIMARY);
            hint.setText("数据来源：视图 v_book_stat");
        } catch (Exception ex) {
            UIUtil.error(this, "统计失败：\n" + ex.getMessage());
        }
    }

    private void showReaderStat() {
        try {
            List<ReaderStat> list = service.readerStat();
            reset("读者类型", "级别", "读者人数", "借阅总次数", "人均借阅次数");
            Map<String, Integer> m = new LinkedHashMap<>();
            for (ReaderStat s : list) {
                model.addRow(new Object[]{s.getType(), s.getGrade(), s.getReaderCount(),
                        s.getBorrowCount(), s.getAvgCount()});
                m.put(s.getType() + "·" + s.getGrade(), s.getBorrowCount());
            }
            chart.setData("各类型读者的借阅总次数", m, new Color(0x42949E));
            hint.setText("数据来源：视图 v_reader_stat");
        } catch (Exception ex) {
            UIUtil.error(this, "统计失败：\n" + ex.getMessage());
        }
    }

    private void showPublisher() {
        try {
            Map<String, Integer> all = service.publisherStat();
            reset("排名", "出版社", "借阅次数", "占比");
            int total = all.values().stream().mapToInt(Integer::intValue).sum();
            Map<String, Integer> m = new LinkedHashMap<>();
            int i = 1;
            for (Map.Entry<String, Integer> e : all.entrySet()) {
                String pct = total == 0 ? "0.0%"
                        : String.format("%.1f%%", e.getValue() * 100.0 / total);
                model.addRow(new Object[]{i++, e.getKey(), e.getValue(), pct});
                if (i <= 8) {
                    m.put(e.getKey(), e.getValue());
                }
            }
            chart.setData("各出版社图书借阅次数（前 8 名）", m, new Color(0x8BCF8B));
            hint.setText("数据来源：borrow 与 book 连接后的分组统计");
        } catch (Exception ex) {
            UIUtil.error(this, "统计失败：\n" + ex.getMessage());
        }
    }

    private void showMonthly() {
        try {
            Map<String, Integer> all = service.monthlyStat();
            reset("月份", "借阅次数");
            Map<String, Integer> m = new LinkedHashMap<>();
            for (Map.Entry<String, Integer> e : all.entrySet()) {
                model.addRow(new Object[]{e.getKey(), e.getValue()});
                m.put(e.getKey(), e.getValue());
            }
            chart.setData("月度借阅量变化趋势", m, new Color(0x9A4D8E));
            hint.setText("数据来源：borrow 表按借书时间分组统计");
        } catch (Exception ex) {
            UIUtil.error(this, "统计失败：\n" + ex.getMessage());
        }
    }
}
