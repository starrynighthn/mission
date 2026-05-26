# Project Rules — Mission Workspace

## Single Source of Truth (SSOT)

Toàn bộ dữ liệu mission được quản lý trong workspace này. Không lưu trữ mission data ở nơi khác. Workspace này là nguồn duy nhất và chính xác nhất cho mọi thông tin về mission, workstream, người phụ trách, và stakeholder.

## File Format

- All entity files use **Markdown** with **YAML frontmatter** (delimited by `---`).
- Frontmatter contains structured metadata (key-value pairs).
- Body contains free-form notes, update logs, and descriptions.

Example structure:

```markdown
---
entity: mission
mission_key: WEB-001
title: "Xây dựng trang landing page"
status: New
pic: robin
workstream: web-development
created_date: 2026-01-15
updated_date: 2026-01-15
---

# WEB-001 — Xây dựng trang landing page

## Mô tả
...

## Update log
...
```

## Entity Types

| Entity        | Directory        | Description                              |
|---------------|------------------|------------------------------------------|
| `mission`     | `missions/`      | Nhiệm vụ cụ thể cần hoàn thành         |
| `person`      | `people/`        | Người phụ trách (PIC)                    |
| `stakeholder` | `stakeholders/`  | Bên liên quan / đối tác                  |
| `workstream`  | `workstreams/`   | Luồng công việc / nhóm nhiệm vụ         |
| `risk`        | `risks/`         | Rủi ro liên quan đến mission             |
| `project`     | `projects/`      | Dự án tổng thể chứa nhiều workstream     |

## Mission Key Format

Mission keys follow the pattern: `{PREFIX}-{NNN}`

- `PREFIX` — Workstream code (uppercase, 2–3 characters)
- `NNN` — Zero-padded 3-digit sequential number

Examples: `WEB-001`, `ADH-045`, `CCV-012`

## Workstream Codes & Prefixes

| Workstream Code     | Prefix | Description                        |
|---------------------|--------|------------------------------------|
| `web-development`   | `WEB`  | Web development tasks              |
| `mobile`            | `MOB`  | Mobile app development             |
| `ccv`               | `CCV`  | CCV-related missions               |
| `qubikcoin`         | `QBC`  | QuBikCoin blockchain missions      |
| `kpi`               | `KPI`  | KPI tracking & reporting           |
| `airdrop`           | `AIR`  | Airdrop campaigns                  |
| `adhoc`             | `ADH`  | Ad-hoc / miscellaneous tasks       |

## Bidirectional Links

- Every **mission** file MUST reference its parent `workstream` in frontmatter.
- Every **workstream** file MUST list its child missions in a `missions` array in frontmatter.
- When a mission is created, updated, or removed — both sides MUST be updated.

Example — mission frontmatter:
```yaml
workstream: web-development
```

Example — workstream frontmatter:
```yaml
missions:
  - WEB-001
  - WEB-002
  - WEB-003
```

## PIC (Person In Charge)

- The `pic` field in mission frontmatter MUST reference an existing person file in `people/`.
- The value must match the filename (without extension) of a file in `people/`.
- Example: `pic: robin` → file `people/robin.md` must exist.

## Path Rules

- **No absolute paths** in any file. Use relative references only.
- **No private data** (passwords, tokens, API keys, personal info) in any file.

## Language Convention

- **English** for all metadata fields, keys, filenames, and frontmatter values.
- **Vietnamese (Tiếng Việt)** is acceptable for:
  - `title` and `description` fields
  - Free-form notes and update logs in the body
  - Comments and explanations

## Date Format

- All date fields MUST use **`YYYY-MM-DD`** format.
- Acceptable date fields: `created_date`, `updated_date`, `due_date`, `completed_date`, `start_date`.
- If a date is not yet known, use `null`.
