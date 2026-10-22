---
name: checkplan
description: Rà TRẠNG THÁI Plan: đọc mục lục Plan_Pass, VERIFY QUA CODE Plan nào thật sự xong (tick todolist KHÔNG tin được cả 2 chiều), hỏi xác nhận rồi chuyển dòng Plan_Pass sang Plan_Done (Plan chết sang Plan_Cancel) bằng activerole.py; tệp Plan đứng yên, ⛔ không dời, ⛔ không nắn link. Dùng khi user nói "checkplan", "check plan", "dọn plan", "rà plan", "kiểm tra plan", "đóng plan".
---

# CheckPlan: rà trạng thái Plan (verify qua CODE, không tin todolist)

Viết tiếng Việt, ⛔ cấm em dash. Mục tiêu: mục lục `Plan_Pass` chỉ còn Plan **SỐNG thật** (code chưa xong, code dở); Plan **code xong** thì
chuyển dòng sang `Plan_Done`. Tệp Plan **đứng yên** trong `Plan_List/` *(⛔ không còn dời tệp, ⛔ không còn nắn link)*.
Luật chuyển dòng: `${CLAUDE_PLUGIN_ROOT}/rulebook/Roles.md` (*Đóng Plan* là việc **Leader**; Planner chạy skill này thì chỉ báo).

