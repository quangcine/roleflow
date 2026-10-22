---
name: pause
description: Tạm dừng vai còn việc dở: viết tệp nợ ngắn hạn (⛔ không quá 40 dòng, khuôn năm mục), thêm dòng vào sổ nợ, rồi rời vai như /roleflow:done để phiên sau nhận tiếp bằng /roleflow:start. Dùng khi user gõ "/roleflow:pause", "tạm dừng", "ghi nợ rồi nghỉ", "bàn giao việc dở", "hết ngữ cảnh".
---

# pause · Ghi nợ rồi rời vai

Viết tiếng Việt, ⛔ cấm em dash. Luật: `${CLAUDE_PLUGIN_ROOT}/rulebook/Roles.md` mục ①, ⑥. `A=${CLAUDE_PLUGIN_ROOT}/scripts/activerole.py` (gọi `python3 $A …`);
⛔ không sửa sổ, tệp nợ bằng tay. Mã nằm ở dòng 1 kết quả; dòng `CANH_BAO …` thì báo lại chủ dự án.
⛔ Không ghi memory *(bài học ghi vào tệp nợ, Leader quyết)* · ⛔ không quét Plan · ⛔ không `SendMessage` ai.

## Bước 1 · Tìm mình, chờ subagent
- `python3 $A show` → dòng có tên phiên mình *(dòng đầu `ListAgents`)*, lấy `<vai> <mã> <ts>`. ⛔ Không có thì báo "phiên này chưa vào vai", DỪNG.
- **Leader** đang có subagent chạy ⟹ chờ mọi subagent xong rồi mới ghi nợ *(luật ⑨)*.

## Bước 2 · Có gì dở không
Soát như Bước 3 của `/roleflow:done` *(tệp chạm chưa commit trong ranh giới mình; Plan, Idea đang viết, rà; ô Đang cầm mang mã mình hoặc `🔨 L` qua `index list <sổ>`)*.
⛔ Không có gì dở ⟹ `AskUserQuestion`: **dùng `/roleflow:done`** (rời vai, ⛔ không tạo tệp nợ rỗng) hay **vẫn ghi nợ** (khi chủ dự án biết việc dở mà soát ⛔ không thấy).
Chọn `/roleflow:done` ⟹ `python3 $A off <mã> <ts>`, trả lời như Bước 5 của `/roleflow:done`, DỪNG.

## Bước 3 · Viết nháp tệp nợ
Ghi nháp vào scratchpad *(⛔ không ghi vào kho)*, đúng **năm** mục theo thứ tự, tên mục chép y nguyên:
```
## Việc dở
<một dòng tóm việc dở, trùng --viec>
<vì sao chưa xong, tới đâu>
## Plan, Idea đang cầm
<đường từ gốc lấy ở trường 3 của index list; ⛔ không chép nội dung>
## Tệp đã chạm chưa commit
<đường đầy đủ từng tệp, mỗi tệp một dòng>
## Bước tiếp theo
<1 tới 3 dòng>
## Câu đang chờ chủ dự án
<câu hỏi chưa có lời đáp, hoặc "Không có">
```
Script tự thêm 3 dòng đầu (tên, trạng thái ⏳, vai, mã, ts, phiên) nên nháp ⛔ không quá **37 dòng**.

## Bước 4 · Ghi nợ
`python3 $A debt-write --vai <Leader|Planner> --ma <mã> --ten <TenNgan> --viec "<một dòng>" --phien "<tên phiên>" --body <đường nháp>`
- `<TenNgan>` chỉ chữ, số *(ví dụ `RaPlanLuong`)*. `--viec` ≤ 120 ký tự, cũng là dòng sổ nợ.
- Thành công: `DA_GHI_NO <đường tệp nợ>`.
- `QUA_40_DONG`: rút gọn nháp rồi chạy lại. `NHAP_THIEU_MUC`: sửa tên mục cho đúng. `TEN_NGAN_CHI_CHU_SO`: đổi tên.
  `TEP_NO_DA_CO`: đổi `--ten`. Mã khác: báo chủ dự án nguyên dòng, DỪNG, ⛔ không rời vai.

## Bước 5 · Rời vai
`python3 $A off <mã> <ts>` → `DA_XOA <n>`, `DA_NHA_CAM <n>` *(ô Đang cầm của mình nhả hết; phiên nhận nợ sẽ cầm lại)*. `DA_XOA 0` thì báo chủ dự án.

## Bước 6 · Trả lời
Dòng đầu: `Tôi là <vai> <mã> lúc <ts>, đã ghi nợ và rời vai`, rồi một dòng đường tệp nợ. Phiên sau gõ `/roleflow:start` sẽ thấy nợ này.
