# NextPy CLI Command Reference

The NextPy Command-Line Interface (CLI) automates project scaffolding, module generation, database administration, and production assembly optimization.

---

## 🚀 Core Management Commands

### `nextpy create <name>`
* **Description:** Scaffolds a complete, full-stack NextPy project boilerplate from scratch.
* **Mechanism:** 
  * Provisions a standard workspace architecture containing `pages/`, `components/`, `models/`, `templates/`, and `public/` directories.
  * Generates optimized static fallback templates (`_page.html`, `_404.html`) and writes localized, secure, cryptographically unique secrets to your project `.env` file.
  * Evaluates your system toolchain and executes automatic background dependencies processing (`npm install` for frontend Tailwind architecture and `pip install` for backend Python modules).
* **Arguments & Flags:**
  * `--psx / --no-psx` *(Default: `True`)*: Toggles compilation-free Python Syntax Extension (True JSX in Python) virtual layout parsing. Disabling this falls back to a raw traditional string HTML template builder engine.
  * `--template <string>` *(Default: `"default"`)*: Targets an alternative starting framework layout structure configuration.

### `nextpy dev`
* **Description:** Launches a local ASGI development engine equipped with fine-grained hot-reloading asset watches.
* **Mechanism:** 
  * Reads application settings, normalizes relative SQLite strings into absolute file system locations, and fires core ORM database (`init_db()`) infrastructure health checks.
  * Provisions an active file system listener through `watchdog`. If the library is missing, it dynamically falls back to optimized system interval polling.
  * Watches cross-stack formats (`.py`, `.psx`, `.jsx`, `.html`, `.css`, `.json`) to hot-swap virtual workspace states seamlessly.
* **Arguments & Flags:**
  * `-p, --port <int>` *(Default: `8000` or config configuration)*: Overrides the target listening network port block.
  * `-h, --host <string>` *(Default: `"0.0.0.0"` or config configuration)*: Configures the target network binding gateway.
  * `--reload / --no-reload` *(Default: `True`)*: Explicitly enables or disables asynchronous system file watchers.
  * `--debug / --no-debug` *(Default: `True`)*: Dictates framework-level logging and error telemetry exposure thresholds.

---

## 📦 Generation & Route Utilities

### `nextpy generate <type> <name>`
* **Description:** Speeds up your development cycle by writing convention-compliant stubs for key framework layout nodes.
* **Valid Module Types:** `page`, `api`, `component`.
* **Mechanism:**
  * `page`: Injects a new file-based router view component under `pages/<name>.py` populated with virtual rendering structures and a decoupled asymmetric `getServerSideProps` lifecycle anchor.
  * `api`: Spits out an isolated API gateway node under `pages/api/<name>.py` complete with asynchronous REST boilerplate controllers (`async def get()` and `async def post()`).
  * `component`: Provisions a structured, isolated, reusable interface block inside `components/<name>.py` mapping layout property matrices cleanly.

### `nextpy routes`
* **Description:** Runs real-time reflection across local directories to print a structured breakdown of every reachable endpoint.
* **Mechanism:** Instantiates your project's custom router system context, evaluates directory layout arrays, and charts active paths out to the user sorted into **Page Routes** (static or dynamic paths) and **API Endpoints** along with their supported HTTP methods.

---

## 🔒 Administration & Database Controls

### `nextpy createsuperuser`
* **Description:** Provisions or overwrites a high-privilege master administrative account inside the active persistence schema.
* **Mechanism:** Launches interactive terminal capture prompts to gather administrative attributes. It processes the raw inputs safely through the project's hashing utilities and stores the account with the necessary security permission flag arrays to unlock the built-in administrative dashboard.

### `nextpy flushdb`
* **Description:** Destroys and completely resets all connected metadata-tracked table layouts.
* **Mechanism:** To protect production environments from destructive actions, it requires active superuser credential validation before execution. Once verified, it executes structured drop actions across all tables and immediately re-scaffolds fresh, empty table layouts.
* **Arguments & Flags:**
  * `--yes`: Bypasses the terminal safety confirmation step.

---

## 🏭 Production & Assembly Optimization

### `nextpy build`
* **Description:** Assembles, serializes, and packages your workspace layout for scalable production lifecycles.
* **Mechanism:** Dispatches the internal builder optimization loop to execute recursive asset minification, code-splitting chunk division arrays, and tree-shaking evaluations to minimize file weight.
* **Arguments & Flags:**
  * `-o, --out <string>` *(Default: `"out"`)*: Specifies the destination folder structure path for compiled production assets.
  * `--clean / --no-clean` *(Default: `True`)*: Purges all previous build directory contents before execution.
  * `--minify / --no-minify` *(Default: `True`)*: Controls active JavaScript, HTML, and CSS compaction pipelines.

### `nextpy export`
* **Description:** Builds and exports completely decoupled, standalone static artifacts tailored for serverless storage or static providers.
* **Mechanism:** Compiles all layout paths down to fully pre-rendered static nodes, tracking bundle sizes and distribution footprints in real time.

### `nextpy start`
* **Description:** Starts up your NextPy site tuned for maximized runtime efficiency.
* **Mechanism:** Shuts down framework debug telemetry and file-watching routines to preserve CPU cycles. Boots a Uvicorn container running an enterprise-ready cluster of **4 parallel worker processes** underneath an active system `warning` logging suppression mask to handle higher transaction throughput.

---

## 🧩 Plugin Architecture Controls

### `nextpy plugin list`
* **Description:** Displays an executive status summary of all recognized, locally available framework plugins.
* **Output Matrix:** Yields total counts, version specifications, activation switches (`enabled` or `disabled`), execution load hierarchy priorities, and cross-plugin dependency chains.

### `nextpy plugin enable <name>`
* **Description:** Shifts internal state registries to toggle a target plugin extension dynamically between on or off execution paths.
* **Arguments & Flags:**
  * `--enable / --disable`: Toggles structural activation states.

### `nextpy plugin configure <name>`
* **Description:** Injects granular parameter maps directly to individual system plugin registries.
* **Arguments & Flags:**
  * `--config '<json_string>'`: Passes a localized raw string JSON dictionary block to modify internal operational variables instantly.

### `nextpy plugin load <file_path>`
* **Description:** Directly maps, verifies, and installs an uncompiled plugin archive file straight from your filesystem into your framework workspace.

---

## ℹ️ Diagnostics

* **`nextpy version`**: Outputs structural information about your environment (NextPy version, Python runtime engine details, core architecture layouts, and home documentation links).
* **`nextpy info`**: Runs an extensive diagnostic suite across your current working directory, validating the health of directory trees (`pages/`, `components/`, etc.), `watchdog` state support, and critical command maps.
