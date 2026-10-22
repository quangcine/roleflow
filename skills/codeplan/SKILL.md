---
name: codeplan
description: Thi công MỘT Plan đã chắc bằng 3 subagent: Coder (Executor) code → Reviewer soát (chỉ xem) → Tester (QA Testing) chạy cửa verify và DevTools chụp ảnh thật; mắc đâu chạy lại đó, xong thì xuất báo cáo HTML kèm ảnh bằng chứng. Chỉ Leader chạy, khi Plan đã /roleflow:reviewplan PASS và user đã bảo giao. Dùng khi user gõ "/roleflow:codeplan", "codeplan <Plan>", "cho subagent code Plan".
---

# codeplan · thi công Plan bằng 3 subagent, có ảnh bằng chứng

Viết tiếng Việt, ⛔ cấm em dash. Luật nền: `${CLAUDE_PLUGIN_ROOT}/rulebook/Roles.md`, luật ③ ④ ⑤ ⑧ ⑨. Lệnh sổ: `${CLAUDE_PLUGIN_ROOT}/scripts/activerole.py`.
⛔ **Không có Planner**: Plan đã được hỏi kỹ với user và `/roleflow:reviewplan` tới PASS, Coder làm đúng Plan, ⛔ không tự thiết kế lại.
Mọi vai *(Coder lượt đầu và vòng sửa, Reviewer, Tester)* gọi `model: "opus"`; effort khoá trong tệp agent.

## Theo dự án

