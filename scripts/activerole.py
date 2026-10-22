#!/usr/bin/env python3
# Sổ vai Active-Role.md, mục lục Plan/Idea và sổ nợ ngắn hạn cho ba lệnh /roleflow:start, /roleflow:done, /roleflow:pause
#
# Mọi đường dẫn theo dự án nằm ở đây; skill ⛔ không ghi đường. Mọi lệnh ghi đi qua khoá mkdir của dự án.
#
#   activerole.py start [--leader|--planner] [--thay] [--no <tệp nợ> --phien <tên>] [--phien <tên>] [--viec <đang làm gì>]
#                       --no chỉ nhận nợ đúng vai vừa chọn, ở ⏳ hoặc 🔒 của chính --phien; --no bắt buộc --phien
#   activerole.py off  <mã> <ts>                  xoá dòng mã + ts; xoá được thì nhả mã ở mọi cột Đang cầm
#   activerole.py note <mã> <ts> <đang làm gì>    sửa cột Đang làm gì
#   activerole.py show                             in dự án, gốc, các dòng đang sống
#   activerole.py debt-write --vai <Leader|Planner> --ma <mã> --ten <TenNgan> --viec <một dòng>
#                            [--phien <tên>] [--body <tệp nháp các mục ##>]
#   activerole.py debt-list [--vai <Leader|Planner>]
#   activerole.py debt-take <tệp nợ> --phien <tên>        ⏳ thành 🔒, xoá dòng index; thiếu --phien ra THIEU_PHIEN
#                           --phien đang có dòng sống trong sổ (nhận nợ giữa vai) thì ghi ✅ ngay, in NO_DA_NHAN
#   activerole.py debt-return <tệp nợ>                     🔒 về ⏳, dòng về index
#   activerole.py index move <timecode|tên tệp> <từ> <tới> [--value <ngày xong|lý do dừng|lý do hoãn>]
#                 vào Plan_Cancel, Plan_Debt bắt buộc --value; Plan_Debt (nợ dài hạn) chỉ đọc khi chủ dự án hỏi
#   activerole.py index hold|release <timecode|tên tệp> <mã> [--in <sổ>]
#   activerole.py index add Idea_Draft|Plan_Draft --value "<dòng đúng khuôn | Timecode | Tên | [link](…) | Đang cầm | Ghi chú |>"   trùng tệp đích trong nhóm thì từ chối
#   activerole.py index list <sổ> [--free]   chỉ đọc, ⛔ không lấy khoá; --free chỉ in dòng Đang cầm trống
#   Một timecode khớp nhiều dòng thì in NHIEU_DONG kèm đường tệp từ gốc dự án; gọi lại bằng đường đó.
#   activerole.py ctx <session id>     context đã dùng của phiên, mốc 500k
#   activerole.py usage [giờ]          đo hạn mức mọi dự án trong N giờ (mặc định 24)
#
# Dự án nhận theo thư mục làm việc (tệp ~/.claude/flow-projects.json, dạng {"Tên": "~/Gốc"});
# thư mục lạ hoặc thiếu tệp in KHONG_RO_DU_AN và thoát mã 2; tệp hỏng in FLOW_PROJECTS_HONG, thoát mã 2.
# Biến môi trường ACTIVEROLE_ROOT trỏ sang gốc khác (dùng để test trên sổ tạm).
# Biến môi trường ACTIVEROLE_PROJECTS trỏ sang tệp flow-projects.json khác (dùng để test tệp hỏng).
import datetime
import glob
import json
import os
import re
import shutil
import sys
import time

LIMIT = 500_000
LOCK_STALE = 20   # giây: khoá cũ hơn mức này là mồ côi
LOCK_WAIT = 40    # giây: chờ lâu hơn ngưỡng mồ côi, để khoá mồ côi mới vẫn được gỡ
MAX_SESSION, MAX_TASK, MAX_VALUE = 60, 120, 80

HOME = os.path.expanduser('~')
PROJECTS_FILE = os.path.join(HOME, '.claude', 'flow-projects.json')

BOOK_NAME = 'Active-Role.md'
PLAN_BOOKS = ('Plan_Draft', 'Plan_Pass', 'Plan_Done', 'Plan_Cancel', 'Plan_Debt')
IDEA_BOOKS = ('Idea_Draft', 'Idea_Pass', 'Idea_Done')
# Sổ có cột Đang cầm (Plan_Done, Plan_Cancel, Plan_Debt thay cột đó bằng ngày xong, lý do dừng, lý do hoãn).
HOLD_BOOKS = ('Plan_Draft', 'Plan_Pass', 'Idea_Draft', 'Idea_Pass', 'Idea_Done')
# Sổ mà dòng chuyển vào phải kèm --value (lý do). Plan_Debt là nợ dài hạn: chỉ đọc khi chủ dự án hỏi.
REASON_BOOKS = ('Plan_Cancel', 'Plan_Debt')
# Ai được chuyển dòng nào: Roles.md mục Planner và đoạn Đóng Plan của mục Leader; (mới) → *_Draft ⛔ không đi qua index move.
MOVES = {
    ('Idea_Draft', 'Idea_Pass'), ('Idea_Pass', 'Idea_Done'),
    ('Plan_Draft', 'Plan_Pass'), ('Plan_Pass', 'Plan_Draft'), ('Plan_Pass', 'Plan_Done'),
    ('Plan_Draft', 'Plan_Cancel'), ('Plan_Pass', 'Plan_Cancel'), ('Plan_Done', 'Plan_Cancel'),
    # Hoãn dài hạn vào Plan_Debt; sống lại thì về Draft để rà lại.
    ('Plan_Pass', 'Plan_Debt'), ('Plan_Draft', 'Plan_Debt'), ('Plan_Debt', 'Plan_Draft'),
    # `Plan_*` → `Plan_Cancel`: nợ dài hạn chủ dự án bảo dừng hẳn thì sang Cancel (bắt buộc lý do).
    ('Plan_Debt', 'Plan_Cancel'),
}

