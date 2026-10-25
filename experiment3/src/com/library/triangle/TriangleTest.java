package com.library.triangle;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/**
 * 实验三：三角形判定程序的表驱动测试（不依赖 JUnit）。
 *
 * <p>覆盖等价类划分与边界值分析，共 22 条用例；运行后：
 * <ul>
 *   <li>在控制台逐条打印 PASS/FAIL 与汇总；</li>
 *   <li>把同样的记录写入 _work/exp3_triangle_test.txt（UTF-8）；</li>
 *   <li>把用例清单写入 _work/exp3_triangle_cases.json（UTF-8）；</li>
 *   <li>全部通过时以退出码 0 结束，否则以退出码 1 结束。</li>
 * </ul>
 *
 * <p>运行命令：java -cp experiment3/out com.library.triangle.TriangleTest [输出目录]
 */
public final class TriangleTest {

    /** 一条表驱动用例。cover 记录它覆盖的等价类或边界值点。 */
    private record TestCase(String id, int a, int b, int c, String expected, String cover) {
    }

    /** 一条用例的执行结果。 */
    private record TestResult(TestCase testCase, String actual, boolean pass) {
    }

    /** 用例表：等价类 13 条 + 边界值 9 条，合计 22 条。 */
    private static final List<TestCase> CASES = List.of(
            new TestCase("TC01", 5, 5, 5, TriangleClassifier.EQUILATERAL,
                    "等价类：合法输入—三边全等（常规值）"),
            new TestCase("TC02", 1, 1, 1, TriangleClassifier.EQUILATERAL,
                    "边界值：三边均取下界 1"),
            new TestCase("TC03", 100, 100, 100, TriangleClassifier.EQUILATERAL,
                    "边界值：三边均取上界 100"),
            new TestCase("TC04", 5, 5, 8, TriangleClassifier.ISOSCELES,
                    "等价类：合法输入—a=b 的等腰三角形"),
            new TestCase("TC05", 5, 8, 5, TriangleClassifier.ISOSCELES,
                    "等价类：a=c 的等腰三角形（输入顺序无关）"),
            new TestCase("TC06", 8, 5, 5, TriangleClassifier.ISOSCELES,
                    "等价类：b=c 的等腰三角形（输入顺序无关）"),
            new TestCase("TC07", 1, 2, 2, TriangleClassifier.ISOSCELES,
                    "边界值：最短边为 1，1+2>2 恰好成立"),
            new TestCase("TC08", 1, 100, 100, TriangleClassifier.ISOSCELES,
                    "边界值：最短边 1 与两条上界边，1+100>100 成立"),
            new TestCase("TC09", 3, 4, 5, TriangleClassifier.SCALENE,
                    "等价类：合法输入—三边互不相等（典型勾股数）"),
            new TestCase("TC10", 5, 3, 4, TriangleClassifier.SCALENE,
                    "等价类：三边互不相等且输入顺序不同"),
            new TestCase("TC11", 2, 3, 4, TriangleClassifier.SCALENE,
                    "等价类：三边互不相等的较小取值"),
            new TestCase("TC12", 100, 99, 98, TriangleClassifier.SCALENE,
                    "边界值：接近上界的合法一般三角形"),
            new TestCase("TC13", 1, 2, 3, TriangleClassifier.NOT_TRIANGLE,
                    "边界值：a+b=c，退化三角形（经典非三角用例）"),
            new TestCase("TC14", 1, 1, 2, TriangleClassifier.NOT_TRIANGLE,
                    "边界值：等腰退化 a+b=c，不构成三角形"),
            new TestCase("TC15", 1, 2, 4, TriangleClassifier.NOT_TRIANGLE,
                    "等价类：a+b<c，两边之和小于第三边"),
            new TestCase("TC16", 100, 50, 50, TriangleClassifier.NOT_TRIANGLE,
                    "边界值：50+50=100，大数下的退化三角形"),
            new TestCase("TC17", 100, 1, 1, TriangleClassifier.NOT_TRIANGLE,
                    "边界值：两条最短边之和远小于最长边"),
            new TestCase("TC18", 0, 3, 4, TriangleClassifier.OUT_OF_RANGE,
                    "边界值：下边界外一点 0"),
            new TestCase("TC19", 101, 50, 50, TriangleClassifier.OUT_OF_RANGE,
                    "边界值：上边界外一点 101"),
            new TestCase("TC20", -3, 4, 5, TriangleClassifier.OUT_OF_RANGE,
                    "等价类：负整数输入"),
            new TestCase("TC21", 0, 0, 0, TriangleClassifier.OUT_OF_RANGE,
                    "等价类：全零输入"),
            new TestCase("TC22", 100, 100, 1, TriangleClassifier.ISOSCELES,
                    "边界值：两条上界边与最短边 1，构成等腰三角形")
    );

    private TriangleTest() {
        // 测试入口类，禁止实例化
    }

