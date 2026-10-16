import com.library.entity.Book;
import com.library.entity.BookStat;
import com.library.entity.ReaderStat;
import com.library.service.LibraryService;

import java.math.BigDecimal;
import java.util.Arrays;
import java.util.List;
import java.util.Map;

/** 命令行冒烟测试：验证 JDBC 连接、存储过程调用与视图查询是否正常。 */
public class SmokeTest {

    public static void main(String[] args) throws Exception {
        LibraryService s = new LibraryService();

        System.out.println("总览[图书,读者,借阅,未还] = " + Arrays.toString(s.totals()));
        System.out.println("图书全部     = " + s.listBooks(null).size());
        System.out.println("图书查询'数据' = " + s.listBooks("数据").size());
        System.out.println("读者全部     = " + s.listReaders(null).size());
        System.out.println("借阅明细     = " + s.listBorrows(null).size());
        System.out.println("未归还       = " + s.listOpenLoans().size());

        List<BookStat> rank = s.bookRank(3);
        System.out.println("借阅排行前3  = " + rank.size());
        for (BookStat b : rank) {
            System.out.println("    " + b.getTitle() + " / " + b.getPublisher()
                    + " / 借阅 " + b.getBorrowCount() + " 次 / 在借 " + b.getOpenCount());
        }

        System.out.println("读者统计:");
        for (ReaderStat r : s.readerStat()) {
            System.out.println("    " + r.getType() + " " + r.getGrade() + " 人数=" + r.getReaderCount()
                    + " 借阅=" + r.getBorrowCount() + " 人均=" + r.getAvgCount());
        }

        Map<String, Integer> pub = s.publisherStat();
        System.out.println("出版社种类   = " + pub.size() + " 首位=" + pub.entrySet().iterator().next());
        System.out.println("月度统计     = " + s.monthlyStat());

        // ---- 存储过程：录入 -> 修改 -> 删除 ----
        String no = "B0099";
        s.addBook(new Book(no, "Java核心技术", "Cay S. Horstmann", new BigDecimal("149.00"),
                "机械工业出版社", "Java 平台经典参考书。"));
        System.out.println("录入后查询   = " + s.listBooks(no).size());

        s.modifyBook(new Book(no, "Java核心技术 卷I", "Cay S. Horstmann", new BigDecimal("159.00"),
                "机械工业出版社", "第12版，覆盖 Java 17 特性。"));
        Book b = s.listBooks(no).get(0);
        System.out.println("修改后       = " + b.getTitle() + " / " + b.getPrice());

        // ---- 触发器：把尚未归还的图书再次借出，应被数据库拒绝 ----
        String[] open = {"", ""};
        for (var o : s.listOpenLoans()) {
            open[0] = o.getBookNo();
            open[1] = o.getCardNo();
            break;
        }
        try {
            s.borrowBook(open[0], "R0002", null);
            System.out.println("触发器测试   = 未生效（异常！）");
        } catch (Exception e) {
            System.out.println("触发器拦截   = " + e.getMessage());
        }

        // ---- 主键冲突 ----
        try {
            s.addBook(new Book("B0001", "重复书号", "测试", new BigDecimal("1"), "测试", ""));
            System.out.println("主键测试     = 未生效（异常！）");
        } catch (Exception e) {
            System.out.println("主键拦截     = " + e.getMessage());
        }

        s.removeBook(no);
        System.out.println("删除后查询   = " + s.listBooks(no).size());
        System.out.println("总览[图书,读者,借阅,未还] = " + Arrays.toString(s.totals()));
        System.out.println("SMOKE_OK");
    }
}
