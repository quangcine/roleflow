---
name: done
description: Rời vai (Leader hoặc Planner): xoá dòng sổ vai, nhả mã ở mọi cột Đang cầm; còn việc dở thì cảnh báo, hỏi có dùng /roleflow:pause không. Dùng khi user gõ "/roleflow:done", "rời vai", "thôi vai", "xong việc rời phiên", "đóng tab".
---

# done · Rời vai

Viết tiếng Việt, ⛔ cấm em dash. Luật: `${CLAUDE_PLUGIN_ROOT}/rulebook/Roles.md` mục ①. `A=${CLAUDE_PLUGIN_ROOT}/scripts/activerole.py` (gọi `python3 $A …`);
⛔ không sửa sổ bằng tay. Mã nằm ở dòng 1 kết quả; dòng `CANH_BAO …` thì báo lại chủ dự án.
🔑 Tên `/roleflow:done` thay `/stop` vì `/stop` trùng lệnh dựng sẵn của Claude Code *("Stop this background session")*.

## Bước 1 · Tìm mình trong sổ
`python3 $A show` → tìm dòng có tên phiên mình *(dòng đầu `ListAgents`)* và `<mã> <ts>` đã in lúc `/roleflow:start`.
⛔ Không có dòng nào của mình ⟹ báo một dòng "phiên này chưa vào vai", DỪNG; ⛔ không xoá dòng của phiên khác.

## Bước 2 · Chờ subagent *(Leader)*
Đang có subagent chạy *(`/roleflow:codeplan`, Agent nền)* ⟹ chờ mọi subagent xong rồi mới đi tiếp *(luật ⑨)*.

## Bước 3 · Soát việc dở
Việc dở là một trong:
- tệp đã chạm mà chưa commit, **trong ranh giới mình chạm** *(`git status --short` ở đúng các kho mình đã sửa)*: **chỉ tính cho Leader**.
  Vai Planner ⛔ không tính, ⛔ không hỏi: commit là việc Leader (luật ⑤); Planner chỉ liệt kê đường dẫn đầy đủ ở câu trả lời Bước 5;
- Plan, Idea đang viết hoặc đang rà dở, **kể cả khi chưa thành tệp**: chủ dự án vừa nói trong phiên là đang làm, đang soạn dở thì tính là việc dở;
- dòng mục lục mình đang cầm: `python3 $A index list <sổ>` với `Plan_Draft`, `Plan_Pass`, `Idea_Draft`, `Idea_Pass`, `Idea_Done`,
  lọc trường 5 *(`cut -f5`, `awk -F'\t'`)* bằng mã mình hoặc `🔨 L`.

Có việc dở ⟹ cảnh báo, liệt kê từng việc, rồi `AskUserQuestion`:
- **`/roleflow:pause`**: ghi tệp nợ để phiên sau nhận tiếp, rồi mới rời vai. Được: việc ⛔ không mất dấu. Mất: vài phút ghi nợ.
- **Vẫn `/roleflow:done`**: rời ngay. Được: nhanh. Mất: việc dở chỉ còn trong tệp, ⛔ không ai được nhắc.
Chọn `/roleflow:pause` ⟹ đọc `${CLAUDE_PLUGIN_ROOT}/skills/pause/SKILL.md` và làm theo từ Bước 3 của skill đó; DỪNG skill này.

## Bước 4 · Rời vai
`python3 $A off <mã> <ts>` → dòng 1 `DA_XOA <n>`, dòng 2 `DA_NHA_CAM <n>`.
- `DA_XOA 0`: ⛔ không có dòng đúng mã cộng ts *(có thể tab khác đã thay Leader)*; báo chủ dự án nguyên kết quả.
- Lỗi `THIEU_MA`, `THIEU_TS`, `MA_SAI`: kiểm lại cặp `<mã> <ts>` bằng `show`, chạy lại.

## Bước 5 · Trả lời
Dòng đầu: `Tôi là <vai> <mã> lúc <ts>, đã rời vai` kèm số ô Đang cầm đã nhả. Planner thêm danh sách đường dẫn tệp đã chạm chưa commit (cho Leader, luật ⑤). ⛔ Không ghi memory, ⛔ không quét Plan, ⛔ không `SendMessage` ai.
