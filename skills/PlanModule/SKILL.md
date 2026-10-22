---
name: PlanModule
description: "Lập kế hoạch một MODULE LỚN (nhiều Plan con): điều phối cấp trên của /plan. Dùng khi user muốn thiết kế/đại phẫu một mảng lớn cần chia thành Master hub + N sub-plan (mỗi Plan chạy 1 session để chống over-context), có khảo sát current-state thật rồi chốt thiết kế qua hỏi tuần tự. Kích hoạt khi user gõ /roleflow:PlanModule <tên module> hoặc yêu cầu 'lập kế hoạch module', 'đại phẫu', 'chia nhỏ thành nhiều plan'."
---

# PlanModule: quy trình lập kế hoạch module lớn (chống over-context)

Viết mọi văn bản bằng **tiếng Việt đủ dấu**. Đây là quy trình ĐIỀU PHỐI (trên `/plan`): module lớn → **1 Master hub + N sub-plan** + khảo sát current-state + Q&A chốt thiết kế. **Chỉ đọc + lập kế hoạch**, KHÔNG tự code (trừ khi user chuyển sang thực thi ở session riêng).

> Skill này chỉ THAM CHIẾU các quy ước đã có, ⛔ KHÔNG lặp lại: **đặt câu hỏi** và **kỷ luật deploy** theo `~/.claude/CLAUDE.md` (chép từ mẫu `templates/CLAUDE.md` của plugin) · tiêu chí *"Plan XONG = code xong"* và luật mục lục theo skill `roleflow:checkplan` · **kỷ luật token/MCP**: query targeted, ⛔ không full-dump.

## Nguyên tắc xuyên suốt
- **KHÔNG BỊA** tên hàm/view/cột/route: mọi tiền-đề trong Plan phải đến từ khảo sát current-state THẬT (bước ②).
- **Hỏi nhiều**: mọi điểm mơ hồ/nhiều hướng → AskUserQuestion (tiếng Việt CÓ DẤU, kèm giải thích + ví dụ + mục đích + đề xuất; option đầu = Recommended). **TRÁNH ký tự `&` và `%` trong JSON** (viết "và" / "phần trăm"): đó là nguyên nhân lỗi parse, KHÔNG phải do dấu.
- **DỪNG ở các mốc chờ duyệt** (sau Master, sau khi viết xong Plan): không tự đi tiếp việc lớn.

## ① Khởi tạo & phạm vi
1. Nhận **tên module** + mục tiêu. Mơ hồ → HỎI phạm vi/scope trước khi làm.
2. Lấy timecode: `date +%Y%m%d%H%M`.
3. Xác định **thư mục nhóm của module** (gom mọi Plan con + Master + design-doc vào một chỗ):

Thư mục nhóm, thư mục Idea, cửa verify tĩnh, nơi xuất HTML: đọc mục tương ứng ở `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án.

- Mục lục ở gốc workspace: `05_PLANS/Plan_Draft.md`, `01_IDEA/Idea_Draft.md`; thêm dòng **chỉ qua** `${CLAUDE_PLUGIN_ROOT}/scripts/activerole.py index add Plan_Draft|Idea_Draft --value "<dòng>"`,
  Master trước rồi sub theo thứ tự. Đọc mã ở **dòng 1**: phải là `DA_THEM`; `SAI_KHUON_DONG` thì sửa dòng rồi gọi lại, ⛔ không ghi tay;
  `DA_CO_DONG` *(tệp đã có dòng)* hay mã lỗi khác thì DỪNG, báo user. Tệp đứng yên, trạng thái là dòng mục lục.
- 🔴 Dự án **chưa rõ đường dẫn, cửa verify, tài khoản** thì ⛔ ĐỪNG ĐOÁN: bám `CLAUDE.md` của dự án, không thấy thì **HỎI user**.

## ② Khảo sát current-state (SONG SONG · bắt buộc, chống bịa)
1. **ƯỚC LƯỢNG token trước rồi HỎI xác nhận** (user đã chốt: tự chạy nhưng phải hỏi). Nêu: sẽ fan-out mấy điều tra viên, quét gì (baseline/migrations/services/UI), ước ~bao nhiêu token → chờ user OK.
2. Sau khi OK → fan-out (nhiều Agent song song): mỗi điều tra viên trích **tên hàm/view/cột/dòng THẬT** cho 1 phân hệ, trả FACT-SHEET (không đề xuất, chỉ current-state). Đối chiếu cả forward-migrations mới hơn baseline.
3. Tổng hợp thành **F-list** = phát hiện bất ngờ (khác thiết kế giấy), đánh số F1..Fn.
4. Tôn trọng cost discipline (không list_tables/full-dump).

## ②b 💡 Idea (phần VÌ SAO) · viết TRƯỚC hoặc song song Master hub

Quy ước: ý tưởng lớn phải tách đôi. **Plan = LÀM GÌ · Idea = VÌ SAO.**
- File: **thư mục Idea của dự án** theo **quy ước tên của dự án đó** (xem `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án), thêm dòng `Idea_Draft` (`index add`, ①.3). ⛔ Đừng bê quy ước tên của dự án này sang dự án kia.
- Idea ghi: câu chuyện xuất phát · TOÀN BỘ hỏi đáp và từng cái đã chốt · các phương án đã cân nhắc rồi **LOẠI kèm lý do** · giả định bị số đo lật ngược · số đo thu được.
- Plan và Idea **trỏ link sang nhau ở đầu file**.
- 🔴 **Idea giữ VĨNH VIỄN, ⛔ không xoá.** Lý do: sáu tháng sau đọc Plan chỉ thấy "làm gì", không thấy "vì sao không chọn cách kia". Viết xong Plan đầu tiên của Idea thì `index move <tc> Idea_Pass Idea_Done`,
  chỉ khi Idea đang ở `Idea_Pass` *(đã qua `/roleflow:reviewplan` chế độ Idea)*. Đọc mã dòng 1: phải là `DA_CHUYEN`; `KHONG_THAY_DONG` *(Idea còn ở `Idea_Draft`)* thì ⛔ không chuyển, báo user; mã lỗi khác thì DỪNG, báo user.
