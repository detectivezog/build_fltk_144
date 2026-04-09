import os, urllib.request, tarfile, shutil
from pathlib import Path

def setup():
    print("--- 🛠️ Re-aligning Cantatron Infrastructure ---")
    root = Path(os.getcwd()).absolute()
    deps = root / "deps"
    include = root / "include"
    deps.mkdir(exist_ok=True)
    include.mkdir(exist_ok=True)

    # 1. THE STABLE FLTK DOWNLOAD (Version 1.3.9 includes 'configure')
    fltk_dir = deps / "fltk-1.3.9"
    if not fltk_dir.exists():
        print("📥 Downloading FLTK 1.3.9 Stable Tarball...")
        tar_path = deps / "fltk.tar.gz"
        url = "https://fltk.org/pub/fltk/1.3.9/fltk-1.3.9-source.tar.gz"
        urllib.request.urlretrieve(url, tar_path)
        
        print("📦 Extracting source...")
        with tarfile.open(tar_path, "r:gz") as tar:
            tar.extractall(path=deps)
        os.remove(tar_path)
        print(f"✅ FLTK 1.3.9 ready at {fltk_dir}")

    # 2. FETCH SIGNAL HEADERS
    print("📥 Fetching Standard Headers...")
    ma_h = include / "miniaudio.h"
    if not ma_h.exists():
        urllib.request.urlretrieve("https://raw.githubusercontent.com/mackron/miniaudio/master/miniaudio.h", ma_h)

    print("\n✅ Infrastructure ready. Proceed to brew_fltk.py.")

if __name__ == "__main__":
    setup()
