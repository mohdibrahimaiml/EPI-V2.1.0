"""Debug context manager test"""
import sys
import traceback
from pathlib import Path
import time
from epi_recorder import record

test_file = Path(f"test_context_{int(time.time())}.epi")
print(f"Testing with file: {test_file}")

try:
    print("Entering context manager...")
    with record(test_file, 
                goal="Test goal",
                metrics={"test": 1},
                metadata_tags=["validation"]) as session:
        print("Inside context manager, logging step...")
        session.log_step("test.step", {"data": "test"})
        print("Step logged successfully")
    
    print(f"Context exited, file exists: {test_file.exists()}")
    
    if test_file.exists():
        print(f"File size: {test_file.stat().st_size} bytes")
        test_file.unlink()
        print("SUCCESS: Test passed")
    else:
        print("FAIL: File was not created")
        # Check if there are any error hints
        if (test_file.parent / "epi-recordings").exists():
            print(f"Checking epi-recordings directory...")
            for f in (test_file.parent / "epi-recordings").iterdir():
                print(f"  Found: {f}")
        sys.exit(1)

except Exception as e:
    print(f"FAIL: Exception occurred: {e}")
    traceback.print_exc()
    
    # Still try to clean up
    if test_file.exists():
        test_file.unlink()
    
    sys.exit(1)

        print(f"File size: {test_file.stat().st_size} bytes")
        test_file.unlink()
        print("SUCCESS: Test passed")
    else:
        print("FAIL: File was not created")
        sys.exit(1)

except Exception as e:
    print(f"FAIL: Exception occurred: {e}")
    traceback.print_exc()
    sys.exit(1)