Plan và mục lục, cửa verify, thư mục pipeline và báo cáo, cách đo bằng DevTools: đọc mục tương ứng ở `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án.

Không thấy thư mục báo cáo hay cửa verify thì **HỎI user**, ⛔ đừng đoán.

## Thư mục pipeline *(mọi agent đọc và ghi vào đây)*

`P = 06_REPORT/CodePlan/<ts>_<TenPlan>/` chứa: `coder_v<n>.md` · `migration/` *(nháp, ngoài kho)* · `review_v<n>.md` · `test_v<n>.md` · `anh/` · `manifest.json` · báo cáo HTML.
🔑 Agent sau **đọc tệp của agent trước** thay vì Leader chép lại vào tin gọi: context Leader nhẹ, và Leader `/roleflow:pause` giữa chừng
thì phiên sau đọc `P` là biết đang ở vòng nào. Leader chỉ đọc **dòng kết luận** của mỗi tệp, ⛔ đừng đọc trọn.

## Bước 0 · Cổng vào *(thiếu một điều là DỪNG, báo user)*
- Chỉ **Leader** chạy *(dòng `L` của `activerole.py show`)*. Plan ở `Plan_Pass`, `**THỰC HIỆN: Leader**`.
- Plan có dấu `/roleflow:reviewplan` PASS, user **đã bảo giao** *(luật ⑧)*, ⛔ không còn câu hỏi treo hay mục *"chốt khi code"*.
  🔴 `grep -n "chấm\|chờ chủ dự án" <Plan>`: M0 hay mục "điểm tự suy" còn chờ user chấm thì HỎI chấm TRƯỚC khi gọi Coder.
- Dòng `**Nhật ký Code:**` của Plan ⛔ không có ai đang giữ *(`bắt đầu Code` chưa có `Dừng Code`; tên cũ là lịch sử)*.
- Ghi vào Plan: `<ts>: Leader (subagent) bắt đầu Code *(codeplan)*`. Cầm dòng: `activerole.py index hold <tc> L --in Plan_Pass` *(ô thành 🔨 L)*; `activerole.py note L <ts vào> "codeplan <TenPlan>"`.
  Đọc mã ở **dòng 1** của `index hold`: phải là `DA_CAM`. `NHIEU_DONG` thì gọi lại bằng đường ở dòng `DONG` đúng Plan; `DA_CO_NGUOI_CAM`, `KHONG_THAY_DONG` hay mã lỗi khác thì DỪNG, báo user.
- Tạo `P` và `P/anh/`. Ghi `ts` bắt đầu bằng `date +%Y%m%d%H%M`.

## Bước 1 · Coder *(`roleflow:Executor`)*
Gọi `Agent` `subagent_type: "roleflow:Executor"`, `model: "opus"`, chạy tiền cảnh. Tin gọi PHẢI có:
- Đường dẫn Plan, phạm vi *(trọn Plan hay mốc nào)*, đường dẫn `P`.
- 🔴 **Giao theo mốc, đọc theo dòng** *(đo 8 ngày: Executor trung bình 241k ngữ cảnh mỗi lượt vì ôm trọn Plan)*: Plan có từ hai mốc trở lên
  thì mỗi mốc một Executor, chạy nối tiếp. Tin gọi ghi **khoảng dòng** của mốc đó và của mục chung *(ranh giới tệp, nghiệm thu)*;
  ⛔ không giao đọc trọn Plan, ⛔ không giao đọc Idea *(Idea là phần vì sao, đã chốt vào Plan)*. Reviewer và Tester nhận cùng khoảng dòng.
- Ba điều luật ⑨: gặp chỗ mơ hồ thì **DỪNG, trả câu hỏi về Leader** · ⛔ không commit, push, deploy, `db push`, ⛔ không ghi memory ·
  liệt kê **đường dẫn đầy đủ TỪNG tệp** đã chạm.
- Soi Plan trước khi code *(luật ③)*; tick `[x]` kèm mốc giờ ô đã làm; chạy cửa verify tĩnh của **đúng kho** trước khi báo xong.
  🔴 Chạy từ hai `/roleflow:codeplan` song song trở lên thì tin gọi dặn Executor ⛔ không tick, Leader tick sau *(ca thật: ba Executor ghi đè nhau)*.
- 🔴 Migration: ghi **nháp vào `P/migration/`**, ⛔ không đặt thẳng vào `supabase/migrations/` *(`db push` đẩy MỌI migration đang chờ trong kho)*.
- Ghi kết quả vào `P/coder_v<n>.md` *(tệp đã chạm, phép đo đã chạy, việc còn treo)*, dòng đầu là kết luận một câu.
🔴 **Vòng sửa** *(Bước 2 `CẦN SỬA`, Bước 4 `KHÔNG ĐẠT`)*: gọi `Agent` `subagent_type: "roleflow:Executor"` **MỚI**, `model: "opus"`, ⛔ không nhắn tiếp Coder của vòng trước.
Tin gọi chỉ gồm: đường dẫn `P/review_v<n>.md` hoặc `P/test_v<n>.md` · danh sách tệp liên quan · mục Plan liên quan · đường dẫn Plan để tra khi cần.
*(Vì sao: 97% tới 98% chi phí subagent là đọc lại ngữ cảnh.)*
Mỗi lượt gọi *(mọi agent)* ghi `agentId` vào `P/manifest.json` trường `agents`.
🔴 **Chụp mốc sau mỗi `coder_v<n>`** *(để vòng sau chỉ soát phần vừa sửa)*: mỗi kho Coder chạm, `git -C <kho> stash create` *(in rỗng thì `git -C <kho> rev-parse HEAD`)*,
ghi vào `P/manifest.json` trường `snapshots` `{round, repo, hash}`. Mốc này ⛔ không gồm tệp `??`:
chép các tệp `??` trong `coder_v<n>.md` vào `P/snap_v<n>/` giữ nguyên đường dẫn.
Coder trả câu hỏi → Leader hỏi user *(bối cảnh văn xuôi trước, rồi mới `AskUserQuestion`)* → nhắn tiếp **đúng Coder vừa hỏi** bằng `SendMessage` tới `agentId` của lượt đó *(câu hỏi nằm trong cùng một lượt, ⛔ không phải vòng sửa)*.

## Bước 2 · Reviewer *(`roleflow:Reviewer`, CHỈ XEM)*
1. Leader chụp trạng thái kho **trước**: `git -C <kho> status --porcelain | shasum`.
2. Gọi `Agent` `subagent_type: "roleflow:Reviewer"`, `model: "opus"`. Tin gọi: đường dẫn Plan, `P/coder_v<n>.md`, lệnh xem diff đúng kho,
   **mọi** `P/review_v*.md` trước đó *(để kiểm lỗi cũ đã sửa chưa)*, `P/migration/` nếu có; từ vòng 2 thêm mốc `snapshots` của vòng trước. Dặn: **⛔ không sửa tệp nào trong kho**, chỉ ghi `P/review_v<n>.md`.
   Dòng đầu là `PASS` hoặc `CẦN SỬA`, sau đó mỗi lỗi một dòng: `loại · tệp:dòng · vì sao sai · cách sửa đề xuất · chỗ cùng loại`.
   🔴 Từ vòng 2 dặn thêm *(theo bài học review của nhóm Claude Code: phần lớn lỗi vòng sau đã nằm đó từ vòng đầu)*:
   chỉ soát `git diff <mốc vòng trước>` cộng `diff -ru P/snap_v<n-1>/` với tệp `??`, ⛔ không quét lại cả diff Plan ·
   chỉ báo lỗi cũ chưa sửa thật và lỗi nằm trong phần vừa sửa · lỗi ở chỗ mã vòng trước đã có mà chưa báo thì ghi Nhẹ, ⛔ không làm `CẦN SỬA`.
3. Chụp lại **sau**. Hai mã băm lệch = Reviewer đã đụng code ⟹ **loại vòng review đó**, báo user, ⛔ đừng dùng kết quả.
4. Leader soát nhanh *(luật ④)*: đọc mã ở MỘT hai lỗi Reviewer nêu, ⛔ đừng chuyển tiếp mù.
5. `CẦN SỬA` → gọi Coder MỚI *(vòng sửa, Bước 1)* đọc `P/review_v<n>.md` rồi sửa, ghi `P/coder_v<n+1>.md` → quay lại Bước 2.
6. 🔴 `PASS` kèm lỗi Nhẹ → ⛔ không gọi Coder sửa. Leader chép lỗi Nhẹ vào `P/manifest.json` `notes`, báo user ở Bước 5; user bảo sửa mới sửa
   *(đo 79 lượt: 126 bản review PASS còn kèm Nhẹ, có lượt chạy tới 16 vòng Coder vì sửa Nhẹ nối đuôi)*.

## Bước 3 · Migration *(chỉ khi Plan có migration)*
Reviewer đã PASS thì Leader dời nháp từ `P/migration/` vào thư mục migration của kho **ngay trước** khi `db push`, và push **trước** bước Tester vì màn thật cần cấu trúc mới:
CỬA #0 *(`supabase projects list`, in ra cho user thấy)* rồi 🔴 liệt kê mọi mig chờ.
⛔ Không push khi Reviewer chưa PASS.

## Bước 4 · Tester *(`roleflow:QA Testing`, có DevTools)*
Gọi `Agent` `subagent_type: "roleflow:QA Testing"`, `model: "opus"`. Tin gọi: đường dẫn Plan *(mục tiêu chí nghiệm thu)*, `P`, cách đo ghi ở `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án. Dặn:
1. Chạy cửa verify tĩnh đúng kho, ghi lệnh và kết quả.
2. Bật dev server **chỉ app cần đo**, đăng nhập tài khoản đo, mở màn thật bằng DevTools *(`curl` ⛔ không thay được)*.
3. Mỗi tiêu chí nghiệm thu: thao tác, `take_screenshot` lưu `P/anh/<nn>_<ten>.png`, ghi ĐẠT hoặc KHÔNG ĐẠT kèm điều thấy.
4. **Ca biên, tự nghĩ thêm ngoài Plan**: dữ liệu rỗng · tài khoản quyền thấp · bấm dồn dập · một ca chắc chắn SAI phải bị chặn *(đối chứng âm)*.
5. 🔴 **Thao tác GHI dữ liệu thật thì DỪNG**, trả về Leader hỏi user trước *(lưu form, đánh dấu đã đọc, mở link tự ghi lần xem…)*.
6. Đo xong tắt dev server, đăng xuất tài khoản đo.
7. Ghi `P/test_v<n>.md` *(dòng đầu `ĐẠT` hoặc `KHÔNG ĐẠT`)* và nối vào `P/manifest.json` mảng `criteria` *(khuôn ở `build_report.py`)*.
Leader kiểm chéo *(luật ④)*: tự `Read` ÍT NHẤT MỘT ảnh. Ảnh trắng, màn đăng nhập hay màn lỗi mà ghi ĐẠT = vòng đó ⛔ không tính.
`KHÔNG ĐẠT` → gọi Coder MỚI *(vòng sửa, Bước 1)* đọc `P/test_v<n>.md` → Reviewer *(Bước 2)* → Tester lại.

