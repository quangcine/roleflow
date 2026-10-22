---
name: git
description: Quy trình deploy an toàn (khung DÙNG CHUNG mọi dự án), chạy khi user ra lệnh "Git" (db push TRƯỚC → rồi commit+git push cả repo code lẫn kho tài liệu ở gốc) hoặc "Push" (CHỈ supabase db push, không git). BẮT BUỘC kiểm tài khoản trước mỗi lệnh đẩy, db push trước git, quét secret, chạy cửa verify của dự án, commit thẳng main. Dùng khi user nói "Git", "Push", "db push", "commit", "đẩy lên", "push DB". ⛔ Không dùng khi user gõ một lệnh đẩy đã có skill riêng.
---

# Git/Deploy: DB push TRƯỚC, git SAU

> 📍 **Đây là KHUNG DÙNG CHUNG, cố ý ⛔ KHÔNG mang số liệu của dự án nào.**
>
> 🔴 **Dự án có bản riêng thì bản riêng THẮNG file này**, đọc thẳng bản đó:
> - Đường bản riêng của dự án: đọc mục tương ứng ở `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án.
>
> 🔴 **Dự án KHÔNG có bản riêng thì ⛔ ĐỪNG ĐOÁN SỐ LIỆU.** Đọc `CLAUDE.md` của dự án; vẫn không thấy project-ref, remote hay cửa verify thì **HỎI user**, rồi dựng một bản riêng cho dự án đó thay vì nhét vào file này.
>
> ⛔ **Tuyệt đối không mượn số liệu dự án này cho dự án kia**: project-ref, tên repo, đường thư mục, tên script guard đều khác nhau, và đẩy nhầm là lỗi không hoàn tác được.

**Từ vựng:**
- "**Push**" = **CHỈ `supabase db push`** (đẩy DB/migration lên cloud). ⛔ KHÔNG đụng git/GitHub.
- "**Git**" = `supabase db push` **TRƯỚC** → rồi **commit + git push** GitHub. "Git" ĐÃ BAO GỒM "Push DB". DB luôn lên TRƯỚC code, để app deploy ra không gọi RPC/schema chưa tồn tại.
- `supabase functions deploy` · `wrangler deploy` · EAS build = lệnh **RIÊNG**, ⛔ KHÔNG nằm trong Git/Push.

**Chỉ chạy khi user RA LỆNH RÕ** (Git / Push / db push / commit / đẩy lên). ⛔ KHÔNG tự suy, ⛔ KHÔNG tự deploy. Viết tiếng Việt.

| Lệnh | Bước 0 (DB push) | Bước 1-4 (git) |
|---|---|---|
| **"Push"** | ✅ chạy | ❌ DỪNG sau Bước 0 |
| **"Git"** | ✅ chạy TRƯỚC | ✅ rồi chạy tiếp |

## 📋 Bốn số liệu phải tra TRƯỚC khi gõ lệnh đầu tiên

Lấy từ bản riêng của dự án, hoặc từ `CLAUDE.md` của nó. Thiếu bất kỳ dòng nào thì **HỎI**, ⛔ đừng suy:

| Cần biết | Dùng ở bước |
|---|---|
| **Tài khoản** của dự án (email / account-id) | Cửa #0 |
| **Supabase project-ref** | Cửa #0 + Bước 0 |
| **Remote git** đúng owner/repo | Cửa #0 + Bước 4 |
| **Cửa verify** của dự án và nó có pre-commit hook không | Bước 3 |

---

## 🔴 CỬA #0 · KIỂM TÀI KHOẢN NGAY TRƯỚC MỖI LỆNH ĐẨY

> Một máy có thể đăng nhập **nhiều tài khoản song song**. Deploy nhầm account là lỗi **KHÔNG hoàn tác được**: một phiên đã dựng nguyên hạ tầng lên nhầm account, Cloudflare ⛔ không chuyển tài nguyên giữa 2 account nên phải xoá tạo lại từ đầu.

- **Kiểm rồi mới đẩy, không kiểm thì không đẩy.** Kết quả kiểm phải **in ra cho user thấy**, ⛔ không tự nhủ trong đầu.
- ⚠️ **Kiểm MỖI lệnh, ⛔ đừng cache kết quả cũ.** Token-per-command: lệnh TRƯỚC đúng account KHÔNG bảo đảm lệnh SAU đúng, shell không giữ trạng thái.
- Lệnh kiểm theo đích:
  - `supabase db push` → `supabase projects list` (thấy đúng project-ref của dự án đang làm, và **KHÔNG thấy** project của dự án kia)
  - `git push` → `git remote -v` (khớp đúng owner/repo)
  - `wrangler deploy` → `npx wrangler whoami` (khớp email + account-id)
  - EAS build → `eas whoami`
  ⚠️ Dự án có thể đòi **biến môi trường token riêng** cho mỗi lệnh supabase: tra bản riêng, ⛔ đừng dùng lệnh trần theo quán tính.
- 🛑 **RA SAI ACCOUNT thì DỪNG NGAY, BÁO USER, ⛔ KHÔNG TỰ SỬA.** In rõ *đang thấy account nào* vs *cần account nào* rồi chờ user. ⛔ Tuyệt đối KHÔNG tự `logout`/`login`/đổi token/đoán thêm biến môi trường rồi chạy lại.
- ⚠️ Thấy tên dự án LẠ trong account KHÔNG có nghĩa đứng nhầm chỗ. **Căn cứ duy nhất là email/account-id/project-ref**, ⛔ không phải tên tài nguyên.

---

## Bước 0 · 🗄️ DB PUSH (làm TRƯỚC, cho cả "Git" lẫn "Push")
- Xác nhận đang link đúng DB SỐNG: `supabase projects list` / `supabase migration list`. ⚠️ Dự án có nhiều DB (bản chết cũ) thì tra bản riêng để biết ref nào là sống.
- `supabase migration list` → liệt kê migration **Local chưa có ở Remote** (pending). Trình cho user xem cái gì SẼ áp.
- **Soát an toàn migration**: additive (`CREATE` / `ADD` / `CREATE OR REPLACE`) là an toàn. Có `DROP` / `DELETE` / `TRUNCATE` / đổi kiểu cột / sửa dữ liệu → **DỪNG, báo user xác nhận** trước khi áp, vì đụng dữ liệu thật.
- 💀 **Khối tự kiểm `do $$` trong migration GHI THẬT và ⛔ KHÔNG tự hoàn tác khi `db push`.** Thử qua Management API bọc `begin/rollback` thì xanh sạch vì rollback dọn hộ, đẩy lên cloud thì mọi câu `update`/`delete` mô phỏng **nằm lại**.
- Áp: `supabase db push`. Báo kết quả: migration nào đã áp.
- **Push lỗi thì DỪNG, ⛔ KHÔNG sang git** (tránh đẩy code lên GitHub mà DB chưa khớp). Báo user.
- Lệnh **"Push"** → xong Bước 0 thì **DỪNG**. Lệnh **"Git"** → tiếp Bước 1.
- Không có migration pending → báo "DB đã khớp, không có gì để push" rồi tiếp Bước 1 nếu là "Git".

## Bước 1 · Khảo sát + dọn rác (git)
- `git status --short` → xác định cái gì CHỦ ĐÍCH commit. ⛔ KHÔNG `git add -A` mù quáng.
- Loại file rác: `supabase/.temp/`, `*.tsbuildinfo`, `.DS_Store`, thư mục build. Rác đang bị track → `git rm -r --cached <path>` rồi bổ sung `.gitignore`.
- ⚠️ Thư mục **dữ liệu nặng** (ảnh, video test) ⛔ đừng commit.

## Bước 2 · 🔒 QUÉT SECRET (BẮT BUỘC, chặn cứng trước khi commit/push)
Grep các file SẼ commit (mới + sửa) tìm **GIÁ TRỊ** secret:
- `eyJ[A-Za-z0-9_-]{30,}` (JWT / anon / service_role) · `sbp_[A-Za-z0-9]{20,}` (Supabase token) · `re_[A-Za-z0-9]{12,}` (Resend) · `sk-[A-Za-z0-9]{20,}` (OpenAI) · `password\s*=\s*['"]…` · `secret\s*=\s*['"]…`.
- ⚠️ Dự án có **mẫu mật khẩu riêng** (seed, admin) thì tra bản riêng và quét thêm.
- Thấy **GIÁ TRỊ thật** → **DỪNG**, redact về `` `<đã redact, không lưu repo>` ``, báo user, rồi mới tiếp.
- **TÊN biến** (`RESEND_API_KEY`, chữ "service_role") là OK, bỏ qua.
- Secret đã lỡ vào history → báo user cân nhắc rotate; commit này ⛔ không sửa được history.
- File secret đã gitignore thì ⛔ đừng stage.

## Bước 3 · Stage + commit
- 🔴 **Chạy cửa verify của dự án** → báo PASS hoặc lỗi **TRƯỚC** commit. ⛔ Đừng commit khi verify đỏ, trừ khi user chấp nhận.
  ⚠️ Dự án **không có pre-commit hook** thì ⛔ không ai chạy hộ: bỏ bước này là đẩy code đỏ thẳng lên CI.
  ⚠️ Cửa `tsc` **mù hoàn toàn với SQL**. Dự án có migration thì phải có cửa riêng soi SQL (quyền, trigger, policy); tra bản riêng xem có những cửa nào và cửa nào **không** nằm trong pre-commit.
- `git add <đường dẫn chủ đích>` → `git status --short` hiện staged cho user xem.
- Commit message: tiêu đề `<type>: <mô tả VN ngắn>` (feat/fix/docs/refactor/chore); thân gạch đầu dòng việc chính (file/quyết định/migration); **KẾT bằng trailer `Co-Authored-By:`**.
  - 🔴 **Tên model trong trailer lấy từ chỉ dẫn hệ thống của phiên đang chạy** (mục "End git commit messages with"), ⛔ **KHÔNG chép cứng ở đây**. Chép cứng thì tụt hậu mỗi lần model đổi. Model đổi thì chỉ dẫn hệ thống tự đổi theo, skill khỏi sửa lại.
- Commit thẳng **`main`** (trừ khi user nói khác). `git log --oneline -1` xác nhận.

## Bước 4 · git push
- `git push origin main` → báo: commit hash + `main -> main` + `git status -sb`.
- 🔴 **Phiên cloud** *(`CLAUDE_CODE_REMOTE=true`)*: thay hai dòng commit/push `main` bằng `git push -u origin HEAD` rồi mở PR, ⛔ không đẩy `main` (luật ở skill `roleflow:rules-details` mục Deploy).
- 🔴 **Verify xanh ở máy ⛔ KHÔNG chứng minh CI xanh**: CI lấy mã từ git nên **mọi thứ bị `.gitignore` là thứ CI ⛔ không bao giờ thấy**. Dự án có CI thì push xong phải đọc kết quả CI (tra bản riêng để biết cách đọc).
- ⚠️ Kho **nối build tự động** (Cloudflare Workers Builds, Pages) thì `git push` **CHÍNH LÀ deploy**, không có bước duyệt. Tra bản riêng trước khi push.
- Bộ phân loại quyền CHẶN push → ⛔ **KHÔNG lách**. Báo user gõ "Git"/"Push" minh bạch.

## 📚 KHO TÀI LIỆU · mỗi gốc workspace là một kho Git riêng

**Gốc workspace là kho tài liệu** (`01_IDEA/` tới `11_DEBT/`, `CLAUDE.md`, `AGENTS.md`, `.claude/skills/`), tách khỏi repo code.
**Lệnh "Git" commit, push CẢ repo code lẫn kho tài liệu** của dự án đang làm (bên nào ⛔ không có thay đổi thì bỏ qua bên đó).

- 🔴 **Kho code, kho tài liệu, tài khoản, lệnh kiểm tài khoản của từng dự án ghi ở PHẦN RIÊNG của dự án** (bản riêng skill `roleflow:git`,
  hoặc mục kho Git trong `CLAUDE.md`, `AGENTS.md` ở gốc). Phần riêng chưa ghi thì **HỎI user**, ⛔ không đoán, ⛔ không mượn số dự án khác.
- **Bỏ Bước 0** (kho tài liệu ⛔ không có migration); giữ CỬA #0, Bước 1, quét secret Bước 2, commit thẳng `main`.
- 🔴 **CỬA #0 kiểm TỪNG kho**: `git -C <gốc> remote -v` cho kho tài liệu, `git -C <repo code> remote -v` cho repo code; in cả hai cho user.
  Đúng tên kho mà sai chủ (kho tài liệu trỏ tài khoản của dự án khác) là **DỪNG, báo user**. Kho chưa có remote thì báo user, ⛔ không tự tạo.
- **Hook pre-commit** *(nếu kho có)*: hook chặn thì sửa tệp, ⛔ không dùng cờ bỏ qua hook (`no-verify`); ngoại lệ duy nhất là **commit đầu** của kho, lời commit ghi lý do.
  `.git/hooks` ⛔ không được Git theo dõi: máy mới phải chép lại hook.
- Danh sách trắng `.gitignore` của kho tài liệu đã loại repo code, `08_SHARE/`, `09_REFERENCE/`, `10_EXPORT/`, `12_TRASH/`, `06_REPORT/CodePlan/`, `06_REPORT/Test/`, `Active-Role.md`; ⛔ không `add -f` mấy thứ đó.
- Quét secret Bước 2 áp cả kho tài liệu: Plan, tệp nợ hay chép nhầm giá trị khoá từ terminal.

## Ràng buộc (tuyệt đối)
- **Thứ tự**: DB push TRƯỚC, git SAU. db push lỗi thì ⛔ không git.
- ⛔ KHÔNG bao giờ commit/push **giá trị** secret. ⛔ KHÔNG stage file ngoài chủ đích.
- ⚠️ **Mỗi dự án có HAI loại kho**: kho tài liệu ở gốc workspace và repo code ở thư mục con (đường từng kho ở phần riêng của dự án). Chạy `git` đúng thư mục, ⛔ không đẩy code từ gốc.
- ⛔ KHÔNG `functions deploy` / `wrangler deploy` / EAS trừ khi user ra lệnh riêng.
- Báo cáo cuối: db push (migration nào) + git (commit hash, số file, đã push chưa) + kết luận CI nếu dự án có.
