# roleflow

Plugin Claude Code chạy **flow hai vai** (Leader, Planner) trên dự án của bạn: ý tưởng thành Plan, Plan được rà,
rồi thi công bằng subagent (Coder, Reviewer, Tester), có sổ vai, mục lục việc và sổ nợ để nhiều phiên chạy song song không giẫm chân nhau.

## Flow là gì

- **Hai vai:** Planner viết Idea, Plan; Leader cầm Plan đã chắc, giao subagent thi công, đo, đóng Plan.
  Luật đầy đủ ở `rulebook/Roles.md` (gọi skill `roleflow:role-show` để đọc lại).
- **Lệnh chính:** `/roleflow:start` (vào vai), `/roleflow:done` (rời vai), `/roleflow:pause` (dừng giữa chừng, ghi việc dở),
  `/roleflow:codeplan` (thi công một Plan bằng Coder, Reviewer, Tester), `/roleflow:reviewplan` (rà nội dung Plan), `/roleflow:checkplan` (rà trạng thái Plan),
  `/roleflow:PlanModule` (lập kế hoạch module lớn), `/roleflow:exportplan` (xuất Plan ra HTML), `/roleflow:newprojectapp` (khởi tạo dự án mới), `/roleflow:git` (quy trình deploy an toàn).
- **Agent đi kèm:** executor, reviewer, qa-testing, plan-reviewer, plan-checker, researcher, security-auditor,
  database-architect, supabase-expert, ui-designer.
- **Skill tra luật:** `roleflow:rules-details` (bản đầy đủ luật chung), `roleflow:english-naming` (đặt tên tiếng Anh),
  `roleflow:ctx` (đo ngữ cảnh phiên), `roleflow:role-show` (nạp lại luật vai, xem sổ vai).
- **Sổ, mục lục:** `scripts/activerole.py` giữ sổ vai, mục lục Plan, sổ nợ của từng dự án; mọi lệnh vai đều gọi script này.

## Yêu cầu

- **macOS**: vài skill mở tệp ảnh, HTML bằng lệnh `open` của macOS.
- **python3**: mọi lệnh vai gọi `scripts/activerole.py`.
- **MCP** cho agent cần tới: `chrome-devtools` (đo giao diện, chụp màn), `supabase` (đọc, soát cơ sở dữ liệu).

## Cài

```
claude plugin marketplace add quangcine/roleflow
claude plugin install roleflow@roleflow
```

Hoặc gõ trong phiên Claude Code:

```
/plugin marketplace add quangcine/roleflow
/plugin install roleflow@roleflow
```

Mở phiên Claude Code mới để plugin có hiệu lực.

Lệnh, agent của plugin mang tiền tố `roleflow:`. Gõ tên trần (vd <code>/start</code>) cũng chạy khi máy không có skill nào khác trùng tên; tài liệu dùng tên có tiền tố cho chắc.

## Cập nhật

```
claude plugin marketplace update roleflow
claude plugin update roleflow@roleflow
```

Mở phiên Claude Code mới để bản mới có hiệu lực. Bản mới chỉ về khi số `version` đổi; `CHANGELOG.md` ghi từng bản.

## Chép mẫu CLAUDE.md

Luật chung của flow nằm ở `templates/CLAUDE.md`. Chép vào `~/.claude/CLAUDE.md` (đã có tệp này thì sao lưu trước, rồi gộp tay phần của bạn):

```
cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak 2>/dev/null
curl -fsSL https://raw.githubusercontent.com/quangcine/roleflow/main/templates/CLAUDE.md -o ~/.claude/CLAUDE.md
```

Mẫu đổi theo bản mới thì `CHANGELOG.md` ghi "chép lại mẫu CLAUDE.md": chép lại như trên.

## Khai dự án vào flow-projects.json

`activerole.py` nhận dự án theo thư mục làm việc, đọc từ `~/.claude/flow-projects.json`.
Mỗi dự án một dòng, tên dự án trỏ tới thư mục gốc:

```json
{
  "MyApp": "~/MyAppDev",
  "Blog": "~/BlogDev"
}
```

Chưa có tệp thì tạo mới. Dự án mới tạo bằng `/roleflow:newprojectapp` thì skill tự thêm dòng này.
Mở Claude Code từ thư mục gốc dự án, gõ `/roleflow:start` để vào vai.

Cửa verify, tài khoản deploy của từng dự án ghi ở `CLAUDE.md` (hoặc `AGENTS.md`) gốc dự án đó.
Thư mục việc thì cố định, ⛔ không khai được: `activerole.py` ghi vào `01_IDEA/`, `05_PLANS/`, `11_DEBT/` và sổ vai `Active-Role.md` ở gốc dự án.
Dự án mới thì `/roleflow:newprojectapp` dựng đủ cây thư mục này.

## Giấy phép

MIT, xem `LICENSE`.
