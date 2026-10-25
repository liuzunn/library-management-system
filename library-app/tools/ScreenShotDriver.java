import com.library.library.ui.MainFrame;

import javax.imageio.ImageIO;
import javax.swing.*;
import javax.swing.border.TitledBorder;
import java.awt.*;
import java.awt.event.KeyEvent;
import java.awt.image.BufferedImage;
import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

/**
 * 界面截图工具（仅用于生成实验报告插图，不属于图书管理系统本身）。
 * 启动主窗口，逐一切换选项卡并用 Robot 截屏。
 */
public class ScreenShotDriver {

    static Robot robot;

    public static void main(String[] args) throws Exception {
        Path out = Paths.get(args[0]);
        Files.createDirectories(out);

        UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        UIManager.put("Label.font", new Font("Microsoft YaHei", Font.PLAIN, 13));
        UIManager.put("Button.font", new Font("Microsoft YaHei", Font.PLAIN, 13));
        UIManager.put("TextField.font", new Font("Microsoft YaHei", Font.PLAIN, 13));
        UIManager.put("Table.font", new Font("Microsoft YaHei", Font.PLAIN, 13));
        UIManager.put("TableHeader.font", new Font("Microsoft YaHei", Font.BOLD, 13));
        UIManager.put("TabbedPane.font", new Font("Microsoft YaHei", Font.PLAIN, 14));
        UIManager.put("ComboBox.font", new Font("Microsoft YaHei", Font.PLAIN, 13));

        robot = new Robot();
        MainFrame frame = new MainFrame();
        SwingUtilities.invokeAndWait(() -> {
            frame.setLocation(30, 30);
            frame.setVisible(true);
        });
        Thread.sleep(3000);

        JTabbedPane tabs = (JTabbedPane) find(frame, JTabbedPane.class);
        String[] names = {"01-图书管理", "02-读者管理", "03-借阅管理"};

        for (int i = 0; i < 3; i++) {
            final int idx = i;
            SwingUtilities.invokeAndWait(() -> tabs.setSelectedIndex(idx));
            Thread.sleep(1400);
            shootWindow(frame, out.resolve(names[i] + ".png"));
            System.out.println("shot " + names[i]);
        }

        // 统计查询：借阅排行
        SwingUtilities.invokeAndWait(() -> tabs.setSelectedIndex(3));
        Thread.sleep(1600);
        shootWindow(frame, out.resolve("04-统计查询-借阅排行.png"));
        System.out.println("shot 04-统计查询-借阅排行");

        // 统计查询：月度借阅趋势
        JButton monthly = findButton(frame, "月度借阅趋势");
        if (monthly != null) {
            SwingUtilities.invokeAndWait(monthly::doClick);
            Thread.sleep(1200);
            shootWindow(frame, out.resolve("05-统计查询-月度趋势.png"));
            System.out.println("shot 05-统计查询-月度趋势");
        }

        // 统计查询：各出版社
        JButton pub = findButton(frame, "各出版社借阅次数");
        if (pub != null) {
            SwingUtilities.invokeAndWait(pub::doClick);
            Thread.sleep(1200);
            shootWindow(frame, out.resolve("06-统计查询-出版社.png"));
            System.out.println("shot 06-统计查询-出版社");
        }

        // 借阅管理：办理借书时触发器拒绝（未归还的图书不能重复借出）
        SwingUtilities.invokeAndWait(() -> tabs.setSelectedIndex(2));
        Thread.sleep(1000);
        JPanel borrowArea = findTitledPanel(frame, "办理借书");
        if (borrowArea != null) {
            List<JTextField> fs = fieldsOf(borrowArea);
            String bookNo = null;
            List<?> open = new com.library.library.service.LibraryService().listOpenLoans();
            if (!open.isEmpty()) {
                bookNo = ((com.library.library.entity.Borrow) open.get(0)).getBookNo();
            }
            final String no = bookNo;
            SwingUtilities.invokeAndWait(() -> {
                if (fs.size() >= 2) {
                    fs.get(0).setText(no);
                    fs.get(1).setText("R0002");
                }
            });
            Thread.sleep(600);
            JButton borrowBtn = findButton(borrowArea, "借 书");
            if (borrowBtn != null) {
                new Thread(borrowBtn::doClick, "clicker").start();
                Thread.sleep(2200);
                shootFull(out.resolve("07-触发器拒绝重复借出.png"));
                System.out.println("shot 07-触发器拒绝重复借出");
                robot.keyPress(KeyEvent.VK_ENTER);
                robot.keyRelease(KeyEvent.VK_ENTER);
                Thread.sleep(800);
            }
        }

        // 借阅管理：只显示未归还
        SwingUtilities.invokeAndWait(() -> tabs.setSelectedIndex(2));
        Thread.sleep(600);
        JCheckBox open2 = (JCheckBox) find(frame, JCheckBox.class);
        if (open2 != null) {
            SwingUtilities.invokeAndWait(() -> open2.setSelected(true));
            Thread.sleep(1200);
            shootWindow(frame, out.resolve("08-借阅管理-未归还清单.png"));
            System.out.println("shot 08-借阅管理-未归还清单");
        }

        System.out.println("DONE");
        System.exit(0);
    }

    static void shootWindow(JFrame frame, Path file) throws Exception {
        Rectangle r = frame.getBounds();
        BufferedImage img = robot.createScreenCapture(r);
        ImageIO.write(img, "png", file.toFile());
    }

    static void shootFull(Path file) throws Exception {
        Rectangle r = new Rectangle(Toolkit.getDefaultToolkit().getScreenSize());
        BufferedImage img = robot.createScreenCapture(r);
        ImageIO.write(img, "png", file.toFile());
    }

    static Component find(Container root, Class<?> type) {
        for (Component c : root.getComponents()) {
            if (type.isInstance(c)) {
                return c;
            }
            if (c instanceof Container cc) {
                Component r = find(cc, type);
                if (r != null) {
                    return r;
                }
            }
        }
        return null;
    }

    static JPanel findTitledPanel(Container root, String title) {
        for (Component c : root.getComponents()) {
            if (c instanceof JPanel p && p.getBorder() instanceof TitledBorder tb
                    && title.equals(tb.getTitle())) {
                return p;
            }
            if (c instanceof Container cc) {
                JPanel r = findTitledPanel(cc, title);
                if (r != null) {
                    return r;
                }
            }
        }
        return null;
    }

    static JButton findButton(Container root, String text) {
        for (Component c : root.getComponents()) {
            if (c instanceof JButton b && text.equals(b.getText())) {
                return b;
            }
            if (c instanceof Container cc) {
                JButton r = findButton(cc, text);
                if (r != null) {
                    return r;
                }
            }
        }
        return null;
    }

    static List<JTextField> fieldsOf(Container root) {
        List<JTextField> list = new ArrayList<>();
        collectFields(root, list);
        return list;
    }

    static void collectFields(Container root, List<JTextField> out) {
        for (Component c : root.getComponents()) {
            if (c instanceof JTextField f) {
                out.add(f);
            }
            if (c instanceof Container cc) {
                collectFields(cc, out);
            }
        }
    }
}
