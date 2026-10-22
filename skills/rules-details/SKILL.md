---
name: rules-details
description: Đọc bản đầy đủ của luật chung (CT): lý do, ca thật, các mục Deploy, Database, Code style, Ba luật quản lý luật, Bộ công cụ. Dùng khi mẫu CLAUDE.md trỏ "CT §…" hoặc cần tra luật chi tiết.
---

# rules-details · Bản đầy đủ luật chung

Dùng `Read` đọc `${CLAUDE_PLUGIN_ROOT}/rulebook/Details.md`. Đang cần một mục (vd `§Database`) thì tìm tiêu đề mục đó trước
rồi đọc theo `offset`, `limit`; ⛔ không đọc trọn tệp khi chỉ cần một mục.
