(function quantEditor() {
  const CM_VER = "5.65.16";
  const BASE = "https://cdn.jsdelivr.net/npm/codemirror@" + CM_VER + "/";
  const mounted = [];
  let loading = null;

  function loadStyle(href) {
    if ([...document.querySelectorAll("link")].some(l => l.href === href)) return;
    const l = document.createElement("link");
    l.rel = "stylesheet";
    l.href = href;
    document.head.appendChild(l);
  }

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const found = [...document.getElementsByTagName("script")].find(s => s.src === src);
      if (found) {
        if (found.dataset.ok === "1" || (src.endsWith("codemirror.js") && window.CodeMirror)) {
          resolve();
          return;
        }
        found.addEventListener("load", resolve, { once: true });
        found.addEventListener("error", () => reject(new Error("Could not load " + src)), { once: true });
        return;
      }
      const s = document.createElement("script");
      s.src = src;
      s.onload = () => {
        s.dataset.ok = "1";
        resolve();
      };
      s.onerror = () => reject(new Error("Could not load " + src));
      document.head.appendChild(s);
    });
  }

  function bindTab(textarea, onChange) {
    textarea.addEventListener("keydown", e => {
      if (e.key !== "Tab" || textarea.readOnly) return;
      e.preventDefault();
      const s = textarea.selectionStart;
      const end = textarea.selectionEnd;
      textarea.value = textarea.value.slice(0, s) + "    " + textarea.value.slice(end);
      textarea.selectionStart = textarea.selectionEnd = s + 4;
      if (onChange) onChange();
    });
    if (onChange) textarea.addEventListener("input", onChange);
  }

  function fallback(textarea, opts) {
    bindTab(textarea, opts.onChange);
    return {
      get: () => textarea.value,
      set: v => {
        textarea.value = v == null ? "" : v;
      },
      setReadOnly: ro => {
        textarea.readOnly = !!ro;
      },
      refresh: () => {}
    };
  }

  window.ensureCodeMirror = function ensureCodeMirror() {
    if (window.CodeMirror && window.CodeMirror.modes && window.CodeMirror.modes.python) {
      return Promise.resolve(window.CodeMirror);
    }
    if (loading) return loading;
    loading = (async () => {
      loadStyle(BASE + "lib/codemirror.css");
      await loadScript(BASE + "lib/codemirror.js");
      await loadScript(BASE + "mode/python/python.js");
      await loadScript(BASE + "addon/edit/matchbrackets.js");
      await loadScript(BASE + "addon/selection/active-line.js");
      await loadScript(BASE + "addon/runmode/runmode.js");
      return window.CodeMirror;
    })();
    try {
      return loading;
    } finally {
      loading.catch(() => {
        loading = null;
      });
    }
  };

  window.colorQuantCode = function colorQuantCode(root) {
    const CM = window.CodeMirror;
    if (!CM || !CM.runMode) return;
    const scope = root || document;
    scope.querySelectorAll("pre code").forEach(el => {
      if (el.dataset.cm === "1") return;
      if (el.closest(".CodeMirror")) return;
      const text = el.textContent;
      el.textContent = "";
      const pre = el.parentElement;
      if (pre) pre.classList.add("cm-s-blotter", "cm-static");
      CM.runMode(text, "python", el);
      el.dataset.cm = "1";
    });
  };

  window.refreshQuantEditors = function refreshQuantEditors() {
    mounted.forEach(cm => {
      try {
        cm.refresh();
      } catch (_) {}
    });
  };

  window.mountQuantEditor = async function mountQuantEditor(textarea, opts) {
    opts = opts || {};
    try {
      const CM = await window.ensureCodeMirror();
      const cm = CM.fromTextArea(textarea, {
        mode: "python",
        theme: "blotter",
        lineNumbers: true,
        indentUnit: 4,
        tabSize: 4,
        indentWithTabs: false,
        lineWrapping: true,
        matchBrackets: true,
        styleActiveLine: true,
        extraKeys: {
          Tab(cm) {
            if (cm.getOption("readOnly")) return;
            if (cm.somethingSelected()) cm.indentSelection("add");
            else cm.replaceSelection("    ", "end");
          }
        }
      });
      cm.setSize("100%", opts.height || "420px");
      if (opts.readOnly) cm.setOption("readOnly", true);
      if (opts.onChange) cm.on("change", opts.onChange);
      mounted.push(cm);
      requestAnimationFrame(() => cm.refresh());
      window.colorQuantCode(document);
      return {
        get: () => cm.getValue(),
        set: v => {
          const next = v == null ? "" : v;
          if (cm.getValue() !== next) cm.setValue(next);
        },
        setReadOnly: ro => {
          cm.setOption("readOnly", !!ro);
          cm.getWrapperElement().classList.toggle("cm-readonly", !!ro);
        },
        refresh: () => cm.refresh()
      };
    } catch (_) {
      return fallback(textarea, opts);
    }
  };
})();
