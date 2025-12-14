"""Debug signing in detail"""
import sys
import time
from pathlib import Path
from epi_recorder import EpiRecorderSession

test_file = Path(f"debug_test_{int(time.time())}.epi")
print(f"Test file: {test_file}")

session = EpiRecorderSession(
    test_file,
    goal="Test",
    metrics={"test": 1},
    metadata_tags=["val"],
    auto_sign=True
)

try:
    print("1. Entering session...")
    session.__enter__()
    print("2. Session entered")
    
    print("3. Logging step...")
    session.log_step("test.step", {"data": "test"})
    print("4. Step logged")
    
    print("5. Exiting session (will pack then sign)...")
    # Check before exit
    print(f"   File exists before exit: {test_file.exists()}")
    
    session.__exit__(None, None, None)
    
    print("6. Session exited")
    print(f"   File exists after exit: {test_file.exists()}")
    
    if test_file.exists():
        print(f"   File size: {test_file.stat().st_size} bytes")
        
        # Verify it's a valid ZIP
        import zipfile
        try:
            with zipfile.ZipFile(test_file) as zf:
                print(f"   ZIP contents: {zf.namelist()}")
                # Check for manifest
                manifest_data = zf.read('manifest.json').decode('utf-8')
                print(f"   Has manifest: True")
                import json
                manifest = json.loads(manifest_data)
                print(f"   Has signature: {'signature' in manifest and manifest['signature'] is not None}")
        except Exception as zip_err:
            print(f"   ZIP error: {zip_err}")
        
        test_file.unlink()
        print("SUCCESS!")
    else:
        print("FAIL: File not created")
        sys.exit(1)
        
except Exception as e:
    print(f"EXCEPTION: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
