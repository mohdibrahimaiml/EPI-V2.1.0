"""Simpler debug test for context manager"""
import sys
from pathlib import Path
import time
from epi_recorder import record

test_file = Path(f"test_{int(time.time())}.epi")
print(f"Test file: {test_file}")

try:
    with record(test_file, goal="Test", metrics={"test": 1}, metadata_tags=["val"]) as session:
        session.log_step("test.step", {"data": "test"})
    print(f"File exists: {test_file.exists()}")
    if test_file.exists():
        print("SUCCESS")
        test_file.unlink()
    else:
        print("FAIL: File not created")
        sys.exit(1)
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
