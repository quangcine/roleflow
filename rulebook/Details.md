# Chi tiết luật global · lý do, ca thật, lịch sử

> Tách nguyên văn khỏi `~/.claude/CLAUDE.md` cho nhẹ phần nạp mỗi lượt *(đo 8 ngày: đọc lại khung khởi động chiếm 27.7% quota)*.
> Luật đang hiệu lực là bản ngắn trong `CLAUDE.md`; tệp này giữ lý do và ca thật. Hai nơi vênh nhau thì `CLAUDE.md` thắng.

## Giao tiếp
- 🔴 **NGHIÊM CẤM ký tự gạch dài `U+2014` (em dash)** trong MỌI thứ Claude viết ra: câu trả lời cho user, Idea, Plan, tệp nợ, comment trong code, tài liệu `.md`, thông điệp commit.
  ⟹ Thay bằng: dấu hai chấm `:` · dấu phẩy · ngoặc đơn · gạch nối ngắn `-` · dấu chấm phẩy `;` · hoặc **tách hẳn thành câu mới**.
  📌 *Dấu hiệu sắp sai:* đang định chèn một mệnh đề giải thích vào giữa câu. Chỗ đó dùng ngoặc đơn, hoặc cắt thành câu riêng.
- Chủ động **HỎI NHIỀU** điểm chưa chắc (scope, cơ chế, hạ tầng, retention, ai thực thi) → dùng AskUserQuestion thay vì tự suy đoán.
- 🔴 **MỖI CÂU HỎI PHẢI KÈM BỐI CẢNH + VÍ DỤ CỤ THỂ.** Trước khi đưa lựa chọn, nêu: *cái gì đang có · vì sao nó thành câu hỏi · **một ca thật** minh hoạ*. ⛔ Không hỏi trống kiểu *"chọn A hay B?"*. Mỗi option phải nói rõ **được gì / mất gì**. Lý do: user không đọc được thứ đang ở trong đầu Claude: thiếu bối cảnh thì câu trả lời là **đoán**, mà quyết định sai đi thẳng vào tài liệu/code.
- 🔴 **BỐI CẢNH DỰNG Ở VĂN XUÔI TRƯỚC, RỒI MỚI GỌI `AskUserQuestion`: LẦN NÀO CŨNG THẾ**. Nhét ca thật vào **bên trong ô `question` của tool là CHƯA ĐỦ**: user mở hộp bấm chọn chỉ thấy một câu dài đặc số liệu, không thấy cơ chế đang chạy và chỗ hở. Trình tự bắt buộc, ⛔ không rút gọn dù câu hỏi trông nhỏ:
  **① văn xuôi**: cơ chế đang chạy → chỗ hở → **một ca thật có tên người + số tiền** → vì sao Claude không tự quyết được · **② rồi mới gọi tool**, lúc này ô câu hỏi chỉ còn một dòng ngắn để bấm.
  📌 *Dấu hiệu sắp sai:* đang viết câu hỏi **dài quá 2 dòng bên trong tool** ⟹ phần đó thuộc về văn xuôi. *(Ca thật: câu hỏi bị bác 2 lượt liên tiếp: "Giải thích cụ thể bối cảnh và tình huống", rồi "Đưa vào quy tắc… lần nào cũng phải nhắc": dù câu hỏi ĐÃ có tên người và số tiền thật.)*

## Ba luật quản lý luật
- 🔴 **THỨ GÌ ĐÃ CÓ MEMORY THÌ DẪN LINK, ⛔ KHÔNG VIẾT LẠI**. Áp cho MỌI tài liệu: Idea · Plan · tệp nợ `11_DEBT/` · Bug · tài liệu `.md`.
  ⟹ Khuôn một dòng: `🔴 <nhãn 5 tới 10 chữ, đủ biết có cần mở hay không> → [[tên-memory]]`. 📏 **Quá 100 ký tự tức là đang viết lại chứ ⛔ không phải dẫn link.**
  **Vì sao:** chép sang chỗ khác là **nuôi hai bản của cùng một luật**, rồi có ngày lệch nhau mà ⛔ không cửa nào bắt. Ca thật: một tệp lời nhắc chép tay phình **34.187 ký tự / 237 luật**, nặng hơn cả `MEMORY.md` *(23.999)*, mà phần lớn khối cạm bẫy trong đó **đã có memory riêng**.
  ⚠️ Chưa có memory thì **viết memory TRƯỚC** rồi mới rút về một dòng, ⛔ đừng rút gọn một luật khi chưa có chỗ nào khác giữ nó. Việc **nhất thời** *(ranh giới file, số đo tạm)* thì viết thẳng, ⛔ đừng nhét vào memory.