    public static void main(String[] args) throws IOException {
        Path outDir = Paths.get(args.length > 0 ? args[0] : "_work");
        Files.createDirectories(outDir);

        String javaVersion = System.getProperty("java.version");
        String vmName = System.getProperty("java.vm.name");
        String timestamp = LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));

        List<TestResult> results = new ArrayList<>();
        for (TestCase tc : CASES) {
            String actual = TriangleClassifier.classify(tc.a(), tc.b(), tc.c());
            results.add(new TestResult(tc, actual, tc.expected().equals(actual)));
        }

        long passCount = results.stream().filter(TestResult::pass).count();
        long failCount = results.size() - passCount;

        int symmetryChecked = 0;
        int symmetryPass = 0;
        for (TestResult r : results) {
            TestCase tc = r.testCase();
            if (TriangleClassifier.OUT_OF_RANGE.equals(tc.expected())) {
                continue;
            }
            int[][] perms = {{tc.a(), tc.b(), tc.c()}, {tc.a(), tc.c(), tc.b()},
                    {tc.b(), tc.a(), tc.c()}, {tc.b(), tc.c(), tc.a()},
                    {tc.c(), tc.a(), tc.b()}, {tc.c(), tc.b(), tc.a()}};
            for (int[] p : perms) {
                symmetryChecked++;
                if (tc.expected().equals(TriangleClassifier.classify(p[0], p[1], p[2]))) {
                    symmetryPass++;
                }
            }
        }

        int validateChecked = 0;
        int validatePass = 0;
        for (TestResult r : results) {
            TestCase tc = r.testCase();
            validateChecked++;
            boolean outOfRange = TriangleClassifier.OUT_OF_RANGE.equals(tc.expected());
            boolean validateSaysInvalid = TriangleClassifier.validate(tc.a(), tc.b(), tc.c()) != null;
            if (outOfRange == validateSaysInvalid) {
                validatePass++;
            }
        }

        boolean allPass = failCount == 0 && symmetryChecked == symmetryPass && validateChecked == validatePass;

        StringBuilder log = new StringBuilder();
        String rule = "=".repeat(72);
        String thin = "-".repeat(72);
        log.append(rule).append('\n');
        log.append(" 实验三 三角形判定程序 —— 表驱动测试记录（无 JUnit）\n");
        log.append(rule).append('\n');
        log.append("运行环境 : Java ").append(javaVersion).append(" / ").append(vmName).append('\n');
        log.append("测试时间 : ").append(timestamp).append('\n');
        log.append("用例总数 : ").append(results.size()).append('\n');
        log.append(thin).append('\n');
        for (TestResult r : results) {
            TestCase tc = r.testCase();
            log.append('[').append(r.pass() ? "PASS" : "FAIL").append("] ")
                    .append(tc.id())
                    .append("  (a=").append(tc.a())
                    .append(", b=").append(tc.b())
                    .append(", c=").append(tc.c()).append(')')
                    .append("  期望=").append(tc.expected())
                    .append("  实际=").append(r.actual()).append('\n');
            log.append("       覆盖：").append(tc.cover()).append('\n');
        }
        log.append(thin).append('\n');
        log.append(String.format(Locale.ROOT, "用例汇总：共 %d 条，PASS %d 条，FAIL %d 条%n",
                results.size(), passCount, failCount));
        log.append(String.format(Locale.ROOT, "附加校验 1（输入顺序无关性/全排列）：%d/%d 次判定与期望一致%n",
                symmetryPass, symmetryChecked));
        log.append(String.format(Locale.ROOT, "附加校验 2（validate 与 classify 越界判定一致性）：%d/%d 条一致%n",
                validatePass, validateChecked));
        log.append("结论：").append(allPass ? "全部测试通过（退出码 0）" : "存在失败用例（退出码 1）").append('\n');
        log.append(rule).append('\n');

        String text = log.toString();
        Path txtPath = outDir.resolve("exp3_triangle_test.txt");
        Files.writeString(txtPath, text, StandardCharsets.UTF_8);
        Path jsonPath = outDir.resolve("exp3_triangle_cases.json");
        Files.writeString(jsonPath, buildJson(results), StandardCharsets.UTF_8);

        System.out.print(text);
        System.out.println("测试记录已保存: " + txtPath.toAbsolutePath());
        System.out.println("用例清单已保存: " + jsonPath.toAbsolutePath());

        System.exit(allPass ? 0 : 1);
    }

    /** 把用例清单序列化为 JSON 数组（字段：id,a,b,c,expected,actual,pass,cover）。 */
    private static String buildJson(List<TestResult> results) {
        StringBuilder json = new StringBuilder();
        json.append("[\n");
        for (int i = 0; i < results.size(); i++) {
            TestResult r = results.get(i);
            TestCase tc = r.testCase();
            json.append("  {\n");
            json.append("    \"id\": \"").append(escapeJson(tc.id())).append("\",\n");
            json.append("    \"a\": ").append(tc.a()).append(",\n");
            json.append("    \"b\": ").append(tc.b()).append(",\n");
            json.append("    \"c\": ").append(tc.c()).append(",\n");
            json.append("    \"expected\": \"").append(escapeJson(tc.expected())).append("\",\n");
            json.append("    \"actual\": \"").append(escapeJson(r.actual())).append("\",\n");
            json.append("    \"pass\": ").append(r.pass()).append(",\n");
            json.append("    \"cover\": \"").append(escapeJson(tc.cover())).append("\"\n");
            json.append("  }").append(i < results.size() - 1 ? "," : "").append('\n');
        }
        json.append("]\n");
        return json.toString();
    }

    private static String escapeJson(String s) {
        StringBuilder sb = new StringBuilder();
        for (char ch : s.toCharArray()) {
            switch (ch) {
                case '\\' -> sb.append("\\\\");
                case '"' -> sb.append("\\\"");
                case '\n' -> sb.append("\\n");
                case '\r' -> sb.append("\\r");
                case '\t' -> sb.append("\\t");
                default -> sb.append(ch);
            }
        }
        return sb.toString();
    }
}