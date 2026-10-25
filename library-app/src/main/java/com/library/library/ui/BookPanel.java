package com.library.library.ui;

import com.library.library.entity.Book;
import com.library.library.service.LibraryService;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JScrollPane;
import javax.swing.JTable;
import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableModel;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.util.List;

/** 图书管理选项卡：显示图书列表，并完成录入、修改、删除、查询。 */
public class BookPanel extends JPanel {

    private final MainFrame owner;
    private final LibraryService service = new LibraryService();

    private final DefaultTableModel model =
            UIUtil.model("书号", "书名", "作者", "价格", "出版社", "摘要");
    private final JTable table = new JTable(model);

    private final JTextField kwField = new JTextField(18);
    private final JTextField noField = new JTextField(12);
    private final JTextField titleField = new JTextField(22);
    private final JTextField authorField = new JTextField(14);
    private final JTextField priceField = new JTextField(10);
    private final JTextField pubField = new JTextField(18);
    private final JTextArea summaryArea = new JTextArea(2, 34);

    public BookPanel(MainFrame owner) {
        this.owner = owner;
        setLayout(new BorderLayout(0, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 10, 8, 10));

        add(buildToolbar(), BorderLayout.NORTH);
        add(UIUtil.scroll(table), BorderLayout.CENTER);
        add(buildForm(), BorderLayout.SOUTH);

        table.getSelectionModel().addListSelectionListener(e -> {
            if (!e.getValueIsAdjusting() && table.getSelectedRow() >= 0) {
                fillForm(table.getSelectedRow());
            }
        });
    }

    private JPanel buildToolbar() {
        JPanel bar = new JPanel(new FlowLayout(FlowLayout.LEFT, 8, 4));
        bar.add(UIUtil.sectionLabel("图书信息管理", UIUtil.PRIMARY));
        bar.add(new JLabel("关键字："));
        bar.add(kwField);
        JButton search = new JButton("查 询");
        JButton all = new JButton("显示全部");
        search.addActionListener(e -> reload());
        all.addActionListener(e -> {
            kwField.setText("");
            reload();
        });
        bar.add(search);
        bar.add(all);
        bar.add(new JLabel("（可按书号 / 书名 / 作者 / 出版社模糊查询）"));
        return bar;
    }

    private JPanel buildForm() {
        JPanel wrap = new JPanel(new BorderLayout());
        wrap.setBorder(BorderFactory.createTitledBorder("图书信息录入 / 修改 / 删除"));

        JPanel form = new JPanel(new GridBagLayout());
        GridBagConstraints c = new GridBagConstraints();
        c.insets = new Insets(3, 5, 3, 5);
        c.anchor = GridBagConstraints.WEST;

        addRow(form, c, 0, "书号：", noField, "书名：", titleField);
        addRow(form, c, 1, "作者：", authorField, "价格：", priceField);
        addRow(form, c, 2, "出版社：", pubField, null, null);

        c.gridx = 0;
        c.gridy = 3;
        form.add(new JLabel("摘要："), c);
        c.gridx = 1;
        c.gridwidth = 3;
        c.fill = GridBagConstraints.HORIZONTAL;
        summaryArea.setLineWrap(true);
        summaryArea.setWrapStyleWord(true);
        summaryArea.setFont(UIUtil.FONT);
        JScrollPane sp = new JScrollPane(summaryArea);
        sp.setPreferredSize(new java.awt.Dimension(600, 46));
        form.add(sp, c);

        JPanel buttons = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 6));
        JButton insert = new JButton("录 入");
        JButton update = new JButton("修 改");
        JButton delete = new JButton("删 除");
        JButton clear = new JButton("清 空");
        insert.setForeground(UIUtil.PRIMARY);
        update.setForeground(UIUtil.PRIMARY);
        delete.setForeground(UIUtil.ACCENT);
        insert.addActionListener(e -> doInsert());
        update.addActionListener(e -> doUpdate());
        delete.addActionListener(e -> doDelete());
        clear.addActionListener(e -> clearForm());
        buttons.add(insert);
        buttons.add(update);
        buttons.add(delete);
        buttons.add(clear);

        wrap.add(form, BorderLayout.CENTER);
        wrap.add(buttons, BorderLayout.SOUTH);
        return wrap;
    }

    private void addRow(JPanel form, GridBagConstraints c, int row,
                        String l1, JTextField f1, String l2, JTextField f2) {
        c.gridy = row;
        c.gridwidth = 1;
        c.fill = GridBagConstraints.NONE;
        c.gridx = 0;
        form.add(new JLabel(l1), c);
        c.gridx = 1;
        form.add(f1, c);
        if (l2 != null) {
            c.gridx = 2;
            form.add(new JLabel(l2), c);
            c.gridx = 3;
            form.add(f2, c);
        }
    }

    /** 重新载入表格数据。 */
    public void reload() {
        try {
            List<Book> books = service.listBooks(kwField.getText());
            SwingUtilities.invokeLater(() -> {
                model.setRowCount(0);
                for (Book b : books) {
                    model.addRow(new Object[]{b.getBookNo(), b.getTitle(), b.getAuthor(),
                            b.getPrice(), b.getPublisher(), b.getSummary()});
                }
                owner.refreshStatus();
            });
        } catch (Exception ex) {
            UIUtil.error(this, "查询图书失败：\n" + ex.getMessage());
        }
    }

    private void fillForm(int row) {
        noField.setText(str(row, 0));
        titleField.setText(str(row, 1));
        authorField.setText(str(row, 2));
        priceField.setText(str(row, 3));
        pubField.setText(str(row, 4));
        summaryArea.setText(str(row, 5));
    }

    private String str(int row, int col) {
        Object v = model.getValueAt(row, col);
        return v == null ? "" : v.toString();
    }

    private Book readForm() {
        Book b = new Book();
        b.setBookNo(UIUtil.trim(noField.getText()));
        b.setTitle(UIUtil.trim(titleField.getText()));
        b.setAuthor(UIUtil.trim(authorField.getText()));
        b.setPrice(UIUtil.parsePrice(priceField.getText()));
        b.setPublisher(UIUtil.trim(pubField.getText()));
        b.setSummary(UIUtil.trim(summaryArea.getText()));
        return b;
    }

    private void doInsert() {
        try {
            service.addBook(readForm());
            UIUtil.info(this, "图书录入成功。");
            clearForm();
            reload();
        } catch (Exception ex) {
            UIUtil.error(this, "录入失败：\n" + ex.getMessage());
        }
    }

    private void doUpdate() {
        try {
            service.modifyBook(readForm());
            UIUtil.info(this, "图书信息修改成功。");
            reload();
        } catch (Exception ex) {
            UIUtil.error(this, "修改失败：\n" + ex.getMessage());
        }
    }

    private void doDelete() {
        String no = UIUtil.trim(noField.getText());
        if (no.isEmpty()) {
            UIUtil.error(this, "请先在表格中选择要删除的图书。");
            return;
        }
        if (!UIUtil.confirm(this, "确定要删除书号为 " + no + " 的图书吗？")) {
            return;
        }
        try {
            service.removeBook(no);
            UIUtil.info(this, "图书删除成功。");
            clearForm();
            reload();
        } catch (Exception ex) {
            UIUtil.error(this, "删除失败：\n" + ex.getMessage());
        }
    }

    private void clearForm() {
        noField.setText("");
        titleField.setText("");
        authorField.setText("");
        priceField.setText("");
        pubField.setText("");
        summaryArea.setText("");
        table.clearSelection();
    }
}
