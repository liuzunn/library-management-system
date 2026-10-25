# 软件工程实验 —— 图书管理系统

> 数据库：**MySQL 8.0.44**（库名 `library_db`） · 应用程序：**Java 21 + JDBC + Swing**
> 实验一、实验二、实验三的实验报告均已完成，数据库与程序都已实际运行验证通过。

---

## 目录

| 实验 | 内容 | 报告 |
|---|---|---|
| 实验一 | 建立相关数据库（E-R 图、数据字典、数据流图、建库建表） | `实验报告（上机）-图书管理系统数据库设计.docx / .pdf` |
| 实验二 | 图书管理系统应用程序设计（Java + JDBC + Swing） | `实验报告（上机）-图书管理系统应用程序设计.docx / .pdf` |
| 实验三 | 编码设计（四个信息管理模块代码 + 三角形判定程序与流程图） | `实验报告（上机）-图书管理系统编码设计.docx / .pdf` |

---

## 一、快速开始

```
1. 双击 启动MySQL服务.bat           启动数据库（开机后需要执行一次）
2. 双击 library-app\运行程序.bat     启动图书管理系统
```

数据库连接信息：

| 项目 | 值 |
|---|---|
| 主机 / 端口 | `127.0.0.1:3306` |
| 用户名 | `root` |
| 密码 | 见 `library-app/src/main/resources/db.properties`（不入库，需自行创建） |
| 数据库 | `library_db`（utf8mb4） |

Navicat Premium 17 连接方法：连接 → MySQL → 主机 127.0.0.1、端口 3306、
用户名 root、密码 <见环境变量 LIBRARY_DB_PASSWORD> → 测试连接 → 确定。

---

## 二、实验一  建立相关数据库

### 要求与完成情况

| 实验要求 | 成果 |
|---|---|
| 设计实体-联系图（E-R 图） | 报告图 1、`figures/fig1_er_diagram.png` |
| 用数据字典描述数据元素 | 报告表 1～表 4 |
| 建立图书 / 读者 / 借阅三张表 | `sql/01_create_database.sql` |
| 实现信息录入、删除、修改 | 8 个存储过程 + 功能测试记录 |
| 绘制数据流图 | 报告图 2（顶层图）、图 3（第 1 层展开图） |

### 数据库对象

**基本表**：`book`（图书）、`reader`（读者）、`borrow`（借阅，主键为书号+卡号+借书时间）
**外键**：`fk_borrow_book`、`fk_borrow_reader`
**视图**：`v_borrow_detail`、`v_book_stat`、`v_reader_stat`
**触发器**：`trg_borrow_before_insert`（拒绝重复借出、拒绝还书早于借书）
**存储过程**：`sp_book_insert/update/delete`、`sp_reader_insert/update/delete`、`sp_borrow_book`、`sp_return_book`

数据量：图书 24 种、读者 18 人、借阅记录 128 条。

---

## 三、实验二  图书管理系统应用程序设计

### 技术要点

| 项目 | 说明 |
|---|---|
| 语言 / JDK | Java 21（`JAVA_HOME=D:\Develop\JDK21`） |
| 界面 | Java Swing（`JFrame` + `JTabbedPane` + `JTable`） |
| 数据库访问 | JDBC，驱动 mysql-connector-java 8.0.28 |
| 体系结构 | 表示层 → 业务逻辑层 → 数据访问层 → 数据库层 |
| 代码规模 | 19 个应用源文件（另 2 个测试工具）、物理行 2179 |

### 程序功能

- **图书管理**：图书信息的录入、修改、删除、按书号/书名/作者/出版社模糊查询
- **读者管理**：读者信息的录入、修改、删除、查询（性别/类型/级别用下拉框约束取值）
- **借阅管理**：办理借书、还书，查看借阅明细，可勾选「只显示未归还」
- **统计查询**：借阅排行、读者统计、出版社统计、月度趋势（表格 + Java2D 条形图）

