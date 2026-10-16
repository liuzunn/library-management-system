package com.library.entity;

/** 读者实体，对应数据库中的 reader 表。 */
public class Reader {

    private String cardNo;   // 卡号
    private String name;     // 姓名
    private String gender;   // 性别（男 / 女）
    private String unit;     // 单位
    private String type;     // 类型（学生 / 教师 / 职工）
    private String grade;    // 级别（本科 / 硕士 / 博士 / 教职工）

    public Reader() {
    }

    public Reader(String cardNo, String name, String gender, String unit,
                  String type, String grade) {
        this.cardNo = cardNo;
        this.name = name;
        this.gender = gender;
        this.unit = unit;
        this.type = type;
        this.grade = grade;
    }

    public String getCardNo() {
        return cardNo;
    }

    public void setCardNo(String cardNo) {
        this.cardNo = cardNo;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getGender() {
        return gender;
    }

    public void setGender(String gender) {
        this.gender = gender;
    }

    public String getUnit() {
        return unit;
    }

    public void setUnit(String unit) {
        this.unit = unit;
    }

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

    @Override
    public String toString() {
        return cardNo + " " + name;
    }
}
