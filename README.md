# KiCad Library Automator

**Automatically watches your Downloads folder for KiCad-symbol ZIPs**, then moves & unpacks them into a central library folder.

> **Purpose:** I created this tool for SnapEDA and UltraLibrarian workflows—copying and pasting symbols every time is annoying and time-consuming.

* Waits for downloads to finish (configurable delay & stability check)
* Verifies the `.zip` contains a `.kicad_sym` file
* Creates a subfolder named after the part (zip stem)
* Moves, unzips, and cleans up the original archive
* Logs all actions to `kicad_monitor.log`

---

## Repo layout

```
kicad-library-automator/
├── .gitignore
├── README.md
├── config.json          ← your settings
├── process_kicad_libs.py ← main watcher script
├── requirements.txt     ← dependencies
└── LICENSE
```

---

## Installation

1. Clone the repo

   ```bash
   git clone https://github.com/<YOUR_USERNAME>/kicad-library-automator.git
   cd kicad-library-automator
   ```

2. (Optional) Create & activate a venv

   ```bash
   python -m venv venv
   .\venv\Scripts\activate   # Windows
   source venv/bin/activate   # macOS/Linux
   ```

3. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

4. Edit `config.json` to match your paths and timing preferences.

---

## Usage

* **As a script**

  ```bash
  python process_kicad_libs.py
  ```

* **Bundled as an EXE** (no console window)

  ```bash
  pyinstaller --onefile --noconsole --add-data "config.json;." process_kicad_libs.py
  ```

---

## Configuration (`config.json`)

```json
{
  "downloads_dir": "C:/Users/angel/Downloads",
  "library_root": "D:/MY FILES/PROJECTS/Angelo/my_kicad_lib",
  "check_interval": 1.0,
  "max_wait": 30,
  "processing_delay": 20,
  "file_extensions": {
    "archive": ".zip",
    "symbol": ".kicad_sym"
  }
}
```

* `check_interval` & `max_wait`: polling for file‐size stability
* `processing_delay`: seconds to wait before checking a new `.zip`
* `downloads_dir` & `library_root`: where to watch & where to move/unzip

---

## License

This project is released under the MIT License. See [LICENSE](LICENSE) for details.