> **TIÊU CHÍ "Plan XONG" = CODE XONG:** phần CODE đã viết + verify tĩnh (cửa verify của dự án EXIT 0, xem `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án, + artifact
> tồn tại thật). **⛔ Không chờ Git, ⛔ không chờ user test in-app, ⛔ không chờ user vận hành hạ tầng** (tạo bucket, cutover NS, quét QR…).
> Việc vận hành còn lại ghi sổ nợ hoặc memory, ⛔ không giữ Plan sống vì nó.

> **Bài học cốt lõi:** todolist `- [x]`/`- [ ]` **⛔ không đáng tin CẢ HAI CHIỀU**: vừa *tick nhầm thành xong*, vừa *làm rồi quên tick*.
> **PHẢI verify qua CODE.**

> 🤖 **Bước 0 tới 2 giao `Agent` `subagent_type: "roleflow:PlanChecker"`** *(chỉ báo, ⛔ không sửa, ⛔ không chuyển dòng)*. Tin gọi: gốc workspace, phạm vi.
> **Bước 3 tới 5 phiên chính giữ** *(hỏi user, chuyển dòng, báo cáo)*, vì subagent ⛔ không có `AskUserQuestion`.

## Bước 0 · Phạm vi
- Cây ở **gốc workspace** (mọi dự án cùng khuôn): mục lục `05_PLANS/Plan_Pass.md`, mỗi dòng `| Timecode | Tên | [link](Plan_List/…) | Đang cầm | Ghi chú |`.
  User chỉ định Plan thì chỉ rà các dòng đó.

Cửa verify tĩnh, nơi verify artifact: đọc mục tương ứng ở `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án.

- 🔴 Dự án **chưa rõ đường dẫn, cửa verify, tài khoản** thì ⛔ ĐỪNG ĐOÁN: bám `CLAUDE.md`, không thấy thì **HỎI user**.
- ⚠️ **Cạm bẫy cwd:** dùng `(cd <thư-mục> && …)` hoặc `git -C`, ⛔ không `cd` trần.

## Bước 1 · Đọc mục lục, phân loại
Đọc `05_PLANS/Plan_Pass.md`. ⛔ Không quét đệ quy `Plan_List/`, ⛔ không đọc `Plan_Done.md`, `Plan_Cancel.md`, `Plan_Debt.md` *(trừ khi user hỏi)*.
Mỗi dòng: theo link, **chỉ `rg`, `head`** lấy dòng trạng thái, `Hoàn thành Plan lúc`, `Nhật ký Code`, đếm `- [x]` với `- [ ]`
⚡ ⛔ không `Read` trọn tệp Plan (nhiều tệp 90k tới 160k ký tự). Ô Đang cầm có 🔨 *(Leader đang code)* thì bỏ qua, trừ khi user chỉ định.
- **A. Nghi ĐÃ XONG**: trạng thái nói code xong, tick gần hết, hoặc chỉ còn ô test in-app, Git, vận hành user (các ô này ⛔ không chặn Done).
- **B. Code MỘT PHẦN**: còn pha **code** thật chưa làm.
- **C. Chỉ THIẾT KẾ**: chưa code.
- **D. Plan CHẾT**: dòng trạng thái nói *"DỪNG HẲN"*, *"hết hiệu lực"*, *"đừng nhặt lên làm tiếp"* mà ⛔ không đủ artifact.
  Đề xuất `Plan_Cancel`, ⛔ không đề xuất `Plan_Done` *(Done là làm xong, nhóm này sẽ ⛔ không bao giờ làm)*. Nghi ngờ thì HỎI user.

## Bước 2 · VERIFY QUA CODE (bắt buộc, mọi Plan nhóm A)
1. Lấy tên file, route, hàm, migration đặc trưng từ mục *Critical files* (⛔ không có mục đó thì lấy từ thân Plan vài cái **đặc trưng nhất**).
2. 🔴 **Liệt kê app trước, rồi quét TOÀN REPO**: quét một app là **sót**.
   File: `find . -name 'X.tsx' -not -path '*/node_modules/*'` · symbol: `rg -l 'tênHàm' --glob '!node_modules'` · DB: `rg -l 'tên_bảng' --glob '*.sql'`.
   🪤 Tên file migration ⛔ không chứng minh việc đã xong: kiểm bằng **nội dung**.
3. Kết luận: **CODE-VERIFIED-XONG** (artifact có, kể cả còn ô test, Git, vận hành) hay **NGHI SAI** (todolist nói xong mà code ⛔ không có: báo user, ⛔ không chuyển).
   Code có mà ô còn `[ ]` là **tick ngược**: ghi để tick lại.
4. 💀 **HAI PLAN ĐÙN NHAU**: Plan nhắc Plan khác kiểu *"chỗ X đã chừa"* thì đếm **đường điều hướng thật** trên gốc repo
   (`rg -n 'push\(.{0,3}/<route>/' --glob '!node_modules'`); ra 0 hoặc 1 chỗ thì nghi màn bị cô lập, ⛔ không chuyển Done.
5. 🔴 **Trước khi báo "còn việc"**: `rg` tên việc qua `05_PLANS/Plan_List/` (cả Plan đã xong), `06_REPORT/HandOff/`, `11_DEBT/`. Việc treo có thể
   **đã xong ở Plan khác**, hoặc là một **quyết định** bị ghi thành câu hỏi.

## Bước 3 · Báo cáo, HỎI (⛔ không tự chuyển khi chưa hỏi)
Bảng: **sẽ chuyển `Plan_Done`** (mỗi Plan một dòng bằng chứng code, kèm việc user còn lại) · **sẽ chuyển `Plan_Cancel`** (kèm lý do) ·
**sẽ chuyển `Plan_Debt`** (chỉ khi user bảo hoãn dài hạn, kèm điều kiện sống lại) · **giữ `Plan_Pass`** (lý do) · tick ngược, dòng git sai. Rồi `AskUserQuestion` duyệt; user chỉ duyệt một phần thì làm một phần.

## Bước 4 · Chuyển dòng (sau khi user duyệt; chỉ **Leader**)
1. Tick nốt `- [ ]` thuộc phần code đã xong; ô thuần test, Git, vận hành user thì tick nhưng NÊU phần user còn làm.
2. Điền `Hoàn thành Plan lúc` (`date "+%Y-%m-%d"`): `<ngày>: CODE HOÀN THÀNH: <tóm tắt>. Còn (user): <liệt kê>.`
3. `${CLAUDE_PLUGIN_ROOT}/scripts/activerole.py index move <tc> Plan_Pass Plan_Done` *(ô Đang cầm thành ngày xong)*;
   Plan chết: `index move <tc> Plan_Pass Plan_Cancel --value "<lý do>"`;
   user bảo hoãn dài hạn: `index move <tc> Plan_Pass Plan_Debt --value "⏸️ <điều kiện sống lại>"` rồi thêm một dòng
   `11_DEBT/Long_Debt_Index.md` trỏ tới tệp Plan *(tệp đứng yên; `Plan_Debt` chỉ đọc khi user hỏi, ⛔ không tự nhắc)*. Đọc mã ở **dòng 1**: phải là `DA_CHUYEN`; `NHIEU_DONG` thì gọi lại bằng đường ở dòng `DONG`; `KHONG_THAY_DONG`, `CHUYEN_SAI` hay mã lỗi khác thì DỪNG, báo user.
4. Dòng git trạng thái sai trong Plan (vd "chưa git push" mà user đã Git): sửa thành "đã Git", giữ dòng quy trình. Lệnh git ⛔ không ghi vào Plan.
- ⛔ không `mv`, ⛔ không sửa tay mục lục, ⛔ không nắn link: tệp đứng yên nên link ⛔ không đổi.
- Script ⛔ không có chiều `Plan_Done` → `Plan_Pass`: chuyển nhầm thì DỪNG, báo user.

## Bước 5 · Báo cáo cuối
Đã chuyển mấy dòng (`Plan_Done`, `Plan_Cancel`, `Plan_Debt`), giữ mấy Plan (lý do), tick ngược, nghi sai, việc user còn lại. Plan lớn đổi trạng thái thì nhắc memory.

## Ràng buộc
- Hỏi trước khi chuyển · verify qua code · ⛔ không commit, push, deploy · ⛔ không chuyển Plan nghi sai.
- 🔴 **`grep -oE` với `{0,N}` CHẾT trên văn bản tiếng Việt** (báo `exceeds complexity limits` hoặc treo): dùng `rg` hoặc `python3` heredoc.
  *(Cờ `rg` cắn nhau: `-oh` = help → viết `-o --no-filename`.)*
- 🔴 **Backtick trong lệnh `zsh` bị nuốt**: chuỗi có `` ` `` thì làm trong `python3` heredoc.
