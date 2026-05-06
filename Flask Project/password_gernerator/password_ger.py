from flask import Flask, request
import random
import string

app = Flask(__name__)

# ─────────────────────────────────────────────
# Shared CSS
# ─────────────────────────────────────────────
STYLES = """
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --bg:#0f0f0f; --surface:#1a1a1a; --surface2:#242424;
    --border:#2e2e2e; --accent:#e8ff47; --accent-dim:rgba(232,255,71,0.12);
    --text:#f0f0f0; --muted:#888;
    --green:#4dff91; --green-dim:rgba(77,255,145,0.12);
    --r:12px;
  }
  * { margin:0; padding:0; box-sizing:border-box; }
  body {
    background:var(--bg); color:var(--text);
    font-family:'DM Sans',sans-serif;
    min-height:100vh; display:flex;
    align-items:center; justify-content:center; padding:24px;
  }
  @keyframes fadeUp {
    from { opacity:0; transform:translateY(24px); }
    to   { opacity:1; transform:translateY(0); }
  }
  @keyframes popIn {
    from { opacity:0; transform:scale(.94); }
    to   { opacity:1; transform:scale(1); }
  }

  /* ── Card ── */
  .card {
    background:var(--surface); border:1px solid var(--border);
    border-radius:20px; padding:48px; width:100%; max-width:480px;
    animation:fadeUp .45s ease both;
  }
  .badge {
    display:inline-flex; align-items:center; gap:6px;
    font-family:'Syne',sans-serif; font-size:11px; font-weight:700;
    letter-spacing:.08em; text-transform:uppercase;
    padding:5px 12px; border-radius:100px; margin-bottom:16px;
    background:var(--accent-dim); color:var(--accent);
  }
  .card h1 {
    font-family:'Syne',sans-serif; font-size:32px; font-weight:800;
    letter-spacing:-.5px; margin-bottom:8px;
  }
  .subtitle { color:var(--muted); font-size:14px; margin-bottom:36px; }

  /* ── Slider ── */
  .length-row {
    display:flex; align-items:center; justify-content:space-between; margin-bottom:10px;
  }
  .length-label {
    font-size:12px; font-weight:600; font-family:'Syne',sans-serif;
    letter-spacing:.06em; text-transform:uppercase; color:var(--muted);
  }
  .length-value { font-family:'Syne',sans-serif; font-size:22px; font-weight:800; color:var(--accent); }
  input[type=range] {
    -webkit-appearance:none; width:100%; height:4px;
    background:var(--border); border-radius:2px; outline:none;
    margin-bottom:28px; cursor:pointer;
  }
  input[type=range]::-webkit-slider-thumb {
    -webkit-appearance:none; width:18px; height:18px;
    background:var(--accent); border-radius:50%;
    box-shadow:0 0 0 3px var(--accent-dim); transition:box-shadow .15s;
  }
  input[type=range]::-webkit-slider-thumb:hover { box-shadow:0 0 0 6px var(--accent-dim); }

  /* ── Option cards ── */
  .options-label {
    font-size:12px; font-weight:600; font-family:'Syne',sans-serif;
    letter-spacing:.06em; text-transform:uppercase; color:var(--muted);
    margin-bottom:12px; display:block;
  }
  .options-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:28px; }
  .option-card {
    display:flex; align-items:center; gap:10px;
    background:#111; border:1.5px solid var(--border);
    border-radius:var(--r); padding:12px 14px;
    cursor:pointer; transition:border-color .15s, background .15s;
    user-select:none;
  }
  .option-card:hover { border-color:#444; background:var(--surface2); }
  .option-card input[type=checkbox] { display:none; }
  .option-card.checked { border-color:var(--accent); background:var(--accent-dim); }
  .check-icon {
    width:18px; height:18px; border-radius:5px; border:1.5px solid var(--border);
    display:flex; align-items:center; justify-content:center; flex-shrink:0;
    transition:background .15s, border-color .15s;
  }
  .option-card.checked .check-icon { background:var(--accent); border-color:var(--accent); }
  .check-icon svg { display:none; }
  .option-card.checked .check-icon svg { display:block; }
  .option-text { font-size:13px; font-weight:500; }
  .option-card.disabled { pointer-events:none; opacity:.55; }

  /* ── Strength ── */
  .strength-wrap { margin-top:16px; }
  .strength-label-row {
    display:flex; justify-content:space-between; font-size:12px;
    color:var(--muted); margin-bottom:8px;
    font-family:'Syne',sans-serif; font-weight:600;
    text-transform:uppercase; letter-spacing:.06em;
  }
  .strength-bars { display:flex; gap:5px; }
  .s-bar { height:4px; flex:1; border-radius:2px; background:var(--border); transition:background .3s; }

  /* ── Generate button ── */
  .btn-generate {
    width:100%; background:var(--accent); color:#0f0f0f;
    border:none; border-radius:var(--r);
    font-family:'Syne',sans-serif; font-size:15px; font-weight:700;
    padding:16px; cursor:pointer; transition:transform .15s, box-shadow .15s;
  }
  .btn-generate:hover { transform:translateY(-2px); box-shadow:0 10px 28px rgba(232,255,71,.25); }
  .btn-generate:active { transform:translateY(0); }

  /* ── Result box ── */
  .result-box {
    margin-top:28px; background:#111;
    border:1.5px solid var(--green); border-radius:var(--r);
    padding:20px; animation:popIn .3s ease both;
  }
  .result-label {
    font-size:11px; font-weight:700; font-family:'Syne',sans-serif;
    letter-spacing:.08em; text-transform:uppercase;
    color:var(--green); margin-bottom:10px;
    display:flex; align-items:center; gap:6px;
  }
  .password-text {
    font-family:'DM Mono',monospace; font-size:18px; font-weight:500;
    color:var(--text); word-break:break-all; line-height:1.5; letter-spacing:.05em;
  }
  .copy-row { display:flex; justify-content:flex-end; margin-top:14px; }
  .btn-copy {
    display:inline-flex; align-items:center; gap:6px;
    background:var(--green-dim); border:1px solid rgba(77,255,145,.3);
    color:var(--green); font-family:'Syne',sans-serif;
    font-size:12px; font-weight:700; padding:7px 14px;
    border-radius:8px; cursor:pointer; transition:background .15s; letter-spacing:.04em;
  }
  .btn-copy:hover { background:rgba(77,255,145,.2); }

  /* ── Back link ── */
  .back-link {
    display:inline-flex; align-items:center; gap:6px;
    color:var(--muted); text-decoration:none; font-size:13px;
    margin-bottom:32px; transition:color .15s;
  }
  .back-link:hover { color:var(--text); }

  /* ── Index / hero ── */
  .hero { text-align:center; }
  .big-icon { font-size:56px; margin-bottom:24px; display:block; }
  .hero h1 {
    font-family:'Syne',sans-serif; font-size:38px; font-weight:800;
    letter-spacing:-1px; margin-bottom:12px;
  }
  .hero p { color:var(--muted); font-size:15px; margin-bottom:36px; line-height:1.6; }
  .btn-hero {
    display:inline-flex; align-items:center; gap:10px;
    background:var(--accent); color:#0f0f0f; text-decoration:none;
    font-family:'Syne',sans-serif; font-weight:700; font-size:15px;
    padding:16px 32px; border-radius:var(--r);
    transition:transform .15s, box-shadow .15s;
  }
  .btn-hero:hover { transform:translateY(-2px); box-shadow:0 10px 28px rgba(232,255,71,.25); }
  .features { display:grid; grid-template-columns:repeat(3,1fr); gap:10px; margin-top:36px; }
  .feat {
    background:#111; border:1px solid var(--border);
    border-radius:var(--r); padding:16px 12px; text-align:center;
  }
  .feat .feat-icon { font-size:22px; margin-bottom:8px; }
  .feat p { font-size:12px; color:var(--muted); }
</style>
"""

