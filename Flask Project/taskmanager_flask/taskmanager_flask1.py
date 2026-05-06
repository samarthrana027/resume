import streamlit as st
import requests

API = "http://localhost:5000"

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Task Manager",
    page_icon="✅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Space+Mono&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] { background: #0f172a; }
    [data-testid="stSidebar"] * { color: #e2e8f0 !important; }

    /* ── Task cards ── */
    .task-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: .75rem;
        border-left: 5px solid #6366f1;
        box-shadow: 0 1px 6px rgba(0,0,0,.07);
        transition: transform .15s;
    }
    .task-card:hover { transform: translateY(-2px); }
    .task-card.high   { border-left-color: #ef4444; }
    .task-card.medium { border-left-color: #f59e0b; }
    .task-card.low    { border-left-color: #22c55e; }

    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 999px;
        font-size: .72rem;
        font-weight: 700;
        letter-spacing: .04em;
        text-transform: uppercase;
        margin-right: 6px;
    }
    .badge-pending     { background:#e0e7ff; color:#4338ca; }
    .badge-in_progress { background:#fef3c7; color:#92400e; }
    .badge-completed   { background:#dcfce7; color:#166534; }
    .badge-high        { background:#fee2e2; color:#991b1b; }
    .badge-medium      { background:#fef9c3; color:#713f12; }
    .badge-low         { background:#d1fae5; color:#065f46; }

    /* ── Stat cards ── */
    .stat-card {
        background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%);
        color: #fff !important;
        border-radius: 12px;
        padding: 1.1rem 1.25rem;
        text-align: center;
        margin-bottom: .5rem;
    }
    .stat-card .big { font-size: 2.2rem; font-weight: 700; }
    .stat-card .lbl { font-size: .8rem; opacity: .85; }

    /* ── Section heading ── */
    .section-head {
        font-size: 1.35rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
        padding-bottom: .4rem;
        border-bottom: 2px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)


# ─── API helpers ──────────────────────────────────────────────────────────────
def api_get(path, params=None):
    try:
        r = requests.get(f"{API}{path}", params=params, timeout=4)
        return r.json() if r.ok else {}
    except Exception:
        return {}

def api_post(path, payload):
    try:
        r = requests.post(f"{API}{path}", json=payload, timeout=4)
        return r.json(), r.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def api_put(path, payload):
    try:
        r = requests.put(f"{API}{path}", json=payload, timeout=4)
        return r.json(), r.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def api_delete(path):
    try:
        r = requests.delete(f"{API}{path}", timeout=4)
        return r.json(), r.status_code
    except Exception as e:
        return {"error": str(e)}, 500


# ─── Sidebar nav ──────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✅ Task Manager")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        ["📋 All Tasks", "➕ Add Task", "✏️ Edit / Delete", "📊 Dashboard"],
        label_visibility="collapsed",
    )
    st.markdown("---")

    # Quick filters
    st.markdown("### Filters")
    filter_status   = st.selectbox("Status",   ["All", "pending", "in_progress", "completed"])
    filter_priority = st.selectbox("Priority", ["All", "high", "medium", "low"])
    st.markdown("---")
    st.caption("Flask API → http://localhost:5000")


# ─── Helper: render a task card ───────────────────────────────────────────────
def render_task_card(task):
    p  = task.get("priority", "medium")
    s  = task.get("status", "pending")
    dd = f"📅 {task['due_date']}" if task.get("due_date") else ""
    st.markdown(f"""
    <div class="task-card {p}">
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <strong style="font-size:1.05rem">{task['title']}</strong>
            <span>
                <span class="badge badge-{s}">{s.replace('_',' ')}</span>
                <span class="badge badge-{p}">{p}</span>
            </span>
        </div>
        <div style="color:#64748b;margin-top:.3rem;font-size:.9rem">{task.get('description','')}</div>
        <div style="color:#94a3b8;margin-top:.4rem;font-size:.78rem">{dd} &nbsp;·&nbsp; ID #{task['id']} &nbsp;·&nbsp; Created {task['created_at']}</div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: All Tasks
# ═══════════════════════════════════════════════════════════════════════════════
if page == "📋 All Tasks":
    st.markdown('<div class="section-head">📋 All Tasks</div>', unsafe_allow_html=True)

    params = {}
    if filter_status   != "All": params["status"]   = filter_status
    if filter_priority != "All": params["priority"] = filter_priority

    data  = api_get("/tasks", params)
    tasks = data.get("tasks", [])

    st.caption(f"{len(tasks)} task(s) found")
    if not tasks:
        st.info("No tasks yet. Use **➕ Add Task** to create one.")
    else:
        for task in tasks:
            render_task_card(task)


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Add Task
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "➕ Add Task":
    st.markdown('<div class="section-head">➕ Add New Task</div>', unsafe_allow_html=True)

    with st.form("add_task_form", clear_on_submit=True):
        title       = st.text_input("Task Title *", placeholder="e.g. Write project proposal")
        description = st.text_area("Description", placeholder="Details about the task…")
        col1, col2, col3 = st.columns(3)
        with col1:
            status   = st.selectbox("Status",   ["pending", "in_progress", "completed"])
        with col2:
            priority = st.selectbox("Priority", ["medium", "high", "low"])
        with col3:
            due_date = st.date_input("Due Date", value=None)

        submitted = st.form_submit_button("🚀 Create Task", use_container_width=True)

    if submitted:
        if not title.strip():
            st.error("Title is required.")
        else:
            payload = {
                "title":       title,
                "description": description,
                "status":      status,
                "priority":    priority,
                "due_date":    str(due_date) if due_date else "",
            }
            res, code = api_post("/tasks", payload)
            if code == 201:
                st.success(f"✅ Task **{title}** created! (ID #{res['task']['id']})")
            else:
                st.error(res.get("error", "Failed to create task."))


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Edit / Delete
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "✏️ Edit / Delete":
    st.markdown('<div class="section-head">✏️ Edit or Delete a Task</div>', unsafe_allow_html=True)

    data  = api_get("/tasks")
    tasks = data.get("tasks", [])

    if not tasks:
        st.info("No tasks found. Add some first.")
    else:
        options = {f"#{t['id']} — {t['title']}": t["id"] for t in tasks}
        choice  = st.selectbox("Select a task", list(options.keys()))
        task_id = options[choice]
        task    = api_get(f"/tasks/{task_id}")

        if task:
            st.markdown("---")
            tab_edit, tab_delete = st.tabs(["✏️ Edit", "🗑️ Delete"])

            with tab_edit:
                with st.form("edit_form"):
                    new_title = st.text_input("Title", value=task["title"])
                    new_desc  = st.text_area("Description", value=task.get("description", ""))
                    col1, col2 = st.columns(2)
                    with col1:
                        new_status = st.selectbox(
                            "Status",
                            ["pending", "in_progress", "completed"],
                            index=["pending", "in_progress", "completed"].index(task["status"]),
                        )
                    with col2:
                        new_priority = st.selectbox(
                            "Priority",
                            ["low", "medium", "high"],
                            index=["low", "medium", "high"].index(task["priority"]),
                        )
                    new_due = st.text_input("Due Date (YYYY-MM-DD)", value=task.get("due_date", ""))
                    save = st.form_submit_button("💾 Save Changes", use_container_width=True)

                if save:
                    payload = {
                        "title": new_title, "description": new_desc,
                        "status": new_status, "priority": new_priority,
                        "due_date": new_due,
                    }
                    res, code = api_put(f"/tasks/{task_id}", payload)
                    if code == 200:
                        st.success("✅ Task updated successfully!")
                    else:
                        st.error(res.get("error", "Update failed."))

            with tab_delete:
                st.warning(f"You are about to delete **{task['title']}**. This cannot be undone.")
                if st.button("🗑️ Confirm Delete", use_container_width=True):
                    res, code = api_delete(f"/tasks/{task_id}")
                    if code == 200:
                        st.success("✅ Task deleted.")
                        st.rerun()
                    else:
                        st.error(res.get("error", "Delete failed."))


# ═══════════════════════════════════════════════════════════════════════════════
# PAGE: Dashboard
# ═══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Dashboard":
    st.markdown('<div class="section-head">📊 Dashboard</div>', unsafe_allow_html=True)

    stats = api_get("/tasks/stats")

    if not stats:
        st.warning("Could not load stats — is the Flask API running?")
    else:
        # Stat row
        c1, c2, c3, c4 = st.columns(4)
        for col, label, key, color in [
            (c1, "Total",       "total",       "#6366f1"),
            (c2, "Pending",     "pending",     "#f59e0b"),
            (c3, "In Progress", "in_progress", "#3b82f6"),
            (c4, "Completed",   "completed",   "#22c55e"),
        ]:
            col.markdown(f"""
            <div class="stat-card" style="background:linear-gradient(135deg,{color}cc,{color})">
                <div class="big">{stats.get(key, 0)}</div>
                <div class="lbl">{label}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("---")

        # Priority breakdown
        st.markdown("#### Priority Breakdown")
        p1, p2, p3 = st.columns(3)
        for col, label, key, color in [
            (p1, "🔴 High",   "high",   "#fee2e2"),
            (p2, "🟡 Medium", "medium", "#fef9c3"),
            (p3, "🟢 Low",    "low",    "#d1fae5"),
        ]:
            col.markdown(f"""
            <div style="background:{color};border-radius:10px;padding:.8rem;text-align:center;">
                <div style="font-size:1.8rem;font-weight:700">{stats.get(key,0)}</div>
                <div style="font-size:.8rem;font-weight:500">{label}</div>
            </div>""", unsafe_allow_html=True)

        # Recent tasks list
        st.markdown("---")
        st.markdown("#### Recent Tasks")
        data  = api_get("/tasks")
        tasks = data.get("tasks", [])
        if tasks:
            for t in tasks[-5:][::-1]:
                render_task_card(t)
        else:
            st.info("No tasks yet.")
