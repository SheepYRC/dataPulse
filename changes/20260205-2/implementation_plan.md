# Implementation Plan - Phase 2: Core Logic

Implement the core interactive features of DataPulse, focusing on data import, SQL execution, and metadata management.

## Proposed Changes

### Core Logic enhancements
#### [MODIFY] [database.py](file:///d:/uvProjects/dataPulse/src/core/database.py)
Add methods for:
- Logging SQL queries to SQLite.
- Executing queries and returning Polars DataFrames.
- Listing all tables and their metadata.

#### [MODIFY] [io_handler.py](file:///d:/uvProjects/dataPulse/src/utils/io_handler.py)
Implement robust CSV/Excel reading using Polars, including automatic encoding and separator detection.

### functional Modules Implementation
#### [MODIFY] [workbench.py](file:///d:/uvProjects/dataPulse/src/modules/workbench.py)
- Add file uploader for CSV/Excel/Parquet.
- Implement SQL editor with a result table.
- Add pagination logic to handle million-row datasets without browser lag.

#### [MODIFY] [assets.py](file:///d:/uvProjects/dataPulse/src/modules/assets.py)
- Implement a dashboard showing DuckDB table statistics.
- Add a "Health Audit" feature to scan for nulls and duplicates.

#### [MODIFY] [history.py](file:///d:/uvProjects/dataPulse/src/modules/history.py)
- Fetch and display the SQL history from SQLite.
- Implement "Save Snapshot" functionality using Parquet.

### UI Components
#### [MODIFY] [components.py](file:///d:/uvProjects/dataPulse/src/ui/components.py)
Add reusable components for:
- Data tables with pagination.
- Metric cards showing storage info.

## Verification Plan

### Automated/Scripted Tests
1. Script to generate a 1M row CSV for stress testing.
2. Verify DuckDB's `COPY` command speed for large imports.

### Manual Verification
1. Upload a CSV and verify it appears in "Data Assets".
2. Run a `SELECT COUNT(*)` on a large table in the "Workbench".
3. Check if the query appears in "History".
4. Create a snapshot and verify it exists in `data/snapshots/`.
