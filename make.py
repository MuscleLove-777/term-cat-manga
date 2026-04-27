#!/usr/bin/env python3
"""
用語を入れたら 4コマ猫漫画ページを生成して GitHub Pages に push するCLI。

Usage:
    python make.py "Docker"
    python make.py "プロキシ"
    python make.py --no-push "テスト用語"   # ローカル生成だけ
    python make.py --rebuild-index           # index.html だけ作り直し
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

# Windows cp932 回避: stdout/stderr を UTF-8 化
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
DATA = ROOT / "data" / "terms.json"
TEMPLATE_CSS = ROOT / "template" / "style.css"

sys.path.insert(0, str(ROOT))
from lib.render import render_page, render_index  # noqa

DEFAULT_SITE_URL = "https://musclelove-777.github.io/term-cat-manga"


# ===== 1. slug =====
_ASCII = re.compile(r"[a-z0-9]+")
def slugify(term: str) -> str:
    t = term.strip().lower()
    if all(ord(c) < 128 for c in t):
        s = "-".join(_ASCII.findall(t))
        return s or hashlib.md5(t.encode()).hexdigest()[:8]
    # 日本語等を含む: ハッシュ8桁 + URLエンコード版を残す形にせず、ハッシュのみ
    safe = re.sub(r"[^\w\-]", "", t)[:24]
    h = hashlib.md5(term.encode("utf-8")).hexdigest()[:6]
    return f"{safe}-{h}" if safe else f"term-{h}"


# ===== 2. claude -p で4コマ生成 =====
PROMPT_TMPL = """あなたは「にゃんこ用語マンガ」の脚本担当。
用語「{term}」について、先輩シャム猫と後輩黒猫の掛け合いで4コマ漫画の脚本を作る。

# キャラ設定
- senpai: 物知りな先輩シャム猫。落ち着いた敬語まじりの口調。「〜だにゃ」を時々使う。説明役。
- kohai: 元気な後輩黒猫。フランク。「マジっすか！」「えっ、それって…？」と素直に驚く。質問役。

# 構成
- panel 1: 後輩がその用語に出会って戸惑う / 質問する（kohai発話）
- panel 2: 先輩が要点をズバッと説明（senpai発話）
- panel 3: 具体例 or よくある誤解を出す（どちらかが発話、テンポ重視）
- panel 4: ピシッとオチ＋一言まとめ（senpai発話を推奨）

# 制約
- 各セリフは日本語、句読点込みで45〜90文字。改行なし。
- 専門用語の中身が分かるよう、たとえ話を必ず1つ入れる。
- 表情(expression)は normal/explain/surprise/think/happy のどれか1つ。
- summary は 80〜140文字で「結局これは何で、どんな時に使うか」を1段落。

