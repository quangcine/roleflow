# start · phần riêng Leader

Đọc tệp này **chỉ khi** skill `roleflow:start` đã chọn vai Leader. `A` và `Roles.md` dùng đúng đường thật đã định ở `SKILL.md` của skill này (tệp này đọc bằng `Read` nên biến đường plugin ⛔ không được thay; ⛔ không tự ghép đường). Quyền Leader: `Roles.md` mục Leader.

## Thay Leader treo *(chỉ khi `/roleflow:start leader` mà sổ đã có dòng `L`)*
Mục này chỉ quyết **có thay hay ⛔ không**; thay thì cờ vai ở Bước 3, 4 của skill là `--leader --thay`.
Lấy dòng `L` từ `python3 $A show`: `<ts L>`, `<tên L>`. Đối chiếu `ListAgents` *(ts với "started X ago", ⛔ không tin tên)*:
- **⛔ không còn phiên đó** ⟹ thay ngay.
- **Còn, `idle`** ⟹ `SendMessage` tới `<tên L>`:
  `Gửi Leader L vào lúc <ts L>: tab <tên> gõ /roleflow:start leader. Còn sống thì trong 2 phút chạy: python3 <đường thật của A, phiên gửi điền> note L <ts L> "còn sống: <việc đang làm>"`.
  Ghi lại cột *Đang làm gì* của dòng `L` lúc gửi; Monitor soi `python3 $A show` tối đa 2 phút, tới khi cột đó đổi khác.
  - Đổi ⟹ Leader cũ còn sống.
  - ⛔ không đổi sau 2 phút ⟹ thay; `start` in `VAI=Leader` xong thì nhắn Leader cũ:
    `Gửi <tên L>: tab <tên> đã thay Leader. Ngừng giao việc, ⛔ không commit; việc dở thì /roleflow:pause rồi đóng tab.`
- **Còn, `busy`** ⟹ `AskUserQuestion` hỏi chủ dự án: *thay* (Leader cũ mất quyền, việc đang chạy có thể đè nhau) hay *giữ* (tab này ⛔ không vào vai).
- **Leader cũ còn sống** *(đáp, hoặc chủ dự án chọn giữ)* ⟹ tab này DỪNG, ⛔ không vào vai, ⛔ không ghi sổ; báo một dòng Leader đang sống là `<tên L>` lúc `<ts L>`.
  Tab đã `debt-take` nợ Leader thì `python3 $A debt-return <tệp>` trước khi dừng.
- `TRUNG_PHUT_THU_LAI`: chờ sang phút sau rồi chạy lại đúng lệnh `--thay`.

## Chọn việc *(khi ⛔ không nhận nợ)*
`python3 $A index list Plan_Pass` *(⛔ không dùng `--free`: Leader phải thấy cả dòng `🔨 L` của Leader trước để nhận tiếp việc dở)* → mỗi dòng `MUC<TAB>tc<TAB>đường<TAB>Tên<TAB>ô Đang cầm`, cuối là `SO_DONG <n>`.
Đọc trường bằng `cut -f2,3,4` hoặc `awk -F'\t'`; ⛔ không dùng `IFS read` *(hai TAB liền bị gộp, trường lệch)*.
- `RONG Plan_Pass` hoặc `SO_DONG 0`: báo ⛔ không có Plan chờ thi công. Sổ ⛔ không có Planner thì Leader làm cả việc Planner: hỏi chủ dự án muốn làm gì.
- Có dòng `🔨 L`: nêu trước dưới mục *đang thi công dở* (Leader cũ bỏ dở hoặc vừa `--thay`), đọc nhật ký Code của Plan đó khi chủ dự án chọn làm tiếp.
- Có dòng: `AskUserQuestion` liệt kê *Tên* kèm *tc*, cộng lựa chọn *việc khác*. ⛔ Không đọc tệp nào khác (kể cả tệp Plan) trừ khi chủ dự án yêu cầu.
- ⛔ Không đọc `Plan_Debt` *(nợ dài hạn)*, ⛔ không `index list Plan_Debt`, trừ khi chủ dự án hỏi.
- Đọc một Plan: nối `GOC=` của `show` với *đường* (trường 3).
- Chủ dự án bảo giao ⟹ `/roleflow:codeplan <Plan>` *(skill đó tự `index hold` thành 🔨 L, tự `note`)*. Chưa bảo giao thì ⛔ không giao *(luật ⑧)*.

## Nhắc khi làm
- Trước mỗi lần giao việc: `python3 $A show` và `python3 $A debt-list` *(luật Leader trong `Roles.md`)*.
- Đang có subagent chạy thì chờ xong rồi mới `/roleflow:pause`, `/roleflow:done` hay "sửa luôn".
