"""Test with manual inspection of temp dir"""
import sys
import tempfile
import time
import shutil
from pathlib import Path
from epi_recorder import record

test_file = Path(f"test_{int(time.time())}.epi")
print(f"Test file will be: {test_file}")

# Create session but inspect temp dir
from epi_recorder import EpiRecorderSession

session = EpiRecorderSession(
    test_file,
    goal="Test",
    metrics={"test": 1},
    metadata_tags=["val"],
    auto_sign=False  # Disable signing to simplify
)

try:
    session.__enter__()
    print(f" Temp dir created: {session.temp_dir}")
    print(f"Temp dir exists: {session.temp_dir.exists()}")
    
    # Log a test step
    session.log_step("test.step", {"data": "test"})
    
    # Check files in temp dir
    print(f"\nFiles in temp dir:")
    for f in session.temp_dir.rglob("*"):
        if f.is_file():
            print(f"  {f.relative_to(session.temp_dir)}: {f.stat().st_size} bytes")
    
    # Exit manually
    session.__exit__(None, None, None)
    
    #  Check if output file was created
    print(f"\nOutput file exists: {test_file.exists()}")
    if test_file.exists():
        print(f"Output file size: {test_file.stat().st_size} bytes")
        test_file.unlink()
        print("SUCCESS!")
    else:
        print("FAIL: File was not created")
        sys.exit(1)
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
