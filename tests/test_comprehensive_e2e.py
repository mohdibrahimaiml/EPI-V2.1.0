"""
Comprehensive end-to-end test of all functionality
"""
import sys
import time
from pathlib import Path

print("=" * 80)
print("COMPREHENSIVE END-TO-END TEST")
print("=" * 80)

errors = []

# Test 1: Import all modules
print("\n[1/7] Testing imports...")
try:
    from epi_recorder import record, EpiRecorderSession
    from epi_core.container import EPIContainer
    from epi_core.trust import sign_manifest, verify_signature
    from epi_core.redactor import Redactor
    from epi_cli.keys import KeyManager
    print("  ✓ All imports successful")
except Exception as e:
    print(f"  ✗ Import failed: {e}")
    errors.append(f"Import error: {e}")

# Test 2: Create .epi file with record()
print("\n[2/7] Testing record() function...")
try:
    test_file = Path(f"e2e_test_{int(time.time())}.epi")
    with record(test_file, goal="E2E Test", metadata_tags=["test"]) as session:
        session.log_step("test", {"data": "value"})
    
    if test_file.exists():
        size = test_file.stat().st_size
        print(f"  ✓ File created: {test_file} ({size} bytes)")
        test_file.unlink()
    else:
        print(f"  ✗ File not created: {test_file}")
        errors.append("record() failed to create file")
except Exception as e:
    print(f"  ✗ record() failed: {e}")
    errors.append(f"record() error: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Create .epi file with EpiRecorderSession
print("\n[3/7] Testing EpiRecorderSession class...")
try:
    test_file = Path(f"e2e_session_{int(time.time())}.epi")
    with EpiRecorderSession(test_file, goal="Session Test") as session:
        session.log_step("session.test", {"key": "value"})
    
    if test_file.exists():
        size = test_file.stat().st_size
        print(f"  ✓ File created: {test_file} ({size} bytes)")
        test_file.unlink()
    else:
        print(f"  ✗ File not created: {test_file}")
        errors.append("EpiRecorderSession failed to create file")
except Exception as e:
    print(f"  ✗ EpiRecorderSession failed: {e}")
    errors.append(f"EpiRecorderSession error: {e}")

# Test 4: Test auto-signing
print("\n[4/7] Testing auto-signing...")
try:
    test_file = Path(f"e2e_signed_{int(time.time())}.epi")
    with record(test_file, auto_sign=True, goal="Signing Test") as session:
        session.log_step("sign.test", {"signed": True})
    
    if test_file.exists():
        manifest = EPIContainer.read_manifest(test_file)
        if manifest.signature:
            print(f"  ✓ File signed: {manifest.signature[:20]}...")
        else:
            print("  ✗ File not signed")
            errors.append("auto_sign=True did not sign file")
        test_file.unlink()
    else:
        print(f"  ✗ File not created")
        errors.append("Signing test failed - file not created")
except Exception as e:
    print(f"  ✗ Signing failed: {e}")
    errors.append(f"Signing error: {e}")

# Test 5: Test artifact logging
print("\n[5/7] Testing artifact logging...")
try:
    artifact = Path("test_artifact_e2e.txt")
    artifact.write_text("test content")
    
    test_file = Path(f"e2e_artifact_{int(time.time())}.epi")
    with record(test_file, auto_sign=False) as session:
        session.log_artifact(artifact)
    
    if test_file.exists():
        import zipfile
        with zipfile.ZipFile(test_file) as zf:
            if any('test_artifact_e2e.txt' in name for name in zf.namelist()):
                print("  ✓ Artifact logged successfully")
            else:
                print("  ✗ Artifact not in .epi file")
                errors.append("Artifact not logged")
        test_file.unlink()
    artifact.unlink()
except Exception as e:
    print(f"  ✗ Artifact logging failed: {e}")
    errors.append(f"Artifact error: {e}")

# Test 6: Test redaction
print("\n[6/7] Testing redaction...")
try:
    r = Redactor()
    fake_key = "sk-proj-" + "a" * 48
    sensitive = f"My key is {fake_key}"
    redacted, count = r.redact(sensitive)
    
    if fake_key not in redacted and count > 0:
        print(f"  ✓ Redaction working ({count} items redacted)")
    else:
        print(f"  ✗ Redaction failed (count={count})")
        errors.append("Redaction not working")
except Exception as e:
    print(f"  ✗ Redaction failed: {e}")
    errors.append(f"Redaction error: {e}")

# Test 7: Test file integrity
print("\n[7/7] Testing file integrity...")
try:
    test_file = Path(f"e2e_integrity_{int(time.time())}.epi")
    with record(test_file, auto_sign=False,  goal="Integrity Test") as session:
        session.log_step("integrity", {"test": True})
    
    if test_file.exists():
        integrity_ok, issues = EPIContainer.verify_integrity(test_file)
        if integrity_ok:
            print("  ✓ Integrity verification passed")
        else:
            print(f"  ✗ Integrity issues: {issues}")
            errors.append(f"Integrity issues: {issues}")
        test_file.unlink()
except Exception as e:
    print(f"  ✗ Integrity check failed: {e}")
    errors.append(f"Integrity error: {e}")

# Summary
print("\n" + "=" * 80)
if errors:
    print(f"FAILED - {len(errors)} error(s) found:")
    for i, error in enumerate(errors, 1):
        print(f"  {i}. {error}")
    sys.exit(1)
else:
    print("ALL TESTS PASSED ✓")
    print("Package is production-ready!")
    sys.exit(0)
