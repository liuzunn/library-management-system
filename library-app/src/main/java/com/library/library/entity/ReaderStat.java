package com.library.library.entity;

/** 读者借阅统计，对应视图 v_reader_stat。 */
public class ReaderStat {

    private String type;          // 读者类型
    private String grade;         // 级别
    private int readerCount;      // 读者人数
    private int borrowCount;      // 借阅总次数
    private double avgCount;      // 人均借阅次数

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getGrade() {
        return grade;
    }

    public void setGrade(String grade) {
        this.grade = grade;
    }

    public int getReaderCount() {
        return readerCount;
    }

    public void setReaderCount(int readerCount) {
        this.readerCount = readerCount;
    }

    public int getBorrowCount() {
        return borrowCount;
    }

    public void setBorrowCount(int borrowCount) {
        this.borrowCount = borrowCount;
    }

    public double getAvgCount() {
        return avgCount;
    }

    public void setAvgCount(double avgCount) {
        this.avgCount = avgCount;
    }
}
