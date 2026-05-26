# Mission Agent - Operational Guide

## Overview
This workspace is the **Single Source of Truth (SSOT)** for managing VOffice project missions. All data is stored as Markdown files with YAML frontmatter, synchronized via Git.

## Before You Start
1. Always read ALL files in `rules/` before performing any operations
2. Pull latest changes from Git before making modifications
3. Validate all data before writing files

## Entity Types

| Entity | Directory | ID Format | Example |
|--------|-----------|-----------|----------|
| Mission | `missions/` | `{PREFIX}-NNN` | `WEB-001` |
| Person | `people/` | `{username}` | `TienCB1` |
| Stakeholder | `stakeholders/` | `{username}` | `TrieuQuangVinh` |
| Workstream | `workstreams/` | `{code}` | `web-4.0` |
| Risk | `risks/` | `RISK-NNN` | `RISK-001` |
| Project | `project/` | `{name}` | `voffice` |

## Mission Prefixes

| Workstream | Prefix | Description |
|------------|--------|-------------|
| web-4.0 | WEB | Web 4.0 deployment |
| ton-mobile | MOB | Mobile backlog |
| cai-tien-cong-cu-cv | CCV | Workflow tool improvements |
| quan-ly-bc | QBC | Report management |
| giam-sat-kpi-cv | KPI | KPI monitoring |
| ai-agent | AIR | AI Agent integration |
| yc-phat-sinh | ADH | Ad-hoc requests |

## File Format
Every data file MUST use YAML frontmatter:
```yaml
---
entity: mission
mission_key: WEB-001
title: "..."
status: New
# ... other fields
---
```

## Status Values
- `New` — Not started
- `Doing` — In progress
- `Done` — Completed
- `Pending` — Blocked/waiting

## Mandatory Fields for Missions
- `entity`: Always `mission`
- `mission_key`: Unique identifier
- `workstream`: Reference to workstream code
- `title`: Mission description
- `status`: Current status
- `pic`: Person In Charge (must exist in `people/`)
- `deadline`: Target completion date

## Bidirectional Links
- Every mission's `workstream` field must reference a valid workstream
- Every workstream's `missions` array must include all its missions
- Every mission's `pic` must reference a valid person in `people/`

## Validation Rules
Before writing any file:
1. Check that `pic` exists in `people/`
2. Check that `workstream` exists in `workstreams/`
3. Check that `status` is one of: New, Doing, Done, Pending
4. Check date format is YYYY-MM-DD
5. Ensure mission_key follows `{PREFIX}-NNN` format

## Git Sync
- Run `scripts/scan_all.py` before committing
- Update `README.md` dashboard before committing
- Commit with descriptive message: `[mission] description of changes`
- Push to remote after every session

## Dashboard
The `README.md` serves as the project dashboard. It should be auto-updated with:
- Mission status counts per workstream
- Overall progress percentages
- Active risks
- Team allocation summary

## Scripts
- `scripts/scan_all.py` — Full scan of all entities, outputs JSON
- `scripts/scan_missions.py` — Mission-only scan with status counts
- `scripts/generate_from_excel.py` — Initial import from Excel (one-time use)
