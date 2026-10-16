package com.library.service;

import com.library.dao.BookDao;
import com.library.dao.BorrowDao;
import com.library.dao.ReaderDao;
import com.library.dao.StatDao;
import com.library.entity.Book;
import com.library.entity.BookStat;
import com.library.entity.Borrow;
import com.library.entity.Reader;
import com.library.entity.ReaderStat;

import java.math.BigDecimal;
import java.sql.SQLException;
import java.time.LocalDate;
import java.util.List;
import java.util.Map;

/**
 * 业务逻辑层。
 *
 * <p>位于表示层（Swing 界面）与数据访问层（DAO）之间：一方面做输入合法性检查，
 * 另一方面把数据库返回的异常转换成对用户友好的提示。界面层不直接接触 SQL。</p>
 */
public class LibraryService {

    private final BookDao bookDao = new BookDao();
    private final ReaderDao readerDao = new ReaderDao();
    private final BorrowDao borrowDao = new BorrowDao();
    private final StatDao statDao = new StatDao();

    /** 业务校验失败时抛出。 */
    public static class BusinessException extends Exception {
        public BusinessException(String message) {
            super(message);
        }
    }

    // ------------------------------------------------------------------ 图书

    public List<Book> listBooks(String keyword) throws SQLException {
        return bookDao.search(keyword);
    }

    public void addBook(Book b) throws SQLException, BusinessException {
        checkBook(b);
        bookDao.insert(b);
    }

    public void modifyBook(Book b) throws SQLException, BusinessException {
        checkBook(b);
        bookDao.update(b);
    }

    public void removeBook(String bookNo) throws SQLException, BusinessException {
        if (isBlank(bookNo)) {
            throw new BusinessException("请先在表格中选择要删除的图书。");
        }
        bookDao.delete(bookNo);
    }

    private void checkBook(Book b) throws BusinessException {
        if (isBlank(b.getBookNo())) {
            throw new BusinessException("书号不能为空。");
        }
        if (isBlank(b.getTitle())) {
            throw new BusinessException("书名不能为空。");
        }
        if (isBlank(b.getAuthor())) {
            throw new BusinessException("作者不能为空。");
        }
        if (b.getPrice() == null || b.getPrice().compareTo(BigDecimal.ZERO) < 0) {
            throw new BusinessException("价格必须是不小于 0 的数字。");
        }
    }

    // ------------------------------------------------------------------ 读者

    public List<Reader> listReaders(String keyword) throws SQLException {
        return readerDao.search(keyword);
    }

    public void addReader(Reader r) throws SQLException, BusinessException {
        checkReader(r);
        readerDao.insert(r);
    }

    public void modifyReader(Reader r) throws SQLException, BusinessException {
        checkReader(r);
        readerDao.update(r);
    }

    public void removeReader(String cardNo) throws SQLException, BusinessException {
        if (isBlank(cardNo)) {
            throw new BusinessException("请先在表格中选择要删除的读者。");
        }
        readerDao.delete(cardNo);
    }

    private void checkReader(Reader r) throws BusinessException {
        if (isBlank(r.getCardNo())) {
            throw new BusinessException("卡号不能为空。");
        }
        if (isBlank(r.getName())) {
            throw new BusinessException("姓名不能为空。");
        }
        if (!"男".equals(r.getGender()) && !"女".equals(r.getGender())) {
            throw new BusinessException("性别只能取“男”或“女”。");
        }
    }

    // ------------------------------------------------------------------ 借阅

    public void borrowBook(String bookNo, String cardNo, LocalDate date)
            throws SQLException, BusinessException {
        if (isBlank(bookNo) || isBlank(cardNo)) {
            throw new BusinessException("借书时书号和卡号都不能为空。");
        }
        borrowDao.borrow(bookNo.trim(), cardNo.trim(), date == null ? LocalDate.now() : date);
    }

    public void returnBook(String bookNo, String cardNo, LocalDate date)
            throws SQLException, BusinessException {
        if (isBlank(bookNo) || isBlank(cardNo)) {
            throw new BusinessException("还书时书号和卡号都不能为空。");
        }
        borrowDao.giveBack(bookNo.trim(), cardNo.trim(), date == null ? LocalDate.now() : date);
    }

    public List<Borrow> listBorrows(String keyword) throws SQLException {
        return borrowDao.searchDetails(keyword);
    }

    public List<Borrow> listOpenLoans() throws SQLException {
        return borrowDao.findOpenLoans();
    }

    // ------------------------------------------------------------------ 统计

    public List<BookStat> bookRank(int limit) throws SQLException {
        return statDao.bookRank(limit);
    }

    public List<ReaderStat> readerStat() throws SQLException {
        return statDao.readerStat();
    }

    public Map<String, Integer> publisherStat() throws SQLException {
        return statDao.publisherStat();
    }

    public Map<String, Integer> monthlyStat() throws SQLException {
        return statDao.monthlyStat();
    }

    public int[] totals() throws SQLException {
        return statDao.totals();
    }

    private static boolean isBlank(String s) {
        return s == null || s.trim().isEmpty();
    }
}
