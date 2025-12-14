"""Test signing with verbose output"""
import sys
import time
from pathlib import Path
from epi_recorder import record

test_file = Path(f"test_verbose_{int(time.time())}.epi")
print(f"Test file: {test_file}")
print("Testing with auto_sign=True...")

try:
    with record(test_file, goal="Test", metrics={"test": 1}, metadata_tags=["val"], auto_sign=True) as session:
        session.log_step("test.step", {"data": "test"})
    
    print(f"\nFile exists: {test_file.exists()}")
    if test_file.exists():
        print(f"File size: {test_file.stat().st_size} bytes")
        test_file.unlink()
        print("SUCCESS!")
    else:
        # Check if temp file exists
        temp_file = test_file.with_suffix('.epi.tmp')
        print(f"Temp file exists: {temp_file.exists()}")
        if temp_file.exists():
            print(f"Temp file size: {temp_file.stat().st_size} bytes")
            print("ERROR: Temp file created but not renamed!")
            temp_file.unlink()
        print("FAIL")
        sys.exit(1)
        
except Exception as e:
    print(f"EXCEPTION: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
