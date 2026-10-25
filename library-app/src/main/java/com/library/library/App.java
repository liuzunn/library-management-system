package com.library.library;

import com.library.library.ui.MainFrame;

import javax.swing.*;

/**
 * 图书管理系统 程序入口。
 *
 * <p>软件工程实验二：在实验一建立的关系数据库 library_db 之上，
 * 用 Java（JDBC + Swing）实现图书信息、读者信息与借阅信息的管理功能。</p>
 *
 * @author XXX  XXXXXXXXXX
 */
public final class App {

    private App() {
    }

    public static void main(String[] args) {
        // 使用与操作系统一致的外观
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception ignored) {
            // 取不到系统外观时退回默认外观
        }
        // 全局字体，保证中文显示正常
        javax.swing.UIManager.put("Label.font", new java.awt.Font("Microsoft YaHei", java.awt.Font.PLAIN, 13));
        javax.swing.UIManager.put("Button.font", new java.awt.Font("Microsoft YaHei", java.awt.Font.PLAIN, 13));
        javax.swing.UIManager.put("TextField.font", new java.awt.Font("Microsoft YaHei", java.awt.Font.PLAIN, 13));
        javax.swing.UIManager.put("Table.font", new java.awt.Font("Microsoft YaHei", java.awt.Font.PLAIN, 13));
        javax.swing.UIManager.put("TableHeader.font", new java.awt.Font("Microsoft YaHei", java.awt.Font.BOLD, 13));
        javax.swing.UIManager.put("TabbedPane.font", new java.awt.Font("Microsoft YaHei", java.awt.Font.PLAIN, 14));
        javax.swing.UIManager.put("ComboBox.font", new java.awt.Font("Microsoft YaHei", java.awt.Font.PLAIN, 13));
        javax.swing.UIManager.put("Menu.font", new java.awt.Font("Microsoft YaHei", java.awt.Font.PLAIN, 13));

        SwingUtilities.invokeLater(() -> new MainFrame().setVisible(true));
    }
}
