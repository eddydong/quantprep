(function pythonSandbox() {
  const root = document.getElementById("sandbox-lab");
  if (!root || !window.mountQuantEditor) return;

  const STORE = (typeof SANDBOX_STORE === "string" && SANDBOX_STORE) || "quantprep-sandbox";
  const host = document.getElementById("sb-ed");
  const out = document.getElementById("sb-out");
  const status = document.getElementById("sb-status");
  const runBtn = document.getElementById("sb-run");
  const resetBtn = document.getElementById("sb-reset");
  const clearBtn = document.getElementById("sb-clear");

  const STARTER = `# This is a scratch pad. Click Run (or Ctrl/Cmd+Enter).
# print() sends a line to the console below.

print("hello")

bid = 7.7800
ask = 7.7804
print("mid", (bid + ask) / 2)

# A last line that is just a value is also shown:
1 + 1
`;

  let editor = null;

  function stub() {
    return STARTER;
  }
  function saved() {
    try {
      return localStorage.getItem(STORE);
    } catch {
      return null;
    }
  }
  function persist() {
    if (!editor) return;
    try {
      localStorage.setItem(STORE, editor.get());
    } catch (_) {}
  }
  function setStatus(t) {
    status.textContent = t || "";
  }
  function showOut(text, kind) {
    const body = text == null ? "" : String(text);
    out.hidden = false;
    out.textContent = body || "Nothing printed this run. Add print(\"hello\") and Run again.";
    out.className = "lab-out" + (kind ? " " + kind : "");
  }

  const RUNNER = String.raw`
import ast, io, sys, traceback

src = open("sandbox_user.py", encoding="utf-8").read()
buf = io.StringIO()
sys.stdout = buf
sys.stderr = buf
ns = {"__name__": "__main__"}
try:
    tree = ast.parse(src, filename="<sandbox>")
    body = list(tree.body)
    last_val = None
    if body and isinstance(body[-1], ast.Expr):
        last = body.pop()
        if body:
            exec(compile(ast.Module(body, type_ignores=[]), "<sandbox>", "exec"), ns)
        last_val = eval(compile(ast.Expression(last.value), "<sandbox>", "eval"), ns)
        if last_val is not None:
            print(repr(last_val))
    else:
        exec(compile(tree, "<sandbox>", "exec"), ns)
except Exception:
    traceback.print_exc()
finally:
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
buf.getvalue()
`;

  async function run() {
    persist();
    runBtn.disabled = true;
    try {
      if (typeof window.ensureQuantPy !== "function") {
        throw new Error("Python runtime is not on this page.");
      }
      const py = await window.ensureQuantPy(setStatus);
      py.FS.writeFile("sandbox_user.py", editor ? editor.get() : host.value);
      setStatus("Running…");
      const raw = py.runPython(RUNNER);
      const text = typeof raw === "string" ? raw : (raw && raw.toString ? raw.toString() : "");
      const failed = /^\s*Traceback \(most recent call last\):/m.test(text) || /\n[A-Za-z].*Error:/m.test(text);
      setStatus(failed ? "Stopped on an error — read the console." : "Done.");
      showOut(text.replace(/\s+$/, ""), failed ? "fail" : "pass");
    } catch (err) {
      setStatus("Could not run.");
      showOut(String(err.message || err), "fail");
    } finally {
      runBtn.disabled = false;
    }
  }

  runBtn.addEventListener("click", run);
  resetBtn.addEventListener("click", () => {
    if (!editor) return;
    editor.set(stub());
    persist();
    setStatus("Starter restored.");
  });
  clearBtn.addEventListener("click", () => {
    out.hidden = false;
    out.textContent = "";
    out.className = "lab-out";
    setStatus("Console cleared.");
  });

  function fitEditor() {
    const wrap = root.querySelector(".sb-ed-wrap");
    const cmEl = wrap && wrap.querySelector(".CodeMirror");
    if (!wrap || !cmEl || !cmEl.CodeMirror) {
      if (editor) editor.refresh();
      return;
    }
    const h = wrap.clientHeight;
    cmEl.CodeMirror.setSize("100%", Math.max(80, h) + "px");
    cmEl.CodeMirror.refresh();
  }
  window.fitSandboxEditor = fitEditor;
  window.addEventListener("resize", () => {
    if (document.body.classList.contains("sandbox-ide")) fitEditor();
  });
  const wrap = root.querySelector(".sb-ed-wrap");
  if (wrap && window.ResizeObserver) {
    new ResizeObserver(() => fitEditor()).observe(wrap);
  }
  const help = root.querySelector(".sb-help");
  if (help) help.addEventListener("toggle", fitEditor);

  host.value = saved() || stub();
  window.mountQuantEditor(host, {
    height: "100%",
    onChange: persist,
    onRun: run
  }).then(ed => {
    editor = ed;
    requestAnimationFrame(() => requestAnimationFrame(fitEditor));
  });
})();
