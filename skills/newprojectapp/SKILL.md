---
name: newprojectapp
description: Khởi tạo một DỰ ÁN APP MỚI theo cấu trúc chuẩn (cây 12 thư mục đánh số 01-12 ở gốc workspace là kho Git tài liệu riêng, mục lục rỗng, CLAUDE.md + AGENTS.md) và KHAI BÁO dự án đó vào ~/.claude/flow-projects.json, để các lệnh vai không phải hỏi lại đường dẫn mỗi phiên. CHỈ dành cho dự án APP (có code, DB, deploy); loại dự án khác (nội dung, tài liệu) có cây riêng, ⛔ đừng dùng skill này. Dùng khi user nói "newprojectapp", "dự án app mới", "tạo project app", "dựng cây thư mục app".
---

# NewProjectApp: dựng dự án APP mới + khai báo vào bộ skill

Viết mọi văn bản bằng **tiếng Việt có dấu**.

> 🔴 **PHẠM VI: chỉ dự án APP** (có code, database, deploy). Cây 11 thư mục dưới đây là cây của **app**, ⛔ KHÔNG phải cây dùng chung cho mọi loại dự án.
> ⚠️ Loại dự án khác có cây **hoàn toàn khác**, ⛔ đừng bê cây này sang.
> 📌 Chưa chắc dự án thuộc loại nào thì **HỎI user trước**, ⛔ đừng suy từ tên.

Skill này làm **hai việc**, thiếu việc thứ hai là dự án mới sẽ bị mọi skill hỏi lại đường dẫn ở từng phiên:

1. Dựng **cây thư mục, kho tài liệu, file nền** ở gốc workspace.
2. **Khai dự án vào `~/.claude/flow-projects.json`** để ba lệnh vai nhận ra gốc dự án.

> 🔴 **Skill này CHỈ tạo file, thư mục và `git init` kho tài liệu trong máy.** ⛔ KHÔNG tạo tài nguyên cloud (Supabase project, repo GitHub, Cloudflare Worker, bucket), ⛔ KHÔNG `git init` repo code, ⛔ KHÔNG commit, ⛔ KHÔNG deploy.

## Bước 1 · HỎI thông tin, ⛔ ĐỪNG ĐOÁN

🔴 **Hỏi TỪNG CÂU MỘT** (một `AskUserQuestion` = đúng một câu), dựng bối cảnh ở **văn xuôi trước** rồi mới gọi tool. Nói trước *"cần N thứ, tôi hỏi lần lượt"*.

**Nhóm A, bắt buộc để dựng cây:**
1. **Tên dự án** và **slug** *(viết thường không dấu)*.
2. **Gốc workspace** (`~/<Ten>Dev/`, là kho tài liệu) và **tên repo code** bên trong nó.
3. **Một câu mô tả** dự án làm gì.

**Nhóm B, bắt buộc để ghi vào `AGENTS.md`** *(thiếu cái nào thì để `(chưa có)` và ghi vào mục nợ, ⛔ đừng bịa)*:
4. **Tài khoản hạ tầng**: Cloudflare, Supabase, GitHub dùng account nào.
5. **Supabase project-ref** (nếu có) và lệnh supabase có cần **biến môi trường token riêng** không.
6. **Remote git** (nếu có).
7. **Cửa verify** của dự án: lệnh nào, bao nhiêu mục.
8. **Thư mục code** nằm đâu (`src/`, `apps/`, hay khác), và **thư mục migration**.

## Bước 2 · Kiểm trước khi tạo

- `ls -a <gốc>`: đã có thư mục `01_` tới `12_` hoặc `.git` *(gốc đã dựng cây, đã là kho Git)* thì 🔴 **DỪNG, báo user**, ⛔ tuyệt đối không đè lên.
  Gốc chỉ có repo code, `CLAUDE.md`, `AGENTS.md` thì đi tiếp: Bước 4 bổ sung một mục vào hai tệp đó.
- Kiểm tên dự án đã có trong `~/.claude/flow-projects.json` chưa (Bước 5): trùng tên là dấu hiệu dự án này **đã được khai rồi**.

## Bước 3 · Dựng cây ở gốc workspace

```
<gốc>/                kho Git tài liệu riêng; repo code nằm trong nhưng ⛔ không vào kho
  01_IDEA/      Idea_List/ · Idea_Draft.md · Idea_Pass.md · Idea_Done.md   (VÌ SAO, ⛔ không xoá)
  02_RESEARCH/  AI/audits/ (báo cáo review, bảo mật, QA)
  03_DESIGN/ 04_UI/
  05_PLANS/     Plan_List/ · Plan_Draft.md · Plan_Pass.md · Plan_Done.md · Plan_Cancel.md
  06_REPORT/    HandOff/ (giữ khuôn, ⛔ không ghi; bàn giao là tệp nợ 11_DEBT) · CodePlan/ · Test/
  07_DOCS/
  08_SHARE/ 09_REFERENCE/ 10_EXPORT/ 12_TRASH/   chặn Git trọn (cùng 06_REPORT/CodePlan/, Test/)
  11_DEBT/      Short_Debt_List/ · Short_Debt_Index.md · Long_Debt_List/ · Long_Debt_Index.md
  <REPO>/       chỉ code, dự án tự dựng
```

