package com.library.ui;

import com.library.entity.Borrow;
import com.library.service.LibraryService;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableModel;
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.GridLayout;
import java.time.LocalDate;
import java.time.format.DateTimeFormatter;
import java.util.List;

/** 借阅管理选项卡：办理借书、还书，并查看借阅明细。 */
public class BorrowPanel extends JPanel {

    private static final DateTimeFormatter FMT = DateTimeFormatter.ofPattern("yyyy-MM-dd");

    private final MainFrame owner;
    private final LibraryService service = new LibraryService();

    private final DefaultTableModel model = UIUtil.model(
            "书号", "书名", "卡号", "姓名", "读者类型", "借书时间", "还书时间", "状态", "借阅天数");
    private final JTable table = new JTable(model);

    private final JTextField kwField = new JTextField(16);
    private final JCheckBox onlyOpen = new JCheckBox("只显示未归还");

    private final JTextField borrowBook = new JTextField(10);
    private final JTextField borrowCard = new JTextField(10);
    private final JTextField borrowDate = new JTextField(LocalDate.now().format(FMT), 10);
    private final JTextField returnBook = new JTextField(10);
    private final JTextField returnCard = new JTextField(10);
    private final JTextField returnDate = new JTextField(LocalDate.now().format(FMT), 10);

    public BorrowPanel(MainFrame owner) {
        this.owner = owner;
        setLayout(new BorderLayout(0, 6));
        setBorder(BorderFactory.createEmptyBorder(8, 10, 8, 10));

        add(buildToolbar(), BorderLayout.NORTH);
        add(UIUtil.scroll(table), BorderLayout.CENTER);
        add(buildForms(), BorderLayout.SOUTH);
    }

    private JPanel buildToolbar() {
        JPanel bar = new JPanel(new FlowLayout(FlowLayout.LEFT, 8, 4));
        bar.add(UIUtil.sectionLabel("借阅管理", UIUtil.PRIMARY));
        bar.add(new JLabel("关键字："));
        bar.add(kwField);
        JButton search = new JButton("查 询");
        JButton all = new JButton("显示全部");
        search.addActionListener(e -> reload());
        all.addActionListener(e -> {
            kwField.setText("");
            onlyOpen.setSelected(false);
            reload();
        });
        onlyOpen.addActionListener(e -> reload());
        bar.add(search);
        bar.add(all);
        bar.add(onlyOpen);
        return bar;
    }

    private JPanel buildForms() {
        JPanel wrap = new JPanel(new GridLayout(1, 2, 10, 0));

        JPanel bp = new JPanel(new FlowLayout(FlowLayout.LEFT, 6, 8));
        bp.setBorder(BorderFactory.createTitledBorder("办理借书"));
        bp.add(new JLabel("书号："));
        bp.add(borrowBook);
        bp.add(new JLabel("卡号："));
        bp.add(borrowCard);
        bp.add(new JLabel("借书日期："));
        bp.add(borrowDate);
        JButton doBorrow = new JButton("借 书");
        doBorrow.setForeground(UIUtil.PRIMARY);
        doBorrow.addActionListener(e -> doBorrow());
        bp.add(doBorrow);

        JPanel rp = new JPanel(new FlowLayout(FlowLayout.LEFT, 6, 8));
        rp.setBorder(BorderFactory.createTitledBorder("办理还书"));
        rp.add(new JLabel("书号："));
        rp.add(returnBook);
        rp.add(new JLabel("卡号："));
        rp.add(returnCard);
        rp.add(new JLabel("还书日期："));
        rp.add(returnDate);
        JButton doReturn = new JButton("还 书");
        doReturn.setForeground(UIUtil.ACCENT);
        doReturn.addActionListener(e -> doReturn());
        rp.add(doReturn);

        wrap.add(bp);
        wrap.add(rp);
        return wrap;
    }

    public void reload() {
        try {
            List<Borrow> list = onlyOpen.isSelected()
                    ? service.listOpenLoans() : service.listBorrows(kwField.getText());
            SwingUtilities.invokeLater(() -> {
                model.setRowCount(0);
                for (Borrow b : list) {
                    model.addRow(new Object[]{b.getBookNo(), b.getTitle(), b.getCardNo(), b.getName(),
                            b.getReaderType(),
                            b.getBorrowDate() == null ? "" : b.getBorrowDate().format(FMT),
                            b.getReturnDate() == null ? "—" : b.getReturnDate().format(FMT),
                            b.getStatus(), b.getDays()});
                }
                owner.refreshStatus();
            });
        } catch (Exception ex) {
            UIUtil.error(this, "查询借阅记录失败：\n" + ex.getMessage());
        }
    }

    private void doBorrow() {
        try {
            service.borrowBook(borrowBook.getText(), borrowCard.getText(), parseDate(borrowDate.getText()));
            UIUtil.info(this, "借书办理成功。");
            borrowBook.setText("");
            borrowCard.setText("");
            reload();
        } catch (Exception ex) {
            UIUtil.error(this, "借书失败：\n" + ex.getMessage());
        }
    }

    private void doReturn() {
        try {
            service.returnBook(returnBook.getText(), returnCard.getText(), parseDate(returnDate.getText()));
            UIUtil.info(this, "还书办理成功。");
            returnBook.setText("");
            returnCard.setText("");
            reload();
        } catch (Exception ex) {
            UIUtil.error(this, "还书失败：\n" + ex.getMessage());
        }
    }

    private LocalDate parseDate(String text) {
        String s = UIUtil.trim(text);
        if (s.isEmpty()) {
            return LocalDate.now();
        }
        return LocalDate.parse(s, FMT);
    }
}