- 🔴 **TRÙNG THÌ GIỮ MỘT · CŨ ĐÃ CÓ THAY THẾ THÌ BỎ**. Hai thứ làm cùng một việc thì giữ một. Thứ ⛔ không
  còn dùng, hoặc đã có cách mới thay, thì bỏ cái cũ, dùng cái mới. Áp cho mã, tệp, skill, agent, lệnh, memory, tài liệu.
  ⟹ **"Bỏ"**: **mã trong kho** dời vào chỗ xoá mềm của dự án *(sắp đóng dự án mới xoá hẳn; dự án chưa có chỗ xoá mềm thì hỏi user)* · **tệp ngoài mã** dời vào `12_TRASH/` · xoá hẳn chỉ khi dựng lại được *(bộ đệm build)*.
  Chỉ áp khi **user yêu cầu dọn** hoặc khi **thêm cái thay thế**; ngoài hai lúc đó vẫn theo mục 3 *(code chết có sẵn: nhắc user, để yên)*.
  Trước khi bỏ phải **ĐO**: còn ai dùng *(đếm trong nhật ký phiên)*, còn tài liệu nào trỏ tới *(dời thì nắn link)*; rồi trình user danh sách.
  📏 Ca thật: 15 lệnh gạch chéo tự viết **0 lần dùng**, trong khi `/roleflow:codeplan` và bảng agent đã thay việc của chúng.
- 🔴 **GHI LUẬT MỚI THÌ SOÁT LUẬT CŨ MÂU THUẪN, THẤY THÌ BÁO USER**. Trước khi ghi một luật vào `CLAUDE.md`
  *(global, dự án)*, `rulebook/`, memory, skill, agent: `grep` từ khoá của luật ở **cả các nơi đó**, đọc đúng dòng trúng
  để tách **luật đang hiệu lực** khỏi **lời kể lịch sử**. Luật cũ nói ngược, chồng việc, hay bị luật mới thay ⟹ **BÁO user**:
  luật cũ ở đâu, nói gì, vênh chỗ nào, đề xuất gỡ ra sao. ⛔ Đừng tự chọn bên thắng.

## 🔴 Hạn mức token · mọi phiên, mọi dự án
- **Ngữ cảnh chạm `500k` token thì ⛔ không nhận việc MỚI**: làm xong việc đang dở, rồi `/roleflow:pause` (còn dở), `/roleflow:done`, hoặc nhắc user `/compact` ở ranh giới
  việc. Đo bằng skill `roleflow:ctx` *(id là đoạn ngay trước `/scratchpad` trong đường scratchpad;
  in `OVER=1` là đã chạm)*.

## Bộ công cụ có sẵn (global)
- **Agents (10), khi nào gọi** *(cả 10 agent chạy Opus, ⛔ không dùng Sonnet; effort khoá trong frontmatter từng tệp agent, `roleflow:PlanReviewer` `high`, còn lại `medium`)*:

  | Lúc | Agent |
  |---|---|
  | **Thi công** Plan đã chắc *(`/roleflow:codeplan`)* | `roleflow:Executor` code → `roleflow:Reviewer` chỉ xem → `roleflow:QA Testing` verify và chụp ảnh DevTools |
  | **Lập Plan**, soi từng phần trước `/roleflow:reviewplan` | `roleflow:Researcher` khảo sát mã · `roleflow:DatabaseArchitect`, `roleflow:SupabaseExpert` schema, RLS · `roleflow:UIDesigner` màn mới |
  | **Rà Plan** | `roleflow:PlanReviewer` rà nội dung *(`/roleflow:reviewplan`, mỗi vòng một agent mới)* · `roleflow:PlanChecker` rà trạng thái *(`/roleflow:checkplan` Bước 0 tới 2)* |
  | Plan đụng quyền, RLS, dữ liệu cá nhân | thêm `roleflow:SecurityAuditor` |

- Việc thi công dùng `/roleflow:codeplan`, việc tư vấn gọi agent theo bảng trên.

## Nguyên tắc làm việc
#### 1. Nghĩ trước khi làm
- Nêu giả định. Nhiều cách hiểu thì trình bày hết. Mơ hồ thì dừng, gọi tên chỗ mơ hồ, hỏi.
- Có cách đơn giản hơn thì nói, nêu tradeoff, **phản đối** khi user chọn hướng phức tạp hơn cần thiết.

#### 2. Đơn giản trước
- Không thêm tính năng, trừu tượng, cấu hình hoá ngoài yêu cầu; không xử lý lỗi cho ca bất khả thi. 200 dòng mà 50 đủ thì viết lại.
- 🔴 **Đã có memory thì dẫn link, ⛔ không viết lại** (mọi Idea, Plan, tệp nợ, Bug, `.md`):
  khuôn `🔴 <nhãn 5 tới 10 chữ> → [[tên-memory]]`, quá 100 ký tự là đang viết lại. Chưa có memory thì viết memory trước.
