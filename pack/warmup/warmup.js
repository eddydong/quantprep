(function pythonWarmup() {
  const root = document.getElementById("warmup-lab");
  if (!root || typeof WARMUP === "undefined") return;

  const STORE = (typeof WARMUP_STORE === "string" && WARMUP_STORE) || "quantprep-warmup";
  const sessions = WARMUP;
  const n = sessions.length;
  const ed = document.getElementById("wu-ed");
  const out = document.getElementById("wu-out");
  const status = document.getElementById("wu-status");
  const track = document.getElementById("wu-track");
  const progress = document.getElementById("wu-progress");
  const kicker = document.getElementById("wu-kicker");
  const title = document.getElementById("wu-title");
  const goal = document.getElementById("wu-goal");
  const lesson = document.getElementById("wu-lesson");
  const runBtn = document.getElementById("wu-run");
  const hintBtn = document.getElementById("wu-hint");
  const resetBtn = document.getElementById("wu-reset");
  const nextBtn = document.getElementById("wu-next");

  function blank() {
    return {
      i: 0,
      code: sessions.map(s => s.starter),
      done: sessions.map(() => false)
    };
  }
  function load() {
    try {
      const raw = localStorage.getItem(STORE);
      if (!raw) return blank();
      const st = JSON.parse(raw);
      const code = sessions.map((s, i) =>
        typeof (st.code && st.code[i]) === "string" ? st.code[i] : s.starter
      );
      const done = sessions.map((_, i) => Boolean(st.done && st.done[i]));
      const i = Math.min(Math.max(0, st.i | 0), n - 1);
      return { i, code, done };
    } catch {
      return blank();
    }
  }
  const state = load();
  let idx = state.i;

  function persist() {
    state.i = idx;
    state.code[idx] = ed.value;
    try {
      localStorage.setItem(STORE, JSON.stringify(state));
    } catch (_) {}
  }
  function setStatus(t) {
    status.textContent = t || "";
  }
  function showOut(text, kind) {
    out.hidden = false;
    out.textContent = text;
    out.className = "lab-out" + (kind ? " " + kind : "");
  }
  function pad(i) {
    return String(i + 1).padStart(2, "0");
  }
  function paintTrack() {
    track.querySelectorAll("button").forEach((btn, i) => {
      btn.classList.toggle("on", i === idx);
      btn.classList.toggle("done", Boolean(state.done[i]));
    });
    const green = state.done.filter(Boolean).length;
    progress.textContent = green + " / " + n + " sessions green";
  }
  function render() {
    const s = sessions[idx];
    kicker.textContent = "Session " + pad(idx) + " of " + pad(n - 1);
    title.textContent = s.title;
    goal.textContent = s.goal;
    lesson.innerHTML = s.lesson;
    ed.value = state.code[idx] || s.starter;
    ed.readOnly = false;
    nextBtn.disabled = idx >= n - 1;
    paintTrack();
    out.hidden = true;
    out.textContent = "";
    setStatus(state.done[idx] ? "This session already passed." : "");
  }

  sessions.forEach((s, i) => {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.textContent = pad(i);
    btn.title = s.title;
    btn.addEventListener("click", () => {
      persist();
      idx = i;
      render();
    });
    const li = document.createElement("li");
    li.append(btn);
    track.append(li);
  });

  ed.addEventListener("input", persist);
  ed.addEventListener("keydown", e => {
    if (e.key !== "Tab" || ed.readOnly) return;
    e.preventDefault();
    const s = ed.selectionStart;
    const end = ed.selectionEnd;
    ed.value = ed.value.slice(0, s) + "    " + ed.value.slice(end);
    ed.selectionStart = ed.selectionEnd = s + 4;
    persist();
  });

  resetBtn.addEventListener("click", () => {
    ed.value = sessions[idx].starter;
    persist();
    setStatus("Stub restored.");
  });

  hintBtn.addEventListener("click", () => {
    if (!confirm("Show this session’s answer? Try the checks first.")) return;
    ed.value = sessions[idx].solution;
    persist();
    setStatus("Answer in the editor. Run checks to confirm.");
  });

  nextBtn.addEventListener("click", () => {
    if (idx >= n - 1) return;
    persist();
    idx += 1;
    render();
  });

  const RUNNER = String.raw`
import json, sys, traceback

for name in ("wu_student", "wu_checks"):
    sys.modules.pop(name, None)

try:
    import wu_student
    import wu_checks
    _wu_out = json.dumps({"rows": list(wu_checks.run(wu_student))})
except Exception:
    _wu_out = json.dumps({"rows": [{"name": "session", "ok": "fail", "msg": traceback.format_exc()}]})
_wu_out
`;

  runBtn.addEventListener("click", async () => {
    persist();
    runBtn.disabled = true;
    try {
      if (typeof window.ensureQuantPy !== "function") {
        throw new Error("Python runtime is not on this page.");
      }
      const py = await window.ensureQuantPy(setStatus);
      py.FS.writeFile("wu_student.py", ed.value);
      py.FS.writeFile("wu_checks.py", sessions[idx].tests);
      setStatus("Running checks…");
      const raw = py.runPython(RUNNER);
      const data = JSON.parse(typeof raw === "string" ? raw : raw.toString());
      const lines = [];
      let pass = 0, fail = 0;
      for (const row of data.rows || []) {
        if (row.ok === "pass") {
          pass += 1;
          lines.push("ok   " + row.name);
        } else {
          fail += 1;
          lines.push("FAIL " + row.name);
          if (row.msg) lines.push(row.msg.replace(/\s+$/, ""));
        }
      }
      const summary = pass + " passed, " + fail + " failed";
      setStatus(summary);
      showOut(lines.join("\n\n") || "No checks ran.", fail ? "fail" : "pass");
      if (fail === 0 && pass > 0) {
        state.done[idx] = true;
        persist();
        paintTrack();
      }
    } catch (err) {
      setStatus("Could not run.");
      showOut(String(err.message || err), "fail");
    } finally {
      runBtn.disabled = false;
    }
  });

  render();
})();
