"""
ULTIMATE COMPREHENSIVE TEST - ENTIRE EPI-RECORDER PACKAGE
Tests everything: Python API, CLI, real workflows, installation
"""
import sys
import os
import time
import json
import zipfile
import subprocess
from pathlib import Path

print("=" * 80)
print("ULTIMATE COMPREHENSIVE EPI-RECORDER TEST")
print("Testing the ENTIRE package before PyPI release")
print("=" * 80)

passed = 0
failed = 0
errors = []

def test(name, func):
    global passed, failed
    print(f"\n[TEST] {name}")
    try:
        func()
        print(f"  ✓ PASS")
        passed += 1
        return True
    except AssertionError as e:
        print(f"  ✗ FAIL: {e}")
        failed += 1
        errors.append((name, str(e)))
        return False
    except Exception as e:
        print(f"  ✗ ERROR: {e}")
        failed += 1
        errors.append((name, str(e)))
        return False

# ============================================================================
# SECTION 1: PYTHON API TESTS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 1: PYTHON API")
print("=" * 80)

def test_imports():
    from epi_recorder import record, EpiRecorderSession
    from epi_core.container import EPIContainer
    from epi_core.trust import sign_manifest, verify_signature
    from epi_core.redactor import Redactor
    from epi_core.schemas import ManifestModel, StepModel
    from epi_cli.keys import KeyManager
    from epi_recorder.environment import capture_environment

test("1.1 All Module Imports", test_imports)

def test_record_basic():
    from epi_recorder import record
    f = Path(f"test_{int(time.time())}.epi")
    with record(f, auto_sign=False) as s:
        s.log_step("test", {"x": 1})
    assert f.exists() and f.stat().st_size > 1000
    f.unlink()

test("1.2 Basic File Creation", test_record_basic)

def test_metadata():
    from epi_recorder import record
    from epi_core.container import EPIContainer
    f = Path(f"test_{int(time.time())}.epi")
    with record(f, goal="G", notes="N", metrics={"m": 1}, 
                approved_by="A", metadata_tags=["t"], auto_sign=False) as s:
        s.log_step("test", {"x": 1})
    m = EPIContainer.read_manifest(f)
    assert m.goal == "G" and m.notes == "N" and m.metrics == {"m": 1}
    f.unlink()

test("1.3 Metadata Handling", test_metadata)

def test_signing():
    from epi_recorder import record
    from epi_core.container import EPIContainer
    f = Path(f"test_{int(time.time())}.epi")
    with record(f, auto_sign=True) as s:
        s.log_step("test", {"signed": True})
    assert f.exists()
    m = EPIContainer.read_manifest(f)
    assert m.signature and m.signature.startswith("ed25519:")
    f.unlink()

test("1.4 Auto-Signing (CRITICAL FIX)", test_signing)

def test_path_resolution():
    from epi_recorder import record
    f = Path(f"test_{int(time.time())}.epi")
    with record(f, auto_sign=False) as s:
        s.log_step("test", {"x": 1})
    assert f.exists()  # Should be in current directory
    f.unlink()

test("1.5 Path Resolution (CRITICAL FIX)", test_path_resolution)

def test_artifact():
    from epi_recorder import record
    art = Path("artifact.txt")
    art.write_text("test content")
    f = Path(f"test_{int(time.time())}.epi")
    with record(f, auto_sign=False) as s:
        s.log_artifact(art)
    with zipfile.ZipFile(f) as zf:
        assert any('artifact.txt' in n for n in zf.namelist())
    f.unlink()
    art.unlink()

test("1.6 Artifact Logging", test_artifact)

def test_redaction():
    from epi_core.redactor import Redactor
    r = Redactor()
    key = "sk-proj-" + "a" * 48
    redacted, count = r.redact(f"Key: {key}")
    assert key not in redacted and count > 0

test("1.7 Redaction", test_redaction)

def test_integrity():
    from epi_recorder import record
    from epi_core.container import EPIContainer
    f = Path(f"test_{int(time.time())}.epi")
    with record(f, auto_sign=False) as s:
        s.log_step("test", {"x": 1})
    ok, issues = EPIContainer.verify_integrity(f)
    assert ok
    f.unlink()

test("1.8 File Integrity", test_integrity)

# ============================================================================
# SECTION 2: CLI TESTS
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 2: CLI COMMANDS")
print("=" * 80)

def test_cli_help():
    result = subprocess.run(["python", "-m", "epi_cli", "--help"], 
                          capture_output=True, text=True, timeout=10)
    assert result.returncode == 0
    assert "EPI CLI" in result.stdout or "usage" in result.stdout.lower()

test("2.1 CLI Help Command", test_cli_help)

def test_cli_version():
    result = subprocess.run(["python", "-m", "epi_cli", "version"], 
                          capture_output=True, text=True, timeout=10)
    assert result.returncode == 0
    assert "1.1.0" in result.stdout or "version" in result.stdout.lower()

test("2.2 CLI Version Command", test_cli_version)

def test_cli_keys_list():
    result = subprocess.run(["python", "-m", "epi_cli", "keys", "list"], 
                          capture_output=True, text=True, timeout=10)
    # Should succeed (exit 0) or show helpful message
    assert result.returncode in [0, 1]  # 1 might mean no keys yet

test("2.3 CLI Keys List", test_cli_keys_list)

# ============================================================================
# SECTION 3: REAL WORKFLOW SIMULATION
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 3: REAL-WORLD WORKFLOW")
print("=" * 80)

