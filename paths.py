import os
import configparser
from pathlib import Path

def main():
    config = configparser.ConfigParser(delimiters=('=',))
    ini_file = 'paths.ini'

    print("=== 🛡️ Cantatron Path Architect: Initialization ===")
    
    # Defaults for your environment
    mingw_default = "C:/.dev/w64devkit/bin"
    zig_default = "C:/.dev/zig_lib/0.13.0"

    mingw = input(f"Enter MinGW bin folder [{mingw_default}]: ").strip() or mingw_default
    zig = input(f"Enter Zig folder [{zig_default}]: ").strip() or zig_default

    config['COMPILERS'] = {
        'mingw': mingw.replace('\\', '/'),
        'zig': zig.replace('\\', '/')
    }

    with open(ini_file, 'w') as f:
        config.write(f)

    print(f"\n✅ Created {ini_file}. Proceed to Step 2.")

if __name__ == "__main__":
    main()
