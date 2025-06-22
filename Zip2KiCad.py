import sys
import time
import json
import logging
import zipfile
import shutil
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# ——— Determine resource vs. output directories ———
if getattr(sys, "frozen", False):
    # Running as a PyInstaller one-file bundle:
    RESOURCE_DIR = Path(sys._MEIPASS)
    OUTPUT_DIR   = Path(sys.executable).resolve().parent
else:
    # Running as a normal .py script:
    RESOURCE_DIR = Path(__file__).resolve().parent
    OUTPUT_DIR   = RESOURCE_DIR

# ——— Load configuration ———
CONFIG_PATH = RESOURCE_DIR / "config.json"
with open(CONFIG_PATH, "r") as f:
    cfg = json.load(f)

DOWNLOADS        = Path(cfg["downloads_dir"])
LIB_ROOT         = Path(cfg["library_root"])
CHECK_INTERVAL   = cfg["check_interval"]
MAX_WAIT         = cfg["max_wait"]
PROCESSING_DELAY = cfg.get("processing_delay", 20)
EXT_ARCHIVE      = cfg["file_extensions"]["archive"].lower()
EXT_SYMBOL       = cfg["file_extensions"]["symbol"].lower()

# ——— Ensure output directory exists and log file is present ———
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
LOG_PATH = OUTPUT_DIR / "kicad_monitor.log"
# (re)create if missing
if not LOG_PATH.exists():
    LOG_PATH.touch()

# ——— File-based Logging Setup ———
logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)

def is_stable_file(path: Path, interval: float, max_wait: float) -> bool:
    """Wait until file size stops changing (or timeout)."""
    last_size = -1
    waited   = 0.0
    while waited < max_wait:
        try:
            size = path.stat().st_size
        except FileNotFoundError:
            return False
        if size == last_size and size > 0:
            return True
        last_size = size
        time.sleep(interval)
        waited += interval
    return False

def process_zip(zip_path: Path):
    part = zip_path.stem
    logging.info(f"→ Detected new archive: {zip_path.name} (part={part})")

    # 1) Ensure it's fully written
    if not is_stable_file(zip_path, CHECK_INTERVAL, MAX_WAIT):
        logging.error(f" File never stabilized: {zip_path}")
        return

    # 2) Check for a KiCad symbol inside
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            if not any(f.lower().endswith(EXT_SYMBOL) for f in z.namelist()):
                logging.info("  • No KiCad symbol inside → skipping")
                return
    except zipfile.BadZipFile:
        logging.error("  • Bad ZIP file → skipping")
        return

    # 3) Prepare destination folder
    dest_folder = LIB_ROOT / part
    dest_folder.mkdir(parents=True, exist_ok=True)

    # 4) Move ZIP into the library folder
    dest_zip = dest_folder / zip_path.name
    shutil.move(str(zip_path), dest_zip)
    logging.info(f"  • Moved archive to {dest_folder}")

    # 5) Unzip contents
    try:
        with zipfile.ZipFile(dest_zip, 'r') as z:
            z.extractall(dest_folder)
        logging.info("  • Unzipped contents")
    except Exception as e:
        logging.error(f"  • Failed to unzip: {e}")

    # 6) Delete the moved ZIP
    try:
        dest_zip.unlink()
        logging.info("  • Deleted archive from library folder")
    except Exception as e:
        logging.warning(f"  • Could not delete archive: {e}")

class ZipMonitor(FileSystemEventHandler):
    def on_created(self, event):
        p = Path(event.src_path)
        if not event.is_directory and p.suffix.lower() == EXT_ARCHIVE:
            logging.info(f"New archive detected: {p.name}, waiting {PROCESSING_DELAY}s…")
            time.sleep(PROCESSING_DELAY)
            process_zip(p)

if __name__ == "__main__":
    # Ensure the target library root exists
    LIB_ROOT.mkdir(parents=True, exist_ok=True)
    DOWNLOADS.mkdir(parents=True, exist_ok=True)

    observer = Observer()
    observer.schedule(ZipMonitor(), str(DOWNLOADS), recursive=False)
    observer.start()
    logging.info(f"Watching {DOWNLOADS} for new {EXT_ARCHIVE} files…")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
