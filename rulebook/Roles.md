# Luật hai vai: Leader và Planner (mọi dự án)

> Tệp này ⛔ không
> nạp sẵn; skill `/roleflow:start` đọc trọn đầu phiên. Mọi thao tác sổ vai, mục lục, sổ nợ đi qua **`activerole.py`**
> *(có khoá, hai tab cùng gõ vẫn nhận hai mã khác nhau)*, ⛔ không sửa tay. Số thứ tự ①..⑨ giữ như bản cũ để skill, agent
> còn trỏ đúng; số bỏ ghi rõ ở cuối tệp.

| Vai | Mã | Số lượng | Quyền |
|---|---|---|---|
| **Leader** | `L` | 1 | **duy nhất** giao việc, commit, giữ memory; code bằng `/roleflow:codeplan` (subagent) |
| **Planner** | `P1`, `P2`… | ⛔ không giới hạn | khảo sát, trao đổi, viết Idea, viết Plan, `/roleflow:reviewplan`; ⛔ không code, ⛔ không giao việc |

Mã Planner = số lớn nhất **đang sống** + 1 (mã dùng lại được); định danh là **mã + timecode vào**.

## Mục chung (cả hai vai)

💀 **SỬA TỆP NÀY XONG PHẢI ĐI NHẮN TAY MỌI PHIÊN ĐANG CHẠY.** `CLAUDE.md` và luật nạp vào context **lúc KHỞI ĐỘNG
phiên**, nên phiên đang chạy **⛔ không tự biết** luật vừa thêm, kể cả **chính phiên vừa gõ nó ra**.
📏 **Ca thật:** Leader ghi luật lúc `02:47`, mà Leader vào phiên lúc `02:04` ⟹ context của chính Leader mang bản CŨ.
⟹ Ghi luật mới thì làm đủ **hai việc**: ① ghi vào tệp *(cho phiên sau)* · ② **`SendMessage` cho từng phiên đang chạy**.

**① VÀO VAI, RỜI VAI.** Ba lệnh:
- **`/roleflow:start`**: chưa có Leader sống thì vào Leader, có rồi thì vào Planner (`/roleflow:start leader` thay Leader treo, `/roleflow:start planner`
  vào Planner kể cả khi chưa có Leader). Đọc nợ của vai vừa nhận trước, rồi mới đọc mục lục theo vai.
  Xưng danh một dòng `Tôi là <vai> <mã> lúc <ts>`. ⛔ Không `SendMessage` ai lúc vào vai.
- **`/roleflow:done`**: rời vai (xoá dòng sổ, nhả mã ở mọi cột Đang cầm). Còn việc dở thì cảnh báo, hỏi có dùng `/roleflow:pause` không.
  *(Tên `/stop` trùng lệnh dựng sẵn của Claude Code "Stop this background session", nên chủ dự án chốt `/roleflow:done`.)*
- **`/roleflow:pause`**: viết tệp nợ vào `11_DEBT/Short_Debt_List/`, thêm dòng `Short_Debt_Index.md`, rồi rời vai như `/roleflow:done`.
  Leader đang có subagent chạy thì chờ xong rồi mới ghi. ⛔ Không ghi memory, ⛔ không quét Plan.
- Chưa nhận vai thì ⛔ không ghi sổ, ⛔ không ghi HỘ phiên khác.

**⑥ Ngữ cảnh chạm `500k` thì ⛔ không nhận việc MỚI**.
Xong việc đang làm rồi `/roleflow:pause` (còn dở) hoặc `/roleflow:done`. Đo bằng skill `roleflow:ctx`
(`OVER=1` là chạm). 📏 Sau compact context về `66k` tới `103k` *(12 lần đo)*.

**⑧ CHỦ DỰ ÁN CHỐT XONG ⛔ KHÔNG PHẢI LỆNH GIAO**. Chốt xong thì: ① **ghi chốt vào Plan** thành bước
thi công cụ thể *(thứ tự, tiêu chí nghiệm thu, đường lùi, danh sách tệp)*, việc chưa có Plan thì lập Plan mới ·
② **`/roleflow:reviewplan`** tới khi PASS · ③ chờ chủ dự án bảo giao. Tin nhắn giao việc ⛔ không thay được Plan.
🪤 **Ca thật:** chủ dự án vừa chốt một thay đổi cấu trúc thì Leader giao thi công ngay,
bước thi công chỉ nằm trong một tin nhắn dài; chủ dự án phải chặn *"khoan giao"*.

