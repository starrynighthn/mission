# Workflow Rules — Mission Workspace

## Mission Statuses

| Status    | Ý nghĩa                                      |
|-----------|-----------------------------------------------|
| `New`     | Mới tạo, chưa bắt đầu                        |
| `Doing`   | Đang thực hiện                                |
| `Done`    | Hoàn thành                                    |
| `Pending` | Tạm dừng / bị chặn, cần chờ                  |

## Status Transition Rules

```
         ┌──────────┐
         │   New    │
         └────┬─────┘
              │ (start work, must have PIC)
              ▼
         ┌──────────┐
    ┌───▶│  Doing   │◀───┐
    │    └──┬────┬──┘    │
    │       │    │       │ (unblocked)
    │       │    │       │
    │       │    ▼       │
    │       │ ┌─────────┐
    │       │ │ Pending │
    │       │ └─────────┘
    │       ▼
    │  ┌──────────┐
    │  │   Done   │
    │  └──────────┘
    │
    └── Any status → New (revert only, must log reason)
```

### Allowed Transitions

| From      | To        | Conditions                                                |
|-----------|-----------|-----------------------------------------------------------|
| `New`     | `Doing`   | Work begins. PIC **must** be assigned.                    |
| `Doing`   | `Done`    | Work completed. **Should** set `completed_date`.          |
| `Doing`   | `Pending` | Blocked. **Should** add notes explaining the blocker.     |
| `Pending` | `Doing`   | Blocker resolved. Add note about resolution.              |
| Any       | `New`     | Revert only. **Must** add entry to Update log explaining. |

### Forbidden Transitions

- `New` → `Done` (cannot skip `Doing`)
- `New` → `Pending` (cannot be blocked before starting)
- `Done` → `Doing` (use revert to `New` first, then transition to `Doing`)
- `Done` → `Pending` (use revert to `New` first)
- `Pending` → `Done` (must go through `Doing` first)

## Creating a New Mission

When creating a new mission file, the following steps **MUST** be performed:

1. **Assign workstream** — The `workstream` field must reference an existing workstream code in `workstreams/`.
2. **Assign PIC** — The `pic` field must reference an existing person in `people/`.
3. **Generate mission_key** — Determine the workstream's prefix, scan existing missions for that prefix, and assign the next available `{PREFIX}-{NNN}`.
   - Example: If `WEB-001` through `WEB-012` exist, the next key is `WEB-013`.
4. **Update workstream** — Add the new `mission_key` to the parent workstream's `missions` array in its frontmatter.
5. **Set initial metadata**:
   - `status: New`
   - `created_date: {today}` (YYYY-MM-DD)
   - `updated_date: {today}` (YYYY-MM-DD)
6. **Create the file** — Save as `missions/{mission_key}.md` (lowercase, e.g., `missions/web-013.md`).

## Updating Mission Status

When changing a mission's status:

1. **Validate transition** — Ensure the transition is allowed per the rules above.
2. **Update `updated_date`** — Set to today's date (YYYY-MM-DD).
3. **Set `completed_date`** — If transitioning to `Done`, set `completed_date` to today.
4. **Add Update log entry** — Append an entry to the `## Update log` section in the body:

```markdown
## Update log

- **2026-01-20** — Status changed: New → Doing. Bắt đầu triển khai. (by robin)
- **2026-01-25** — Status changed: Doing → Pending. Chờ thiết kế UI từ team design. (by robin)
- **2026-02-01** — Status changed: Pending → Doing. Đã nhận được bản thiết kế. (by robin)
- **2026-02-10** — Status changed: Doing → Done. Hoàn thành và deploy lên staging. (by robin)
```

## Deleting / Cancelling a Mission

- **Do NOT delete** mission files. Xóa file sẽ mất lịch sử.
- Instead, set `status: cancelled` in frontmatter.
- **Remove** the `mission_key` from the parent workstream's `missions` array.
- Add an Update log entry explaining the cancellation reason.

```markdown
## Update log

- **2026-03-01** — Status changed: Doing → Cancelled. Không còn phù hợp với roadmap Q2. (by robin)
```
