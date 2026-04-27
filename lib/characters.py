"""
キャラ固定SVGテンプレート。
- senpai: シャムの先輩猫（クリーム×ブラウンポイント、青目）
- kohai : 黒猫の後輩（緑目、目がちょい大きめで初心者キャラ）

各キャラ表情5種:
  normal / explain / surprise / think / happy

セリフ吹き出しは別レイヤで合成するので、ここはキャラ本体のみ。
"""

# ---------- senpai (シャム猫) ----------
SENPAI_BODY = '''
<g class="cat senpai">
  <!-- 体（クリーム）-->
  <ellipse cx="100" cy="170" rx="55" ry="40" fill="#f4e6cf" stroke="#3a2a1a" stroke-width="2.5"/>
  <!-- 顔 -->
  <ellipse cx="100" cy="100" rx="55" ry="50" fill="#f4e6cf" stroke="#3a2a1a" stroke-width="2.5"/>
  <!-- マスク（鼻周りブラウン）-->
  <ellipse cx="100" cy="115" rx="32" ry="22" fill="#7a5a3a" opacity="0.85"/>
  <!-- 耳 -->
  <polygon points="58,65 50,30 85,55" fill="#5a3a25" stroke="#3a2a1a" stroke-width="2"/>
  <polygon points="142,65 150,30 115,55" fill="#5a3a25" stroke="#3a2a1a" stroke-width="2"/>
  <polygon points="62,60 58,42 78,57" fill="#f4cdb0"/>
  <polygon points="138,60 142,42 122,57" fill="#f4cdb0"/>
  <!-- 鼻 -->
  <path d="M95,113 L105,113 L100,120 Z" fill="#3a2a1a"/>
  <!-- 口 -->
  {mouth}
  <!-- 目 -->
  {eyes}
  <!-- ヒゲ -->
  <line x1="55" y1="118" x2="80" y2="116" stroke="#3a2a1a" stroke-width="1.2"/>
  <line x1="55" y1="125" x2="80" y2="123" stroke="#3a2a1a" stroke-width="1.2"/>
  <line x1="120" y1="116" x2="145" y2="118" stroke="#3a2a1a" stroke-width="1.2"/>
  <line x1="120" y1="123" x2="145" y2="125" stroke="#3a2a1a" stroke-width="1.2"/>
  <!-- 前足 -->
  <ellipse cx="78" cy="200" rx="12" ry="8" fill="#5a3a25" stroke="#3a2a1a" stroke-width="2"/>
  <ellipse cx="122" cy="200" rx="12" ry="8" fill="#5a3a25" stroke="#3a2a1a" stroke-width="2"/>
  <!-- 名札 -->
  <text x="100" y="220" text-anchor="middle" font-family="'Noto Sans JP', sans-serif"
        font-size="11" fill="#3a2a1a" font-weight="700">先輩</text>
</g>
'''

# ---------- kohai (黒猫) ----------
KOHAI_BODY = '''
<g class="cat kohai">
  <!-- 体（黒）-->
  <ellipse cx="100" cy="170" rx="55" ry="40" fill="#1a1a1a" stroke="#000" stroke-width="2.5"/>
  <!-- 顔 -->
  <ellipse cx="100" cy="100" rx="55" ry="50" fill="#1a1a1a" stroke="#000" stroke-width="2.5"/>
  <!-- 耳 -->
  <polygon points="58,65 50,30 85,55" fill="#1a1a1a" stroke="#000" stroke-width="2"/>
  <polygon points="142,65 150,30 115,55" fill="#1a1a1a" stroke="#000" stroke-width="2"/>
  <polygon points="62,60 58,42 78,57" fill="#ff9eb6"/>
  <polygon points="138,60 142,42 122,57" fill="#ff9eb6"/>
  <!-- 鼻 -->
  <path d="M95,113 L105,113 L100,120 Z" fill="#ff7799"/>
  <!-- 口 -->
  {mouth}
  <!-- 目（緑、大きめ）-->
  {eyes}
  <!-- ヒゲ -->
  <line x1="55" y1="118" x2="80" y2="116" stroke="#fff" stroke-width="1.2"/>
  <line x1="55" y1="125" x2="80" y2="123" stroke="#fff" stroke-width="1.2"/>
  <line x1="120" y1="116" x2="145" y2="118" stroke="#fff" stroke-width="1.2"/>
  <line x1="120" y1="123" x2="145" y2="125" stroke="#fff" stroke-width="1.2"/>
  <!-- 前足 -->
  <ellipse cx="78" cy="200" rx="12" ry="8" fill="#1a1a1a" stroke="#000" stroke-width="2"/>
  <ellipse cx="122" cy="200" rx="12" ry="8" fill="#1a1a1a" stroke="#000" stroke-width="2"/>
  <!-- 名札 -->
  <text x="100" y="220" text-anchor="middle" font-family="'Noto Sans JP', sans-serif"
        font-size="11" fill="#fff" font-weight="700">後輩</text>
</g>
'''

