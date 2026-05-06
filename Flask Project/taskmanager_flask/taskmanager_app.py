from flask import Flask, request, redirect, url_for
from datetime import datetime, date

app = Flask(__name__)

# ---------- In-memory task store ----------
tasks = []
next_id = 1

# ---------- Helpers ----------
PRIORITY_META = {
    "high":   {"color": "#ff5252", "dim": "rgba(255,82,82,0.12)",  "label": "High"},
    "medium": {"color": "#ffaa47", "dim": "rgba(255,170,71,0.12)", "label": "Medium"},
    "low":    {"color": "#4dff91", "dim": "rgba(77,255,145,0.12)", "label": "Low"},
}

def fmt_date(d_str):
    """Return (readable_string, is_overdue)."""
    if not d_str:
        return "", False
    try:
        d = datetime.strptime(d_str, "%Y-%m-%d").date()
        return d.strftime("%d %b %Y"), d < date.today()
    except ValueError:
        return d_str, False

# ---------- Shared CSS ----------
STYLES = """
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root{
    --bg:#0f0f0f;--surface:#1a1a1a;--surface2:#242424;
    --border:#2e2e2e;--accent:#e8ff47;--accent-dim:rgba(232,255,71,0.12);
    --text:#f0f0f0;--muted:#888;--danger:#ff5252;
    --danger-dim:rgba(255,82,82,0.1);--warn:#ffaa47;
    --warn-dim:rgba(255,170,71,0.12);--green:#4dff91;
    --green-dim:rgba(77,255,145,0.12);--r:12px;
  }
  *{margin:0;padding:0;box-sizing:border-box;}
  body{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;min-height:100vh;padding:48px 24px;}
  .container{max-width:780px;margin:0 auto;animation:fadeUp .5s ease both;}
  @keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}

  .header{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:32px;padding-bottom:24px;border-bottom:1px solid var(--border);}
  .header h1{font-family:'Syne',sans-serif;font-size:42px;font-weight:800;letter-spacing:-1px;line-height:1;}
  .header p{color:var(--muted);font-size:14px;margin-top:6px;}

  .filter-bar{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px;}
  .filter-btn{display:inline-flex;align-items:center;gap:6px;background:var(--surface);border:1px solid var(--border);color:var(--muted);font-size:12px;font-family:'Syne',sans-serif;font-weight:600;letter-spacing:.04em;text-transform:uppercase;padding:6px 14px;border-radius:100px;cursor:pointer;text-decoration:none;transition:all .15s;}
  .filter-btn:hover,.filter-btn.active{background:var(--accent-dim);color:var(--accent);border-color:rgba(232,255,71,.3);}
  .filter-dot{width:6px;height:6px;border-radius:50%;}

  .stats-bar{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:28px;}
  .chip{background:var(--surface);border:1px solid var(--border);border-radius:8px;padding:8px 16px;font-size:13px;color:var(--muted);}
  .chip span{color:var(--text);font-weight:600;font-family:'Syne',sans-serif;}

  .btn{display:inline-flex;align-items:center;gap:8px;text-decoration:none;font-family:'Syne',sans-serif;font-weight:700;font-size:14px;padding:12px 22px;border-radius:var(--r);transition:transform .15s,box-shadow .15s;white-space:nowrap;cursor:pointer;border:none;}
  .btn-accent{background:var(--accent);color:#0f0f0f;}
  .btn-accent:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(232,255,71,.25);}
  .btn-sm{display:inline-flex;align-items:center;gap:5px;text-decoration:none;font-size:12px;font-weight:500;padding:6px 12px;border-radius:8px;transition:background .15s,color .15s;border:1px solid var(--border);color:var(--muted);background:transparent;cursor:pointer;white-space:nowrap;}
  .btn-edit:hover{background:var(--accent-dim);color:var(--accent);border-color:rgba(232,255,71,.3);}
  .btn-delete:hover{background:var(--danger-dim);color:var(--danger);border-color:rgba(255,82,82,.3);}
  .btn-toggle:hover{background:var(--green-dim);color:var(--green);border-color:rgba(77,255,145,.4);}
  .btn-reopen:hover{background:var(--warn-dim);color:var(--warn);border-color:rgba(255,170,71,.4);}

  .task-list{display:flex;flex-direction:column;gap:10px;}
  .task-item{display:flex;align-items:center;justify-content:space-between;background:var(--surface);border:1px solid var(--border);border-radius:var(--r);padding:16px 20px;transition:border-color .2s,background .2s;animation:fadeUp .4s ease both;gap:12px;}
  .task-item:hover{border-color:#444;background:var(--surface2);}
  .task-item.done{opacity:.55;}
  .task-item.done .task-title{text-decoration:line-through;color:var(--muted);}
  .task-left{display:flex;align-items:center;gap:12px;min-width:0;flex:1;}
  .task-index{font-family:'Syne',sans-serif;font-size:11px;font-weight:700;color:var(--muted);width:22px;flex-shrink:0;}
  .priority-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0;}
  .task-info{min-width:0;}
  .task-title{font-size:15px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:block;}
  .task-meta{display:flex;align-items:center;gap:8px;margin-top:4px;flex-wrap:wrap;}
  .meta-tag{font-size:11px;font-family:'Syne',sans-serif;font-weight:600;letter-spacing:.05em;text-transform:uppercase;padding:2px 8px;border-radius:100px;}
  .status-pending{background:var(--warn-dim);color:var(--warn);}
  .status-completed{background:var(--green-dim);color:var(--green);}
  .due-date{font-size:11px;color:var(--muted);display:inline-flex;align-items:center;gap:4px;}
  .due-date.overdue{color:var(--danger);}
  .task-actions{display:flex;align-items:center;gap:6px;flex-shrink:0;}

  .empty{text-align:center;padding:80px 20px;border:1px dashed var(--border);border-radius:var(--r);}
  .empty .icon{font-size:48px;margin-bottom:16px;}
  .empty h2{font-family:'Syne',sans-serif;font-size:20px;font-weight:700;margin-bottom:8px;}
  .empty p{color:var(--muted);font-size:14px;}

  body.card-page{display:flex;align-items:center;justify-content:center;padding:24px;}
  .card{background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:48px;width:100%;max-width:540px;animation:fadeUp .45s ease both;}
  .back-link{display:inline-flex;align-items:center;gap:6px;color:var(--muted);text-decoration:none;font-size:13px;margin-bottom:32px;transition:color .15s;}
  .back-link:hover{color:var(--text);}
  .badge{display:inline-block;font-family:'Syne',sans-serif;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:5px 12px;border-radius:100px;margin-bottom:16px;}
  .badge-green{background:var(--accent-dim);color:var(--accent);}
  .badge-warn{background:var(--warn-dim);color:var(--warn);}
  .card h1{font-family:'Syne',sans-serif;font-size:32px;font-weight:800;letter-spacing:-.5px;margin-bottom:8px;}
  .card .subtitle{color:var(--muted);font-size:14px;margin-bottom:36px;}

  .form-row{display:grid;grid-template-columns:1fr 1fr;gap:16px;}
  .form-group{margin-bottom:20px;}
  label{display:block;font-size:12px;font-weight:600;font-family:'Syne',sans-serif;letter-spacing:.06em;text-transform:uppercase;color:var(--muted);margin-bottom:8px;}
  input[type=text],input[type=date],select{width:100%;background:#111;border:1.5px solid var(--border);border-radius:var(--r);color:var(--text);font-family:'DM Sans',sans-serif;font-size:15px;padding:14px 16px;outline:none;transition:border-color .2s,box-shadow .2s;-webkit-appearance:none;appearance:none;}
  input[type=text]::placeholder{color:#555;}
  input[type=date]::-webkit-calendar-picker-indicator{filter:invert(.5);cursor:pointer;}
  select option{background:#1a1a1a;}
  .focus-green:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(232,255,71,.1);}
  .focus-warn:focus{border-color:var(--warn);box-shadow:0 0 0 3px rgba(255,170,71,.1);}
  .btn-full{width:100%;border:none;border-radius:var(--r);font-family:'Syne',sans-serif;font-size:15px;font-weight:700;padding:16px;cursor:pointer;transition:transform .15s,box-shadow .15s;margin-top:8px;}
  .btn-full-green{background:var(--accent);color:#0f0f0f;}
  .btn-full-green:hover{transform:translateY(-2px);box-shadow:0 10px 28px rgba(232,255,71,.25);}
  .btn-full-warn{background:var(--warn);color:#0f0f0f;}
  .btn-full-warn:hover{transform:translateY(-2px);box-shadow:0 10px 28px rgba(255,170,71,.25);}
  .hint{margin-top:20px;text-align:center;font-size:12px;color:var(--muted);}
  kbd{background:#222;border:1px solid #333;padding:2px 6px;border-radius:4px;font-size:11px;}
  .footer{margin-top:48px;padding-top:20px;border-top:1px solid var(--border);text-align:center;font-size:12px;color:var(--muted);}
</style>
"""

