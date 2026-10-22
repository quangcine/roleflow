---
name: role-show
description: Nạp lại luật hai vai Leader, Planner và xem sổ vai của dự án. Dùng ngay sau compact khi đang giữ vai, hay khi cần luật /roleflow:start, /roleflow:done, /roleflow:pause.
---

# role-show · Nạp lại luật vai

1. Dùng `Read` đọc trọn `${CLAUDE_PLUGIN_ROOT}/rulebook/Roles.md`.
2. Chạy `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/activerole.py" show` ở thư mục dự án, đọc dòng `DU_AN=` và các vai đang giữ.