- Mỗi thư mục đánh số một `README.md` **một đoạn ngắn** (chứa gì, ai ghi).
- **Mục lục, index nợ**: ⛔ không chép tay; `activerole.py` tự dựng tiêu đề ở lần ghi đầu (`index add`, `index move` phía đích, `debt-write`; `index list` gặp tệp chưa có thì in `RONG`, ⛔ không dựng). Riêng `11_DEBT/Long_Debt_Index.md` ⛔ không lệnh nào ghi: tạo sẵn tệp này gồm dòng tiêu đề `# Long_Debt_Index`, một dòng luật "chỉ mở khi chủ dự án hỏi, ⛔ không tự nhắc" và đầu bảng `| Timecode | Tên | Tệp | Lý do hoãn | Điều kiện sống lại |`.
  ⛔ Không tạo `Active-Role.md` (`/roleflow:start` tự tạo).
- Dự án nhỏ được bớt `03`, `04`, `07`, `08`, `09`, `10`, `12`; **giữ** `01_IDEA/`, `05_PLANS/`, `02_RESEARCH/AI/audits/`, `06_REPORT/CodePlan/`, `11_DEBT/`: skill khác **ghi vào** đó.

## Bước 4 · Kho tài liệu, file nền

- `git init -b main <gốc>`. `.gitignore` **danh sách trắng**: chép nguyên `${CLAUDE_PLUGIN_ROOT}/skills/newprojectapp/gitignore.template` thành `<gốc>/.gitignore`
  (`/*` rồi mở `.gitignore`, `0*_*/`, `11_DEBT/`, `CLAUDE.md`, `AGENTS.md`, `.claude/skills/`; ⛔ không mở `10_EXPORT/`; khối cây 12 chặn
  `/08_SHARE/`, `/09_REFERENCE/`, `/06_REPORT/CodePlan/`, `/06_REPORT/Test/`; khối mẫu chung chặn `.DS_Store`, `node_modules/`, `.env*`, khoá…).
- `<gốc>/CLAUDE.md` = **đúng một dòng** `@AGENTS.md`. `<gốc>/AGENTS.md` gồm tối thiểu: **cây** và ý nghĩa từng mục · 🔴 **ràng buộc tài khoản**
  (account nào, account nào ⛔ không liên quan, lệnh kiểm) · **quy tắc chữ** tên dự án · **điểm vào tài liệu** · **cửa verify** và cách chạy.
  Gốc đã có hai tệp đó thì **bổ sung một mục**, ⛔ không ghi đè.

## Bước 5 · 🔴 KHAI DỰ ÁN VÀO `flow-projects.json` (⛔ đừng bỏ bước này)

0. 🔴 Thêm dòng `"<Tên dự án>": "~/<Ten>Dev"` vào `~/.claude/flow-projects.json` (chưa có tệp thì tạo, dạng `{"Tên": "~/Gốc"}`; thiếu là `/roleflow:start` ra `KHONG_RO_DU_AN`); chỗ duy nhất giữ đường của ba lệnh vai.

## Bước 6 · Verify

- `find <gốc> -maxdepth 2 -type d` đủ cây Bước 3.
- `git -C <gốc> status --short` chỉ ra tệp trong danh sách trắng; `git -C <gốc> check-ignore -q <REPO>/x` thoát 0.
- `CLAUDE.md` đúng một dòng, `AGENTS.md` đủ mục Bước 4; `activerole.py show` chạy ở gốc mới ra `DU_AN=<tên>`.
- 🔴 **0 gạch dài** trong mọi file vừa tạo. 🎣 `rg` im lặng có thể là lệnh sai: chạy **mồi nhử** một lần (tệp tạm có một gạch dài, lệnh phải in `1`). Lệnh kiểm dùng mã unicode, ⛔ không gõ thẳng ký tự:
```bash
rg -c '\x{2014}' <file>   # SẠCH thì rg KHÔNG in gì (mã thoát 1), có vi phạm thì in số
```

## Bước 7 · Báo cáo

Nêu: cây đã dựng ở đâu · đã khai vào `flow-projects.json` chưa · **thông tin nào còn thiếu** (đang ghi `(chưa có)`) và cần user bổ sung lúc nào · việc user phải tự làm (tạo repo GitHub cho repo code và kho tài liệu, tạo project Supabase, commit đầu bằng lệnh "Git").

## Ràng buộc
- 🔴 Chỉ tạo file, thư mục, `git init` kho tài liệu trong máy. ⛔ KHÔNG tạo tài nguyên cloud, ⛔ KHÔNG deploy, ⛔ KHÔNG commit.
- ⛔ KHÔNG đè lên thư mục đã có nội dung.
- 🔴 Mọi thông tin hạ tầng phải HỎI, ⛔ không suy từ tên dự án hay từ dự án khác.
- Hỏi **từng câu một**, mỗi option nói rõ **được gì / mất gì**.