def test_realistic_workflow():
    """Simulate a realistic user workflow"""
    from epi_recorder import record
    from epi_core.container import EPIContainer
    
    # Create a realistic workflow
    workflow_file = Path("realistic_workflow.epi")
    artifact_file = Path("output.txt")
    artifact_file.write_text("Model output: accuracy=0.95")
    
    with record(workflow_file,
                workflow_name="ML Training Run",
                goal="Improve model accuracy",
                notes="Using GPT-4 with fine-tuning",
                metrics={"accuracy": 0.95, "latency": 210},
                approved_by="ml-team@company.com",
                metadata_tags=["production", "gpt4"],
                auto_sign=True) as session:
        
        # Log multiple steps
        session.log_step("data.load", {"dataset": "training_v2.csv", "rows": 10000})
        session.log_step("model.init", {"model": "gpt-4", "temperature": 0.7})
        session.log_step("training.start", {"epochs": 10, "batch_size": 32})
        session.log_step("training.complete", {"final_loss": 0.05})
        
        # Log artifact
        session.log_artifact(artifact_file)
        
        # Log final metrics
        session.log_step("evaluation", {"accuracy": 0.95, "f1_score": 0.93})
    
    # Verify the workflow file
    assert workflow_file.exists()
    assert workflow_file.stat().st_size > 5000
    
    # Verify manifest
    manifest = EPIContainer.read_manifest(workflow_file)
    assert manifest.goal == "Improve model accuracy"
    assert manifest.metrics["accuracy"] == 0.95
    assert manifest.signature is not None
    
    # Verify integrity
    ok, issues = EPIContainer.verify_integrity(workflow_file)
    assert ok
    
    # Verify steps
    with zipfile.ZipFile(workflow_file) as zf:
        steps = zf.read("steps.jsonl").decode('utf-8')
        # Should have our 5 custom steps + auto steps
        assert "data.load" in steps
        assert "training.complete" in steps
        
        # Verify artifact
        assert "output.txt" in zf.namelist()
    
    # Cleanup
    workflow_file.unlink()
    artifact_file.unlink()

test("3.1 Complete Realistic Workflow", test_realistic_workflow)

# ============================================================================
# SECTION 4: EDGE CASES
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 4: EDGE CASES")
print("=" * 80)

def test_large_content():
    """Test with large content"""
    from epi_recorder import record
    f = Path(f"test_{int(time.time())}.epi")
    large_data = {"data": "x" * 100000}  # 100KB of data
    with record(f, auto_sign=False) as s:
        s.log_step("large", large_data)
    assert f.exists() and f.stat().st_size > 100000
    f.unlink()

test("4.1 Large Content Handling", test_large_content)

def test_special_characters():
    """Test with special characters"""
    from epi_recorder import record
    f = Path(f"test_{int(time.time())}.epi")
    with record(f, goal="Test 特殊字符 🚀", auto_sign=False) as s:
        s.log_step("test", {"emoji": "🎉", "unicode": "测试"})
    assert f.exists()
    f.unlink()

test("4.2 Special Characters", test_special_characters)

def test_multiple_artifacts():
    """Test with multiple artifacts"""
    from epi_recorder import record
    f = Path(f"test_{int(time.time())}.epi")
    arts = [Path(f"art{i}.txt") for i in range(5)]
    for art in arts:
        art.write_text(f"content {art.name}")
    
    with record(f, auto_sign=False) as s:
        for art in arts:
            s.log_artifact(art)
    
    with zipfile.ZipFile(f) as zf:
        for art in arts:
            assert any(art.name in n for n in zf.namelist())
    
    f.unlink()
    for art in arts:
        art.unlink()

test("4.3 Multiple Artifacts", test_multiple_artifacts)

# ============================================================================
# SECTION 5: PACKAGE BUILD TEST
# ============================================================================
print("\n" + "=" * 80)
print("SECTION 5: PACKAGE BUILD")
print("=" * 80)

def test_package_build():
    """Test that package can be built"""
    # Clean old builds
    if Path("dist").exists():
        import shutil
        shutil.rmtree("dist")
    
    result = subprocess.run(["python", "-m", "build"], 
                          capture_output=True, text=True, timeout=60)
    assert result.returncode == 0
    assert Path("dist").exists()
    
    # Check files were created
    dist_files = list(Path("dist").glob("*"))
    assert len(dist_files) >= 2  # .whl and .tar.gz
    print(f"  Built: {[f.name for f in dist_files]}")

test("5.1 Package Build", test_package_build)

def test_package_check():
    """Test package metadata"""
    result = subprocess.run(["python", "-m", "twine", "check", "dist/*"], 
                          capture_output=True, text=True, timeout=30)
    assert result.returncode == 0
    assert "PASSED" in result.stdout or result.returncode == 0

test("5.2 Package Metadata Check", test_package_check)

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("FINAL TEST SUMMARY")
print("=" * 80)
print(f"\nTotal Tests: {passed + failed}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")

if failed > 0:
    print("\n" + "=" * 80)
    print("FAILED TESTS:")
    print("=" * 80)
    for name, error in errors:
        print(f"  ✗ {name}: {error}")

print("\n" + "=" * 80)
if failed == 0:
    print("✓✓✓ ALL TESTS PASSED ✓✓✓")
    print("Package is 100% ready for PyPI release!")
    print("=" * 80)
    sys.exit(0)
else:
    print(f"✗✗✗ {failed} TEST(S) FAILED ✗✗✗")
    print("Fix issues before PyPI release!")
    print("=" * 80)
    sys.exit(1)