- 🔴 **Trùng thì giữ một, cũ đã có thay thế thì bỏ**: chỉ khi user bảo dọn hoặc khi thêm cái thay thế. Đo trước (còn ai dùng,
  link nào trỏ tới) rồi trình user. "Bỏ" là dời vào chỗ xoá mềm
  *(tệp ngoài mã vào `12_TRASH/`)*, ⛔ không xoá hẳn trừ thứ dựng lại được.
- 🔴 **Ghi luật mới thì `grep` luật cũ** ở `CLAUDE.md`, `rulebook/`, memory, skill, agent;
  vênh, chồng việc thì **báo user** (ở đâu, nói gì, đề xuất gỡ), ⛔ đừng tự chọn bên thắng.

#### 3. Sửa đúng chỗ
- Chỉ chạm cái cần; ⛔ không cải thiện, refactor lân cận. Khớp style có sẵn *(trừ luật định danh tiếng Anh)*.
- Code chết, lệch chuẩn ngoài phạm vi: nhắc user, để yên. Trong phạm vi mình chạm thì sửa về chuẩn. Orphan do mình tạo thì xoá.

#### 4. Làm tới khi verify
- Định tiêu chí xong trước. Verify = **cửa đúng kho của dự án**
  + test thật trong app; phần động Claude ⛔ không tự đo được thì báo user test.
- Việc nhiều bước: nêu kế hoạch `1.[Bước] → verify:[kiểm tra] · 2.…`.

## Kho cấu hình
- Hai vai Leader, Planner và ba lệnh `/roleflow:start` `/roleflow:done` `/roleflow:pause`: luật đầy đủ ở `Roles.md` (đọc qua skill `roleflow:role-show`) *(skill `/roleflow:start` đọc đầu phiên)*;
  sổ vai, mục lục, sổ nợ đi qua `activerole.py`. 🔴 ⛔ Đừng đặt lại tên `rules/`: Claude Code tự nạp mọi `.md` trong thư mục `rules/` của thư mục cấu hình Claude Code vào mọi phiên và mọi subagent (đo được thêm khoảng 12k token mỗi nơi), nên giữ tên `rulebook/`.
- 💀 Sửa tệp này, `rulebook/`, skill, agent, memory xong: **nhắn tay mọi phiên đang chạy** (luật nạp lúc khởi động).

## Deploy
- **CỬA #0**: ngay trước **mỗi** lệnh đẩy (`db push`, `functions deploy`, `wrangler deploy`, `git push`, EAS) chạy lệnh kiểm
  tài khoản và **in ra cho user**: `supabase projects list` · `npx wrangler whoami` · `git remote -v` · `eas whoami`. Một máy đăng nhập nhiều tài khoản;
  căn cứ là email, account-id, project-ref, ⛔ không phải tên tài nguyên. 🛑 **Sai tài khoản thì DỪNG, báo user**, ⛔ không tự `logout`, `login`, đổi token.
- Tự làm sau CỬA #0: `supabase db push`, `functions deploy`. **GitHub và EAS chờ lệnh**: làm xong thì verify, `git status`, mô tả thay đổi, rồi đợi.
- Từ vựng: **"Push"** = chỉ `supabase db push` · **"Git"** = `db push` trước, rồi commit + push thẳng `main`. ⛔ Không commit secret.
  Phiên cloud (`CLAUDE_CODE_REMOTE=true`): "Git" đẩy nhánh đang làm và mở PR, bỏ `db push`; user merge rồi "Push" ở Mac.

## Database
- PK `id UUID PRIMARY KEY DEFAULT gen_random_uuid()`; mọi bảng có `created_at`/`updated_at` TIMESTAMPTZ; FK tường minh + index cho FK và cột query.
- **RLS bắt buộc** bảng user-facing. Migration tạo tệp MỚI, ⛔ không sửa migration cũ. `service_role` chỉ ở backend, edge. Realtime subscribe channel cụ thể.

## Code style
- 🔴 **Mọi định danh code mới bằng tiếng Anh**, kể cả tệp mới đặt cạnh tệp tên Việt (luật này thắng "khớp style"). Tiếng Việt chỉ ở chuỗi hiển thị,
  comment WHY, tên tệp tài liệu `.md`. Ngoại lệ duy nhất: khoá của kiểu, API đã có. Tên Việt cũ là nợ, ⛔ không tự đại phẫu → skill `roleflow:english-naming`
- `snake_case` bảng, cột · `camelCase` hàm, biến · `UPPER_CASE` hằng · `PascalCase` component. Tránh `any`; ⛔ không nối chuỗi SQL; validate input;
  ⛔ không dùng `dangerouslySetInnerHTML` với nội dung user.