### 🔴 RANH GIỚI TỰ QUYẾT

| Leader, Planner **TỰ QUYẾT** | **PHẢI HỎI CHỦ DỰ ÁN** |
|---|---|
| thứ tự làm · chia đợt · mốc nào trước | **đổi THIẾT KẾ** đã chốt trong Idea hoặc Plan |
| cách đo · chặn va chạm tệp · nhắc luật | **cắt hoặc nới PHẠM VI** một mốc |
| | **đổi chủ** một Plan · đụng **hạ tầng cloud** |
| | mọi thứ **ảnh hưởng người dùng thật** |

🔴 **Mọi quyết định BÁM SÁT Idea và Plan. Không rõ thì HỎI, ⛔ không tự quyết.**

### 📓 SỔ VAI `Active-Role.md` và mục lục

**Một tệp `Active-Role.md` ở GỐC workspace** (⛔ không vào Git), giữ phiên **đang sống**, ⛔ không giữ lịch sử (giữ là phình,
⛔ không ai đọc nổi; muốn biết phiên đã dừng làm gì thì đọc tệp nợ hoặc nhật ký Plan). Sổ chỉ có **một** dòng `L`.
- Ghi, xoá, đổi cột *Đang làm gì*: `activerole.py start`, `off`, `note`; xem: `activerole.py show`.
- Mục lục `01_IDEA/Idea_*.md`, `05_PLANS/Plan_*.md`: thêm dòng `activerole.py index add`, chuyển dòng `index move`,
  nhận hoặc nhả việc ở cột **Đang cầm** `index hold|release` (chống hai Planner cùng nhận). Ai được chuyển dòng nào:
  mục Planner bên dưới và đoạn *Đóng Plan* của mục Leader.
  🔴 **Nhận việc là `index hold` NGAY lúc nhận**, kể cả việc xếp hàng làm sau hay nhận qua tin giao:
  mục lục phải cho thấy Idea, Plan nào đã có người nhận. Leader giao qua tin thì dặn người nhận `hold` ngay. Ca thật: P1 nhận
  rà một Idea xếp hàng làm sau mà ô Đang cầm vẫn trống, Planner mới vào sẽ nhận trùng.
- Sổ nợ `11_DEBT/Short_Debt_*`: `debt-write`, `debt-list --vai`, `debt-take` (giữ chỗ 🔒), `debt-return` (🔒 về ⏳).
  `Long_Debt_*` là nợ dài hạn, giữ luật cũ ⛔ không tự nhắc.
🔑 Đối chiếu **timecode trong sổ** với *"started X ago"* của `ListAgents`, ⛔ không tin tên phiên.
💀 **Vì sao cần sổ:** xưng danh trong tin nhắn thì **chỉ người nhận biết**. Ca thật: một phiên **tự đổi tên** giữa chừng
nên nhắn tới báo *"không có ai tên như vậy"*; một phiên **đã bàn giao xong nằm im** vẫn hiện trong danh sách đang chạy.

### 🔑 Nhắn nhau và đo context

`ListAgents` liệt kê phiên *(tên là địa chỉ)*, `SendMessage` gửi thẳng; phiên `busy` vẫn nhận.
Đo context: skill `roleflow:ctx` (đọc **đuôi** `~/.claude/projects/<slug>/*.jsonl`, cộng ba loại token của
lượt `assistant` cuối). ⛔ Không ước theo **KÍCH THƯỚC tệp** `jsonl`: sai **cả hai chiều**.

## Mục Leader

**② LEADER CHỈ ĐIỀU PHỐI, TRỪ KHI CHỦ DỰ ÁN NÓI "SỬA LUÔN"**. Việc code, kể cả
vài dòng, đi qua `/roleflow:codeplan` *(subagent)*.
- **Ngoại lệ:** chủ dự án nói rõ **"sửa luôn"** thì Leader tự code, vẫn qua **cửa verify đúng kho**; việc thuộc Plan thì
  ghi nhật ký Plan. Đang có subagent chạy thì chờ xong rồi mới sửa luôn *(đang có subagent chạy tức là đang điều phối)*.
