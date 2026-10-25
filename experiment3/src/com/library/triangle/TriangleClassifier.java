package com.library.triangle;

import java.util.Scanner;

/**
 * 实验三：三角形判定程序。
 *
 * <p>判定逻辑严格遵循“先输入校验与取值范围、再三角形不等式、最后等边→等腰→一般”的顺序：
 * <ol>
 *   <li>输入个数必须是 3 个，且每个都必须能解析为整数；</li>
 *   <li>三条边都必须落在 [1, 100] 闭区间内；</li>
 *   <li>任意两边之和必须严格大于第三边，否则不构成三角形；</li>
 *   <li>三边全等为等边三角形；恰有两边相等为等腰三角形；三边互不相等为一般三角形。</li>
 * </ol>
 *
 * <p>除了 {@link #main(String[])} 之外，本类还提供 {@link #validate(int, int, int)} 与
 * {@link #classify(int, int, int)} 两个 public static 方法，便于 TriangleTest 直接调用做表驱动测试。
 */
public final class TriangleClassifier {

    /** 边长的下界（含）。 */
    public static final int MIN_SIDE = 1;
    /** 边长的上界（含）。 */
    public static final int MAX_SIDE = 100;

    /** 等边三角形。 */
    public static final String EQUILATERAL = "等边三角形";
    /** 等腰三角形。 */
    public static final String ISOSCELES = "等腰三角形";
    /** 一般三角形。 */
    public static final String SCALENE = "一般三角形";
    /** 不构成三角形。 */
    public static final String NOT_TRIANGLE = "不构成三角形";
    /** 输入越界（边长不在 [1, 100] 内）。 */
    public static final String OUT_OF_RANGE = "输入越界";

    private TriangleClassifier() {
        // 工具类，禁止实例化
    }

    /**
     * 校验三条边的取值范围。
     *
     * @return 三边均落在 [1, 100] 时返回 {@code null}；否则返回第一条越界边的说明文字
     */
    public static String validate(int a, int b, int c) {
        if (a < MIN_SIDE || a > MAX_SIDE) {
            return "边 a=" + a + " 超出 " + MIN_SIDE + "~" + MAX_SIDE + " 范围";
        }
        if (b < MIN_SIDE || b > MAX_SIDE) {
            return "边 b=" + b + " 超出 " + MIN_SIDE + "~" + MAX_SIDE + " 范围";
        }
        if (c < MIN_SIDE || c > MAX_SIDE) {
            return "边 c=" + c + " 超出 " + MIN_SIDE + "~" + MAX_SIDE + " 范围";
        }
        return null;
    }

    /**
     * 判定三条边构成的三角形类型。
     *
     * <p>判定顺序（不可交换）：范围校验 → 三角形不等式 → 等边 → 等腰 → 一般。
     *
     * @return 等边三角形 / 等腰三角形 / 一般三角形 / 不构成三角形 / 输入越界 之一
     */
    public static String classify(int a, int b, int c) {
        // 第一步：范围校验。必须在三角形不等式之前，否则负数、0 等非法输入可能被误判。
        if (validate(a, b, c) != null) {
            return OUT_OF_RANGE;
        }
        // 第二步：三角形不等式。用“和 <= 第三边”判否，可覆盖退化三角形（如 1,2,3）。
        // 采用 long 运算防止极端输入下 int 加法溢出。
        if ((long) a + b <= c || (long) a + c <= b || (long) b + c <= a) {
            return NOT_TRIANGLE;
        }
        // 第三步：等边 → 等腰 → 一般。
        if (a == b && b == c) {
            return EQUILATERAL;
        }
        if (a == b || b == c || a == c) {
            return ISOSCELES;
        }
        return SCALENE;
    }

    /** 命令行入口：从标准输入读取 3 个整数并输出判定结果。 */
    public static void main(String[] args) {
        int[] sides = readThreeIntegers();
        int a = sides[0];
        int b = sides[1];
        int c = sides[2];

        System.out.println("输入：a=" + a + ", b=" + b + ", c=" + c);

        String rangeError = validate(a, b, c);
        if (rangeError != null) {
            System.out.println("输入错误：" + rangeError + "（要求 " + MIN_SIDE + "~" + MAX_SIDE + "）");
            System.exit(1);
        }

        String result = classify(a, b, c);
        System.out.println("判定结果：" + result);
        if (NOT_TRIANGLE.equals(result)) {
            System.out.println("说明：三边不满足任意两边之和大于第三边。");
        }
        System.exit(0);
    }

    /**
     * 用 Scanner 从标准输入读取恰好 3 个整数。
     *
     * <p>出错时打印原因并以非 0 退出码结束：2 = 输入个数不对，3 = 存在非整数。读到合法三边时返回数组。
     */
    private static int[] readThreeIntegers() {
        Scanner scanner = new Scanner(System.in);
        int[] sides = new int[3];
        int count = 0;
        while (count < 3 && scanner.hasNext()) {
            String token = scanner.next();
            try {
                sides[count] = Integer.parseInt(token);
            } catch (NumberFormatException ex) {
                System.out.println("输入错误：\"" + token + "\" 不是整数");
                System.out.println("用法：依次输入 3 个整数 a、b、c（每边 " + MIN_SIDE + "~" + MAX_SIDE + "）");
                System.exit(3);
            }
            count++;
        }
        if (count < 3) {
            System.out.println("输入错误：需要输入 3 个整数（a、b、c），实际只读到 " + count + " 个");
            System.out.println("用法：依次输入 3 个整数 a、b、c（每边 " + MIN_SIDE + "~" + MAX_SIDE + "）");
            System.exit(2);
        }
        if (scanner.hasNext()) {
            String extra = scanner.next();
            System.out.println("输入错误：只需要 3 个整数，多余的输入为 \"" + extra + "\"");
            System.out.println("用法：依次输入 3 个整数 a、b、c（每边 " + MIN_SIDE + "~" + MAX_SIDE + "）");
            System.exit(2);
        }
        return sides;
    }
}