- ⚠️ Task nhỏ thì không cần Idea. Module lớn (đúng phạm vi skill này) thì **cần**.

## ③ Master hub (mục lục + checklist) · rồi CHỜ DUYỆT
1. Tạo `Plan_<tc>_<Module>_Master.md`: **bối cảnh** (vì sao đại phẫu) + **F-list** + **đề xuất chia N sub-plan** (mỗi cái 1 phạm vi + phụ thuộc) + **sơ đồ phụ thuộc/thứ tự** + **câu-hỏi-cross-cutting** (đề xuất kèm).
2. **DỪNG: báo user duyệt cách chia + trả lời câu hỏi** trước khi viết chi tiết sub-plan.

## ④ Viết sub-plan (mỗi file = 1 session)
Mỗi `Plan_<tc>_<tên>.md` PHẢI có, theo khuôn:
- **§0 Tiền-đề current-state** (facts THẬT từ ②, kèm dòng số) + chốt thiết kế liên quan.
- **§1 Todolist Bx**: bước cụ thể (hàm/migration/UI), có `- [ ]`.
- **§2 Rủi ro + thứ tự** (nuốt lỗi âm thầm, ripple, phụ thuộc).
- **§3 ❓ Câu-hỏi-chốt** (đề xuất kèm) → sau khi user trả lời đổi thành "✅ QUYẾT ĐỊNH ĐÃ CHỐT".
- **§ Định-nghĩa-"xong" = verify tĩnh**: **cửa verify của dự án** EXIT 0 (xem `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án) + artifact tồn tại thật.
- **§ Liên hệ Plan khác** + **Nhật ký** + **"Hoàn thành Plan lúc"** (điền khi CODE xong).
Đầu Master: checklist tick `[x] 📝 ĐÃ VIẾT` khi viết xong từng Plan.

## ⑤ Chốt thiết kế (Q&A tuần tự)
1. 🔴 **Hỏi TỪNG CÂU MỘT**: một `AskUserQuestion` = **đúng một câu**, ⛔ không gộp 2-4 câu vào một lần gọi dù chúng cùng chủ đề. Còn N việc cần chốt thì nói trước *"còn N thứ, tôi hỏi lần lượt"* rồi đi từ **quan trọng / ảnh hưởng chéo** xuống, chờ trả lời xong mới hỏi câu sau. *(Câu sau thường phụ thuộc câu trước, hỏi song song là mất chính cái phụ thuộc đó.)*
   Dựng bối cảnh ở **văn xuôi TRƯỚC** rồi mới gọi tool: cơ chế đang chạy → chỗ hở → một **ca thật** → vì sao ⛔ không tự quyết được.
2. **Giải thích lại** khi user chưa hiểu (đừng ép chọn). **Bắt các quyết định MỚI nổi lên** giữa chừng (user hay mở rộng yêu cầu).
3. **Sau MỖI câu được trả lời**: cập nhật ngay vào Plan + Master, ⛔ đừng dồn tới cuối rồi ghi một thể.

## ⑥ Đồng bộ nguồn sự thật
- Cập nhật **design-doc** + **memory** liên quan + Master §quyết-định + đổi §3 mỗi Plan thành "✅ QUYẾT ĐỊNH ĐÃ CHỐT". Ghi các phát hiện chỉnh lại F-list.

## ⑦ HTML trực quan · HỎI ở 2 MỐC, chỉ xuất khi duyệt
- **Mốc 1: viết xong Plan VÀ đã rà PASS ở bước ⑨** → HỎI "có xuất HTML trực quan không?". ⛔ Đừng xuất HTML cho Plan **chưa rà**: bản in ra sẽ mang nguyên lỗi, mà nhìn đẹp nên càng dễ tin.
- **Mốc 2: thực hiện xong Plan (code xong)** → HỎI lại.
- User OK → xuất **HTML self-contained** (dark, tab theo ĐỐI TƯỢNG: lý do cho người duyệt · cấu trúc dữ liệu cho Dev · demo · ô nhập thử có máy tính) vào **thư mục xuất của dự án** (xem `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án): nội bộ, GIỮ số thật, số minh họa thì ghi rõ. KHÔNG auto.