BOOK_HEADER = """# Active-Role.md · vai nào đang sống

> Hai vai: **Leader** (mã `L`, một người) và **Planner** (mã `P1`, `P2`…, số lớn nhất đang sống + 1).
> Vào bằng `/roleflow:start`, rời bằng `/roleflow:done` hoặc `/roleflow:pause`. ⛔ Không giữ lịch sử, ⛔ không đưa vào Git.
> ⛔ Đừng sửa tay: mọi thao tác đi qua `activerole.py` (có khoá chống trùng mã).
> Định danh là **mã + timecode vào**, vì mã được dùng lại sau khi rời.

| Mã | Vai | Timecode vào | Tên phiên để nhắn | Đang làm gì |
|---|---|---|---|---|
"""
DEBT_INDEX_HEADER = """# Short_Debt_Index

> Nợ ngắn hạn **chưa nhận**. Tệp nợ ở `Short_Debt_List/`; nhận thì xoá dòng ở đây, tệp ở lại.

| Timecode ghi | Vai | Mã cũ | Việc dở | Tệp nợ |
|---|---|---|---|---|
"""
DEBT_SECTIONS = ('## Việc dở', '## Plan, Idea đang cầm', '## Tệp đã chạm chưa commit',
                 '## Bước tiếp theo', '## Câu đang chờ chủ dự án')
DEBT_MAX_LINES = 40

ROLE_ROW = re.compile(r'^\|\s*(L|P\d+)\s*\|\s*(Leader|Planner)\s*\|\s*(\d{12})\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*$')
TABLE_ROW = re.compile(r'^\|(.*)\|\s*$')
STATUS = re.compile(r'^\*\*TRẠNG THÁI:\*\*\s*(.*)$')
DEBT_META = re.compile(r'^\*\*Vai:\*\*\s*(\S+)\s*·\s*\*\*Mã cũ:\*\*\s*(\S+)\s*·\s*\*\*Ghi lúc:\*\*\s*(\d{12})')
HELD_BY = re.compile(r'^🔒 Đang nhận bởi (.*) lúc (\d{12})$')
LINK = re.compile(r'\]\(([^)]+?\.md)\)')
CODE = re.compile(r'L|P\d+')
WAITING = '⏳ Chưa nhận'
NO_SESSION = '(chưa đặt)'
WARNINGS = []


def now():
    return datetime.datetime.now().strftime('%Y%m%d%H%M')


def die(msg, code=1):
    print(msg)
    sys.exit(code)


def clean(text, limit):
    # Chuỗi vào một ô bảng: bỏ xuống dòng, '|' thành '/', cắt độ dài.
    text = re.sub(r'\s+', ' ', text.replace('|', '/')).strip()
    return text if len(text) <= limit else text[:limit - 1] + '…'


def check_code(code):
    if not CODE.fullmatch(code):
        die('MA_SAI ' + clean(code, MAX_SESSION))
    return code


def required_session(o):
    # Nhận nợ phải gắn đúng một phiên thật: thiếu --phien (hoặc trùng giá trị mặc định) thì ô 🔒
    # ghi '(chưa đặt)' và tab nào gõ cùng chữ đó cũng nhận được.
    session = clean(o.get('--phien', ''), MAX_SESSION)
    if not session or session == NO_SESSION:
        die('THIEU_PHIEN: nhận nợ bắt buộc --phien <tên phiên thật>')
    return session


# ---------- dự án, đường dẫn ----------

def load_roots(path):
    # {tên dự án: gốc}; thiếu tệp trả None (find_project in KHONG_RO_DU_AN), tệp hỏng thì dừng.
    try:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as e:
        die(f'FLOW_PROJECTS_HONG {path}: {e}', 2)
    if not isinstance(data, dict) or not all(
            isinstance(k, str) and isinstance(v, str) and v.strip() for k, v in data.items()):
        die(f'FLOW_PROJECTS_HONG {path}: cần một object {{"Tên": "~/Gốc"}}, giá trị là chuỗi khác rỗng', 2)
    roots = {name: os.path.expanduser(root) for name, root in data.items()}
    rel = [name for name, root in roots.items() if not os.path.isabs(root)]
    if rel:
        die(f'FLOW_PROJECTS_HONG {path}: gốc phải là đường tuyệt đối hoặc bắt đầu bằng ~/ ({", ".join(rel)})', 2)
    return roots


def find_project():
    override = os.environ.get('ACTIVEROLE_ROOT')
    if override:
        return 'TEST', os.path.realpath(override)
    cwd = os.path.realpath(os.getcwd())
    path = os.path.expanduser(os.environ.get('ACTIVEROLE_PROJECTS') or PROJECTS_FILE)
    # Gốc lồng nhau thì lấy gốc sâu nhất chứa cwd, ⛔ không theo thứ tự khai trong tệp.
    hits = []
    for name, root in (load_roots(path) or {}).items():
        real = os.path.realpath(root)
        if cwd == real or cwd.startswith(real + os.sep):
            hits.append((len(real), name, real))
    if hits:
        _, name, real = max(hits)
        return name, real
    die(f'KHONG_RO_DU_AN {cwd}\n'
        f'Thêm dòng "<Tên dự án>": "<gốc, ví dụ ~/TenDev>" vào {path} rồi chạy lại.', 2)


def book_path(root, name):
    if name in PLAN_BOOKS:
        return os.path.join(root, '05_PLANS', name + '.md')
    if name in IDEA_BOOKS:
        return os.path.join(root, '01_IDEA', name + '.md')
    die('SO_LA ' + name)


def debt_dir(root):
    return os.path.join(root, '11_DEBT', 'Short_Debt_List')


