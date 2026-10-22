# Quy ước chung (mọi dự án): nạp mỗi phiên

> Áp cho mọi dự án; phần riêng ở `<dự-án>/CLAUDE.md`. Bản đầy đủ, lý do, ca thật → skill `roleflow:rules-details` (gọi tắt **CT**).

## Luôn nhớ
- Trả lời **tiếng Việt** (giữ nguyên thuật ngữ, tên tệp, code). 🔴 **Cấm em dash `U+2014`** trong mọi thứ Claude viết;
  thay bằng `:` · `,` · ngoặc đơn · `-` · `;` hoặc tách câu.
- 🔴 **Chưa chắc thì hỏi bằng `AskUserQuestion`**, ⛔ đừng đoán: văn xuôi trước (cơ chế, chỗ hở, một ca thật có tên người và số tiền),
  rồi mới gọi tool với câu hỏi một dòng; mỗi lựa chọn nói được gì, mất gì.
- 🔴 **Hỏi về UI thì MỞ ảnh từng lựa chọn lên** (`open <tệp ảnh>`) ngay trước `AskUserQuestion`; chỉ đưa link là ⛔ không đủ.
- Nêu giả định; có cách đơn giản hơn thì nói và phản đối hướng phức tạp thừa. ⛔ Không thêm gì ngoài yêu cầu.
- Sửa đúng chỗ: ⛔ không refactor lân cận; lỗi ngoài phạm vi thì nhắc user, để yên; orphan do mình tạo thì xoá.
- Định tiêu chí xong trước, làm tới khi qua **cửa verify đúng kho**;
  phần động ⛔ không tự đo được thì báo user test.
- 🔴 Định danh code mới bằng **tiếng Anh**, kể cả khi đặt cạnh tệp tên Việt → skill `roleflow:english-naming`
- 🔴 Ngữ cảnh chạm **`500k`** thì ⛔ không nhận việc mới: xong việc dở rồi `/roleflow:pause` (còn dở) hoặc `/roleflow:done`, hay nhắc `/compact`.
  Đo bằng skill `roleflow:ctx` (`OVER=1` là chạm). Gộp lệnh, ⛔ không `cd` trần
- 🔴 Đang giữ vai mà vừa compact thì trước khi làm tiếp: gọi skill `roleflow:role-show`
  · đọc lại mốc Plan đang cầm *(⛔ không tin bản tóm tắt)* · Leader kiểm subagent còn sống.
- 🔴 **CỬA #0**: ngay trước mỗi lệnh đẩy lên cloud, kiểm tài khoản và in ra cho user; sai thì DỪNG, báo user.
  GitHub, EAS chờ lệnh **"Git"**; **"Push"** chỉ là `supabase db push` → skill `roleflow:git`

## Làm việc gì thì đọc gì
| Khi | Đọc |
|---|---|
| Deploy, "Git", "Push", phiên cloud | skill `roleflow:git` · CT §Deploy |
| Viết schema, SQL, RLS | CT §Database |
| Viết code (đặt tên, an toàn) | CT §Code style · skill `roleflow:english-naming` |
| Viết tài liệu, memory, luật; dọn đồ thừa | CT §Ba luật quản lý luật |
| Sửa `~/.claude` (luật, skill, agent, memory) | CT §Kho cấu hình |
| Vào vai, rời vai (`/roleflow:start` `/roleflow:done` `/roleflow:pause`); hai vai Leader, Planner | skill `roleflow:role-show` |
| Chọn agent, lệnh | CT §Bộ công cụ |