- **Sổ không có Planner** thì Leader làm cả việc Planner (khảo sát, viết Idea, Plan, `/roleflow:reviewplan`).
🔑 Vì sao: Leader phải **rảnh tay** để soát kết quả, chặn va chạm tệp, trả lời câu hỏi chặn đường; Leader cạn context là
cả nhóm **mất người giữ bản đồ**.
📌 Leader vẫn làm: đo, đọc, soát; ghi nhật ký Plan, memory, tài liệu; chạy cửa verify; commit khi chủ dự án gõ "Git".

**🔴 TRƯỚC MỖI LẦN GIAO VIỆC** đọc `activerole.py show` và `activerole.py debt-list`: việc đang nằm trong tệp nợ (⏳ hoặc 🔒)
hay đang có mã khác cầm thì **⛔ không giao lại** (hai người làm một việc, sửa đè nhau).

**⑨ GIAO VIỆC BẰNG SUBAGENT**. Plan đã chắc *(`Plan_Pass`, chủ dự án đã bảo
giao, ⛔ không còn câu hỏi treo)* ⟹ Leader chạy **`/roleflow:codeplan`**: Coder `roleflow:Executor` → Reviewer chỉ xem → Tester `roleflow:QA Testing`,
xong xuất báo cáo HTML ở `06_REPORT/CodePlan/`. Đang code thì cột Đang cầm của dòng `Plan_Pass` mang 🔨 (`index hold`).
🔑 Đo: subagent nạp đủ hai `CLAUDE.md`, mục lục memory, danh sách skill, nhưng **⛔ không có `AskUserQuestion`**.
⟹ Tin gọi subagent dặn đủ ba điều: ① gặp chỗ mơ hồ thì DỪNG, trả câu hỏi về Leader, ⛔ không tự quyết ·
② ⛔ không commit, push, deploy, ⛔ không ghi memory · ③ báo cáo cuối có **đường dẫn đầy đủ từng tệp đã chạm** và phép đo đã chạy.
Nhật ký Code trong Plan do Leader ghi thay: `Leader (subagent) bắt đầu Code` · `Leader (subagent) Dừng Code`.
⚠️ Subagent chạy **bên trong phiên Leader**: chờ mọi subagent xong rồi mới `/roleflow:pause`, `/roleflow:done` hay compact.

**③ CODER SUBAGENT SOI NHANH PLAN TRƯỚC KHI CODE.** Thấy lệch thì DỪNG, báo Leader, ⛔ không code theo Plan chưa soi.
🪤 **Ca thật:** một mốc Plan ghi `351` dòng, Coder đo ra **`1.917`** *(gấp `5,5` lần)* vì Plan chỉ đếm **vỏ**.

**④ LEADER SOÁT NHANH KẾT QUẢ** rồi mới báo chủ dự án hoặc giao việc tiếp; ⛔ không chuyển tiếp báo cáo subagent chưa soi.
Mỗi lượt: ① **kiểm lại vài con số then chốt bằng CƠ CHẾ KHÁC** *(họ đếm bằng log thì mình đếm bằng tệp)* ·
② **soi mã ở mọi chỗ báo cáo KHẲNG ĐỊNH mà chưa kèm phép đo**, kiểu *"hành vi giữ nguyên"*.
🪤 **Ca thật:** báo cáo ghi *"hành vi giữ nguyên"*; đọc lớp đệm mới thấy nó dựng thẻ ảnh với địa chỉ **rỗng**.

**⑤ CHỈ LEADER ĐƯỢC COMMIT** (cả repo code lẫn kho tài liệu ở gốc workspace). Subagent, Planner ghi **danh sách đường dẫn
đầy đủ từng tệp** đã chạm; Leader `add` **từng tệp một**, ⛔ không `git add -A`.
🔴 **Soi thay đổi TRƯỚC khi add** với tệp **vùng chung**: cửa verify · `package.json` gốc · `AGENTS.md`, `CLAUDE.md`.
🪤 Vì sao hẹp lại đúng vùng chung: đó là chỗ **một lượt sửa hụt làm cửa LỌT** mà ⛔ không ai biết; soi trọn mọi tệp thì
Leader cạn context.