## Giới hạn vòng
Tối đa **3 vòng sửa cho cả lượt**, đếm chung mọi lần gọi Coder sửa *(do Reviewer `CẦN SỬA` hay Tester `KHÔNG ĐẠT`)*, ⛔ không đếm lại từ 0 khi sang chặng khác.
Vòng sửa thứ 3 vẫn lỗi → **DỪNG**, báo user lỗi còn lại, `P`, và câu hỏi *Plan hay cách làm có sai hướng không*, ⛔ đừng vá tiếp vòng 4.
User chốt thêm việc giữa chừng thì bộ đếm mở lại cho phần thêm, ghi một dòng vào `notes`.

## Bước 5 · Hoàn thiện
1. Điền `P/manifest.json`: `plan` · `plan_path` · `title` · `started` · `finished` · `rounds` · `files` *(đủ đường dẫn)* · `verify` · `review` · `notes` ·
   `agents` *(mỗi lượt gọi một phần tử `{role, round, model, agentId}`: lần đo token sau tìm đúng tệp nhật ký subagent)*.
2. `python3 ${CLAUDE_PLUGIN_ROOT}/skills/codeplan/build_report.py "<P>"` phải ra `THIEU=0`. Thiếu ảnh thì thoát mã 1, tức là chưa xong.
3. Plan: ghi dòng `**Báo cáo thi công:** <đường dẫn HTML>` · `<ts>: Leader (subagent) Dừng Code` · điền *"Hoàn thành Plan lúc"* ·
   chuyển dòng `activerole.py index move <tc> Plan_Pass Plan_Done`. Tệp Plan đứng yên, ⛔ không `mv`.
   Đọc mã ở **dòng 1**: phải là `DA_CHUYEN`. `NHIEU_DONG` thì gọi lại bằng đường ở dòng `DONG`; `KHONG_THAY_DONG`, `CHUYEN_SAI` hay mã lỗi khác thì DỪNG, báo user.
4. Báo user: Plan, số vòng từng chặng, đường dẫn báo cáo, danh sách tệp chờ "Git". ⛔ Không commit.
   ⛔ Không hỏi `/roleflow:exportplan` ở mốc *"thực hiện xong Plan"*: báo cáo này đã thay.

## Dừng và hỏi user khi
Coder hay Tester trả câu hỏi · quá 3 vòng · cần ghi dữ liệu thật · cửa verify đỏ vì tệp ⛔ không thuộc Plan · Reviewer đụng code ·
ngữ cảnh Leader chạm `500k` *(chờ subagent đang chạy xong rồi mới `/roleflow:pause`, luật ⑨)*.
Plan ⛔ không thi công tiếp *(quá 3 vòng, user dừng)* thì nhả ô: `activerole.py index release <tc> L` *(phải ra `DA_NHA`; mã lỗi thì báo user)*.
