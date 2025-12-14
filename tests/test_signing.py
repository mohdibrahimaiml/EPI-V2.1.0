"""Test with auto_sign enabled"""
import sys
import time
from pathlib import Path
from epi_recorder import record

test_file = Path(f"test_{int(time.time())}.epi")
print(f"Test file: {test_file}")

try:
    print("Testing with auto_sign=True (default)...")
    with record(test_file, goal="Test", metrics={"test": 1}, metadata_tags=["val"], auto_sign=True) as session:
        session.log_step("test.step", {"data": "test"})
    
    if test_file.exists():
        print(f"SUCCESS! File created: {test_file.stat().st_size} bytes")
        test_file.unlink()
    else:
        print("FAIL: File not created when auto_sign=True")
        sys.exit(1)
        
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
