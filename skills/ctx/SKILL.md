---
name: ctx
description: Đo ngữ cảnh phiên đang dùng bao nhiêu token so với hạn mức; in OVER=1 là đã chạm, ⛔ không nhận việc mới. Dùng khi luật hạn mức token cần đo, hay user hỏi "còn bao nhiêu ngữ cảnh".
---

# ctx · Đo ngữ cảnh

1. Lấy session id: đoạn ngay trước `/scratchpad` trong đường thư mục scratchpad của phiên.
2. Chạy `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/activerole.py" ctx <session id>`.
3. Báo lại dòng in ra (`CTX=… LIMIT=… LEFT=… OVER=…`). `OVER=1` thì làm xong việc đang dở rồi `/roleflow:pause` hoặc `/roleflow:done`, hay nhắc user `/compact`.