# 出力フォーマット (必ずこのJSONだけを出す。前後に余計な文字や```は禁止)
{{
  "term": "{term}",
  "summary": "...",
  "panels": [
    {{"n": 1, "speaker": "kohai",  "expression": "surprise", "text": "..."}},
    {{"n": 2, "speaker": "senpai", "expression": "explain",  "text": "..."}},
    {{"n": 3, "speaker": "kohai",  "expression": "think",    "text": "..."}},
    {{"n": 4, "speaker": "senpai", "expression": "happy",    "text": "..."}}
  ]
}}
"""


def gen_script(term: str) -> dict:
    prompt = PROMPT_TMPL.format(term=term)
    print(f"[claude] generating script for: {term}", flush=True)
    proc = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True, text=True, timeout=180,
        encoding="utf-8", errors="replace",
    )
    if proc.returncode != 0:
        raise RuntimeError(f"claude failed: {proc.stderr[:500]}")
    raw = proc.stdout.strip()
    # JSON抽出（前後に説明文が混ざる可能性ガード）
    m = re.search(r"\{[\s\S]*\}", raw)
    if not m:
        raise RuntimeError(f"no JSON found in claude output:\n{raw[:500]}")
    data = json.loads(m.group(0))
    # 検証
    assert "summary" in data and len(data["summary"]) >= 30, "summary too short"
    assert isinstance(data.get("panels"), list) and len(data["panels"]) == 4, "need 4 panels"
    for p in data["panels"]:
        assert p["speaker"] in ("senpai", "kohai")
        assert p["expression"] in ("normal", "explain", "surprise", "think", "happy")
        assert 10 <= len(p["text"]) <= 120
    return data


# ===== 3. ファイル書き出し =====
def write_page(term: str, slug: str, data: dict, site_url: str) -> Path:
    out_dir = DOCS / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    html = render_page(term, data["summary"], data["panels"], site_url, slug)
    (out_dir / "index.html").write_text(html, encoding="utf-8")
    return out_dir / "index.html"


def update_registry(term: str, slug: str, summary: str) -> list[dict]:
    DATA.parent.mkdir(parents=True, exist_ok=True)
    if DATA.exists():
        terms = json.loads(DATA.read_text(encoding="utf-8"))
    else:
        terms = []
    # 重複除去（slug で）
    terms = [t for t in terms if t.get("slug") != slug]
    terms.insert(0, {
        "term": term,
        "slug": slug,
        "summary": summary,
        "created": datetime.now().strftime("%Y-%m-%d"),
    })
    DATA.write_text(json.dumps(terms, ensure_ascii=False, indent=2), encoding="utf-8")
    return terms


def write_index(terms: list[dict], site_url: str) -> None:
    DOCS.mkdir(parents=True, exist_ok=True)
    (DOCS / "index.html").write_text(render_index(terms, site_url), encoding="utf-8")
    shutil.copy(TEMPLATE_CSS, DOCS / "style.css")
    # GitHub Pages用 .nojekyll
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")


# ===== 4. git push =====
def git_push(term: str, slug: str) -> None:
    if not (ROOT / ".git").exists():
        print("[git] not a git repo yet, skipping push", flush=True)
        return
    cmds = [
        ["git", "add", "docs", "data"],
        ["git", "commit", "-m", f"add: {term} ({slug})"],
        ["git", "push"],
    ]
    for c in cmds:
        r = subprocess.run(c, cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        if r.returncode != 0 and "nothing to commit" not in (r.stdout + r.stderr):
            print(f"[git] {' '.join(c)} -> {r.stderr[:300]}", flush=True)
            return
    print("[git] pushed", flush=True)


# ===== 5. main =====
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("term", nargs="?")
    ap.add_argument("--no-push", action="store_true")
    ap.add_argument("--rebuild-index", action="store_true")
    ap.add_argument("--site-url", default=os.environ.get("SITE_URL", DEFAULT_SITE_URL))
    args = ap.parse_args()

    if args.rebuild_index:
        terms = json.loads(DATA.read_text(encoding="utf-8")) if DATA.exists() else []
        write_index(terms, args.site_url)
        print(f"[ok] rebuilt index ({len(terms)} terms)")
        return

    if not args.term:
        ap.error("term is required")

    term = args.term.strip()
    slug = slugify(term)

    data = gen_script(term)
    page = write_page(term, slug, data, args.site_url)
    terms = update_registry(term, slug, data["summary"])
    write_index(terms, args.site_url)

    if not args.no_push:
        git_push(term, slug)

    page_url = f"{args.site_url}/{slug}/"
    line_text = f"【にゃんこ用語解説】{term}\n{data['summary'][:80]}…\n{page_url}"
    line_share = "https://line.me/R/msg/text/?" + urllib.parse.quote(line_text)

    print()
    print("=" * 56)
    print(f"✅ 生成完了: {term}")
    print(f"📄 ローカル : {page}")
    print(f"🌐 公開URL  : {page_url}")
    print(f"📲 LINE共有 : {line_share}")
    print("=" * 56)


if __name__ == "__main__":
    main()
