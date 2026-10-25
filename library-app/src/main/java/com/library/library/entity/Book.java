package com.library.library.entity;

import java.math.BigDecimal;

/** 图书实体，对应数据库中的 book 表。 */
public class Book {

    private String bookNo;      // 书号
    private String title;       // 书名
    private String author;      // 作者
    private BigDecimal price;   // 价格
    private String publisher;   // 出版社
    private String summary;     // 摘要

    public Book() {
    }

    public Book(String bookNo, String title, String author, BigDecimal price,
                String publisher, String summary) {
        this.bookNo = bookNo;
        this.title = title;
        this.author = author;
        this.price = price;
        this.publisher = publisher;
        this.summary = summary;
    }

    public String getBookNo() {
        return bookNo;
    }

    public void setBookNo(String bookNo) {
        this.bookNo = bookNo;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getAuthor() {
        return author;
    }

    public void setAuthor(String author) {
        this.author = author;
    }

    public BigDecimal getPrice() {
        return price;
    }

    public void setPrice(BigDecimal price) {
        this.price = price;
    }

    public String getPublisher() {
        return publisher;
    }

    public void setPublisher(String publisher) {
        this.publisher = publisher;
    }

    public String getSummary() {
        return summary;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    @Override
    public String toString() {
        return bookNo + " " + title;
    }
}
