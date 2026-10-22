---
name: exportplan
description: Xuất 1 Plan ra file HTML trực quan (tabs/sơ đồ/máy tính) TRÙNG TÊN Plan, đặt cạnh file .md. Dùng khi user nói "xuất plan", "export plan", "xuất HTML plan", "html plan", "xem plan trực quan", HOẶC khi user ĐỒNG Ý lời mời xuất HTML ở 2 mốc (viết-xong-Plan / thực-hiện-xong-Plan).
---

# ExportPlan: xuất Plan ra HTML trực quan (trùng tên Plan)

Viết mọi văn bản bằng **tiếng Việt**. Mục tiêu: biến 1 file Plan `.md` (dày chữ, khó đọc cho người ⛔ không quen đọc đặc tả) thành **HTML self-contained trực quan** để user trình bày/duyệt.

## 🔴 QUY TẮC HỎI (bắt buộc): 2 MỐC
Mỗi Plan có **2 thời điểm** PHẢI hỏi user "có xuất HTML để xem trực quan không?":
1. **Khi VIẾT XONG Plan** (vừa tạo/cập nhật lớn file `.md`) → hỏi trước khi đi tiếp.
2. **Khi THỰC HIỆN XONG Plan** (code/deploy xong, chuẩn bị đóng Plan) → hỏi để xuất bản tổng kết.
- **CHỈ xuất khi user ĐỒNG Ý**: ⛔ không auto. Xong Plan hoặc sửa lớn thì **hỏi rồi chờ duyệt**.
- Hỏi gọn 1 dòng (vd "Xuất HTML trực quan cho Plan này để xem không?"). User OK → chạy skill này.

## Vị trí + tên file
- **HTML TRÙNG TÊN Plan**, đặt **CẠNH file `.md`** trong **cùng thư mục** với nó.
- Tệp Plan đứng yên trong `05_PLANS/Plan_List/` (hoặc thư mục module con) dù xong hay chưa, nên HTML cũng nằm yên cạnh `.md`.

Thư mục Plan, mẫu HTML tham khảo, nguồn màu: đọc mục tương ứng ở `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án.

- 🔴 Dự án **chưa rõ đường dẫn, cửa verify, tài khoản** thì ⛔ ĐỪNG ĐOÁN: bám `CLAUDE.md` của dự án, không thấy thì **HỎI user**.
- KHÁC tài liệu trình bày chung: loại kia sống NGOÀI luồng Plan; ExportPlan là **ảnh chụp 1 Plan cụ thể**, sống cạnh Plan.

## Cách viết HTML (bám mẫu sẵn có của dự án, xem `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án)
- **Self-contained 1 file** (nhúng CSS + JS + data inline, mở offline, không cần internet/lib ngoài; nếu cần chart thì nhúng Chart.js inline).
- **Style tối** (dark). 🔴 **Lấy màu từ nguồn của dự án** (xem `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án), ⛔ đừng bê bảng màu dự án khác sang: bản in ra sẽ lạc tông với chính sản phẩm.
  - Màu trạng thái dùng chung được: OK `#34d399`, DANGER `#f87171`, WARN `#fbbf24`, BLUE `#60a5fa`, PURPLE `#a78bfa`.
- **Nhiều TAB** (1 tab/chủ đề lớn của Plan): công thức, sơ đồ luồng/state-machine, bảng số liệu, ví dụ, máy tính thử, "cần chốt", "đã chốt".
- **Trực quan hóa**: công thức trong `.formula` (mono, nền tối); state machine = các `.node` + mũi tên `↓`; bảng số thật; **máy tính tương tác** (input → JS tính realtime) cho phần có công thức.
- **GIỮ SỐ THẬT** vì đây là bản **nội bộ**. ⚠️ Bản mang RA NGOÀI (gửi khách, đăng công khai) là việc khác và **phải sanitize số**; ⛔ đừng lẫn hai loại.
- Header ghi rõ: tên Plan (mono) + trạng thái (CHƯA code / ĐÃ code…) + ngày.
- **Mở file sau khi tạo**: `open <đường-dẫn>.html`.

## Quy trình
1. Đọc file Plan `.md` (đường dẫn user chỉ, hoặc Plan vừa làm việc).
2. **Xác định dự án** rồi lấy **nguồn màu** và **mẫu tham khảo** của nó (xem `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án), ⛔ đừng dùng mặc định.
3. Rút các phần lớn → mỗi phần 1 tab. Tìm công thức/số liệu/state-machine để trực quan hóa + máy tính.
4. Viết file HTML trùng tên cạnh `.md`. `open` nó.
5. Báo user 1-2 dòng: đã xuất gì (mấy tab), đường dẫn.

## Ràng buộc
- Tiếng Việt · chỉ xuất khi user duyệt (không auto) · giữ số thật (nội bộ).
- Chỉ tạo/mở file HTML; KHÔNG commit/push/deploy.
- HTML là ẢNH CHỤP Plan tại thời điểm xuất: Plan `.md` vẫn là nguồn sự thật; nếu Plan đổi nhiều thì xuất lại (ghi đè).
