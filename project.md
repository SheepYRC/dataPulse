DataPulse——本地数据管理系统

---

## 核心架构

为了实现“百万级处理、低开销、易交付”

* **存储引擎：** **DuckDB**。适合单机本地分析的 OLAP 数据库，处理百万级数据仅需毫秒级，且无需安装服务端，直接内嵌在程序中。同时**SQLite**作为OLTP。
* **计算库：** **Polars**。配合 DuckDB 极速处理大规模数据的转换。增加**Pandas**作为协同/备选方案。
* **UI 框架：** **Streamlit**。
* **开发辅助：** uv，pydantic，pydoc-markdown，mkdocs，schemathesis

---

## 功能模块说明书

### 1. 首页：工作看板 (Workboard)

**以任务为中心**的引导页

* **任务卡片：** 支持创建“数据处理流水线”任务，例如“处理 2 月销售报表”，并关联相应的 SQL 脚本。
* **最近访问：** 自动罗列最近查询过的表或最近导出的结果。
* **快捷动作：** 一键清理临时缓存、一键备份当前数据库。

### 2. 数据资产看板 (Data Assets)

**元数据管理**。

* **库容审计：** 不仅看体积，还要展示**压缩比**（DuckDB 这种列式存储的优势）。
* **健康评估：** 识别空值率高的列、重复数据较多的表。
* **活跃度画像：** 通过热力图展示你对哪些表操作最频繁。

### 3. 数据实验室 (SQL Workbench)

**数据交互模块**

* **智能导入：** 自动识别 CSV/Excel 的编码、分隔符和字段类型（尤其是日期格式的自动解析）。
* **混合管理：** 支持常规的 **GUI 交互** 与 **SQL 模式** 并行。
* **分页加载：** 即使是百万级数据，前端也只按配置渲染当前可见的行数，确保界面不卡顿。
* **Schema 预览：** 侧边栏实时展示字段类型、注释、索引情况。

### 4. 历史与快照 (History & Snapshots)

* **查询回溯：** 记录每一条执行过的 SQL，支持一键复用。
* **结果快照：** 对于复杂的耗时查询，支持将结果存为 **.parquet** 临时文件。这样下次查看时无需重新计算，直接读取。
* **版本备注：** 可以给某次查询结果打标签（如：“2024年终最终核算版”）。

### 5. 可视化探索 (Insights Engine)

* **快速绘制：** 根据选择的图表类型自动绘制并提供参数调节，快速调整。
* **交互式看板：** 绘图不仅仅是静态图片，支持缩放、悬停查看数值。
* **导出能力：** 支持将图表导出为高质量的网页 (HTML) 或矢量图 (SVG)，方便放入报告。

---

## 界面增强设计 (UX & Performance)

| 模块 | 专业化改进点 | 目的 |
| --- | --- | --- |
| **底部状态栏** | 增加 **内存占用预警** 与 **磁盘 I/O 监控** | 让用户直观看到“数据量过大”或“读写瓶颈”。 |
| **交付模式** | **绿色单文件部署** (Zero-Config) | 对方收到后双击即可运行，无需配置 Python 环境或数据库。 |
| **全局搜索** | 类似 VS Code 的 `Ctrl+P` 命令面板 | 快速切换页面、搜索表名、搜索历史 SQL。 |

---

## 进阶优化建议

### 数据安全性

* 增加“操作撤销”或“事务回滚”机制，防止 SQL 误删数据。

### 交付便利性

* **环境自检：** 启动时检查剩余磁盘空间，如果空间不足及时提醒。
* **示例数据：** 内置一个 10 万行左右的示例库，方便接收者快速上手功能。


---

## 工程目录结构