def debt_index(root):
    return os.path.join(root, '11_DEBT', 'Short_Debt_Index.md')


def debt_file(root, arg):
    name = os.path.basename(arg)
    if not name.endswith('.md'):
        name += '.md'
    path = os.path.join(debt_dir(root), name)
    if not os.path.exists(path):
        die('KHONG_CO_TEP_NO ' + path)
    return path


# ---------- khoá, đọc ghi ----------

def is_stale(path):
    try:
        return time.time() - os.stat(path).st_mtime > LOCK_STALE
    except FileNotFoundError:
        return None


def clear_stale(path):
    # Khoá mồ côi (phiên chết giữa chừng). Việc gỡ đi qua khoá phụ .break nên mỗi lúc chỉ một bên gỡ;
    # bên đó đo lại trong khoá phụ (bên trước có thể đã gỡ và lấy khoá mới), rồi dời khoá sang tên tạm
    # duy nhất mới xoá. Dời nhầm khoá khác (định danh đổi giữa hai lần đo) thì trả lại.
    # Đo: ⛔ không có khoá phụ thì 2/20 lượt ba tiến trình cùng vào được (bên chậm dời nhầm khoá mới).
    if is_stale(path) is not True:
        return is_stale(path) is None
    guard = path + '.break'
    try:
        os.mkdir(guard)
    except FileExistsError:
        if is_stale(guard):
            try:
                os.rmdir(guard)  # bên gỡ trước chết giữa chừng
            except OSError:
                pass
        return False
    try:
        try:
            old = os.stat(path)
        except FileNotFoundError:
            return True
        if time.time() - old.st_mtime <= LOCK_STALE:
            return False
        tmp = f'{path}.stale.{os.getpid()}.{time.time_ns()}'
        try:
            os.rename(path, tmp)
        except OSError:
            return True
        moved = os.stat(tmp)
        if (moved.st_ino, moved.st_mtime_ns) != (old.st_ino, old.st_mtime_ns):
            try:
                os.rename(tmp, path)
            except OSError:
                die('KHOA_LOI ' + tmp)
            return True
        shutil.rmtree(tmp, ignore_errors=True)
        return True
    finally:
        try:
            os.rmdir(guard)
        except OSError:
            pass


def lock(root):
    path = os.path.join(root, '.activerole.lock')
    token = f'{os.getpid()} {time.time_ns()}'
    deadline = time.time() + LOCK_WAIT
    while time.time() < deadline:
        try:
            os.mkdir(path)
        except FileExistsError:
            if not clear_stale(path):
                time.sleep(0.05)
            continue
        with open(os.path.join(path, 'owner'), 'w') as f:
            f.write(token)
        return path, token
    die('KHONG_LAY_DUOC_KHOA ' + path)


def unlock(held):
    # Chỉ gỡ khoá của chính mình (khoá giữ quá ngưỡng có thể đã bị bên khác gỡ và lấy lại).
    path, token = held
    owner = os.path.join(path, 'owner')
    try:
        if open(owner).read() != token:
            return
        os.remove(owner)
        os.rmdir(path)
    except FileNotFoundError:
        pass


def ensure_table(lines, header):
    # Tệp có mà rỗng hoặc mất tiêu đề bảng: dựng lại tiêu đề theo khuôn trước khi ghi dòng.
    if any(l.startswith('|---') for l in lines):
        return lines
    if not any(l.strip() for l in lines):
        return header.splitlines(keepends=True)
    head = [l for l in header.splitlines(keepends=True) if l.startswith('|')]
    at = next((i for i, l in enumerate(lines) if l.startswith('|')), None)
    if at is None:
        return lines + ['\n'] + head
    return lines[:at] + head + lines[at:]


def read_lines(path, header=None):
    if not os.path.exists(path):
        return header.splitlines(keepends=True) if header is not None else None
    lines = open(path, encoding='utf-8').read().splitlines(keepends=True)
    if lines and not lines[-1].endswith('\n'):
        lines[-1] += '\n'
    return ensure_table(lines, header) if header is not None else lines


def write_lines(path, lines):
    tmp = path + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    os.replace(tmp, path)


def cells(line):
    m = TABLE_ROW.match(line.rstrip('\n'))
    if not m:
        return None
    return [c.strip() for c in m.group(1).split('|')]


def is_data_row(line):
    c = cells(line)
    return bool(c) and len(c) == 5 and re.fullmatch(r'\d{12}', c[0]) is not None


def fmt_row(c):
    return '| ' + ' | '.join(c) + ' |\n'


def insert_row(lines, row, module=None):
    # Dòng mới vào sau dòng cuối cùng module (Master trước, sub theo thứ tự), không có thì cuối bảng.
    new = cells(row)
    is_master = 'master' in new[1].rsplit('/', 1)[-1].lower()
    last_data, first_module, last_module, before = None, None, None, None
    for i, line in enumerate(lines):
        if is_data_row(line) or (cells(line) and line.startswith('|---')):
            last_data = i
        if module and is_data_row(line) and cells(line)[1].startswith(module + '/'):
            c = cells(line)
            first_module = i if first_module is None else first_module
            last_module = i
            if before is None and 'master' not in c[1].rsplit('/', 1)[-1].lower() and c[0] > new[0]:
                before = i
    if last_data is None:
        last_data = len(lines) - 1
    if first_module is not None and is_master:
        at = first_module
    elif before is not None:
        at = before
    elif last_module is not None:
        at = last_module + 1
    else:
        at = last_data + 1
    lines.insert(at, row)


# ---------- sổ vai ----------

def live_roles(lines):
    return [(i, ROLE_ROW.match(l)) for i, l in enumerate(lines) if ROLE_ROW.match(l)]


def role_row(code, role, ts, session, doing):
    return f'| {code} | {role} | {ts} | {session} | {doing} |\n'


