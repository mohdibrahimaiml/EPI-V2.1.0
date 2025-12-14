"""Test exactly what validate_complete.py does"""
import sys
import time
from pathlib import Path

try:
    from epi_recorder import record
    
    test_file = Path(f"validation_test_{int(time.time())}.epi")
    
    print(f"Creating {test_file}...")
    with record(test_file, 
                goal="Test goal",
                metrics={"test": 1},
                metadata_tags=["validation"]) as session:
        session.log_step("test.step", {"data": "test"})
    
    print(f"File exists: {test_file.exists()}")
    assert test_file.exists(), "File was not created!"
    
    print(f"File size: {test_file.stat().st_size} bytes")
    test_file.unlink()
    print("SUCCESS!")
    
except Exception as e:
    print(f"FAIL: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