### 与实验一数据库的衔接

程序的写操作全部通过 JDBC 的 `CallableStatement` 调用实验一建立的存储过程，
查询直接使用实验一建立的视图。数据库触发器、外键、主键、ENUM 等完整性约束在
程序中直接体现：非法操作会被数据库拦下，程序把数据库返回的中文消息显示给用户，
例如「该图书尚未归还，不能重复借出」。

### 编译与运行

```
library-app\编译.bat      用 javac 编译并打包（无需联网）
library-app\运行程序.bat   启动程序
```

也可以手工执行：

```powershell
cd library-app
javac -encoding UTF-8 -d target\classes -cp lib\mysql-connector-java-8.0.28.jar @target\sources.txt
jar --create --file target\library-app.jar --main-class com.library.library.App -C target\classes .
java -cp "target\library-app.jar;lib\mysql-connector-java-8.0.28.jar" com.library.library.App
```

> 说明：工程自带 `pom.xml`，可以用 IDE 或 `mvn package` 构建。
> 但在本机当前网络环境下 Maven 中央仓库不可达，因此实际是用 JDK 自带的 javac 编译打包的。

---

## 四、实验三  图书管理系统编码设计

### 必做：三角形判定程序

| 项目 | 成果 |
|---|---|
| 主程序 | `experiment3/src/com/library/triangle/TriangleClassifier.java`（Java 21，控制台） |
| 表驱动测试 | `experiment3/src/com/library/triangle/TriangleTest.java`，22 条用例（等价类 + 边界值） |
| 测试结果 | 22/22 PASS；输入顺序全排列 108/108 一致；validate 与 classify 越界判定 22/22 一致 |
| 程序流程图 | `figures/figB1_triangle_flow.png` / `.pdf`（报告图 1） |
| 运行记录 | `_work/exp3_triangle_test.txt`、`_work/exp3_triangle_demo.txt` |

运行方法：

```powershell
cd experiment3
javac -encoding UTF-8 -d out src\com\library\triangle\*.java
java -cp out com.library.triangle.TriangleClassifier     # 依次输入 3 个整数
java -cp out com.library.triangle.TriangleTest           # 运行 22 条测试
```

退出码：0 正常分类 / 1 输入越界 / 2 输入个数错误 / 3 存在非整数。

### 选作：录入、删除、修改、查询模块代码

报告第四章按“界面事件处理 → 业务逻辑 → 数据访问 → 数据库对象”的调用链，
给出图书信息四个模块的完整代码与说明（读者模块结构相同），并对程序做了回归测试与代码度量。

| 项目 | 成果 |
|---|---|
| 回归测试 | `_work/smoke3.txt`（SmokeTest 输出，末行 SMOKE_OK，三表 24 / 18 / 128，未还 24） |
| 代码度量 | 19 个应用源文件、20 个类、174 个方法、物理行 2179、注释率 4.64%，见 `_work/exp3_code_metrics.json` |
| 度量插图 | `figures/figB2_code_metrics.png` / `.pdf`（报告图 3） |
| 代码评审 | `_work/exp3_code_review.md` |

---

---

## 界面与图表

### 程序界面

![图书管理](screenshots/01-books.png)

![借阅管理](screenshots/03-borrow.png)

![统计查询 · 借阅排行](screenshots/04-stats-ranking.png)

![统计查询 · 月度趋势](screenshots/05-stats-monthly.png)

![触发器拒绝重复借出](screenshots/07-trigger-reject.png)

### 数据库设计

![E-R 图](figures/fig1_er_diagram.png)

![顶层数据流图](figures/fig2_dfd_top.png)

![一层数据流图](figures/fig3_dfd_level1.png)

![关系模式图](figures/fig4_schema.png)

### 程序结构

![系统架构](figures/figA2_architecture.png)

![借阅流程](figures/figA4_flow_borrow.png)

---

## 五、文件说明

