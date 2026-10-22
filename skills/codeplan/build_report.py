#!/usr/bin/env python3
# Dựng báo cáo thi công HTML một tệp (ảnh nhúng base64) từ <thư mục>/manifest.json của /roleflow:codeplan.
#   build_report.py <thư mục bằng chứng>
# Thiếu ảnh nào thì thoát mã 1: báo cáo thiếu bằng chứng ⛔ không được coi là xong.
# Khuôn manifest.json (ảnh là đường dẫn tương đối trong thư mục bằng chứng):
#   {"plan": "Plan_<ts>_<Ten>.md", "plan_path": "...", "title": "...", "started": "<ts>", "finished": "<ts>",
#    "rounds": {"coder": 1, "reviewer": 1, "tester": 1},
#    "files": ["<repo>/apps/.../page.tsx"],
#    "verify": [{"cmd": "...", "result": "11/11", "ok": true}],
#    "criteria": [{"name": "...", "ok": true, "note": "...", "image": "anh/01_ten.png"}],
#    "review": ["vòng 1: ..."], "notes": ["..."]}
import base64
import html
import json
import mimetypes
import os
import re
import sys


def esc(value):
    return html.escape(str(value if value is not None else ''))


def badge(ok):
    return '<span class="b ok">ĐẠT</span>' if ok else '<span class="b ng">KHÔNG ĐẠT</span>'


def main():
    root = os.path.abspath(sys.argv[1])
    m = json.load(open(os.path.join(root, 'manifest.json'), encoding='utf-8'))
    plan = m.get('plan', 'Plan')
    short = re.sub(r'^Plan_\d{12}_|\.md$', '', plan) or 'Plan'
    out = os.path.join(root, f"BaoCao_{m.get('started', '')}_{short}.html")

    missing, embedded, cards = [], 0, []
    for i, c in enumerate(m.get('criteria', []), 1):
        img = ''
        if c.get('image'):
            path = os.path.join(root, c['image'])
            if os.path.isfile(path):
                mime = mimetypes.guess_type(path)[0] or 'image/png'
                data = base64.b64encode(open(path, 'rb').read()).decode()
                img = f'<img src="data:{mime};base64,{data}" alt="{esc(c.get("name"))}" loading="lazy">'
                embedded += 1
            else:
                missing.append(c['image'])
                img = f'<p class="miss">Thiếu ảnh: {esc(c["image"])}</p>'
        cards.append(f'<section class="card"><h3>{i}. {esc(c.get("name"))} {badge(c.get("ok"))}</h3>'
                     f'<p>{esc(c.get("note"))}</p>{img}</section>')

    rounds = m.get('rounds', {})
    verify = ''.join(f'<tr><td><code>{esc(v.get("cmd"))}</code></td><td>{esc(v.get("result"))}</td><td>{badge(v.get("ok"))}</td></tr>'
                     for v in m.get('verify', []))
    files = ''.join(f'<li><code>{esc(f)}</code></li>' for f in m.get('files', []))
    review = ''.join(f'<li>{esc(r)}</li>' for r in m.get('review', []))
    notes = ''.join(f'<li>{esc(n)}</li>' for n in m.get('notes', []))
    passed = sum(1 for c in m.get('criteria', []) if c.get('ok'))
    total = len(m.get('criteria', []))

    page = f'''<!doctype html><html lang="vi"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Báo cáo thi công</title>
<style>
:root{{--bg:#fafaf9;--fg:#1c1917;--mut:#57534e;--card:#fff;--line:#e7e5e4;--ok:#15803d;--ng:#b91c1c}}
@media (prefers-color-scheme:dark){{:root{{--bg:#1c1917;--fg:#f5f5f4;--mut:#a8a29e;--card:#292524;--line:#44403c;--ok:#4ade80;--ng:#f87171}}}}
body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.6 system-ui,sans-serif}}
main{{max-width:960px;margin:0 auto;padding:24px 16px}}
h1{{font-size:22px;margin:0 0 4px}} h2{{font-size:17px;margin:28px 0 8px}} h3{{font-size:15px;margin:0 0 6px}}
.mut{{color:var(--mut)}} code{{font-size:13px;word-break:break-all}}
.stats{{display:grid;grid-template-columns:repeat(auto-fit,minmax(140px,1fr));gap:8px;margin:16px 0}}
.stat,.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}}
.stat b{{display:block;font-size:20px}} .card{{margin:10px 0}}
.card img{{width:100%;height:auto;border:1px solid var(--line);border-radius:6px;margin-top:8px}}
table{{width:100%;border-collapse:collapse}} td{{border-top:1px solid var(--line);padding:6px 4px;vertical-align:top}}
.b{{font-size:12px;font-weight:600;padding:1px 6px;border-radius:4px;border:1px solid}}
.ok{{color:var(--ok)}} .ng{{color:var(--ng)}} .miss{{color:var(--ng)}}
</style></head><body><main>
<h1>Báo cáo thi công: {esc(m.get('title', short))}</h1>
<p class="mut">Plan <code>{esc(m.get('plan_path', plan))}</code> · bắt đầu {esc(m.get('started'))} · xong {esc(m.get('finished'))}</p>
<div class="stats">
<div class="stat"><b>{passed}/{total}</b>tiêu chí đạt</div>
<div class="stat"><b>{esc(rounds.get('coder', 0))}</b>vòng Coder</div>
<div class="stat"><b>{esc(rounds.get('reviewer', 0))}</b>vòng Reviewer</div>
<div class="stat"><b>{esc(rounds.get('tester', 0))}</b>vòng Tester</div>
</div>
<h2>Cửa verify</h2><table><tbody>{verify}</tbody></table>
<h2>Tiêu chí nghiệm thu và ảnh bằng chứng</h2>{''.join(cards)}
<h2>Review qua các vòng</h2><ul>{review}</ul>
<h2>Tệp đã chạm (chờ lệnh "Git")</h2><ul>{files}</ul>
<h2>Ghi chú</h2><ul>{notes}</ul>
</main></body></html>'''
    open(out, 'w', encoding='utf-8').write(page)
    print(f'HTML={out}')
    print(f'KB={os.path.getsize(out) // 1024} ANH_NHUNG={embedded} THIEU={len(missing)} DAT={passed}/{total}')
    if missing:
        sys.exit('THIEU_ANH ' + ', '.join(missing))


main()