def print_roles(lines):
    for _, m in live_roles(lines):
        print('| ' + ' | '.join(m.groups()) + ' |')


def opts(args, flags, valued):
    # Đọc cờ đơn giản: flags là cờ bật/tắt, valued là cờ có giá trị.
    found, rest = {}, []
    i = 0
    while i < len(args):
        a = args[i]
        if a in flags:
            found[a] = True
        elif a in valued:
            if i + 1 >= len(args):
                die('THIEU_GIA_TRI ' + a)
            found[a] = args[i + 1]
            i += 1
        else:
            rest.append(a)
        i += 1
    return found, rest


def cmd_start(root, args):
    o, rest = opts(args, ('--leader', '--planner', '--thay'), ('--no', '--phien', '--viec'))
    if rest:
        die('THAM_SO_LA ' + ' '.join(rest))
    if o.get('--leader') and o.get('--planner'):
        die('CHON_MOT_VAI')
    if o.get('--no'):
        session = required_session(o)
    else:
        session = clean(o.get('--phien', NO_SESSION), MAX_SESSION) or NO_SESSION
    doing = clean(o.get('--viec', 'vừa vào'), MAX_TASK) or 'vừa vào'
    book = os.path.join(root, BOOK_NAME)
    lines = read_lines(book, BOOK_HEADER)
    live = live_roles(lines)
    leaders = [(i, m) for i, m in live if m.group(2) == 'Leader']
    old = (f'LEADER_CU={leaders[0][1].group(1)} {leaders[0][1].group(3)} {leaders[0][1].group(4)}'
           if leaders else None)

    debt = debt_file(root, o['--no']) if o.get('--no') else None

    if o.get('--planner') or (leaders and not o.get('--leader')):
        role = 'Planner'
    elif leaders and not o.get('--thay'):
        # /roleflow:start leader khi đã có Leader: ⛔ không tự thay, skill xử lý (leader.md mục Thay Leader treo).
        print(old)
        die('KHONG_GHI', 0)
    else:
        role = 'Leader'

    if debt:
        # Vai do script quyết trong khoá, nên đối chiếu vai của tệp nợ ở đây, trước khi ghi sổ.
        debt_role = debt_meta(debt)[0]
        if debt_role != role:
            die(f'VAI_NO_KHAC {debt_role} (vai vừa chọn {role}), ⛔ không ghi')
        status = debt_status(debt)
        held = HELD_BY.match(status)
        if status != WAITING and not (held and held.group(1) == session):
            die('DA_CO_NGUOI_NHAN ' + status)

    ts = now()
    if role == 'Leader' and any(m.group(3) == ts for _, m in leaders):
        # Định danh là mã + ts theo phút: thay trong cùng phút thì off của Leader cũ sẽ xoá nhầm dòng mới.
        print(old)
        die('TRUNG_PHUT_THU_LAI: ts mới trùng phút với dòng L cũ, ⛔ không ghi; chờ sang phút sau rồi chạy lại')
    if role == 'Leader':
        for i, m in reversed(leaders):
            print('THAY_DONG_CU', lines[i].strip())
            del lines[i]
        code = 'L'
    else:
        nums = [int(m.group(1)[1:]) for _, m in live if m.group(2) == 'Planner']
        code = f'P{max([0] + nums) + 1}'
    lines.append(role_row(code, role, ts, session, doing))
    write_lines(book, lines)

    if debt:
        if debt_status(debt) == WAITING:
            take_debt(root, debt, session, ts)
        set_status(debt, f'✅ Đã nhận bởi {code} ({session}) lúc {ts}')
        print('NO_DA_NHAN', os.path.basename(debt))
    print(f'VAI={role} MA={code} TS={ts}')
    if old and role == 'Planner':
        print(old)
    print_roles(lines)


def cmd_off(root, args):
    if not args:
        die('THIEU_MA')
    if len(args) < 2:
        die('THIEU_TS off <mã> <ts>: định danh là mã + timecode vào')
    code, ts = check_code(args[0]), args[1]
    book = os.path.join(root, BOOK_NAME)
    lines = read_lines(book, BOOK_HEADER)
    hits = [i for i, m in live_roles(lines) if m.group(1) == code and m.group(3) == ts]
    for i in reversed(hits):
        del lines[i]
    released = 0
    if hits:
        write_lines(book, lines)
        # Chỉ nhả cột Đang cầm khi đúng dòng của mình đã xoá: mã đã sang người khác thì để yên.
        for name in HOLD_BOOKS:
            released += release_all(root, name, code)
    print('DA_XOA', len(hits))
    print('DA_NHA_CAM', released)
    print_roles(lines)


def cmd_note(root, args):
    if len(args) < 3:
        die('CU_PHAP note <mã> <ts> <đang làm gì>')
    code, ts, doing = check_code(args[0]), args[1], clean(' '.join(args[2:]), MAX_TASK)
    book = os.path.join(root, BOOK_NAME)
    lines = read_lines(book, BOOK_HEADER)
    hits = [i for i, m in live_roles(lines) if m.group(1) == code and m.group(3) == ts]
    for i in hits:
        m = ROLE_ROW.match(lines[i])
        lines[i] = role_row(m.group(1), m.group(2), m.group(3), m.group(4), doing)
    if hits:
        write_lines(book, lines)
    print('DA_SUA', len(hits))
    print_roles(lines)


def cmd_show(name, root):
    print(f'DU_AN={name} GOC={root}')
    print_roles(read_lines(os.path.join(root, BOOK_NAME), BOOK_HEADER))


# ---------- sổ nợ ----------

def debt_status(path):
    for line in open(path, encoding='utf-8'):
        m = STATUS.match(line.strip())
        if m:
            return m.group(1).strip()
    die('TEP_NO_THIEU_TRANG_THAI ' + path)


