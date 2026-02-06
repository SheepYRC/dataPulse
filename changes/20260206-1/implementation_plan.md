# Result of Refactoring DataPulse based on new design

本项目将按照 `project.md` 的新设计进行重构。主要目标是提升数据处理能力（百万级）、完善界面布局（9大模块导航）以及增强系统稳定性。

## Proposed Changes

### 1. 核心层与环境 (Core & Environment)

* **[MODIFY] [pyproject.toml](file:///d:/uvProjects/dataPulse/pyproject.toml)**: 确保包含 `duckdb`, `polars`, `pandas`, `streamlit`, `psutil`, `chardet` 等必要依赖。
* **[MODIFY] [config.py](file:///d:/uvProjects/dataPulse/src/core/config.py)**: 完善路径配置，包括 `data/analytics.duckdb` 和 `data/datapulse.db`。
* **[MODIFY] [database.py](file:///d:/uvProjects/dataPulse/src/core/database.py)**: 实现双数据库管理逻辑。SQLite 用于存储配置、SQL 历史、任务卡片；DuckDB 用于业务数据分析。
* **[MODIFY] [engine.py](file:///d:/uvProjects/dataPulse/src/core/engine.py)**: 封装 Polars 和 Pandas 的计算转换逻辑。

### 2. UI 框架与导航 (UI Framework & Navigation)

* **[MODIFY] [main.py](file:///d:/uvProjects/dataPulse/src/main.py)**: 使用 `st.navigation` 重新组织页面结构，共 9 个模块（0-8）。
* **[MODIFY] [status_bar.py](file:///d:/uvProjects/dataPulse/src/ui/status_bar.py)**: 集成 `psutil` 指标，在侧边栏底部显示硬件占用。

### 3. 功能模块 (Functional Modules)

* **[NEW] [dashboard.py](file:///d:/uvProjects/dataPulse/src/pages/dashboard.py)** (M0): 工作看板，支持任务卡片和最近访问。
* **[NEW] [statistics.py](file:///d:/uvProjects/dataPulse/src/pages/statistics.py)** (M1): 概况统计，数据库审计和活跃度画像。
* **[MODIFY] [assets.py](file:///d:/uvProjects/dataPulse/src/pages/assets.py)** (M2): 数据资产，文件导入（增强识别）与表预览。
* **[NEW] [query.py](file:///d:/uvProjects/dataPulse/src/pages/query.py)** (M3): 数据查询，支持 SQL 和 GUI 模式，分页加载。
* **[NEW] [process.py](file:///d:/uvProjects/dataPulse/src/pages/process.py)** (M4): 数据处理，算子链可视化配置。
* **[MODIFY] [insights.py](file:///d:/uvProjects/dataPulse/src/pages/insights.py)** (M5): 可视化引擎，Plotly 交互图表。
* **[MODIFY] [history.py](file:///d:/uvProjects/dataPulse/src/pages/history.py)** (M6): 历史与快照，Parquet 文件管理。
* **[NEW] [system.py](file:///d:/uvProjects/dataPulse/src/pages/system.py)** (M7): 系统管理，主题与路径配置。
* **[NEW] [search.py](file:///d:/uvProjects/dataPulse/src/pages/search.py)** (M8): 全局搜索，Action 命令支持。

### 4. 工具类增强 (Utils)

* **[MODIFY] [io_handler.py](file:///d:/uvProjects/dataPulse/src/utils/io_handler.py)**: 添加编码识别逻辑。
* **[MODIFY] [metrics.py](file:///d:/uvProjects/dataPulse/src/utils/metrics.py)**: 实现硬件指标监控。

## Verification Plan

### Automated Tests
* 验证 `core/database.py` 是否能同时连接两个数据库。
* 导入一个 100万行的 CSV 文件，验证内存占用和耗时。
* 测试 SQL 查询的分页返回逻辑。

### Manual Verification
* 在 Streamlit 界面切换各个模块，检查导航是否流畅。
* 模拟 SQL 错误，检查是否有友好的沙箱报错提示。
* 在系统管理中修改配置，验证持久化是否生效。
