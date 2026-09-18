(function codingLab() {
  const host = document.getElementById("lab-ed");
  const out = document.getElementById("lab-out");
  const status = document.getElementById("lab-status");
  const runBtn = document.getElementById("lab-run");
  const resetBtn = document.getElementById("lab-reset");
  if (!host || typeof CODING === "undefined" || !window.mountQuantEditor) return;

  const STORE = (typeof CODING_STORE === "string" && CODING_STORE) || "quantprep-candidate";
  let tab = "candidate";
  let revealed = false;
  let editor = null;

  function stub() {
    return CODING.candidate;
  }
  function saved() {
    try {
      return localStorage.getItem(STORE);
    } catch {
      return null;
    }
  }
  function persist() {
    if (tab !== "candidate" || !editor) return;
    try {
      localStorage.setItem(STORE, editor.get());
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
  function showTab(next) {
    if (next === "solutions" && !revealed) {
      if (!confirm("Show the answer key? Sit the mock in the editor first.")) return;
      revealed = true;
    }
    if (tab === "candidate") persist();
    tab = next;
    document.querySelectorAll("[data-lab-tab]").forEach(b => b.classList.toggle("on", b.dataset.labTab === tab));
    if (!editor) return;
    if (tab === "candidate") {
      editor.set(saved() || stub());
      editor.setReadOnly(false);
    } else if (tab === "broken") {
      editor.set(CODING.broken);
      editor.setReadOnly(true);
    } else {
      editor.set(CODING.solutions);
      editor.setReadOnly(true);
    }
    editor.refresh();
  }

  document.querySelectorAll("[data-lab-tab]").forEach(btn => {
    btn.addEventListener("click", () => showTab(btn.dataset.labTab));
  });

  resetBtn.addEventListener("click", () => {
    if (tab !== "candidate") showTab("candidate");
    if (!editor) return;
    editor.set(stub());
    persist();
    setStatus("Stub restored.");
  });

  async function ensurePy() {
    if (typeof window.ensureQuantPy !== "function") {
      throw new Error("Python runtime is not on this page.");
    }
    return window.ensureQuantPy(setStatus);
  }

  window.primeCodingLab = function primeCodingLab() {
    if (window.primeQuantPy) window.primeQuantPy(setStatus);
    if (editor) editor.refresh();
  };

  const RUNNER = String.raw`
import json, sys, unittest, traceback

for name in ("candidate", "solutions", "broken_backtest", "test_coding"):
    sys.modules.pop(name, None)

class JsonResult(unittest.TestResult):
    def __init__(self):
        super().__init__()
        self.rows = []
    def addSuccess(self, test):
        super().addSuccess(test)
        self.rows.append({"name": test._testMethodName, "ok": "pass"})
    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.rows.append({"name": test._testMethodName, "ok": "skip", "msg": reason})
    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.rows.append({"name": test._testMethodName, "ok": "fail", "msg": self._exc_info_to_string(err, test)})
    def addError(self, test, err):
        super().addError(test, err)
        self.rows.append({"name": test._testMethodName, "ok": "fail", "msg": self._exc_info_to_string(err, test)})

try:
    import test_coding
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_coding)
    result = JsonResult()
    suite.run(result)
    _lab_out = json.dumps({
        "rows": result.rows,
        "errors": len(result.errors) + len(result.failures),
        "skips": len(result.skipped),
        "passes": result.testsRun - len(result.skipped) - len(result.errors) - len(result.failures),
    })
except Exception:
    _lab_out = json.dumps({"rows": [{"name": "candidate.py", "ok": "fail", "msg": traceback.format_exc()}]})
_lab_out
`;

  runBtn.addEventListener("click", async () => {
    if (tab === "candidate") persist();
    const code = tab === "candidate" && editor ? editor.get() : (saved() || stub());
    runBtn.disabled = true;
    try {
      const py = await ensurePy();
      py.FS.writeFile("candidate.py", code);
      py.FS.writeFile("solutions.py", CODING.solutions);
      py.FS.writeFile("broken_backtest.py", CODING.broken);
      py.FS.writeFile("test_coding.py", CODING.tests);
      setStatus("Running tests…");
      const raw = py.runPython(RUNNER);
      const data = JSON.parse(typeof raw === "string" ? raw : raw.toString());
      const lines = [];
      let pass = 0, skip = 0, fail = 0;
      for (const row of data.rows) {
        if (row.ok === "pass") {
          pass += 1;
          lines.push("ok   " + row.name);
        } else if (row.ok === "skip") {
          skip += 1;
          lines.push("skip " + row.name + " — " + (row.msg || "not implemented"));
        } else {
          fail += 1;
          lines.push("FAIL " + row.name);
          if (row.msg) lines.push(row.msg.replace(/\s+$/, ""));
        }
      }
      const summary = pass + " passed, " + fail + " failed, " + skip + " skipped";
      setStatus(summary);
      showOut(lines.join("\n\n"), fail ? "fail" : skip && !pass ? "skip" : "pass");
    } catch (err) {
      setStatus("Could not run.");
      showOut(String(err.message || err), "fail");
    } finally {
      runBtn.disabled = false;
    }
  });

  host.value = saved() || stub();
  window.mountQuantEditor(host, { height: "420px", onChange: persist }).then(ed => {
    editor = ed;
  });
})();
