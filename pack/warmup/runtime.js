(function quantPyRuntime() {
  const PYODIDE_VER = "0.27.7";
  const PYODIDE_BASE = "https://cdn.jsdelivr.net/pyodide/v" + PYODIDE_VER + "/full/";
  let pyodide = null;
  let loading = null;

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = () => reject(new Error("Could not load " + src));
      document.head.appendChild(s);
    });
  }

  window.ensureQuantPy = async function ensureQuantPy(onStatus) {
    const say = t => {
      if (onStatus) onStatus(t);
    };
    if (pyodide) return pyodide;
    if (loading) return loading;
    loading = (async () => {
      say("Loading Python in this browser… first time is a few megabytes.");
      if (typeof loadPyodide !== "function") {
        await loadScript(PYODIDE_BASE + "pyodide.js");
      }
      const py = await loadPyodide({ indexURL: PYODIDE_BASE });
      say("Loading numpy and pandas…");
      await py.loadPackage(["numpy", "pandas"]);
      pyodide = py;
      say("Python ready.");
      return py;
    })();
    try {
      return await loading;
    } catch (err) {
      loading = null;
      throw err;
    }
  };

  window.primeQuantPy = function primeQuantPy(onStatus) {
    window.ensureQuantPy(onStatus).catch(err => {
      if (onStatus) onStatus(String(err.message || err));
    });
  };
})();