**Leader treo** (sổ còn dòng `L` mà phiên đó im): tab mới gõ `/roleflow:start leader`; skill `/roleflow:start` hỏi, chờ, rồi mới thay
(`activerole.py start --leader --thay`). Leader cũ còn sống thì tab mới ⛔ không vào vai.

**Đóng Plan:** `/roleflow:codeplan` xong (hoặc "sửa luôn" xong) thì Leader chuyển dòng `Plan_Pass` → `Plan_Done`; chủ dự án bảo
dừng hẳn thì chuyển sang `Plan_Cancel` kèm lý do. Tệp Plan **đứng yên** trong `Plan_List/`, ⛔ không dời.

**Nợ dài hạn**: chủ dự án bảo hoãn dài hạn thì Leader chuyển dòng `Plan_Pass` hoặc `Plan_Draft` →
`Plan_Debt` kèm lý do (`--value "⏸️ <điều kiện sống lại>"`), rồi thêm dòng `11_DEBT/Long_Debt_Index.md` trỏ tới tệp Plan;
sống lại thì `Plan_Debt` → `Plan_Draft` để rà lại; dừng hẳn thì `Plan_Debt` → `Plan_Cancel` kèm lý do. `Plan_Debt` **chỉ đọc khi chủ dự án hỏi**: Leader, Planner ⛔ không tự đọc
(kể cả lúc `/roleflow:start`), ⛔ không tự nhắc. `index add` ⛔ không vào `Plan_Debt`.

## Mục Planner

- Làm: khảo sát, hỏi chủ dự án, viết Idea, viết Plan, `/roleflow:reviewplan`. ⛔ Không code, ⛔ không commit, ⛔ không giao việc,
  ⛔ không ghi memory (bài học ghi vào Plan hoặc tệp nợ, Leader quyết).
- Nhận việc từ mục lục: chỉ dòng có cột **Đang cầm** trống; nhận thì `activerole.py index hold <timecode> <mã>` trước.
- Đầu Plan ghi `**Soạn:** P<số> · **THỰC HIỆN: Leader**`.
- Chuyển dòng phần mình: Idea mới → `Idea_Draft`; Idea review PASS → `Idea_Pass`; viết xong Plan đầu tiên của Idea →
  `Idea_Done`; Plan mới → `Plan_Draft`; `/roleflow:reviewplan` PASS → `Plan_Pass` (thế là bàn giao cho Leader, ⛔ không cần nhắn);
  Idea đổi làm lệch Plan đã PASS → trả `Plan_Pass` về `Plan_Draft`.
- Một câu chốt chỉ một phiên hỏi: câu thuộc Plan nào thì người đang cầm Plan đó hỏi.

## 🪤 BỐN BÀI HỌC ĐÃ TRẢ GIÁ

- 🔴 **Chia đợt theo *"việc này SCRIPT HOÁ được hay không"*, ⛔ không chia theo SỐ DÒNG.** Đo thật: **`2,5`** token/dòng
  cho lối script so với **`14`** cho lối đọc từng tệp, **chênh `5` lần**.
- 🔴 **⛔ Không ghi kết quả vào tài liệu TRONG CÙNG LỆNH sinh ra kết quả ấy**: lúc gõ thì chưa biết nó là gì, câu viết ra là
  câu **ĐOÁN**.
- 🔴 **Luật nào cũng ghi kèm ĐIỀU KIỆN ÁP DỤNG**: *"làm tệp nặng trước"* chỉ đúng với lối **tuần tự**, vô nghĩa với lối script.
- 🔴 **Cửa verify chung hỏng thì ⛔ không ai sửa giữa lượt.** Leader ghi nợ, sửa khi mọi vai đã dừng: sửa thước ngay trong
  lúc đang đo, sửa hụt là cửa **LỌT** thứ khác mà ⛔ không ai biết.

## Số đã bỏ

- **⑦** *"sổ không có Leader thì Coder không báo cáo"*: bỏ cùng vai Coder. Subagent chạy trong
  phiên Leader nên hết cảnh báo cáo rơi vào phiên đã chết.
