# Zip2KiCad (KiCad Library Automator)

Automatically watches your Downloads folder for KiCad symbol ZIPs from SnapEDA, UltraLibrarian, etc., then moves & unpacks them into your central library—no more manual copy-paste.

---

**Why Zip2KiCad?**

> "I made this tool for SnapEDA and UltraLibrarian because copying/pasting symbols every time is annoying and time-consuming!"
---

## ✨ Features

* Waits for downloads to finish (configurable delay & stability check)
* Verifies the .zip contains a `.kicad_sym` file
* Creates a subfolder named after the part
* Moves, unzips, and cleans up the original archive
* Logs all actions to `kicad_monitor.log`

---

## Installation & Usage

### **Option 1: Standalone EXE**

You can use the ready-to-run `Zip2KiCad.exe`. No Python needed.

* Place `Zip2KiCad.exe` and `config.json` in the same folder.
* Double-click to start. It will run silently (no window).
* All logs will appear in `kicad_monitor.log` in that folder.

**To change settings** (e.g. folder locations or timing), edit `config.json` in a text editor (like Notepad).

### **Option 2: Python Source (for editing or development)**

If you want to customize the script:

1. Install Python 3.8+

2. Edit `config.json` as needed.

3. Run the watcher:

   ```bash
   python Zip2KiCad.py
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

* `downloads_dir` and `library_root`: folders to watch and manage
* `processing_delay`: seconds to wait after new ZIP appears
* `check_interval`/`max_wait`: how long to check if file download is done

---

## How to run automatically on startup (Windows Task Scheduler)

1. **Open Task Scheduler** (`Win+R`, type `taskschd.msc`, press Enter)
2. **Create Task** > Give it a name like "Zip2KiCad Watcher"
3. In **Actions** tab, choose "Start a program"

   * **Program/script:** Browse to your EXE (e.g. `Zip2KiCad.exe`)
   * **Start in (optional):** Folder where EXE and `config.json` are stored
4. In **Triggers**, set to "At log on" (or as you prefer)
5. In **General**, check "Run with highest privileges" (recommended)
6. Click OK. Now the watcher will launch on login and run in the background.