## ⑧ Verify + kỷ luật deploy
- Khi có code: chạy **cửa verify của dự án** (xem `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án), phải EXIT 0.
- **Thi công theo luật của dự án**: lúc nào tự `db push`, lúc nào chờ lệnh: đọc mục tương ứng ở `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án. Mọi dự án: **GitHub chờ user gõ "Git"**; "Push" = chỉ `supabase db push`. Xem skill `roleflow:git` và bản riêng của dự án nếu có.
- Code xong (verify tĩnh PASS + artifact tồn tại) thì Leader **chuyển dòng `Plan_Pass` → `Plan_Done` ngay**, ⛔ không chờ Git, ⛔ không dời tệp.

## ⑨ 🔎 RÀ BẰNG `/roleflow:reviewplan` RỒI MỚI BÁO CÁO (bắt buộc, ⛔ không rút gọn)

> 🔴 **Viết xong Plan ⛔ KHÔNG phải là xong.** Chưa rà thì ⛔ chưa được báo "đã lập xong kế hoạch". Lý do: bộ Plan của một module lớn có **nhiều file trỏ vào nhau**, mà lỗi nặng nhất luôn nằm ở chỗ **hai file nói ngược nhau**, ⛔ không file nào tự thấy.

1. **Chạy `/roleflow:reviewplan` cho TỪNG Plan của module**, gồm cả Master.
   - **Master** rà *điều phối*: thứ tự, phụ thuộc, ai làm gì, F-list còn đúng không.
   - **Sub-plan** rà *đặc tả*: tiền đề §0, todolist, rủi ro, định nghĩa "xong".
   - ⛔ **Đừng lẫn hai loại**: rà Master bằng con mắt đặc tả là bỏ lọt lỗi điều phối, và ngược lại.
2. 💀 **Hub ghi "🩹 đã vá" ⛔ KHÔNG chứng minh FILE CON đã vá.** Sửa một tiền đề ở Master xong thì **`grep` chính chuỗi vừa sửa trên TOÀN thư mục module**, vì bảng câu hỏi chốt và bảng rủi ro ở file con thường vẫn mang nguyên tiền đề cũ.
3. 🔗 **Rà CHÉO giữa các sub-plan**: hai Plan cùng trỏ sang nhau kiểu *"chỗ X đã chừa"* thì rất dễ **⛔ không ai nối**. Đếm đường thật, ⛔ đừng tin lời hứa của cả hai bên.
4. **Chỉ báo cáo khi `/roleflow:reviewplan` đạt PASS** (đủ 6 tiêu chí). Hết 3 vòng mà vẫn ra lỗi thì **dừng, báo rõ là CHƯA hội tụ** kèm danh sách còn mắc, hỏi user đi tiếp hay xem lại cách viết *(trần 3 vòng)*, ⛔ không im lặng kết thúc.
5. **Báo cáo cuối gồm**: đã viết mấy Plan và tên từng cái · mỗi Plan rà mấy vòng, bắt bao nhiêu lỗi · **ba lỗi nặng nhất** · việc còn **chờ user chốt** · mốc hỏi xuất HTML (bước ⑦).

## Ràng buộc
- Chỉ ĐỌC + lập kế hoạch; KHÔNG tự commit/push GitHub; KHÔNG tự code khi đang ở pha lập kế hoạch.
- Task nhiều bước → nêu kế hoạch ngắn trước. Mỗi mốc lớn xong → DỪNG, tóm tắt, chờ duyệt.
