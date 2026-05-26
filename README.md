# 🎯 Mission Tracker — VOffice

> **Hệ thống theo dõi nhiệm vụ triển khai VOffice**
> Quản lý bằng file Markdown + YAML frontmatter — tương thích AI Agent & Git workflow.

---

## 📌 Quick Links

| Thư mục | Mô tả |
|---------|--------|
| [`missions/`](./missions/) | Toàn bộ nhiệm vụ (113 files) |
| [`workstreams/`](./workstreams/) | 7 luồng công việc chính |
| [`people/`](./people/) | Nhân sự dự án (16 người) |
| [`stakeholders/`](./stakeholders/) | Bên liên quan (27 người) |
| [`risks/`](./risks/) | Quản lý rủi ro |
| [`scripts/`](./scripts/) | Công cụ scan & phân tích |

---

## 📊 Dashboard thống kê

### Tổng quan nhiệm vụ theo Workstream

| # | Workstream | Tổng | 🆕 New | 🔄 Doing | ✅ Done | ⏸️ Pending |
|---|-----------|------|--------|----------|--------|------------|
| I | Triển khai phiên bản Web 4.0 | 26 | 8 | 12 | 6 | 0 |
| II | Tồn Mobile | 4 | 4 | 0 | 0 | 0 |
| III | Cải tiến công cụ CV | 3 | 2 | 1 | 0 | 0 |
| IV | Quản lý BC | 6 | 3 | 1 | 1 | 0 |
| V | Giám sát KPI CV | 5 | 3 | 1 | 0 | 0 |
| VI | AI Agent | 10 | 4 | 3 | 3 | 0 |
| — | YC phát sinh | 59 | 23 | 15 | 17 | 4 |
| | **Tổng cộng** | **113** | **47** | **33** | **27** | **4** |

### Phân bố trạng thái

```
New     ████████████████████░░░░░░░░░░░░░░░░░░░░  41.6%  (47)
Doing   ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░  29.2%  (33)
Done    ██████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░  23.9%  (27)
Pending ██░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░   3.5%  ( 4)
```

> 💡 Chạy `python3 scripts/scan_all.py` để lấy dữ liệu real-time dạng JSON.

---

## 👥 Nhân sự dự án

| # | Username | Vai trò | Hợp đồng |
|---|----------|---------|----------|
| 1 | AnhPT185 | Dev Mobile | IS |
| 2 | GiangKM | Dev Backend | HĐLĐ |
| 3 | GiangPH13 | QC | HĐLĐ |
| 4 | HungTQ24 | Dev Backend | HĐLĐ |
| 5 | LamVT8 | Dev Backend | IS |
| 6 | LuanVV | Dev Backend | HĐLĐ |
| 7 | NgaNV13 | Dev Backend | HĐLĐ |
| 8 | NgocLM10 | Dev Mobile | IS |
| 9 | PhongNQ13 | Dev Frontend | HĐLĐ |
| 10 | PhuongDT80 | Dev Backend | IS |
| 11 | PhuongQT | QC | HĐLĐ |
| 12 | ThanhLV29 | Dev Mobile | HĐLĐ |
| 13 | ThinhCVQ | BA | HĐLĐ |
| 14 | TienCB1 | PM | HĐLĐ |
| 15 | TrangNT214 | QC / Test Lead | HĐLĐ |
| 16 | TungNV168 | Dev Backend | HĐLĐ |

> 📁 Chi tiết từng người: xem thư mục [`people/`](./people/)

---

## ⚠️ Rủi ro hiện tại

### RISK-001 — Thiếu nguồn lực từ VTIT
- **Nội dung**: VTIT không đảm bảo được nguồn lực cho dự án do bị hút quá nhiều vào xử lý phiên bản Web, cũng như đẩy người cho các dự án trọng điểm khác (như Văn phòng TW Đảng)
- **Phương án**: Tìm thêm đối tác OS khác; chia nhỏ yêu cầu để đẩy cho nhiều đối tác
- **Người xử lý**: VietLV2
- **Trạng thái**: 🔴 Open

