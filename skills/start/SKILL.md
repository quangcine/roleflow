---
name: start
description: Vào vai đầu phiên (hai vai Leader, Planner): dọn sổ vai, chọn vai, đọc nợ của vai rồi mới đọc mục lục việc theo vai, xưng danh. Dùng khi user gõ "/roleflow:start", "/roleflow:start leader", "/roleflow:start planner", "vào vai", "bắt đầu phiên", "vào Leader", "vào Planner".
---

# start · Vào vai

Viết tiếng Việt, ⛔ cấm em dash. 🔴 Đọc trọn `${CLAUDE_PLUGIN_ROOT}/rulebook/Roles.md` trước *(luật hai vai)*.
Mọi thao tác sổ đi qua `A=${CLAUDE_PLUGIN_ROOT}/scripts/activerole.py` (gọi `python3 $A …`); ⛔ không sửa sổ, mục lục, tệp nợ bằng tay, ⛔ không tự ghép đường.
**Đọc kết quả:** mã nằm ở dòng mang mã *(dòng đầu ⛔ không bắt đầu bằng `LEADER_CU=`, `THAY_DONG_CU`, `CANH_BAO`)*; dòng `CANH_BAO …` thì báo lại chủ dự án.
Cần chọn thì hỏi bằng `AskUserQuestion`, mỗi lựa chọn nói được gì, mất gì. ⛔ không `SendMessage` ai lúc vào vai (trừ bước thay Leader treo trong `leader.md`).

## Bước 1 · Dọn sổ
- Tên phiên mình = dòng đầu của `ListAgents`; gọi là `<tên>`.
- `python3 $A show` → `DU_AN=… GOC=…` rồi các dòng sổ. `KHONG_RO_DU_AN` thì hỏi chủ dự án đang làm dự án nào, DỪNG.
- Dòng sổ có tên phiên ⛔ không còn trong `ListAgents` *(đối chiếu ts với "started X ago", ⛔ không tin tên)*: liệt kê, hỏi chủ dự án xoá; đồng ý thì `python3 $A off <mã> <ts>`.
- `python3 $A debt-list` → dòng `DANG_NHAN <tệp> 🔒 Đang nhận bởi <phiên> lúc <ts>` mà phiên ⛔ không còn chạy: hỏi trả về ⏳; đồng ý thì `python3 $A debt-return <tệp>`.

## Bước 2 · Chọn vai *(⛔ không ghi gì ở bước này)*
| Gõ | Vai | Cờ |
|---|---|---|
| `/roleflow:start` | sổ chưa có dòng `L` → Leader, in một dòng báo, ⛔ không hỏi lại; có rồi → Planner | `--leader` hoặc `--planner` |
| `/roleflow:start planner` | Planner, kể cả khi chưa có Leader | `--planner` |
| `/roleflow:start leader` | sổ chưa có `L` → Leader; có `L` → làm mục **Thay Leader treo** trong `leader.md` trước | `--leader` (thay: `--leader --thay`) |

Chọn vai xong đọc **đúng một** tệp: `${CLAUDE_PLUGIN_ROOT}/skills/start/leader.md` hoặc `${CLAUDE_PLUGIN_ROOT}/skills/start/planner.md`.

## Bước 3 · Nợ của vai
`python3 $A debt-list --vai <Leader|Planner>` → tìm dòng `SO_NO <n>` *(⛔ không đọc dòng 1)*.
- `n > 0`: hỏi chủ dự án chọn một nợ (việc dở, mã cũ, ts) hoặc **làm việc mới**.
- Nhận nợ: `python3 $A debt-take <No_….md> --phien "<tên>"` → `DA_GIU <đường>`; rồi
  `python3 $A start <cờ vai> --no <No_….md> --phien "<tên>"` *(cùng `--phien`)* → `NO_DA_NHAN`, `VAI=… MA=… TS=…`.
  Xong mới `Read` **một** tệp ở `<đường>` của `DA_GIU`, làm tiếp từ mục *Bước tiếp theo*. Cột *Đang cầm* đã nhả khi phiên cũ rời: cầm lại bằng `index hold` như tệp vai dặn.
- `DA_CO_NGUOI_NHAN`: phiên khác vừa nhận, hỏi chọn lại.

## Bước 4 · Ghi sổ khi ⛔ không nhận nợ
`python3 $A start <cờ vai> --phien "<tên>" --viec "vừa vào"` → `VAI=<vai> MA=<mã> TS=<ts>`. Rồi làm mục **Chọn việc** của tệp vai.

## Mã lỗi của `start`
- `KHONG_GHI` *(sau `LEADER_CU=…`)*: Leader vừa vào ở tab khác. Đã `debt-take` thì `debt-return <tệp>`; rồi `/roleflow:start` trơn quay lại Bước 2 với Planner; `/roleflow:start leader` làm mục *Thay Leader treo* của `leader.md`.
- `VAI_NO_KHAC`: `debt-return <tệp>`, hỏi chọn lại. `THIEU_PHIEN`: thiếu `--phien`, chạy lại có `--phien "<tên>"`.
- `TRUNG_PHUT_THU_LAI`: chờ sang phút sau (Monitor tới khi `date +%M` đổi) rồi chạy lại đúng lệnh.
- Mã khác: báo chủ dự án nguyên dòng, DỪNG. Lệnh lỗi sau `debt-take` thì luôn `debt-return` trước khi dừng.

## Bước 5 · Xưng danh
Dòng đầu câu trả lời: `Tôi là <Leader|Planner> <mã> lúc <ts>` *(lấy ở `VAI=… MA=… TS=…`)*. Có `LEADER_CU=L <ts> <tên>` thì thêm một dòng Leader đang là ai.
Nhớ `<mã> <ts>`: `/roleflow:done`, `/roleflow:pause`, `note` cần đúng cặp này. Đổi việc thì `python3 $A note <mã> <ts> "<việc>"`.