def set_status(path, status):
    lines = read_lines(path)
    for i, line in enumerate(lines):
        if STATUS.match(line.strip()):
            lines[i] = f'**TRẠNG THÁI:** {status}\n'
            break
    write_lines(path, lines)


def debt_meta(path):
    for line in open(path, encoding='utf-8'):
        m = DEBT_META.match(line.strip())
        if m:
            return m.groups()
    die('TEP_NO_THIEU_DONG_VAI ' + path)


def debt_row(path):
    # Dòng index dựng lại từ đầu tệp nợ: Vai, Mã cũ, Ghi lúc, dòng đầu mục Việc dở.
    meta, first, in_section = debt_meta(path), '', False
    for line in open(path, encoding='utf-8'):
        s = line.strip()
        if s.startswith('## '):
            in_section = s.startswith('## Việc dở')
            continue
        if in_section and s and not first:
            first = s
    stem = os.path.basename(path)[:-3]
    return fmt_row([meta[2], meta[0], meta[1], clean(first, MAX_TASK),
                    f'[{stem}](Short_Debt_List/{stem}.md)'])


def take_debt(root, path, session, ts):
    idx = debt_index(root)
    lines = read_lines(idx, DEBT_INDEX_HEADER)
    stem = os.path.basename(path)[:-3]
    kept = [l for l in lines if not (is_data_row(l) and f'Short_Debt_List/{stem}.md' in l)]
    if len(kept) != len(lines) or not os.path.exists(idx):
        write_lines(idx, kept)
    set_status(path, f'🔒 Đang nhận bởi {session} lúc {ts}')


def cmd_debt_write(root, args):
    o, rest = opts(args, (), ('--vai', '--ma', '--ten', '--viec', '--phien', '--body'))
    for k in ('--vai', '--ma', '--ten', '--viec'):
        if k not in o:
            die('THIEU ' + k)
    if rest:
        die('THAM_SO_LA ' + ' '.join(rest))
    if o['--vai'] not in ('Leader', 'Planner'):
        die('VAI_LA ' + clean(o['--vai'], MAX_SESSION))
    check_code(o['--ma'])
    if not re.fullmatch(r'[A-Za-z0-9]+', o['--ten']):
        die('TEN_NGAN_CHI_CHU_SO ' + clean(o['--ten'], MAX_SESSION))
    ts = now()
    stem = f'No_{ts}_{o["--ma"]}_{o["--ten"]}'
    os.makedirs(debt_dir(root), exist_ok=True)
    path = os.path.join(debt_dir(root), stem + '.md')
    if os.path.exists(path):
        die('TEP_NO_DA_CO ' + path)
    task = clean(o['--viec'], MAX_TASK)
    if not task:
        die('THIEU --viec')
    if o.get('--body') and not os.path.isfile(o['--body']):
        die('KHONG_CO_TEP_NHAP ' + o['--body'])
    body = open(o['--body'], encoding='utf-8').read().rstrip('\n') if o.get('--body') else None
    session = clean(o.get('--phien', '(chưa đặt)'), MAX_SESSION) or '(chưa đặt)'
    head = [f'# {stem}', f'**TRẠNG THÁI:** {WAITING}',
            f'**Vai:** {o["--vai"]} · **Mã cũ:** {o["--ma"]} · **Ghi lúc:** {ts} · '
            f'**Phiên:** {session}']
    if body:
        # Bản nháp phải có đủ năm mục, mục Việc dở mở đầu bằng dòng --viec để index dựng lại được.
        missing = [s for s in DEBT_SECTIONS if s not in body]
        if missing:
            die('NHAP_THIEU_MUC ' + ', '.join(missing))
        body_lines = body.splitlines()
        at = next(i for i, l in enumerate(body_lines) if l.startswith('## Việc dở'))
        nxt = body_lines[at + 1].strip() if at + 1 < len(body_lines) else ''
        if nxt != task:
            body_lines.insert(at + 1, task)
        text = head + body_lines
    else:
        text = head + [DEBT_SECTIONS[0], task] + list(DEBT_SECTIONS[1:])
    if len(text) > DEBT_MAX_LINES:
        die(f'QUA_{DEBT_MAX_LINES}_DONG {len(text)}')
    write_lines(path, [l + '\n' for l in text])
    idx = debt_index(root)
    lines = read_lines(idx, DEBT_INDEX_HEADER)
    insert_row(lines, debt_row(path))
    write_lines(idx, lines)
    print('DA_GHI_NO', path)


def cmd_debt_list(root, args):
    o, rest = opts(args, (), ('--vai',))
    want = o.get('--vai')
    lines = read_lines(debt_index(root), DEBT_INDEX_HEADER)
    n = 0
    for l in lines:
        if is_data_row(l) and (not want or cells(l)[1] == want):
            print(l.rstrip('\n'))
            n += 1
    print('SO_NO', n)
    # Nợ 🔒: skill đối chiếu tên phiên với ListAgents.
    for path in sorted(glob.glob(os.path.join(debt_dir(root), 'No_*.md'))):
        status = debt_status(path)
        if status.startswith('🔒'):
            print('DANG_NHAN', os.path.basename(path), status)


def cmd_debt_take(root, args):
    o, rest = opts(args, (), ('--phien',))
    if not rest:
        die('THIEU_TEP_NO')
    session = required_session(o)
    path = debt_file(root, rest[0])
    status = debt_status(path)
    if status != WAITING:
        die('DA_CO_NGUOI_NHAN ' + status)
    # Phiên đã ở trong vai mà nhận thêm nợ thì ⛔ không còn start --no nào ghi ✅: ghi ngay ở đây,
    # kẻo tệp kẹt 🔒 mãi.
    lines = read_lines(os.path.join(root, BOOK_NAME), BOOK_HEADER)
    rows = [m for _, m in live_roles(lines) if m.group(4) == session]
    if len(rows) == 1 and debt_meta(path)[0] != rows[0].group(2):
        die(f'VAI_NO_KHAC {debt_meta(path)[0]} (phiên đang giữ vai {rows[0].group(2)}), ⛔ không ghi')
    ts = now()
    take_debt(root, path, session, ts)
    print('DA_GIU', path)
    if len(rows) == 1:
        set_status(path, f'✅ Đã nhận bởi {rows[0].group(1)} ({session}) lúc {ts}')
        print('NO_DA_NHAN', os.path.basename(path), 'MA=' + rows[0].group(1))


