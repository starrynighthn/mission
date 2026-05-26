#!/usr/bin/env python3
"""
scan_all.py — Quét toàn bộ workspace Mission Tracker và xuất JSON tổng hợp.

Phân tích YAML frontmatter từ tất cả file .md trong:
  missions/, people/, stakeholders/, workstreams/, risks/

Output JSON gồm:
  - MISSION_STATUS_COUNTS
  - MISSIONS_BY_WORKSTREAM
  - PIC_WORKLOAD
  - RISKS
  - PEOPLE_COUNT
  - STAKEHOLDER_COUNT
  - TOTAL_MISSIONS
"""

import os
import re
import json
import glob
import yaml
from collections import defaultdict, Counter
from datetime import date


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

DIRS = {
    "missions":     os.path.join(PROJECT_ROOT, "missions"),
    "people":       os.path.join(PROJECT_ROOT, "people"),
    "stakeholders": os.path.join(PROJECT_ROOT, "stakeholders"),
    "workstreams":  os.path.join(PROJECT_ROOT, "workstreams"),
    "risks":        os.path.join(PROJECT_ROOT, "risks"),
}


# ---------------------------------------------------------------------------
# YAML frontmatter parser
# ---------------------------------------------------------------------------

_FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def parse_frontmatter(filepath: str) -> dict | None:
    """Extract YAML frontmatter from a markdown file.

    Returns the parsed dict, or None when the file is empty / has no
    frontmatter / cannot be parsed.
    """
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


def scan_dir(directory: str) -> list[dict]:
    """Return a list of parsed frontmatter dicts for every .md in *directory*."""
    results = []
    pattern = os.path.join(directory, "*.md")
    for filepath in sorted(glob.glob(pattern)):
        fm = parse_frontmatter(filepath)
        if fm is not None:
            fm["_source_file"] = os.path.basename(filepath)
            results.append(fm)
    return results


# ---------------------------------------------------------------------------
# Normalise helpers
# ---------------------------------------------------------------------------

_VALID_STATUSES = {"New", "Doing", "Done", "Pending"}


def normalise_status(raw) -> str:
    """Map a raw status value to one of the canonical statuses.

    Handles None, empty strings, and case-insensitive matching.
    Falls back to 'New' for unrecognised values.
    """
    if raw is None or str(raw).strip() == "":
        return "New"
    s = str(raw).strip()
    # Case-insensitive match
    for valid in _VALID_STATUSES:
        if s.lower() == valid.lower():
            return valid
    return "New"


def safe_str(value, default: str = "") -> str:
    """Convert any value to a stripped string, using *default* for None."""
    if value is None:
        return default
    return str(value).strip()


# ---------------------------------------------------------------------------
# Build report
# ---------------------------------------------------------------------------

def build_report() -> dict:
    # ------------------------------------------------------------------
    # 1. Parse all entities
    # ------------------------------------------------------------------
    missions_data = scan_dir(DIRS["missions"])
    people_data = scan_dir(DIRS["people"])
    stakeholders_data = scan_dir(DIRS["stakeholders"])
    workstreams_data = scan_dir(DIRS["workstreams"])
    risks_data = scan_dir(DIRS["risks"])

    # ------------------------------------------------------------------
    # 2. Workstream lookup  (code → title)
    # ------------------------------------------------------------------
    ws_titles: dict[str, str] = {}
    for ws in workstreams_data:
        code = safe_str(ws.get("workstream_code"))
        title = safe_str(ws.get("title"), code)
        if code:
            ws_titles[code] = title

    # ------------------------------------------------------------------
    # 3. Mission status counts & grouping
    # ------------------------------------------------------------------
    status_counter: Counter = Counter()
    ws_missions: dict[str, list] = defaultdict(list)
    ws_status_counters: dict[str, Counter] = defaultdict(Counter)
    pic_workload: dict[str, list] = defaultdict(list)

    for m in missions_data:
        status = normalise_status(m.get("status"))
        ws_code = safe_str(m.get("workstream"), "unknown")
        mission_key = safe_str(m.get("mission_key"), m.get("_source_file", "?"))
        pic = safe_str(m.get("pic"))

        status_counter[status] += 1
        ws_status_counters[ws_code][status] += 1
        ws_missions[ws_code].append({
            "mission_key": mission_key,
            "title": safe_str(m.get("title")),
            "status": status,
            "pic": pic,
            "deadline": safe_str(m.get("deadline")),
        })

        if pic:
            pic_workload[pic].append(mission_key)

    # ------------------------------------------------------------------
    # 4. MISSIONS_BY_WORKSTREAM
    # ------------------------------------------------------------------
    missions_by_ws: dict = {}
    for ws_code in sorted(set(list(ws_missions.keys()) + list(ws_titles.keys()))):
        sc = ws_status_counters.get(ws_code, Counter())
        missions_by_ws[ws_code] = {
            "title": ws_titles.get(ws_code, ws_code),
            "status_counts": {
                "New": sc.get("New", 0),
                "Doing": sc.get("Doing", 0),
                "Done": sc.get("Done", 0),
                "Pending": sc.get("Pending", 0),
            },
            "total": sum(sc.values()),
            "missions": ws_missions.get(ws_code, []),
        }

    # ------------------------------------------------------------------
    # 5. Risks
    # ------------------------------------------------------------------
    risk_list = []
    for r in risks_data:
        risk_list.append({
            "risk_id": safe_str(r.get("risk_id")),
            "content": safe_str(r.get("content")),
            "mitigation": safe_str(r.get("mitigation")),
            "owner": safe_str(r.get("owner")),
            "status": safe_str(r.get("status"), "open"),
        })

    # ------------------------------------------------------------------
    # 6. Assemble final report
    # ------------------------------------------------------------------
    report = {
        "generated_at": date.today().isoformat(),
        "TOTAL_MISSIONS": len(missions_data),
        "PEOPLE_COUNT": len(people_data),
        "STAKEHOLDER_COUNT": len(stakeholders_data),
        "MISSION_STATUS_COUNTS": {
            "New": status_counter.get("New", 0),
            "Doing": status_counter.get("Doing", 0),
            "Done": status_counter.get("Done", 0),
            "Pending": status_counter.get("Pending", 0),
        },
        "MISSIONS_BY_WORKSTREAM": missions_by_ws,
        "PIC_WORKLOAD": dict(sorted(pic_workload.items())),
        "RISKS": risk_list,
    }

    return report


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    report = build_report()
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
