package com.library.library.ui;

import javax.swing.JPanel;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.util.LinkedHashMap;
import java.util.Map;

/** 用 Java2D 绘制的简单条形图，用于统计结果的图形化显示。 */
public class BarChartPanel extends JPanel {

    private Map<String, Integer> data = new LinkedHashMap<>();
    private String title = "";
    private Color barColor = UIUtil.PRIMARY;

    public BarChartPanel() {
        setBackground(Color.WHITE);
    }

    public void setData(String title, Map<String, Integer> data, Color barColor) {
        this.title = title == null ? "" : title;
        this.data = data == null ? new LinkedHashMap<>() : data;
        this.barColor = barColor == null ? UIUtil.PRIMARY : barColor;
        repaint();
    }

    @Override
    protected void paintComponent(Graphics g) {
        super.paintComponent(g);
        Graphics2D g2 = (Graphics2D) g;
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON);
        g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);

        int w = getWidth();
        int h = getHeight();
        g2.setFont(new Font("Microsoft YaHei", Font.BOLD, 14));
        g2.setColor(new Color(0x0B2E5C));
        g2.drawString(title, 16, 24);

        if (data.isEmpty()) {
            g2.setFont(UIUtil.FONT);
            g2.setColor(Color.GRAY);
            g2.drawString("暂无数据", 16, 52);
            return;
        }

        int left = 60;
        int right = w - 24;
        int top = 48;
        int bottom = h - 40;
        int chartH = bottom - top;

        int max = data.values().stream().mapToInt(Integer::intValue).max().orElse(1);
        if (max <= 0) {
            max = 1;
        }

        g2.setFont(new Font("Microsoft YaHei", Font.PLAIN, 11));
        g2.setStroke(new BasicStroke(1f));
        for (int i = 0; i <= 4; i++) {
            int y = bottom - chartH * i / 4;
            g2.setColor(new Color(0xE8ECF2));
            g2.drawLine(left, y, right, y);
            g2.setColor(new Color(0x7A8699));
            g2.drawString(String.valueOf(max * i / 4), 18, y + 4);
        }

        int n = data.size();
        int slot = Math.max(28, (right - left) / Math.max(1, n));
        int barW = Math.min(60, (int) (slot * 0.62));
        int i = 0;
        FontMetrics fm = g2.getFontMetrics();
        for (Map.Entry<String, Integer> e : data.entrySet()) {
            int cx = left + slot * i + slot / 2;
            int barH = (int) ((long) chartH * e.getValue() / max);
            int x = cx - barW / 2;
            int y = bottom - barH;

            g2.setColor(barColor);
            g2.fillRoundRect(x, y, barW, barH, 6, 6);
            g2.setColor(barColor.darker());
            g2.drawRoundRect(x, y, barW, barH, 6, 6);

            g2.setColor(new Color(0x333333));
            String v = String.valueOf(e.getValue());
            g2.drawString(v, cx - fm.stringWidth(v) / 2, y - 5);

            String label = e.getKey();
            if (fm.stringWidth(label) > slot - 4) {
                while (label.length() > 1 && fm.stringWidth(label + "…") > slot - 4) {
                    label = label.substring(0, label.length() - 1);
                }
                label = label + "…";
            }
            g2.setColor(new Color(0x555555));
            g2.drawString(label, cx - fm.stringWidth(label) / 2, bottom + 16);
            i++;
        }

        g2.setColor(new Color(0xB0B8C4));
        g2.drawLine(left, bottom, right, bottom);
    }
}