def cmd_debt_return(root, args):
    if not args:
        die('THIEU_TEP_NO')
    path = debt_file(root, args[0])
    status = debt_status(path)
    if not status.startswith('🔒'):
        die('KHONG_DANG_GIU ' + status)
    set_status(path, WAITING)
    idx = debt_index(root)
    lines = read_lines(idx, DEBT_INDEX_HEADER)
    stem = os.path.basename(path)[:-3]
    if not any(is_data_row(l) and f'Short_Debt_List/{stem}.md' in l for l in lines):
        insert_row(lines, debt_row(path))
    write_lines(idx, lines)
    print('DA_TRA', path)


# ---------- mục lục ----------

def index_header(name):
    col4 = {'Plan_Done': 'Ngày xong', 'Plan_Cancel': 'Lý do dừng',
            'Plan_Debt': 'Lý do hoãn'}.get(name, 'Đang cầm')
    folder = 'Plan_List' if name in PLAN_BOOKS else 'Idea_List'
    return (f'# {name}\n\n> Mục lục do `activerole.py` dựng. '
            f'Tệp nằm yên trong `{folder}/`; chỉ dòng mục lục chuyển giữa các sổ.\n\n'
            f'| Timecode | Tên | Link | {col4} | Ghi chú |\n|---|---|---|---|---|\n')


def norm_target(target):
    # Chuẩn hoá đường tệp đích của link: bỏ './', gộp 'a/../b'.
    return os.path.normpath(target.strip().strip('<>'))


def index_rows(name, lines):
    # Các dòng mục lục: (số dòng, ô, tệp đích chuẩn hoá hoặc None). Dòng sai khuôn vẫn trả về
    # (để kiểm trùng tệp) và được báo SO_HONG_KHUON, ⛔ không bỏ qua im lặng.
    rows = []
    for i, l in enumerate(lines):
        if not l.startswith('|') or l.startswith('|---'):
            continue
        c = cells(l)
        if c is None or c[0] == 'Timecode':
            continue
        m = LINK.search(l)
        target = norm_target(m.group(1)) if m else None
        ok = (len(c) == 5 and re.fullmatch(r'\d{12}', c[0]) is not None
              and LINK.search(c[2]) is not None)
        if not ok:
            note = f'SO_HONG_KHUON {name}:{i + 1}: {l.strip()}'
            if note not in WARNINGS:
                WARNINGS.append(note)
        rows.append((i, c, target))
    return rows


def file_matches(target, wanted):
    wanted = norm_target(wanted if wanted.endswith('.md') else wanted + '.md')
    if '/' not in wanted:
        return os.path.basename(target) == wanted
    return target == wanted or target.endswith('/' + wanted) or wanted.endswith('/' + target)


def pick_rows(name, lines, wanted):
    # Chọn dòng theo timecode (12 số) hoặc tên tệp ở cột Link; chỉ dòng đủ 5 ô có link.
    by_tc = re.fullmatch(r'\d{12}', wanted) is not None
    out = []
    for i, c, target in index_rows(name, lines):
        if len(c) != 5 or not target:
            continue
        if (c[0] == wanted) if by_tc else file_matches(target, wanted):
            out.append((i, c, target))
    return out


def root_rel(name, target):
    # Đường tệp đích tính từ gốc dự án (link trong sổ tính từ thư mục của sổ). Đường này
    # chọn được dòng ở move, hold, release, kể cả khi hai module trùng tên tệp.
    folder = '05_PLANS' if name in PLAN_BOOKS else '01_IDEA'
    return os.path.normpath(os.path.join(folder, target))


def die_many(wanted, found):
    # found: [(sổ, tệp đích)]
    lines = [f'NHIEU_DONG {clean(wanted, 200)}: {len(found)} dòng, gọi lại bằng đường ở dòng DONG']
    lines += [f'DONG {name} {root_rel(name, target)}' for name, target in found]
    die('\n'.join(lines))


def cmd_index_list(root, args):
    # Chỉ đọc (⛔ không lấy khoá, như show). Mỗi dòng: MUC<TAB>tc<TAB>đường từ gốc<TAB>Tên<TAB>cột 4.
    o, rest = opts(args, ('--free',), ())
    if len(rest) != 1:
        die('CU_PHAP index list <sổ> [--free]')
    name = rest[0]
    if name not in PLAN_BOOKS + IDEA_BOOKS:
        die('SO_LA ' + clean(name, MAX_SESSION))
    if o.get('--free') and name not in HOLD_BOOKS:
        die('SO_KHONG_CO_COT_DANG_CAM ' + name)
    lines = read_lines(book_path(root, name))
    if lines is None:
        print('RONG', name)
        return
    n = 0
    for _, c, target in index_rows(name, lines):
        if len(c) != 5 or not target:
            continue
        if o.get('--free') and c[3]:
            continue
        print('\t'.join(['MUC', c[0], root_rel(name, target), clean(c[1], 200), clean(c[3], MAX_VALUE)]))
        n += 1
    print('SO_DONG', n)


def release_all(root, name, code):
    path = book_path(root, name)
    lines = read_lines(path)
    if lines is None:
        return 0
    n = 0
    for i, l in enumerate(lines):
        if is_data_row(l):
            c = cells(l)
            if c[3] in (code, '🔨 ' + code):
                c[3] = ''
                lines[i] = fmt_row(c)
                n += 1
    if n:
        write_lines(path, lines)
    return n