ICON_PLUS   = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>'
ICON_EDIT   = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>'
ICON_DEL    = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4h6v2"/></svg>'
ICON_BACK   = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>'
ICON_CHECK  = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"/></svg>'
ICON_REOPEN = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.67"/></svg>'
ICON_CAL    = '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'


def base_page(title, body, body_class=""):
    cls = f' class="{body_class}"' if body_class else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  {STYLES}
</head>
<body{cls}>
{body}
</body>
</html>"""


def build_task_row(i, task, active_filter):
    p       = task.get("priority", "medium")
    status  = task.get("status", "pending")
    done    = status == "completed"
    p_meta  = PRIORITY_META[p]

    date_str, overdue = fmt_date(task.get("due_date", ""))
    due_html = ""
    if date_str:
        is_overdue = overdue and not done
        cls    = "due-date overdue" if is_overdue else "due-date"
        prefix = "⚠ Due" if is_overdue else "Due"
        due_html = f'<span class="{cls}">{ICON_CAL} {prefix} {date_str}</span>'

    p_tag = (f'<span class="meta-tag" '
             f'style="background:{p_meta["dim"]};color:{p_meta["color"]}">'
             f'{p_meta["label"]}</span>')
    s_tag = (f'<span class="meta-tag status-completed">&#10003; Done</span>'
             if done else
             f'<span class="meta-tag status-pending">Pending</span>')

    toggle_btn = (
        f'<a href="/toggle/{task["id"]}?filter={active_filter}" '
        f'class="btn-sm btn-reopen">{ICON_REOPEN} Reopen</a>'
        if done else
        f'<a href="/toggle/{task["id"]}?filter={active_filter}" '
        f'class="btn-sm btn-toggle">{ICON_CHECK} Done</a>'
    )

    done_cls = " done" if done else ""
    delay    = i * 0.05

    return f"""
    <div class="task-item{done_cls}" style="animation-delay:{delay}s">
      <div class="task-left">
        <span class="task-index">{str(i+1).zfill(2)}</span>
        <span class="priority-dot" style="background:{p_meta['color']};flex-shrink:0"
              title="Priority: {p_meta['label']}"></span>
        <div class="task-info" style="min-width:0">
          <span class="task-title">{task['title']}</span>
          <div class="task-meta">
            {p_tag}
            {s_tag}
            {due_html}
          </div>
        </div>
      </div>
      <div class="task-actions">
        {toggle_btn}
        <a href="/edit/{task['id']}" class="btn-sm btn-edit">{ICON_EDIT} Edit</a>
        <a href="/delete/{task['id']}" class="btn-sm btn-delete"
           onclick="return confirm('Delete this task?')">{ICON_DEL} Delete</a>
      </div>
    </div>"""


# ─────────────────────────────────────────────
# INDEX
# ─────────────────────────────────────────────
@app.route("/")
def index():
    f = request.args.get("filter", "all")

    filter_map = {
        "pending":   lambda t: t.get("status") == "pending",
        "completed": lambda t: t.get("status") == "completed",
        "high":      lambda t: t.get("priority") == "high",
        "medium":    lambda t: t.get("priority") == "medium",
        "low":       lambda t: t.get("priority") == "low",
    }
    filtered = [t for t in tasks if filter_map[f](t)] if f in filter_map else tasks

    total     = len(tasks)
    pending   = sum(1 for t in tasks if t.get("status") == "pending")
    completed = sum(1 for t in tasks if t.get("status") == "completed")
    overdue   = sum(1 for t in tasks
                    if t.get("due_date") and t.get("status") == "pending"
                    and datetime.strptime(t["due_date"], "%Y-%m-%d").date() < date.today())

    def fc(key): return "active" if f == key else ""

    filter_html = f"""
    <div class="filter-bar">
      <a href="/?filter=all"       class="filter-btn {fc('all')}">All</a>
      <a href="/?filter=pending"   class="filter-btn {fc('pending')}">
        <span class="filter-dot" style="background:var(--warn)"></span>Pending
      </a>
      <a href="/?filter=completed" class="filter-btn {fc('completed')}">
        <span class="filter-dot" style="background:var(--green)"></span>Completed
      </a>
      <a href="/?filter=high"   class="filter-btn {fc('high')}">
        <span class="filter-dot" style="background:#ff5252"></span>High
      </a>
      <a href="/?filter=medium" class="filter-btn {fc('medium')}">
        <span class="filter-dot" style="background:#ffaa47"></span>Medium
      </a>
      <a href="/?filter=low"    class="filter-btn {fc('low')}">
        <span class="filter-dot" style="background:#4dff91"></span>Low
      </a>
    </div>"""

    overdue_chip = (f'<div class="chip"><span style="color:var(--danger)">{overdue}</span> overdue</div>'
                    if overdue else "")
    stats_html = f"""
    <div class="stats-bar">
      <div class="chip"><span>{total}</span> total</div>
      <div class="chip"><span style="color:var(--warn)">{pending}</span> pending</div>
      <div class="chip"><span style="color:var(--green)">{completed}</span> done</div>
      {overdue_chip}
    </div>"""

    if filtered:
        rows    = "".join(build_task_row(i, t, f) for i, t in enumerate(filtered))
        content = f'<div class="task-list">{rows}</div>'
    else:
        content = """
        <div class="empty">
          <div class="icon">📋</div>
          <h2>No tasks here</h2>
          <p>Try a different filter or add a new task.</p>
        </div>"""

    body = f"""
    <div class="container">
      <div class="header">
        <div>
          <h1>Tasks</h1>
          <p>Stay focused. Get things done.</p>
        </div>
        <a href="/add" class="btn btn-accent">{ICON_PLUS} New Task</a>
      </div>
      {filter_html}
      {stats_html}
      {content}
      <div class="footer">Task Manager &mdash; Built with Flask</div>
    </div>"""

    return base_page("Task Manager", body)


# ─────────────────────────────────────────────
# TOGGLE STATUS (one-click from list)
# ─────────────────────────────────────────────
@app.route("/toggle/<int:task_id>")
def toggle(task_id):
    f    = request.args.get("filter", "all")
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        task["status"] = "completed" if task.get("status") == "pending" else "pending"
    return redirect(url_for("index", filter=f))


# ─────────────────────────────────────────────
# ADD
# ─────────────────────────────────────────────
@app.route("/add", methods=["GET", "POST"])
def add():
    global next_id
    error = ""
    if request.method == "POST":
        title    = request.form.get("title", "").strip()
        priority = request.form.get("priority", "medium")
        due_date = request.form.get("due_date", "").strip()
        if title:
            tasks.append({
                "id":       next_id,
                "title":    title,
                "status":   "pending",
                "priority": priority,
                "due_date": due_date,
            })
            next_id += 1
            return redirect(url_for("index"))
        error = "Task title is required."

    err_html = (f'<p style="color:var(--danger);font-size:13px;margin-bottom:12px">&#9888; {error}</p>'
                if error else "")

    body = f"""
    <div class="card">
      <a href="/" class="back-link">{ICON_BACK} Back to Tasks</a>
      <div class="badge badge-green">New Task</div>
      <h1>What's next?</h1>
      <p class="subtitle">Add a task with priority and due date.</p>
      {err_html}
      <form method="POST">
        <div class="form-group">
          <label for="title">Task Title</label>
          <input class="focus-green" type="text" id="title" name="title"
                 placeholder="e.g. Buy groceries, Call dentist…" required autofocus>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="priority">Priority</label>
            <select class="focus-green" id="priority" name="priority">
              <option value="high">🔴 High</option>
              <option value="medium" selected>🟠 Medium</option>
              <option value="low">🟢 Low</option>
            </select>
          </div>
          <div class="form-group">
            <label for="due_date">Due Date</label>
            <input class="focus-green" type="date" id="due_date" name="due_date">
          </div>
        </div>
        <button type="submit" class="btn-full btn-full-green">Add Task &rarr;</button>
      </form>
    </div>"""

    return base_page("Add Task", body, body_class="card-page")


# ─────────────────────────────────────────────
# EDIT
# ─────────────────────────────────────────────
@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit(task_id):
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task is None:
        return redirect(url_for("index"))

    if request.method == "POST":
        title    = request.form.get("title", "").strip()
        priority = request.form.get("priority", "medium")
        status   = request.form.get("status", "pending")
        due_date = request.form.get("due_date", "").strip()
        if title:
            task.update({"title": title, "priority": priority,
                         "status": status, "due_date": due_date})
        return redirect(url_for("index"))

    p   = task.get("priority", "medium")
    s   = task.get("status",   "pending")
    due = task.get("due_date", "")
    ttl = task.get("title",    "")

    def sp(v): return "selected" if p == v else ""
    def ss(v): return "selected" if s == v else ""

    body = f"""
    <div class="card">
      <a href="/" class="back-link">{ICON_BACK} Back to Tasks</a>
      <div class="badge badge-warn">Editing</div>
      <h1>Update Task</h1>
      <p class="subtitle">Modify details for this task.</p>
      <form method="POST">
        <div class="form-group">
          <label for="title">Task Title</label>
          <input class="focus-warn" type="text" id="title" name="title"
                 value="{ttl}" required autofocus>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label for="priority">Priority</label>
            <select class="focus-warn" id="priority" name="priority">
              <option value="high"   {sp('high')}>🔴 High</option>
              <option value="medium" {sp('medium')}>🟠 Medium</option>
              <option value="low"    {sp('low')}>🟢 Low</option>
            </select>
          </div>
          <div class="form-group">
            <label for="status">Status</label>
            <select class="focus-warn" id="status" name="status">
              <option value="pending"   {ss('pending')}>⏳ Pending</option>
              <option value="completed" {ss('completed')}>&#10003; Completed</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label for="due_date">Due Date</label>
          <input class="focus-warn" type="date" id="due_date" name="due_date" value="{due}">
        </div>
        <button type="submit" class="btn-full btn-full-warn">Save Changes &rarr;</button>
      </form>
      <p class="hint">Press <kbd>Esc</kbd> to discard changes.</p>
    </div>
    <script>
      document.addEventListener('keydown', e => {{
        if (e.key === 'Escape') window.location.href = '/';
      }});
    </script>"""

    return base_page("Edit Task", body, body_class="card-page")


# ─────────────────────────────────────────────
# DELETE
# ─────────────────────────────────────────────
@app.route("/delete/<int:task_id>")
def delete(task_id):
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)