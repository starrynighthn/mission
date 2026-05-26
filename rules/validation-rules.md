# Validation Rules — Mission Workspace

## Overview

Các rules dưới đây phải được kiểm tra khi tạo mới hoặc cập nhật bất kỳ entity nào trong workspace. Vi phạm rule sẽ khiến thao tác bị từ chối.

---

## Rule 1: Mission Key Format

- `mission_key` **must** match the pattern `{PREFIX}-{NNN}`.
- `PREFIX` must be one of: **WEB**, **MOB**, **CCV**, **QBC**, **KPI**, **AIR**, **ADH**.
- `NNN` must be a zero-padded 3-digit number (e.g., `001`, `045`, `100`).
- Regex: `^(WEB|MOB|CCV|QBC|KPI|AIR|ADH)-\d{3}$`

✅ Valid: `WEB-001`, `ADH-045`, `CCV-100`
❌ Invalid: `WEB-1`, `web-001`, `ABC-001`, `WEB001`

---

## Rule 2: PIC Must Exist

- The `pic` field must reference a **username** that corresponds to an existing file in `people/`.
- Validation: Check that `people/{pic}.md` exists.

✅ Valid: `pic: robin` → `people/robin.md` exists
❌ Invalid: `pic: john` → `people/john.md` does not exist

---

## Rule 3: Workstream Must Exist

- The `workstream` field must reference a **workstream_code** that corresponds to an existing file in `workstreams/`.
- Validation: Check that `workstreams/{workstream}.md` exists.

✅ Valid: `workstream: web-development` → `workstreams/web-development.md` exists
❌ Invalid: `workstream: marketing` → `workstreams/marketing.md` does not exist

---

## Rule 4: Valid Status Values

- The `status` field must be one of: **New**, **Doing**, **Done**, **Pending**.
- Status values are **case-sensitive**.
- The special value `cancelled` is also accepted (for soft-deleted missions).

✅ Valid: `status: New`, `status: Doing`, `status: Done`, `status: Pending`, `status: cancelled`
❌ Invalid: `status: new`, `status: In Progress`, `status: Completed`, `status: DONE`

---

## Rule 5: Date Format

- All date fields must be either `null` or in **YYYY-MM-DD** format.
- Applicable fields: `created_date`, `updated_date`, `due_date`, `completed_date`, `start_date`.
- Regex: `^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$`

✅ Valid: `2026-01-15`, `2025-12-31`, `null`
❌ Invalid: `15/01/2026`, `Jan 15, 2026`, `2026-1-5`, `""`

---

## Rule 6: Bidirectional Link Integrity

- When a mission references a workstream (via `workstream` field), that workstream's `missions` array **must** contain the mission's `mission_key`.
- When a workstream lists a mission in its `missions` array, that mission file **must** exist and reference back to the workstream.
- Both sides must be updated atomically — never update one without the other.

✅ Valid:
```yaml
# missions/web-001.md
workstream: web-development

# workstreams/web-development.md
missions:
  - WEB-001
```

❌ Invalid:
```yaml
# missions/web-001.md
workstream: web-development

# workstreams/web-development.md
missions: []  # ← missing WEB-001
```

---

## Rule 7: Entity Field Must Match Directory

- The `entity` field in frontmatter must correspond to the directory where the file resides.
- Mapping:

| Directory        | Expected `entity` value |
|------------------|------------------------|
| `missions/`      | `mission`              |
| `people/`        | `person`               |
| `stakeholders/`  | `stakeholder`          |
| `workstreams/`   | `workstream`           |
| `risks/`         | `risk`                 |
| `projects/`      | `project`              |

✅ Valid: File `missions/web-001.md` has `entity: mission`
❌ Invalid: File `missions/web-001.md` has `entity: workstream`

---

## Rule 8: Stakeholder References

- Stakeholder references should use the `username` field.
- The `username` must match the filename (without extension) in `stakeholders/`.
- Validation: `stakeholders/{username}.md` must exist.

✅ Valid: `stakeholder: partner-abc` → `stakeholders/partner-abc.md` exists
❌ Invalid: `stakeholder: Partner ABC` → no matching file

---

## Rule 9: Risk ID Format

- Risk IDs must follow the pattern `RISK-{NNN}`.
- `NNN` must be a zero-padded 3-digit number.
- Regex: `^RISK-\d{3}$`

✅ Valid: `RISK-001`, `RISK-042`, `RISK-100`
❌ Invalid: `RISK-1`, `risk-001`, `RSK-001`, `RISK001`

---

## Validation Checklist

Khi tạo hoặc cập nhật mission, kiểm tra theo thứ tự:

1. ☐ `mission_key` matches `{PREFIX}-{NNN}` format (Rule 1)
2. ☐ `pic` exists in `people/` (Rule 2)
3. ☐ `workstream` exists in `workstreams/` (Rule 3)
4. ☐ `status` is valid (Rule 4)
5. ☐ All dates are `null` or `YYYY-MM-DD` (Rule 5)
6. ☐ Workstream's `missions` array is updated (Rule 6)
7. ☐ `entity` field matches directory (Rule 7)
8. ☐ Stakeholder refs match files in `stakeholders/` (Rule 8)
9. ☐ Risk IDs follow `RISK-NNN` format (Rule 9)
