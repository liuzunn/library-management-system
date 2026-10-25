package com.library.library.ui;

import com.library.library.entity.Reader;
import com.library.library.service.LibraryService;

import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.SwingUtilities;
import javax.swing.table.DefaultTableModel;
import java.awt.BorderLayout;
import java.awt.FlowLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.util.List;

/** 读者管理选项卡：显示读者列表，并完成录入、修改、删除、查询。 */
public class ReaderPanel extends JPanel {

    private final MainFrame owner;
    private final LibraryService service = new LibraryService();

    private final DefaultTableModel model =
            UIUtil.model("卡号", "姓名", "性别", "单位", "类型", "级别");
    private final JTable table = new JTable(model);

    private final JTextField kwField = new JTextField(18);
    private final JTextField cardField = new JTextField(12);
    private final JTextField nameField = new JTextField(12);
    private final JComboBox<String> genderBox = new JComboBox<>(new String[]{"男", "女"});
    private final JTextField unitField = new JTextField(20);
    private final JComboBox<String> typeBox = new JComboBox<>(new String[]{"学生", "教师", "职工"});
    private final JComboBox<String> gradeBox =
            new JComboBox<>(new String[]{"本科", "硕士", "博士", "教职工"});

    public ReaderPanel(MainFrame owner) {
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
        bar.add(UIUtil.sectionLabel("读者信息管理", UIUtil.PRIMARY));
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
        bar.add(new JLabel("（可按卡号 / 姓名 / 单位 / 类型模糊查询）"));
        return bar;
    }

    private JPanel buildForm() {
        JPanel wrap = new JPanel(new BorderLayout());
        wrap.setBorder(BorderFactory.createTitledBorder("读者信息录入 / 修改 / 删除"));

        JPanel form = new JPanel(new GridBagLayout());
        GridBagConstraints c = new GridBagConstraints();
        c.insets = new Insets(3, 5, 3, 5);
        c.anchor = GridBagConstraints.WEST;

        c.gridy = 0;
        c.gridx = 0;
        form.add(new JLabel("卡号："), c);
        c.gridx = 1;
        form.add(cardField, c);
        c.gridx = 2;
        form.add(new JLabel("姓名："), c);
        c.gridx = 3;
        form.add(nameField, c);
        c.gridx = 4;
        form.add(new JLabel("性别："), c);
        c.gridx = 5;
        form.add(genderBox, c);

        c.gridy = 1;
        c.gridx = 0;
        form.add(new JLabel("单位："), c);
        c.gridx = 1;
        c.gridwidth = 2;
        c.fill = GridBagConstraints.HORIZONTAL;
        form.add(unitField, c);
        c.gridwidth = 1;
        c.fill = GridBagConstraints.NONE;
        c.gridx = 3;
        form.add(new JLabel("类型："), c);
        c.gridx = 4;
        form.add(typeBox, c);
        c.gridx = 5;
        form.add(new JLabel("级别："), c);
        c.gridx = 6;
        form.add(gradeBox, c);

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

    public void reload() {
        try {
            List<Reader> readers = service.listReaders(kwField.getText());
            SwingUtilities.invokeLater(() -> {
                model.setRowCount(0);
                for (Reader r : readers) {
                    model.addRow(new Object[]{r.getCardNo(), r.getName(), r.getGender(),
                            r.getUnit(), r.getType(), r.getGrade()});
                }
                owner.refreshStatus();
            });
        } catch (Exception ex) {
            UIUtil.error(this, "查询读者失败：\n" + ex.getMessage());
        }
    }

    private void fillForm(int row) {
        cardField.setText(str(row, 0));
        nameField.setText(str(row, 1));
        genderBox.setSelectedItem(str(row, 2));
        unitField.setText(str(row, 3));
        typeBox.setSelectedItem(str(row, 4));
        gradeBox.setSelectedItem(str(row, 5));
    }

    private String str(int row, int col) {
        Object v = model.getValueAt(row, col);
        return v == null ? "" : v.toString();
    }

    private Reader readForm() {
        Reader r = new Reader();
        r.setCardNo(UIUtil.trim(cardField.getText()));
        r.setName(UIUtil.trim(nameField.getText()));
        r.setGender((String) genderBox.getSelectedItem());
        r.setUnit(UIUtil.trim(unitField.getText()));
        r.setType((String) typeBox.getSelectedItem());
        r.setGrade((String) gradeBox.getSelectedItem());
        return r;
    }

    private void doInsert() {
        try {
            service.addReader(readForm());
            UIUtil.info(this, "读者录入成功。");
            clearForm();
            reload();
        } catch (Exception ex) {
            UIUtil.error(this, "录入失败：\n" + ex.getMessage());
        }
    }

    private void doUpdate() {
        try {
            service.modifyReader(readForm());
            UIUtil.info(this, "读者信息修改成功。");
            reload();
        } catch (Exception ex) {
            UIUtil.error(this, "修改失败：\n" + ex.getMessage());
        }
    }

    private void doDelete() {
        String no = UIUtil.trim(cardField.getText());
        if (no.isEmpty()) {
            UIUtil.error(this, "请先在表格中选择要删除的读者。");
            return;
        }
        if (!UIUtil.confirm(this, "确定要删除卡号为 " + no + " 的读者吗？")) {
            return;
        }
        try {
            service.removeReader(no);
            UIUtil.info(this, "读者删除成功。");
            clearForm();
            reload();
        } catch (Exception ex) {
            UIUtil.error(this, "删除失败：\n" + ex.getMessage());
        }
    }

    private void clearForm() {
        cardField.setText("");
        nameField.setText("");
        unitField.setText("");
        genderBox.setSelectedIndex(0);
        typeBox.setSelectedIndex(0);
        gradeBox.setSelectedIndex(0);
        table.clearSelection();
    }
}
