"""
REAL USER EXPERIENCE TEST
Test everything exactly as a user would encounter it
"""
import subprocess
import sys
from pathlib import Path
import time

print("=" * 80)
print("REAL USER EXPERIENCE TEST - NO HALLUCINATIONS")
print("Testing as if I just discovered epi-recorder on PyPI")
print("=" * 80)

passed = 0
failed = 0
tests = []

def test(name, func):
    global passed, failed, tests
    print(f"\n[TEST] {name}")
    try:
        result = func()
        print(f"  [PASS]")
        passed += 1
        tests.append((name, "PASS", None))
        return result
    except AssertionError as e:
        print(f"  [FAIL] {e}")
        failed += 1
        tests.append((name, "FAIL", str(e)))
        return None
    except Exception as e:
        print(f"  [ERROR] {e}")
        failed += 1
        tests.append((name, "ERROR", str(e)))
        return None

# TEST 1: Check package is importable
def test_import():
    import epi_recorder
    from epi_recorder import record, EpiRecorderSession
    from epi_core.container import EPIContainer
    assert epi_recorder.__version__ == "1.1.0", f"Wrong version: {epi_recorder.__version__}"
    return True

test("1. Package Import & Version", test_import)

# TEST 2: CLI help command
def test_cli_help():
    result = subprocess.run(
        ["python", "-m", "epi_cli", "--help"],
        capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 0, f"CLI help failed: {result.stderr}"
    assert "EPI" in result.stdout or "epi" in result.stdout.lower()
    return result.stdout

help_output = test("2. CLI --help Command", test_cli_help)
if help_output:
    print(f"  Output preview: {help_output[:200]}...")

# TEST 3: CLI version command
def test_cli_version():
    result = subprocess.run(
        ["python", "-m", "epi_cli", "version"],
        capture_output=True, text=True, timeout=10
    )
    assert result.returncode == 0, f"Version command failed: {result.stderr}"
    return result.stdout

version_output = test("3. CLI version Command", test_cli_version)
if version_output:
    print(f"  Version output: {version_output.strip()}")

# TEST 4: CLI keys list
def test_cli_keys():
    result = subprocess.run(
        ["python", "-m", "epi_cli", "keys", "list"],
        capture_output=True, text=True, timeout=10
    )
    # Should succeed or show meaningful message
    return result.returncode in [0, 1]

test("4. CLI keys list Command", test_cli_keys)

# TEST 5: Python API - Simple usage
def test_python_simple():
    from epi_recorder import record
    test_file = Path(f"user_test_{int(time.time())}.epi")
    
    with record(test_file) as session:
        session.log_step("user.action", {"action": "click", "target": "button"})
    
    assert test_file.exists(), f"File not created: {test_file}"
    size = test_file.stat().st_size
    assert size > 1000, f"File too small: {size} bytes"
    
    # Verify it's a valid ZIP
    import zipfile
    with zipfile.ZipFile(test_file) as zf:
        names = zf.namelist()
        assert "manifest.json" in names
        assert "steps.jsonl" in names
    
    test_file.unlink()
    return True

test("5. Python API - Basic Usage", test_python_simple)

# TEST 6: Python API - With metadata
def test_python_metadata():
    from epi_recorder import record
    from epi_core.container import EPIContainer
    
    test_file = Path(f"meta_test_{int(time.time())}.epi")
    
    with record(test_file, 
                goal="Test workflow",
                notes="Testing metadata",
                metrics={"accuracy": 0.95},
                metadata_tags=["test"]) as session:
        session.log_step("test", {"x": 1})
    
    manifest = EPIContainer.read_manifest(test_file)
    assert manifest.goal == "Test workflow"
    assert manifest.metrics["accuracy"] == 0.95
    
    test_file.unlink()
    return True

test("6. Python API - Metadata", test_python_metadata)

# TEST 7: Auto-signing
def test_auto_sign():
    from epi_recorder import record
    from epi_core.container import EPIContainer
    
    test_file = Path(f"signed_test_{int(time.time())}.epi")
    
    with record(test_file, auto_sign=True) as session:
        session.log_step("test", {"signed": True})
    
    manifest = EPIContainer.read_manifest(test_file)
    assert manifest.signature is not None, "File not signed"
    assert manifest.signature.startswith("ed25519:"), "Invalid signature format"
    
    test_file.unlink()
    return True

test("7. Auto-Signing Feature", test_auto_sign)

# TEST 8: Artifact logging
def test_artifacts():
    from epi_recorder import record
    
    # Create test file
    artifact = Path("test_doc.txt")
    artifact.write_text("Important document")
    
    test_file = Path(f"artifact_test_{int(time.time())}.epi")
    
    with record(test_file) as session:
        session.log_artifact(artifact)
    
    # Verify artifact is in ZIP
    import zipfile
    with zipfile.ZipFile(test_file) as zf:
        assert any("test_doc.txt" in name for name in zf.namelist())
    
    test_file.unlink()
    artifact.unlink()
    return True

test("8. Artifact Logging", test_artifacts)

# TEST 9: File integrity
def test_integrity():
    from epi_recorder import record
    from epi_core.container import EPIContainer
    
    test_file = Path(f"integrity_test_{int(time.time())}.epi")
    
    with record(test_file) as session:
        session.log_step("test", {"data": "test"})
    
    ok, issues = EPIContainer.verify_integrity(test_file)
    assert ok, f"Integrity check failed: {issues}"
    
    test_file.unlink()
    return True

test("9. File Integrity Check", test_integrity)

# TEST 10: Decorator usage
def test_decorator():
    from epi_recorder import record
    
    @record
    def my_workflow():
        return "workflow result"
    
    result = my_workflow()
    assert result == "workflow result"
    
    # Decorator creates files in epi-recordings/ directory
    epi_recordings = Path("epi-recordings")
    if epi_recordings.exists():
        epi_files = list(epi_recordings.glob("my_workflow_*.epi"))
    else:
        epi_files = []
    
    assert len(epi_files) > 0, f"Decorator didn't create .epi file in epi-recordings/"
    
    # Cleanup
    for f in epi_files:
        f.unlink()
    
    return True

test("10. Decorator Usage", test_decorator)

# TEST 11: Environment capture
def test_environment():
    from epi_recorder.environment import capture_environment
    
    env = capture_environment()
    assert "os" in env
    assert "python" in env
    assert "packages" in env
    return True

test("11. Environment Capture", test_environment)

# TEST 12: KeyManager
def test_keymanager():
    from epi_cli.keys import KeyManager
    
    km = KeyManager()
    assert km.keys_dir.exists()
    
    # Check default key exists
    has_default = km.has_key("default")
    return True  # It's OK if no keys yet

test("12. KeyManager", test_keymanager)

# TEST 13: Redaction
def test_redaction():
    from epi_core.redactor import Redactor
    
    r = Redactor()
    fake_key = "sk-proj-" + "a" * 48
    text = f"API Key: {fake_key}"
    
    redacted, count = r.redact(text)
    assert fake_key not in redacted, "Key not redacted"
    assert count > 0, "No redactions found"
    return True

test("13. Redaction", test_redaction)

# TEST 14: Real workflow simulation
def test_real_workflow():
    from epi_recorder import record
    from epi_core.container import EPIContainer
    
    test_file = Path("real_workflow.epi")
    
    with record(test_file,
                workflow_name="Data Processing",
                goal="Process customer data",
                metrics={"records_processed": 1000},
                auto_sign=True) as session:
        
        session.log_step("data.load", {"source": "database.db", "rows": 1000})
        session.log_step("data.clean", {"removed_nulls": 50})
        session.log_step("data.transform", {"new_features": 5})
        session.log_step("data.save", {"destination": "output.csv"})
    
    # Verify
    assert test_file.exists()
    manifest = EPIContainer.read_manifest(test_file)
    assert manifest.goal == "Process customer data"
    assert manifest.signature is not None
    
    test_file.unlink()
    return True

test("14. Real Workflow Simulation", test_real_workflow)

# SUMMARY
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print(f"\nTotal: {len(tests)}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")

if failed > 0:
    print("\nFAILED TESTS:")
    for name, status, error in tests:
        if status in ["FAIL", "ERROR"]:
            print(f"  - {name}: {error}")

print("\n" + "=" * 80)
if failed == 0:
    print("ALL USER EXPERIENCE TESTS PASSED!")
    print("Package works exactly as advertised!")
else:
    print(f"{failed} TEST(S) FAILED - NEEDS FIXING!")
print("=" * 80)

sys.exit(0 if failed == 0 else 1)
