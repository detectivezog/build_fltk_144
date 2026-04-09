import subprocess, os, configparser, shutil
from pathlib import Path

def build():
    print("--- 🔨 Official Brewing: FLTK Static Library ---")
    config = configparser.ConfigParser(delimiters=('=',))
    config.read('paths.ini')
    
    # 1. Resolve and Verify Compiler
    bin_dir = os.path.expandvars(config.get('COMPILERS', 'mingw'))
    bin_path = Path(bin_dir).absolute()
    
    gcc_exe = str(bin_path / "gcc.exe").replace('\\', '/')
    gpp_exe = str(bin_path / "g++.exe").replace('\\', '/')
    ar_exe  = str(bin_path / "ar.exe").replace('\\', '/')
    ranlib_exe = str(bin_path / "ranlib.exe").replace('\\', '/')

    if not os.path.exists(gcc_exe):
        print(f"❌ Error: Cannot find gcc.exe at {gcc_exe}")
        print("Please check your paths.ini")
        return

    root_dir = Path(os.getcwd()).absolute()
    fltk_dir = root_dir / "deps/fltk-1.3.9"
    build_dir = root_dir / "build"
    
    # 2. Prepare Local Tmp
    tmp_dir = build_dir / "tmp"
    build_dir.mkdir(exist_ok=True)
    tmp_dir.mkdir(exist_ok=True)
    
    # 3. Construct Rigorous Environment
    env = os.environ.copy()
    env["PATH"] = str(bin_path) + os.pathsep + env.get("PATH", "")
    
    # THE FIX: Explicitly set compiler environment variables
    env["CC"]  = gcc_exe
    env["CXX"] = gpp_exe
    env["AR"]  = ar_exe
    env["RANLIB"] = ranlib_exe
    
    # Bypassing /tmp panic
    unix_tmp = str(tmp_dir).replace('\\', '/')
    env["TMPDIR"] = unix_tmp
    env["TMP"] = unix_tmp
    env["TEMP"] = unix_tmp

    # 4. CONFIGURE
    # We pass the compilers directly as arguments to be 100% certain
    cmd_conf =[
        "sh", "./configure", 
        f"CC={gcc_exe}", f"CXX={gpp_exe}",
        "--build=x86_64-w64-mingw32",
        "--host=x86_64-w64-mingw32", 
        "--disable-gl", "--disable-shared", 
        "--enable-localjpeg", "--enable-localzlib", "--enable-localpng"
    ]
    
    print("Configuring FLTK...")
    subprocess.run(cmd_conf, cwd=str(fltk_dir), env=env, check=True)
    
    # 5. GNU MAKE
    print("Compiling libfltk.a (Parallel)...")
    # We tell make exactly which compilers to use for the build stage
    cmd_make =["make", f"CC={gcc_exe}", f"CXX={gpp_exe}", "-C", "src", "-j8"]
    subprocess.run(cmd_make, cwd=str(fltk_dir), env=env, check=True)
    
    # 6. SECURE THE LIBRARY
    lib_src = fltk_dir / "lib/libfltk.a"
    lib_dest = build_dir / "libfltk.a"
    if lib_dest.exists(): os.remove(lib_dest)
    shutil.copy(lib_src, lib_dest)
    print(f"✅ libfltk.a manifested in {lib_dest}")

if __name__ == "__main__":
    build()