```
软工/
├── 实验报告（上机）-图书管理系统数据库设计.docx / .pdf      实验一报告
├── 实验报告（上机）-图书管理系统应用程序设计.docx / .pdf     实验二报告
├── 实验报告（上机）-图书管理系统编码设计.docx / .pdf         实验三报告
├── 启动MySQL服务.bat / 停止MySQL服务.bat                 数据库启停
├── README.md
├── sql/                        实验一：建库脚本与初始化数据
│   ├── 01_create_database.sql
│   └── 02_sample_data.sql
├── figures/                    报告插图（PNG 300dpi + 矢量 PDF）
│   ├── fig1_er_diagram.*           E-R 图
│   ├── fig2_dfd_top.*              顶层数据流图
│   ├── fig3_dfd_level1.*           第 1 层数据流图
│   ├── fig4_schema.*               表结构与外码联系图
│   ├── fig5_stats.*                借阅数据统计分析
│   ├── figA1_function_structure.*  系统功能结构图
│   ├── figA2_architecture.*        程序分层体系结构图
│   ├── figA3_flow_book_insert.*    图书信息录入流程图
│   ├── figA4_flow_borrow.*         借书业务流程图
│   ├── figB1_triangle_flow.*       三角形判定程序流程图（实验三）
│   └── figB2_code_metrics.*        各包代码量构成（实验三）
├── library-app/                实验二：Java 工程
│   ├── pom.xml
│   ├── 编译.bat / 运行程序.bat
│   ├── lib/mysql-connector-java-8.0.28.jar
│   ├── src/main/java/com/library/library/   源代码（19 个 .java）
│   ├── src/main/resources/db.properties  数据库连接配置
│   ├── tools/SmokeTest.java              命令行功能测试
│   └── tools/ScreenShotDriver.java       界面截图工具
├── experiment3/                实验三：三角形判定程序
│   ├── src/com/library/triangle/TriangleClassifier.java   主程序
│   ├── src/com/library/triangle/TriangleTest.java         22 条表驱动测试
│   └── run_demo.ps1                                    管道运行记录脚本
└── scripts/                    全部生成脚本（可复现）
    ├── figstyle.py                 绘图统一样式
    ├── figure_er.py                 E-R 图
    ├── figures_dfd.py               数据流图
    ├── figure_schema.py             表结构图
    ├── figure_stats.py              统计分析图
    ├── figures_app.py               功能结构图、分层体系结构图
    ├── figures_app_flow.py          两张程序流程图
    ├── gen_data.py                  生成初始化数据
    ├── db_stats.py / verify_db.py   统计与验证
    ├── report_helpers.py / make_report.py   实验一报告生成
    ├── make_report2.py              实验二报告生成
    ├── make_report3.py              实验三报告生成
    ├── figures_triangle.py          三角形判定程序流程图
    ├── figure_code_metrics.py       各包代码量构成图
    ├── to_pdf.py                    导出 PDF
    └── make_bat.py                  生成数据库启停脚本
```

---

## 六、提交前请自行补充

1. 实验二、实验三报告的封面已按桌面文件填了**班级学号 XXXXXXXXXX、姓名 XXX**，如有误请修改；
   **实验一报告的这两栏当时留空了，可以照着补上**。
2. 封面「课程名称」填的是 **软件工程**，如实际开课名称不同请改。
3. 「成绩」栏留空，由老师填写。

---

## 七、其他说明

- MySQL 未注册为 Windows 服务（当前账户无管理员权限），所以用 `启动MySQL服务.bat` 启动。
  程序目录 `D:\Develop\MySQL\mysql-8.0.44-winx64`，数据目录 `D:\Develop\MySQL\data`。
- 实验一附录二的 E-R 图中「图书—N—借阅—1—读者」，报告按原样绘制；建表时借阅表主键取
  **（书号, 卡号, 借书时间）** 联合主键，既表达「当前借阅」的 N:1 语义，又保留历史借阅记录。
  详见实验一报告 3.5 节与 5.6 节。