```text
dataPulse/
├── .streamlit/                # Streamlit 界面配置 (主题、页面设置)
│   └── config.toml
├── assets/                    # 静态资源 (Logo, 样式表, 示例数据)
│   ├── css/                   # 自定义样式，让 Streamlit 更像原生软件
│   └── samples/               # 内置的 10 万行示例数据 (csv/parquet)
├── changes/                   # 修改记录
│   ├── 20260205-1/            # 某次修改
│   └── ...
├── data/                      # 本地持久化数据 (Git 忽略)
│   ├── datapulse.db           # SQLite: 存储 配置, 日志
│   └── analytics.duckdb       # DuckDB: 存储用户导入的百万级业务数据
├── scripts/                   # 构建与交付脚本
│   └── build.py               # 自动化打包脚本
├── src/                       # 核心源代码
│   ├── __init__.py
│   ├── main.py                # 程序入口 (Streamlit Entry Point)
│   │
│   ├── core/                  # 底层驱动层
│   │   ├── database.py        # 数据库连接池 (DuckDB & SQLite 交互逻辑)
│   │   ├── engine.py          # Polars/Pandas 计算引擎封装
│   │   └── config.py          # 全局配置管理
│   │
│   ├── modules/               # 功能模块层 (对应你的说明书)
│   │   ├── home.py            # 首页：工作看板逻辑
│   │   ├── assets.py          # 数据资产：元数据分析与审计
│   │   ├── workbench.py       # SQL 实验室：查询与导入导出
│   │   ├── history.py         # 历史与快照：快照管理与 .parquet 存储
│   │   └── insights.py        # 可视化探索：绘图组件封装
│   │
│   ├── ui/                    # UI 组件库
│   │   ├── components.py      # 自定义封装的 Streamlit 组件
│   │   └── status_bar.py      # 底部状态栏 (系统性能监控)
│   │
│   └── utils/                 # 通用工具类
│       ├── logger.py          # 日志记录器
│       ├── io_handler.py      # 文件编码自动识别、断点续传逻辑
│       └── metrics.py         # 硬件指标获取 (psutil 封装)
│
├── tests/                     # 单元测试 (百万级数据压力测试)
├── pyproject.toml             # uv/poetry 项目配置文件
└── README.md                  # 项目文档

```

---

## 目录设计要点说明

### 1. 双数据库分离存储 (Core Layer)

* 将 `datapulse.db` (SQLite) 和 `analytics.duckdb` (DuckDB) 分开。
* **理由：** SQLite 处理高频的增删改（Todo、日志）更稳定；DuckDB 专注于只读或大批量写入的分析任务。

### 2. 模块化视图 (Modules Layer)

* 不要把所有逻辑写在 `main.py`。建议使用 Streamlit 的 `st.navigation` (v1.31+) 功能，将每个功能模块解耦。
* 每个模块内部只关心业务逻辑，数据的读取通过 `core/database.py` 统一获取，实现**逻辑与展示分离**。

### 3. 快照管理 (History & Snapshots)

* 在 `data/` 下 `snapshots/` 子目录，专门存放用户点击“结果暂存”后生成的 `.parquet` 文件。
* Parquet 格式与 DuckDB/Polars 完美兼容，读取速度极快。

### 4. 交付与性能监控 (UI & Utils)

* `utils/metrics.py`：使用 `psutil` 库实时监控本地 CPU 和内存。
* 在 `ui/status_bar.py` 中调用这些指标，利用 Streamlit 的 `st.empty()` 或 `st.sidebar` 底部实现动态刷新，让用户对“电脑跑不动了”有直观感受。

### 5. 易于交付 (Packaging)

* 通过 `pyproject.toml` 管理依赖。
* 交付时，可以将整个 `data/` 文件夹初始化（保留结构但不含敏感数据），随程序一起分发。

---

## 可能的优化点

* 编码识别： 导入模块建议集成 chardet 或 charset-normalizer，解决 Excel/CSV 乱码的痛点。
* 进度反馈： 导入百万级数据时，建议使用 st.progress 结合 DuckDB 的 Appender 机制，提供实时的导入百分比。