# ── SVG icons ──
ICON_KEY   = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="7" cy="17" r="3"/><path d="M10 17h10M17 14v6"/><path d="m10 14 7-7"/><path d="M21 3 10 14"/></svg>'
ICON_COPY  = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>'
ICON_CHECK = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>'
ICON_BACK  = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>'
ICON_LOCK  = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'
ICON_SHIELD= '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>'


def base_page(title, body):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  {STYLES}
</head>
<body>
{body}
</body>
</html>"""


# ─────────────────────────────────────────────
# Password logic
# ─────────────────────────────────────────────
def generate_password(length, use_upper, use_numbers, use_symbols):
    pool = list(string.ascii_lowercase)
    guaranteed = [random.choice(string.ascii_lowercase)]

    if use_upper:
        pool += list(string.ascii_uppercase)
        guaranteed.append(random.choice(string.ascii_uppercase))
    if use_numbers:
        pool += list(string.digits)
        guaranteed.append(random.choice(string.digits))
    if use_symbols:
        syms = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        pool += list(syms)
        guaranteed.append(random.choice(syms))

    remaining = length - len(guaranteed)
    pwd = guaranteed + [random.choice(pool) for _ in range(max(remaining, 0))]
    random.shuffle(pwd)
    return "".join(pwd)


def strength_info(length, use_upper, use_numbers, use_symbols):
    score = 0
    if length >= 8:  score += 1
    if length >= 12: score += 1
    if length >= 16: score += 1
    if use_upper:    score += 1
    if use_numbers:  score += 1
    if use_symbols:  score += 1

    if score <= 2: return 1, "Weak",        "#ff5252"
    if score <= 3: return 2, "Fair",        "#ffaa47"
    if score <= 4: return 3, "Good",        "#e8ff47"
    if score == 5: return 4, "Strong",      "#4dff91"
    return            5,    "Very Strong",  "#4dff91"


def strength_bars_html(filled, color):
    return "".join(
        f'<div class="s-bar" style="background:{color if i < filled else "var(--border)"}"></div>'
        for i in range(5)
    )


def option_card(name, emoji, label, checked):
    cls = " checked" if checked else ""
    chk = " checked" if checked else ""
    return f"""
      <label class="option-card{cls}" id="card-{name}">
        <input type="checkbox" name="{name}"{chk}
               onchange="toggleCard(this,'card-{name}')">
        <span class="check-icon">{ICON_CHECK}</span>
        <span class="option-text">{emoji} {label}</span>
      </label>"""


# ─────────────────────────────────────────────
# INDEX
# ─────────────────────────────────────────────
@app.route("/")
def index():
    body = f"""
    <div class="card">
      <div class="hero">
        <span class="big-icon">🔐</span>
        <h1>Password Generator</h1>
        <p>Create strong, secure passwords instantly.<br>
           Customise length, characters &amp; complexity.</p>
        <a href="/generate" class="btn-hero">
          {ICON_LOCK} Generate Password
        </a>
        <div class="features">
          <div class="feat">
            <div class="feat-icon">🔠</div>
            <p>Uppercase &amp; lowercase</p>
          </div>
          <div class="feat">
            <div class="feat-icon">🔢</div>
            <p>Numbers &amp; symbols</p>
          </div>
          <div class="feat">
            <div class="feat-icon">📏</div>
            <p>4 – 30 character length</p>
          </div>
        </div>
      </div>
    </div>"""
    return base_page("Password Generator", body)


# ─────────────────────────────────────────────
# GENERATE
# ─────────────────────────────────────────────
@app.route("/generate", methods=["GET", "POST"])
def generate():
    password    = None
    result_html = ""
    length      = 12
    use_upper   = False
    use_numbers = False
    use_symbols = False

    if request.method == "POST":
        length      = int(request.form.get("length", 12))
        use_upper   = "uppercase" in request.form
        use_numbers = "numbers"   in request.form
        use_symbols = "symbols"   in request.form
        password    = generate_password(length, use_upper, use_numbers, use_symbols)

        filled, label, color = strength_info(length, use_upper, use_numbers, use_symbols)
        bars = strength_bars_html(filled, color)

        result_html = f"""
        <div class="result-box">
          <div class="result-label">{ICON_SHIELD} Generated Password</div>
          <div class="password-text" id="pwd">{password}</div>
          <div class="strength-wrap">
            <div class="strength-label-row">
              <span>Strength</span>
              <span style="color:{color}">{label}</span>
            </div>
            <div class="strength-bars">{bars}</div>
          </div>
          <div class="copy-row">
            <button class="btn-copy" onclick="copyPwd()">{ICON_COPY} Copy</button>
          </div>
        </div>
        <script>
          function copyPwd() {{
            navigator.clipboard.writeText(document.getElementById('pwd').innerText).then(() => {{
              const btn = document.querySelector('.btn-copy');
              btn.innerHTML = `{ICON_CHECK} Copied!`;
              setTimeout(() => btn.innerHTML = `{ICON_COPY} Copy`, 2000);
            }});
          }}
        </script>"""

    body = f"""
    <div class="card">
      <a href="/" class="back-link">{ICON_BACK} Back</a>
      <div class="badge">{ICON_KEY} Password Generator</div>
      <h1>Craft Your<br>Password</h1>
      <p class="subtitle">Adjust the settings and hit Generate.</p>

      <form method="POST">
        <div class="length-row">
          <span class="length-label">Password Length</span>
          <span class="length-value" id="lenDisplay">{length}</span>
        </div>
        <input type="range" name="length" id="lengthSlider"
               min="4" max="30" value="{length}"
               oninput="document.getElementById('lenDisplay').textContent=this.value">

        <span class="options-label">Character Types</span>
        <div class="options-grid">
          {option_card("uppercase", "🔠", "Uppercase",  use_upper)}
          {option_card("numbers",   "🔢", "Numbers",    use_numbers)}
          {option_card("symbols",   "!@#", "Symbols",   use_symbols)}
          <label class="option-card checked disabled">
            <span class="check-icon">{ICON_CHECK}</span>
            <span class="option-text">🔡 Lowercase</span>
          </label>
        </div>

        <button type="submit" class="btn-generate">Generate Password &rarr;</button>
      </form>

      {result_html}
    </div>

    <script>
      function toggleCard(el, cardId) {{
        document.getElementById(cardId).classList.toggle('checked', el.checked);
      }}
    </script>"""

    return base_page("Generate Password", body)


if __name__ == "__main__":
    app.run(debug=True)