def cmd_index(root, args):
    if not args:
        die('CU_PHAP index add|move|hold|release|list …')
    sub, args = args[0], args[1:]
    if sub == 'add':
        o, rest = opts(args, (), ('--value',))
        if len(rest) != 1 or not o.get('--value'):
            die('CU_PHAP index add Idea_Draft|Plan_Draft --value "<dòng đúng khuôn | Timecode | Tên | [link](…) | Đang cầm | Ghi chú |>"')
        name = rest[0]
        # Ai được chuyển dòng nào (Roles.md): dòng (mới) chỉ vào hai sổ Draft.
        if name not in ('Idea_Draft', 'Plan_Draft'):
            die('KHONG_DUOC_ADD ' + clean(name, MAX_SESSION) + ': dòng mới chỉ vào Idea_Draft, Plan_Draft')
        group = PLAN_BOOKS if name in PLAN_BOOKS else IDEA_BOOKS
        raw = o['--value'].strip()
        c = cells(raw) if '\n' not in raw else None
        link = re.fullmatch(r'\[[^\]]+\]\(([^)]+\.md)\)', c[2]) if c and len(c) == 5 else None
        if not link or not re.fullmatch(r'\d{12}', c[0]) or not c[1]:
            die('SAI_KHUON_DONG ' + clean(raw, 200))
        target = norm_target(link.group(1))
        # Trùng tệp đích ở bất kỳ sổ nào cùng nhóm thì từ chối; trùng timecode (Plan viết cùng phút) thì được.
        for other in group:
            olines = read_lines(book_path(root, other)) or []
            for i, oc, otarget in index_rows(other, olines):
                if otarget == target:
                    die(f'DA_CO_DONG {target} trong {other}: {olines[i].strip()}')
        path = book_path(root, name)
        lines = read_lines(path, index_header(name))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        module = c[1].rsplit('/', 1)[0] if '/' in c[1] else None
        insert_row(lines, fmt_row(c), module)
        write_lines(path, lines)
        print(f'DA_THEM {c[0]} {name}')
        print(fmt_row(c).rstrip('\n'))
        return
    if sub == 'move':
        o, rest = opts(args, (), ('--value',))
        if len(rest) != 3:
            die('CU_PHAP index move <timecode|tên tệp> <từ> <tới> [--value …]')
        wanted, src, dst = rest
        if (src, dst) not in MOVES:
            die(f'CHUYEN_SAI {clean(src, MAX_SESSION)} -> {clean(dst, MAX_SESSION)}')
        if dst in REASON_BOOKS and not clean(o.get('--value', ''), MAX_VALUE):
            die('THIEU_LY_DO --value')
        sp, dp = book_path(root, src), book_path(root, dst)
        slines = read_lines(sp)
        if slines is None:
            die('THIEU_SO ' + sp)
        slines = ensure_table(slines, index_header(src))
        dlines = read_lines(dp, index_header(dst))
        hits = pick_rows(src, slines, wanted)
        if not hits:
            die(f'KHONG_THAY_DONG {clean(wanted, 200)} trong {src}')
        if len(hits) > 1:
            die_many(wanted, [(src, t) for _, _, t in hits])
        i, c, target = hits[0]
        dup = [r for r in index_rows(dst, dlines) if r[2] == target]
        if dup:
            die(f'DA_CO_DONG {target} trong {dst}: {dlines[dup[0][0]].strip()}')
        if dst == 'Plan_Done':
            c[3] = o.get('--value') or datetime.datetime.now().strftime('%Y-%m-%d')
        elif dst in REASON_BOOKS:
            c[3] = o['--value']
        else:
            c[3] = ''  # chuyển sổ là giao tay: người cầm cũ nhả, người mới tự hold.
        c[3] = clean(c[3], MAX_VALUE)
        del slines[i]
        module = c[1].rsplit('/', 1)[0] if '/' in c[1] else None
        insert_row(dlines, fmt_row(c), module)
        os.makedirs(os.path.dirname(dp), exist_ok=True)
        write_lines(dp, dlines)
        write_lines(sp, slines)
        print(f'DA_CHUYEN {c[0]} {os.path.basename(target)} {src} -> {dst}')
        print(fmt_row(c).rstrip('\n'))
        return
    if sub in ('hold', 'release'):
        o, rest = opts(args, (), ('--in',))
        if len(rest) != 2:
            die(f'CU_PHAP index {sub} <timecode|tên tệp> <mã> [--in <sổ>]')
        wanted, code = rest[0], check_code(rest[1])
        names = [o['--in']] if o.get('--in') else HOLD_BOOKS
        found = []
        for name in names:
            if name not in HOLD_BOOKS:
                die('SO_KHONG_CO_COT_DANG_CAM ' + clean(name, MAX_SESSION))
            lines = read_lines(book_path(root, name))
            if lines is None:
                continue
            for i, c, target in pick_rows(name, lines, wanted):
                found.append((name, lines, i, c, target))
        if not found:
            die(f'KHONG_THAY_DONG {clean(wanted, 200)} trong ' + ' '.join(names))
        if len(found) > 1:
            die_many(wanted, [(f[0], f[4]) for f in found])
        name, lines, i, c, target = found[0]
        mark = ('🔨 ' + code) if (name == 'Plan_Pass' and code == 'L') else code
        if sub == 'hold':
            if c[3] and c[3] != mark:
                die('DA_CO_NGUOI_CAM ' + c[3])
            c[3] = mark
        else:
            if c[3] not in (code, '🔨 ' + code):
                die('KHONG_PHAI_NGUOI_CAM ' + (c[3] or '(trống)'))
            c[3] = ''
        lines[i] = fmt_row(c)
        write_lines(book_path(root, name), ensure_table(lines, index_header(name)))
        print(('DA_CAM ' if sub == 'hold' else 'DA_NHA ') + f'{c[0]} {os.path.basename(target)} {name}')
        print(lines[i].rstrip('\n'))
        return
    die('LENH_LA index ' + clean(sub, MAX_SESSION))


