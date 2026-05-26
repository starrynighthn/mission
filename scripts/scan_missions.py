#!/usr/bin/env python3
"""
scan_missions.py — Quét trạng thái nhiệm vụ, phân nhóm theo workstream.

Script nhẹ, tập trung vào phân tích mission:
  - Nhóm theo workstream
  - Đếm trạng thái theo từng workstream
  - Tổng hợp overall
  - Liệt kê các mission quá hạn (deadline < hôm nay & status ≠ Done)
"""

import os
import re
import json
import glob
import yaml
from collections import Counter, defaultdict
from datetime import date, datetime


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
MISSIONS_DIR = os.path.join(PROJECT_ROOT, "missions")


# ---------------------------------------------------------------------------
# YAML frontmatter parser
# ---------------------------------------------------------------------------

_FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(filepath: str) -> dict | None:
    """Extract YAML frontmatter from a markdown file."""
    try:
        with open(filepath, "r", encoding="utf-8") as fh:
            content = fh.read()
    except (OSError, UnicodeDecodeError):
        return None

    if not content.strip():
        return None

    match = _FM_RE.match(content)
    if not match:
        return None

    try:
        data = yaml.safe_load(match.group(1))
        return data if isinstance(data, dict) else None
    except yaml.YAMLError:
        return None


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VALID_STATUSES = {"New", "Doing", "Done", "Pending"}


def normalise_status(raw) -> str:
    """Map raw status to canonical value. Defaults to 'New'."""
    if raw is None or str(raw).strip() == "":
        return "New"
    s = str(raw).strip()
    for valid in _VALID_STATUSES:
        if s.lower() == valid.lower():
            return valid
    return "New"


def safe_str(value, default: str = "") -> str:
    if value is None:
        return default
    return str(value).strip()


def parse_date(raw) -> date | None:
    """Try to parse a date from various formats. Returns None on failure."""
    if raw is None:
        return None
    if isinstance(raw, date):
        return raw
    if isinstance(raw, datetime):
        return raw.date()
    s = str(raw).strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------------------
# Core scan
# ---------------------------------------------------------------------------

def scan_missions() -> dict:
    today = date.today()

    all_missions: list[dict] = []
    ws_status: dict[str, Counter] = defaultdict(Counter)
    overall_status: Counter = Counter()
    overdue: list[dict] = []

    pattern = os.path.join(MISSIONS_DIR, "*.md")

    for filepath in sorted(glob.glob(pattern)):
        fm = parse_frontmatter(filepath)
        if fm is None:
            continue

        mission_key = safe_str(fm.get("mission_key"), os.path.basename(filepath))
        ws_code = safe_str(fm.get("workstream"), "unknown")
        status = normalise_status(fm.get("status"))
        title = safe_str(fm.get("title"))
        pic = safe_str(fm.get("pic"))
        deadline_raw = fm.get("deadline")
        deadline_date = parse_date(deadline_raw)
        deadline_str = deadline_date.isoformat() if deadline_date else safe_str(deadline_raw)

        overall_status[status] += 1
        ws_status[ws_code][status] += 1

        mission_info = {
            "mission_key": mission_key,
            "workstream": ws_code,
            "title": title,
            "status": status,
            "pic": pic,
            "deadline": deadline_str,
        }

        all_missions.append(mission_info)

        # Flag overdue: has a valid deadline in the past AND not Done
        if deadline_date and deadline_date < today and status != "Done":
            mission_info_copy = dict(mission_info)
            mission_info_copy["days_overdue"] = (today - deadline_date).days
            overdue.append(mission_info_copy)

    # ------------------------------------------------------------------
    # Build per-workstream summary
    # ------------------------------------------------------------------
    workstreams_summary: dict = {}
    for ws_code in sorted(ws_status.keys()):
        sc = ws_status[ws_code]
        workstreams_summary[ws_code] = {
            "total": sum(sc.values()),
            "New": sc.get("New", 0),
            "Doing": sc.get("Doing", 0),
            "Done": sc.get("Done", 0),
            "Pending": sc.get("Pending", 0),
        }

    # ------------------------------------------------------------------
    # Final output
    # ------------------------------------------------------------------
    report = {
        "generated_at": today.isoformat(),
        "total_missions": len(all_missions),
        "overall_status": {
            "New": overall_status.get("New", 0),
            "Doing": overall_status.get("Doing", 0),
            "Done": overall_status.get("Done", 0),
            "Pending": overall_status.get("Pending", 0),
        },
        "workstreams": workstreams_summary,
        "overdue_missions": sorted(overdue, key=lambda x: x.get("days_overdue", 0), reverse=True),
        "overdue_count": len(overdue),
    }

    return report


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    report = scan_missions()
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