# ---------- 表情パーツ ----------
# 先輩=青目、後輩=緑目
SENPAI_EYE_COLOR = "#3a8fc7"
KOHAI_EYE_COLOR = "#7ad17a"

def _eyes(color, mode, big=False):
    rx = 8 if not big else 11
    ry = 6 if not big else 9
    if mode == "normal":
        return (
            f'<ellipse cx="80" cy="100" rx="{rx}" ry="{ry}" fill="white" stroke="#000" stroke-width="1.5"/>'
            f'<ellipse cx="120" cy="100" rx="{rx}" ry="{ry}" fill="white" stroke="#000" stroke-width="1.5"/>'
            f'<ellipse cx="80" cy="100" rx="3" ry="5" fill="{color}"/>'
            f'<ellipse cx="120" cy="100" rx="3" ry="5" fill="{color}"/>'
        )
    if mode == "explain":  # 半目・自信
        return (
            f'<path d="M70,100 Q80,93 90,100" stroke="#000" stroke-width="2.2" fill="white"/>'
            f'<path d="M110,100 Q120,93 130,100" stroke="#000" stroke-width="2.2" fill="white"/>'
            f'<circle cx="80" cy="98" r="2.5" fill="{color}"/>'
            f'<circle cx="120" cy="98" r="2.5" fill="{color}"/>'
        )
    if mode == "surprise":  # 大きく見開く
        return (
            f'<circle cx="80" cy="100" r="11" fill="white" stroke="#000" stroke-width="2"/>'
            f'<circle cx="120" cy="100" r="11" fill="white" stroke="#000" stroke-width="2"/>'
            f'<circle cx="80" cy="100" r="4" fill="{color}"/>'
            f'<circle cx="120" cy="100" r="4" fill="{color}"/>'
            f'<circle cx="82" cy="97" r="1.5" fill="white"/>'
            f'<circle cx="122" cy="97" r="1.5" fill="white"/>'
        )
    if mode == "think":  # 上目遣い
        return (
            f'<ellipse cx="80" cy="100" rx="{rx}" ry="{ry}" fill="white" stroke="#000" stroke-width="1.5"/>'
            f'<ellipse cx="120" cy="100" rx="{rx}" ry="{ry}" fill="white" stroke="#000" stroke-width="1.5"/>'
            f'<ellipse cx="80" cy="95" rx="3" ry="4" fill="{color}"/>'
            f'<ellipse cx="120" cy="95" rx="3" ry="4" fill="{color}"/>'
        )
    if mode == "happy":  # ニコ目
        return (
            f'<path d="M72,103 Q80,95 88,103" stroke="#000" stroke-width="2.5" fill="none"/>'
            f'<path d="M112,103 Q120,95 128,103" stroke="#000" stroke-width="2.5" fill="none"/>'
        )
    return _eyes(color, "normal", big)

def _mouth(mode):
    if mode == "normal":
        return '<path d="M93,125 Q100,128 107,125" stroke="#3a2a1a" stroke-width="1.8" fill="none"/>'
    if mode == "explain":
        return '<path d="M93,127 Q100,132 107,127" stroke="#3a2a1a" stroke-width="1.8" fill="none"/>'
    if mode == "surprise":
        return '<ellipse cx="100" cy="130" rx="6" ry="7" fill="#3a2a1a"/>'
    if mode == "think":
        return '<path d="M93,127 L107,127" stroke="#3a2a1a" stroke-width="1.8" fill="none"/>'
    if mode == "happy":
        return '<path d="M90,124 Q100,135 110,124" stroke="#3a2a1a" stroke-width="2" fill="none"/>'
    return _mouth("normal")

def render_cat(role: str, expression: str = "normal") -> str:
    """role: 'senpai' or 'kohai'  /  expression: normal|explain|surprise|think|happy"""
    if role == "senpai":
        return SENPAI_BODY.format(
            mouth=_mouth(expression),
            eyes=_eyes(SENPAI_EYE_COLOR, expression, big=False),
        )
    if role == "kohai":
        return KOHAI_BODY.format(
            mouth=_mouth(expression),
            eyes=_eyes(KOHAI_EYE_COLOR, expression, big=True),
        )
    raise ValueError(f"unknown role: {role}")