# ---------- ctx, usage ----------

def context_used(session_id):
    paths = glob.glob(os.path.expanduser(f'~/.claude/projects/*/{session_id}.jsonl'))
    if not paths:
        die('KHONG_TIM_THAY ' + session_id)
    size = os.path.getsize(paths[0])
    # Nhật ký có thể nặng hàng trăm MB: chỉ đọc đuôi, lượt assistant cuối nằm ở đó.
    for tail in (2 << 20, 32 << 20, size):
        with open(paths[0], 'rb') as f:
            f.seek(max(0, size - tail))
            lines = f.read().decode('utf-8', 'ignore').splitlines()
        for line in reversed(lines):
            if '"usage"' not in line:
                continue
            try:
                entry = json.loads(line)
            except ValueError:
                continue
            usage = (entry.get('message') or {}).get('usage')
            if entry.get('type') == 'assistant' and usage and not entry.get('isSidechain'):
                return (usage.get('input_tokens', 0) + usage.get('cache_read_input_tokens', 0)
                        + usage.get('cache_creation_input_tokens', 0))
        if tail >= size:
            break
    die('KHONG_CO_LUOT_ASSISTANT')


def usage_audit(hours):
    # Chi phí ước theo tỉ lệ giá Opus (ghi đệm 1.25, đọc đệm 0.1, đầu ra 5, đầu vào 1).
    from collections import Counter
    base = os.path.expanduser('~/.claude/projects')
    t = time.time()

    def _ctx(u):
        return u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0)

    def cost(u):
        return (u.get('input_tokens', 0) + 1.25 * u.get('cache_creation_input_tokens', 0)
                + 0.1 * u.get('cache_read_input_tokens', 0) + 5 * u.get('output_tokens', 0))

    by_project, by_tool, by_band = Counter(), Counter(), Counter()
    hook_errors, single_bash, bare_cd, total = 0, 0, 0, 0
    files = glob.glob(base + '/*/*.jsonl') + glob.glob(base + '/*/*/subagents/*.jsonl')
    for path in files:
        if t - os.path.getmtime(path) > hours * 3600:
            continue
        project = path[len(base) + 1:].split('/')[0].replace(re.sub(r'[^A-Za-z0-9]', '-', HOME) + '-', '')
        calls = {}
        for line in open(path, errors='ignore'):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get('type') == 'attachment' and (d.get('attachment') or {}).get('type') == 'hook_non_blocking_error':
                hook_errors += 1
            if d.get('type') != 'assistant':
                continue
            m = d['message']
            # One API call can span several jsonl lines with the same message id.
            entry = calls.setdefault(m.get('id'), [m.get('usage') or {}, []])
            for b in m.get('content') or []:
                if isinstance(b, dict) and b.get('type') == 'tool_use':
                    name = 'chrome-devtools' if 'chrome-devtools' in b['name'] else b['name']
                    entry[1].append((name, (b.get('input') or {}).get('command', '')))
        for usage, tools in calls.values():
            c = cost(usage)
            total += c
            by_project[project] += c
            names = sorted({x for x, _ in tools}) or ['(text only)']
            by_tool['+'.join(names)] += c
            size = _ctx(usage)
            by_band['<150k' if size < 150e3 else '150-300k' if size < 300e3 else '300-500k' if size < LIMIT else '>500k'] += c
            if len(tools) == 1 and tools[0][0] == 'Bash':
                single_bash += 1
                bare_cd += tools[0][1].lstrip().startswith('cd ')
    if not total:
        print(f'Last {hours:g}h, total cost units: 0')
        return

    def show(title, counter, top=8):
        print(title)
        for k, v in counter.most_common(top):
            print(f'  {k[:40]:40s} {v / total * 100:5.1f}%')

    print(f'Last {hours:g}h, total cost units: {int(total):,}')
    show('By project:', by_project)
    show('By tool in the call:', by_tool)
    show('By context size:', by_band)
    print(f'Hook errors: {hook_errors} | single-Bash calls: {single_bash} | starting with bare cd: {bare_cd}')


# ---------- main ----------

def main():
    if len(sys.argv) < 2:
        die('CU_PHAP activerole.py <lệnh> …')
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == 'usage':
        usage_audit(float(args[0]) if args else 24)
        return
    if cmd == 'ctx':
        if not args:
            die('THIEU_SESSION_ID')
        used = context_used(args[0])
        print(f'CTX={used} LIMIT={LIMIT} LEFT={LIMIT - used} OVER={int(used >= LIMIT)}')
        return
    handlers = {
        'start': cmd_start, 'off': cmd_off, 'note': cmd_note,
        'debt-write': cmd_debt_write, 'debt-list': cmd_debt_list, 'debt-take': cmd_debt_take,
        'debt-return': cmd_debt_return, 'index': cmd_index,
    }
    if cmd not in handlers and cmd != 'show':
        die('LENH_LA ' + clean(cmd, MAX_SESSION))
    name, root = find_project()
    if cmd == 'show':
        # Chỉ đọc: ghi luôn qua os.replace nên đọc ⛔ không cần khoá.
        cmd_show(name, root)
        return
    if cmd == 'index' and args[:1] == ['list']:
        try:
            cmd_index_list(root, args[1:])
        finally:
            for note in WARNINGS:
                print('CANH_BAO', note)
        return
    held = lock(root)
    try:
        handlers[cmd](root, args)
    finally:
        unlock(held)
        for note in WARNINGS:
            print('CANH_BAO', note)


main()
