#!/usr/bin/env python3
"""
Generate markdown files with YAML frontmatter from MissionVO.xlsx.
Creates: people/, stakeholders/, workstreams/, missions/, risks/
"""

import os
import sys
from datetime import datetime

# Add venv to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../.venv/lib/python3.14/site-packages'))

import openpyxl

EXCEL_PATH = os.path.join(os.path.dirname(__file__), '../../MissionVO.xlsx')
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
TODAY = datetime.now().strftime('%Y-%m-%d')


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def safe_str(val):
    if val is None:
        return ''
    return str(val).strip()


def safe_date(val):
    if val is None:
        return 'null'
    if isinstance(val, datetime):
        return val.strftime('%Y-%m-%d')
    s = str(val).strip()
    if not s:
        return 'null'
    # Try to parse common formats
    for fmt in ['%d/%m/%Y', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']:
        try:
            return datetime.strptime(s, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return s


def yaml_str(val):
    """Escape YAML string value."""
    if not val or val == 'null':
        return '""'
    # Always quote strings that contain special chars
    if any(c in val for c in [':', '#', '"', "'", '\n', '[', ']', '{', '}', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`']):
        escaped = val.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
        return f'"{escaped}"'
    return f'"{val}"'


def write_md(filepath, frontmatter_lines, body=''):
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('---\n')
        for line in frontmatter_lines:
            f.write(line + '\n')
        f.write('---\n\n')
        if body:
            f.write(body + '\n')


# ============================================================
# PEOPLE (from Resources sheet)
# ============================================================
def generate_people(wb):
    ws = wb['Resources']
    people_dir = os.path.join(PROJECT_ROOT, 'people')
    ensure_dir(people_dir)
    
    count = 0
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=8, values_only=False):
        idx = safe_str(row[0].value)
        name = safe_str(row[1].value)
        role = safe_str(row[2].value)
        contract = safe_str(row[3].value)
        start = safe_date(row[4].value)
        end = safe_date(row[5].value)
        task = safe_str(row[6].value)
        
        if not name or not idx.isdigit():
            continue
        
        username = name.strip()
        
        # Map role to standardized roles
        role_map = {
            'PM': 'pm',
            'BA': 'ba',
            'Backend lead': 'backend_lead',
            'Dev Backend': 'dev_backend',
            'Mobile lead': 'mobile_lead',
            'Dev mobile': 'dev_mobile',
            'Tester lead': 'tester_lead',
            'Tester': 'tester',
        }
        std_role = role_map.get(role, role.lower().replace(' ', '_'))
        
        fm = [
            'entity: person',
            f'full_name: {yaml_str(username)}',
            f'username: {yaml_str(username)}',
            f'roles: [{std_role}]',
            'active: true',
            'team: VOffice',
            f'contract_type: {yaml_str(contract)}',
            f'start_date: {start}',
            f'end_date: {end}',
        ]
        
        body = f'# {username}\n\n- **Vai trò**: {role}\n- **Hợp đồng**: {contract}'
        if task:
            body += f'\n- **Ghi chú**: {task}'
        
        filepath = os.path.join(people_dir, f'{username}.md')
        write_md(filepath, fm, body)
        count += 1
    
    print(f'Generated {count} people files')


# ============================================================
# STAKEHOLDERS (from Stakeholders sheet)
# ============================================================
def generate_stakeholders(wb):
    ws = wb['Stakeholders']
    stakeholders_dir = os.path.join(PROJECT_ROOT, 'stakeholders')
    ensure_dir(stakeholders_dir)
    
    count = 0
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=6, values_only=False):
        idx = safe_str(row[0].value)
        name = safe_str(row[1].value)
        role = safe_str(row[2].value)
        org = safe_str(row[3].value)
        notes = safe_str(row[4].value)
        
        if not name or not idx.isdigit():
            continue
        
        username = name.strip()
        
        fm = [
            'entity: stakeholder',
            f'full_name: {yaml_str(username)}',
            f'username: {yaml_str(username)}',
            f'role: {yaml_str(role)}',
            f'organization: {yaml_str(org)}',
            f'notes: {yaml_str(notes)}',
            f'created_date: {TODAY}',
            f'updated_date: {TODAY}',
        ]
        
        body = f'# {username}\n\n- **Vai trò**: {role}\n- **Tổ chức**: {org}'
        if notes:
            body += f'\n\n## Ghi chú\n\n{notes}'
        
        filepath = os.path.join(stakeholders_dir, f'{username}.md')
        write_md(filepath, fm, body)
        count += 1
    
    print(f'Generated {count} stakeholder files')


# ============================================================
# RISKS (from Risks sheet)
# ============================================================
def generate_risks(wb):
    ws = wb['Risks']
    risks_dir = os.path.join(PROJECT_ROOT, 'risks')
    ensure_dir(risks_dir)
    
    count = 0
    for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=1, max_col=4, values_only=False):
        content = safe_str(row[1].value)
        mitigation = safe_str(row[2].value)
        owner = safe_str(row[3].value)
        
        if not content:
            continue
        
        count += 1
        risk_id = f'RISK-{count:03d}'
        
        fm = [
            'entity: risk',
            f'risk_id: {risk_id}',
            f'content: {yaml_str(content)}',
            f'mitigation: {yaml_str(mitigation)}',
            f'owner: {yaml_str(owner)}',
            'status: open',
            f'created_date: {TODAY}',
            f'updated_date: {TODAY}',
        ]
        
        body = f'# {risk_id}\n\n## Nội dung\n\n{content}\n\n## Phương án xử lý\n\n{mitigation}'
        if owner:
            body += f'\n\n## Người xử lý\n\n{owner}'
        
        filepath = os.path.join(risks_dir, f'{risk_id}.md')
        write_md(filepath, fm, body)
    
    print(f'Generated {count} risk files')


# ============================================================
# WORKSTREAMS + MISSIONS
# ============================================================

WORKSTREAM_CONFIG = [
    {
        'sheet': 'I.Web 4.0',
        'code': 'web-4.0',
        'prefix': 'WEB',
        'title': 'Triển khai phiên bản web 4.0',
        'header_row': 3,  # Row with column headers (STT | Nội dung | PIC | ...)
        'data_start': 4,
        'col_map': {
            'content': 1,   # B (0-indexed from min_col=1)
            'pic': 2,       # C
            'collab': 3,    # D
            'status': 4,    # E
            'deadline': 5,  # F
            'start': 6,     # G
            'completed': 7, # H
        },
        'has_type': False,
        'notes_col': None,
    },
    {
        'sheet': 'II.Tồn Mobile',
        'code': 'ton-mobile',
        'prefix': 'MOB',
        'title': 'Xử lý yêu cầu phát sinh trong quá trình triển khai mobile',
        'header_row': 3,
        'data_start': 4,
        'col_map': {
            'content': 0,
            'type': 1,
            'pic': 2,
            'collab': 3,
            'status': 4,
            'deadline': 5,
            'start': 6,
            'completed': 7,
        },
        'has_type': True,
        'notes_col': None,
    },
    {
        'sheet': 'III. Cải tiến công cụ CV',
        'code': 'cai-tien-cong-cu-cv',
        'prefix': 'CCV',
        'title': 'Cải tiến, phát triển công cụ giám sát toàn bộ tiến trình xử lý công việc',
        'header_row': 3,
        'data_start': 4,
        'col_map': {
            'content': 0,
            'type': 1,
            'pic': 2,
            'collab': 3,
            'status': 4,
            'deadline': 5,
            'start': 6,
            'completed': 7,
        },
        'has_type': True,
        'notes_col': None,
    },
    {
        'sheet': 'IV. Quản lý BC',
        'code': 'quan-ly-bc',
        'prefix': 'QBC',
        'title': 'Bổ sung phân hệ quản lý công tác báo cáo',
        'header_row': 3,
        'data_start': 4,
        'col_map': {
            'content': 0,
            'type': 1,
            'pic': 2,
            'collab': 3,
            'status': 4,
            'deadline': 5,
            'start': 6,
            'completed': 7,
        },
        'has_type': True,
        'notes_col': None,
    },
    {
        'sheet': 'V.Giám sát KPI CV',
        'code': 'giam-sat-kpi-cv',
        'prefix': 'KPI',
        'title': 'Hoàn thiện công cụ giám sát KPI hiệu suất xử lý công việc trên VOffice',
        'header_row': 3,
        'data_start': 4,
        'col_map': {
            'content': 0,
            'type': 1,
            'pic': 2,
            'collab': 3,
            'status': 4,
            'deadline': 5,
            'start': 6,
            'completed': 7,
        },
        'has_type': True,
        'notes_col': None,
    },
    {
        'sheet': 'VI.AI Agent',
        'code': 'ai-agent',
        'prefix': 'AIR',
        'title': 'Tích hợp AI Agent cho VOffice',
        'header_row': 2,
        'data_start': 3,
        'col_map': {
            'content': 0,
            'type': 1,
            'pic': 2,
            'collab': 3,
            'status': 4,
            'deadline': 5,
            'start': 6,
            'completed': 7,
        },
        'has_type': True,
        'notes_col': None,
    },
    {
        'sheet': 'YC phát sinh',
        'code': 'yc-phat-sinh',
        'prefix': 'ADH',
        'title': 'Yêu cầu phát sinh trong quá trình triển khai',
        'header_row': 1,
        'data_start': 2,
        'col_map': {
            'content': 0,
            'type': 1,
            'ticket_code': 2,
            'pic': 3,
            'collab': 4,
            'status': 5,
            'deadline': 6,
            'start': 7,
        },
        'has_type': True,
        'notes_col': None,
    },
]


def generate_workstreams_and_missions(wb):
    workstreams_dir = os.path.join(PROJECT_ROOT, 'workstreams')
    missions_dir = os.path.join(PROJECT_ROOT, 'missions')
    ensure_dir(workstreams_dir)
    ensure_dir(missions_dir)
    
    total_missions = 0
    
    for ws_config in WORKSTREAM_CONFIG:
        sheet_name = ws_config['sheet']
        ws = wb[sheet_name]
        
        mission_keys = []
        mission_count = 0
        
        data_start = ws_config['data_start']
        col_map = ws_config['col_map']
        
        for row in ws.iter_rows(min_row=data_start, max_row=ws.max_row, min_col=1, max_col=9, values_only=False):
            # Determine content column based on sheet type
            content_idx = col_map['content']
            content = safe_str(row[content_idx].value)
            
            if not content:
                continue
            
            mission_count += 1
            mission_key = f'{ws_config["prefix"]}-{mission_count:03d}'
            mission_keys.append(mission_key)
            
            # Extract fields
            pic = safe_str(row[col_map['pic']].value) if 'pic' in col_map else ''
            collab = safe_str(row[col_map['collab']].value) if 'collab' in col_map else ''
            status = safe_str(row[col_map['status']].value) if 'status' in col_map else 'New'
            deadline = safe_date(row[col_map['deadline']].value) if 'deadline' in col_map else 'null'
            
            start_date = 'null'
            completed_date = 'null'
            mission_type = ''
            ticket_code = ''
            
            if 'start' in col_map:
                start_date = safe_date(row[col_map['start']].value)
            if 'completed' in col_map:
                completed_date = safe_date(row[col_map['completed']].value)
            if ws_config['has_type'] and 'type' in col_map:
                mission_type = safe_str(row[col_map['type']].value)
            if 'ticket_code' in col_map:
                ticket_code = safe_str(row[col_map['ticket_code']].value)
            
            # Normalize status
            status_map = {
                'New': 'New',
                'Doing': 'Doing',
                'Done': 'Done',
                'Pending': 'Pending',
                '': 'New',
            }
            status = status_map.get(status, status)
            
            # Check for notes - look in remaining columns
            notes = ''
            for ci in range(8, min(len(row), 12)):
                cell_val = safe_str(row[ci].value)
                if cell_val:
                    notes = cell_val
                    break
            
            fm = [
                'entity: mission',
                f'mission_key: {mission_key}',
                f'workstream: {ws_config["code"]}',
                f'title: {yaml_str(content)}',
            ]
            if mission_type:
                fm.append(f'type: {yaml_str(mission_type)}')
            if ticket_code:
                fm.append(f'ticket_code: {yaml_str(ticket_code)}')
            fm.extend([
                f'status: {status}',
                f'pic: {yaml_str(pic)}',
                f'collaborator: {yaml_str(collab)}',
                f'deadline: {deadline}',
                f'start_date: {start_date}',
                f'completed_date: {completed_date}',
            ])
            if notes:
                fm.append(f'notes: {yaml_str(notes)}')
            fm.extend([
                f'created_date: {TODAY}',
                f'updated_date: {TODAY}',
            ])
            
            body = f'# {mission_key}: {content}\n\n'
            body += f'- **Workstream**: {ws_config["title"]}\n'
            body += f'- **PIC**: {pic}\n'
            if collab:
                body += f'- **Phối hợp**: {collab}\n'
            body += f'- **Trạng thái**: {status}\n'
            if deadline != 'null':
                body += f'- **Hạn**: {deadline}\n'
            if notes:
                body += f'\n## Ghi chú\n\n{notes}\n'
            body += f'\n## Update log\n\n| Ngày | Người cập nhật | Nội dung |\n|------|----------------|----------|\n| {TODAY} | system | Import từ MissionVO.xlsx |'
            
            filepath = os.path.join(missions_dir, f'{mission_key}.md')
            write_md(filepath, fm, body)
        
        total_missions += mission_count
        
        # Generate workstream file
        missions_list = ', '.join(mission_keys)
        
        # Count statuses
        ws_fm = [
            'entity: workstream',
            f'workstream_code: {ws_config["code"]}',
            f'title: {yaml_str(ws_config["title"])}',
            'status: active',
            f'mission_prefix: {ws_config["prefix"]}',
            f'total_missions: {mission_count}',
            f'missions: [{missions_list}]',
            f'created_date: {TODAY}',
            f'updated_date: {TODAY}',
        ]
        
        ws_body = f'# {ws_config["title"]}\n\n'
        ws_body += f'- **Mã workstream**: {ws_config["code"]}\n'
        ws_body += f'- **Prefix**: {ws_config["prefix"]}\n'
        ws_body += f'- **Tổng nhiệm vụ**: {mission_count}\n\n'
        ws_body += f'## Danh sách nhiệm vụ\n\n'
        ws_body += '| Mission Key | Nội dung | PIC | Trạng thái |\n'
        ws_body += '|-------------|----------|-----|------------|\n'
        
        # Re-read to build summary table
        mi = 0
        for row in ws.iter_rows(min_row=data_start, max_row=ws.max_row, min_col=1, max_col=9, values_only=False):
            content_idx = col_map['content']
            content = safe_str(row[content_idx].value)
            if not content:
                continue
            mi += 1
            mk = f'{ws_config["prefix"]}-{mi:03d}'
            pic = safe_str(row[col_map['pic']].value) if 'pic' in col_map else ''
            status = safe_str(row[col_map['status']].value) if 'status' in col_map else 'New'
            # Truncate long content for table
            short = content[:60] + '...' if len(content) > 60 else content
            ws_body += f'| {mk} | {short} | {pic} | {status} |\n'
        
        ws_filepath = os.path.join(workstreams_dir, f'{ws_config["code"]}.md')
        write_md(ws_filepath, ws_fm, ws_body)
        
        print(f'  Workstream {ws_config["code"]}: {mission_count} missions')
    
    print(f'Generated {total_missions} total mission files + {len(WORKSTREAM_CONFIG)} workstream files')


def main():
    print(f'Reading {EXCEL_PATH}...')
    wb = openpyxl.load_workbook(EXCEL_PATH)
    print(f'Sheets: {wb.sheetnames}')
    
    print('\n--- Generating People ---')
    generate_people(wb)
    
    print('\n--- Generating Stakeholders ---')
    generate_stakeholders(wb)
    
    print('\n--- Generating Risks ---')
    generate_risks(wb)
    
    print('\n--- Generating Workstreams & Missions ---')
    generate_workstreams_and_missions(wb)
    
    print('\n✅ Done! All files generated.')


if __name__ == '__main__':
    main()