### RISK-002 — Effort support & ad-hoc cao
- **Nội dung**: Dự án chiếm rất nhiều effort cho công tác hỗ trợ và thường rất hay phát sinh các task nóng gấp, đột xuất ("ad-hoc")
- **Phương án**: Ưu tiên chia tách 1–2 nhân sự "cứng" chuyên xử lý support (backend: HungTQ24, mobile: AnhPT185)
- **Trạng thái**: 🔴 Open

---

## 🗂️ Cấu trúc thư mục

```
mission/
├── README.md                    ← Bạn đang đây
├── missions/                    ← 113 nhiệm vụ (.md + YAML frontmatter)
│   ├── WEB-001.md ... WEB-026.md    (Web 4.0)
│   ├── MOB-001.md ... MOB-004.md    (Tồn Mobile)
│   ├── CCV-001.md ... CCV-003.md    (Cải tiến công cụ CV)
│   ├── QBC-001.md ... QBC-006.md    (Quản lý BC)
│   ├── KPI-001.md ... KPI-005.md    (Giám sát KPI CV)
│   ├── AIR-001.md ... AIR-010.md    (AI Agent)
│   └── ADH-001.md ... ADH-059.md    (YC phát sinh)
├── workstreams/                 ← 7 luồng công việc
│   ├── web-4.0.md
│   ├── ton-mobile.md
│   ├── cai-tien-cong-cu-cv.md
│   ├── quan-ly-bc.md
│   ├── giam-sat-kpi-cv.md
│   ├── ai-agent.md
│   └── yc-phat-sinh.md
├── people/                      ← 16 thành viên dự án
├── stakeholders/                ← 27 bên liên quan
├── risks/                       ← Quản lý rủi ro
└── scripts/                     ← Công cụ tự động
    ├── scan_all.py              ← Scan toàn bộ → JSON dashboard
    ├── scan_missions.py         ← Scan mission + phát hiện quá hạn
    └── generate_from_excel.py   ← Import từ MissionVO.xlsx
```

---

## 🚀 Hướng dẫn sử dụng

### Chạy scan tổng hợp

```bash
# Xuất JSON dashboard toàn bộ workspace
python3 scripts/scan_all.py

# Scan riêng mission — bao gồm danh sách quá hạn
python3 scripts/scan_missions.py

# Pipe sang jq để lọc dữ liệu
python3 scripts/scan_all.py | jq '.MISSION_STATUS_COUNTS'
python3 scripts/scan_missions.py | jq '.overdue_missions'
```

### Làm việc với AI Agent

Workspace này được thiết kế để AI Agent có thể:
1. **Đọc trạng thái** — parse YAML frontmatter từ bất kỳ file `.md`
2. **Cập nhật nhiệm vụ** — sửa trường `status`, `notes`, `completed_date` trong frontmatter
3. **Tạo báo cáo** — chạy scan scripts để lấy dữ liệu tổng hợp
4. **Thêm nhiệm vụ mới** — tạo file `.md` mới theo template có sẵn

> 📖 Xem thêm: `AGENTS.md` (nếu có) để biết hướng dẫn chi tiết cho AI agent.

### Git workflow

```bash
# Xem thay đổi
git status
git diff

# Commit thay đổi
git add -A
git commit -m "feat: cập nhật trạng thái WEB-015 → Done"

# Quy ước commit message:
#   feat:     thêm / cập nhật nhiệm vụ
#   fix:      sửa dữ liệu sai
#   docs:     cập nhật README / tài liệu
#   chore:    scripts, config
```

---

## 📚 Tham khảo

| Tài liệu | Mô tả |
|-----------|--------|
| `AGENTS.md` | Hướng dẫn dành cho AI Agent |
| `rules/` | Quy tắc chi tiết cho workspace |
| `scripts/scan_all.py` | Scan toàn bộ dữ liệu → JSON |
| `scripts/scan_missions.py` | Scan mission + phát hiện quá hạn |

---

<div align="center">

**Mission Tracker — VOffice** · Phiên bản khởi tạo: 2026-05-26

*Powered by Markdown + YAML + AI Agent* 🤖

</div>
