package com.library.ui;

import javax.swing.BorderFactory;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.table.DefaultTableCellRenderer;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.JTableHeader;
import java.awt.Color;
import java.awt.Component;
import java.awt.Font;
import java.math.BigDecimal;

/** 界面公共工具：对话框、表格模型、样式。 */
public final class UIUtil {

    public static final Color PRIMARY = new Color(0x0F4D92);
    public static final Color ACCENT = new Color(0xB64342);
    public static final Font FONT = new Font("Microsoft YaHei", Font.PLAIN, 13);
    public static final Font FONT_BOLD = new Font("Microsoft YaHei", Font.BOLD, 13);

    private UIUtil() {
    }

    public static void info(Component parent, String message) {
        JOptionPane.showMessageDialog(parent, message, "提示", JOptionPane.INFORMATION_MESSAGE);
    }

    public static void error(Component parent, String message) {
        JOptionPane.showMessageDialog(parent, message, "操作失败", JOptionPane.ERROR_MESSAGE);
    }

    public static boolean confirm(Component parent, String message) {
        return JOptionPane.showConfirmDialog(parent, message, "请确认",
                JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE) == JOptionPane.YES_OPTION;
    }

    /** 建一个不可编辑的表格模型。 */
    public static DefaultTableModel model(String... columns) {
        return new DefaultTableModel(columns, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
    }

    /** 统一表格外观。 */
    public static JScrollPane scroll(JTable table) {
        table.setRowHeight(26);
        table.setFont(FONT);
        table.setSelectionBackground(new Color(0xDCE6F1));
        table.setSelectionForeground(Color.BLACK);
        table.setGridColor(new Color(0xE3E8EF));
        table.setShowVerticalLines(false);
        JTableHeader header = table.getTableHeader();
        header.setFont(FONT_BOLD);
        header.setBackground(new Color(0xDCE6F1));
        header.setForeground(new Color(0x0B2E5C));
        header.setReorderingAllowed(false);
        DefaultTableCellRenderer center = new DefaultTableCellRenderer();
        center.setHorizontalAlignment(JLabel.CENTER);
        table.setDefaultRenderer(Object.class, center);
        return new JScrollPane(table);
    }

    /** 带边框标题的小面板标签。 */
    public static JLabel sectionLabel(String text, Color color) {
        JLabel label = new JLabel(text);
        label.setFont(FONT_BOLD);
        label.setForeground(color);
        label.setBorder(BorderFactory.createEmptyBorder(4, 2, 4, 8));
        return label;
    }

    public static String trim(String s) {
        return s == null ? "" : s.trim();
    }

    public static BigDecimal parsePrice(String s) {
        try {
            return new BigDecimal(trim(s).isEmpty() ? "0" : trim(s));
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException("价格必须填写数字，例如 45.00");
        }
    }
}
