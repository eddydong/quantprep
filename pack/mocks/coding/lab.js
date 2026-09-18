(function codingLab() {
  const PYODIDE_VER = "0.27.7";
  const PYODIDE_BASE = "https://cdn.jsdelivr.net/pyodide/v" + PYODIDE_VER + "/full/";
  const ed = document.getElementById("lab-ed");
  const out = document.getElementById("lab-out");
  const status = document.getElementById("lab-status");
  const runBtn = document.getElementById("lab-run");
  const resetBtn = document.getElementById("lab-reset");
  if (!ed || typeof CODING === "undefined") return;

  const STORE = (typeof CODING_STORE === "string" && CODING_STORE) || "quantprep-candidate";
  let tab = "candidate";
  let pyodide = null;
  let loading = null;
  let revealed = false;

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
    if (tab !== "candidate") return;
    try {
      localStorage.setItem(STORE, ed.value);
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

  ed.value = saved() || stub();
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

  document.querySelectorAll("[data-lab-tab]").forEach(btn => {
    btn.addEventListener("click", () => {
      const next = btn.dataset.labTab;
      if (next === "solutions" && !revealed) {
        if (!confirm("Show the answer key? Sit the mock in candidate.py first.")) return;
        revealed = true;
      }
      if (tab === "candidate") persist();
      tab = next;
      document.querySelectorAll("[data-lab-tab]").forEach(b => b.classList.toggle("on", b.dataset.labTab === tab));
      if (tab === "candidate") {
        ed.value = saved() || stub();
        ed.readOnly = false;
      } else if (tab === "broken") {
        ed.value = CODING.broken;
        ed.readOnly = true;
      } else {
        ed.value = CODING.solutions;
        ed.readOnly = true;
      }
    });
  });

  resetBtn.addEventListener("click", () => {
    if (tab !== "candidate") {
      document.querySelector("[data-lab-tab='candidate']").click();
    }
    ed.value = stub();
    persist();
    setStatus("Stub restored.");
  });

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = () => reject(new Error("Could not load " + src));
      document.head.appendChild(s);
    });
  }

  async function ensurePy() {
    if (pyodide) return pyodide;
    if (loading) return loading;
    loading = (async () => {
      setStatus("Loading Python in this browser… first time is a few megabytes.");
      if (typeof loadPyodide !== "function") {
        await loadScript(PYODIDE_BASE + "pyodide.js");
      }
      const py = await loadPyodide({ indexURL: PYODIDE_BASE });
      setStatus("Loading numpy and pandas…");
      await py.loadPackage(["numpy", "pandas"]);
      pyodide = py;
      setStatus("Python ready.");
      return py;
    })();
    try {
      return await loading;
    } catch (err) {
      loading = null;
      throw err;
    }
  }

  window.primeCodingLab = function primeCodingLab() {
    ensurePy().catch(err => setStatus(String(err.message || err)));
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
    const code = tab === "candidate" ? ed.value : (saved() || stub());
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
})();
