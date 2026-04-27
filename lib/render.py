"""
1ページHTMLレンダラ。
panels: [{n, speaker, expression, text}, ...] 4要素
"""
from __future__ import annotations
import html
import urllib.parse
from .characters import render_cat


def _bubble(speaker: str, text: str) -> str:
    safe = html.escape(text)
    if speaker == "senpai":
        return f'<div class="bubble senpai"><span class="tag">先輩</span><br>{safe}</div>'
    return f'<div class="bubble kohai"><span class="tag">後輩</span><br>{safe}</div>'


def _scene(speaker: str, expression: str) -> str:
    """話している猫を主役に、相方をやや小さく添える。"""
    main = render_cat(speaker, expression)
    other = "kohai" if speaker == "senpai" else "senpai"
    sub = render_cat(other, "normal")
    if speaker == "senpai":
        return (
            f'<svg class="cat" viewBox="0 0 200 240">{main}</svg>'
            f'<svg class="cat" viewBox="0 0 200 240" style="opacity:0.85; transform: scaleX(-1);">{sub}</svg>'
        )
    return (
        f'<svg class="cat" viewBox="0 0 200 240" style="opacity:0.85;">{sub}</svg>'
        f'<svg class="cat" viewBox="0 0 200 240" style="transform: scaleX(-1);">{main}</svg>'
    )


def _panel(p: dict) -> str:
    return (
        f'<div class="panel">'
        f'<div class="num">{p["n"]}</div>'
        f'<div class="scene">{_scene(p["speaker"], p["expression"])}</div>'
        f'{_bubble(p["speaker"], p["text"])}'
        f'</div>'
    )


def render_page(term: str, summary: str, panels: list[dict],
                site_url: str, slug: str) -> str:
    page_url = f"{site_url}/{slug}/"
    line_text = f"【にゃんこ用語解説】{term}\n{summary[:80]}…\n{page_url}"
    line_share = "https://line.me/R/msg/text/?" + urllib.parse.quote(line_text)
    x_text = f"【にゃんこ用語解説】{term}を猫で説明するマンガ📚🐈"
    x_share = (
        "https://twitter.com/intent/tweet?"
        + urllib.parse.urlencode({"text": x_text, "url": page_url})
    )

    panel_html = "\n".join(_panel(p) for p in panels)
    safe_term = html.escape(term)
    safe_summary = html.escape(summary)

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>{safe_term} を猫が解説 - にゃんこ用語マンガ</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{safe_term}を先輩シャム猫と後輩黒猫が4コマ漫画で解説。{safe_summary[:80]}">
<meta property="og:title" content="{safe_term} を猫が4コマで解説">
<meta property="og:description" content="{safe_summary[:120]}">
<meta property="og:url" content="{page_url}">
<meta property="og:type" content="article">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">
</head>
<body>
<div class="wrap">
  <a class="back" href="../">← 用語一覧に戻る</a>
  <div class="title">
    <h1>🐈 {safe_term} ってなに？</h1>
    <div class="sub">先輩シャム猫と後輩黒猫の4コマ解説</div>
  </div>

  <div class="panels">
    {panel_html}
  </div>

  <div class="summary">
    <h2>📌 まとめ</h2>
    <p>{safe_summary}</p>
  </div>

  <div class="share">
    <a href="{line_share}" target="_blank" rel="noopener">📲 LINEで共有</a>
    <a class="x" href="{x_share}" target="_blank" rel="noopener">𝕏 でポスト</a>
    <a class="copy" onclick="navigator.clipboard.writeText(location.href);this.textContent='✓ コピーしました'">🔗 URLコピー</a>
  </div>

  <div class="musclelove">
    <h3>📚 もっと色々読みたい人は</h3>
    <p style="margin:6px 0 8px; font-size:13px;">運営メディア / 推し情報はこちら</p>
    <a href="https://x.com/MuscleGirlLove7" target="_blank" rel="noopener">X @MuscleGirlLove7</a>
    <a href="https://www.patreon.com/MuscleGirlLove" target="_blank" rel="noopener">Patreon</a>
  </div>

  <p class="foot">© にゃんこ用語マンガ / Powered by Claude Code</p>
</div>
</body>
</html>"""


def render_index(terms: list[dict], site_url: str) -> str:
    if terms:
        cards = "\n".join(
            f'<a class="term-card" href="./{html.escape(t["slug"])}/">'
            f'<div class="term">{html.escape(t["term"])}</div>'
            f'<div class="desc">{html.escape(t["summary"][:60])}…</div>'
            f'</a>'
            for t in terms
        )
        body = f'<div class="terms">{cards}</div>'
    else:
        body = '<div class="empty">まだ用語がないにゃ。最初の1本を作ろう！</div>'

    return f"""<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>にゃんこ用語マンガ - 用語を猫が4コマで解説</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="難しい用語を先輩シャム猫と後輩黒猫が4コマ漫画でゆるく解説。LINEで共有できる用語辞典。">
<meta property="og:title" content="にゃんこ用語マンガ">
<meta property="og:description" content="難しい用語を猫が4コマで解説。LINEで共有OK。">
<meta property="og:url" content="{site_url}/">
<meta property="og:type" content="website">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="./style.css">
</head>
<body>
<div class="wrap">
  <div class="title">
    <h1>🐈 にゃんこ用語マンガ</h1>
    <div class="sub">難しい用語を、先輩シャム猫と後輩黒猫が4コマでゆる〜く解説</div>
  </div>

  {body}

  <div class="musclelove">
    <h3>📚 運営メディア</h3>
    <a href="https://x.com/MuscleGirlLove7" target="_blank" rel="noopener">X @MuscleGirlLove7</a>
    <a href="https://www.patreon.com/MuscleGirlLove" target="_blank" rel="noopener">Patreon</a>
  </div>

  <p class="foot">© にゃんこ用語マンガ / Powered by Claude Code</p>
</div>
</body>
</html>"""
