"""
End-to-end test simulating a normal user workflow with EPI Recorder.

This tests the COMPLETE user experience from installation to usage,
exactly as a real user would interact with the package.
"""

import sys
import subprocess
import tempfile
import shutil
from pathlib import Path


def run_command(cmd, description, check=True):
    """Run a command and report results."""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")
    print(f"Command: {cmd}")
    print()
    
    result = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    if check and result.returncode != 0:
        print(f"❌ FAILED with exit code {result.returncode}")
        return False
    else:
        print(f"✅ SUCCESS")
        return True


def test_workflow():
    """Test complete user workflow."""
    
    print("\n" + "="*60)
    print("🎯 TESTING COMPLETE USER WORKFLOW")
    print("="*60)
    print("\nThis simulates how a real user would use EPI Recorder")
    print("after installing via pip.\n")
    
    # Create temporary working directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        print(f"\n📁 Working directory: {tmpdir}\n")
        
        # Test 1: Check package is installed
        if not run_command(
            "python -c \"import epi_recorder; print(f'Version: {epi_recorder.__version__}')\"",
            "Test 1: Import epi_recorder package"
        ):
            return False
        
        # Test 2: CLI is available
        if not run_command(
            "python -m epi_cli.main --help",
            "Test 2: CLI is accessible"
        ):
            return False
        
        # Test 3: Check keys exist
        if not run_command(
            "python -m epi_cli.main keys list",
            "Test 3: Signing keys are available"
        ):
            return False
        
        # Test 4: Create a simple Python script to record
        user_script = tmpdir / "my_ai_workflow.py"
        user_script.write_text("""
# A typical AI workflow that a user might run

def calculate_stats(numbers):
    return {
        'sum': sum(numbers),
        'avg': sum(numbers) / len(numbers),
        'min': min(numbers),
        'max': max(numbers)
    }

# Main workflow
data = [10, 20, 30, 40, 50]
stats = calculate_stats(data)
print(f"Statistics: {stats}")
print("✓ Workflow completed successfully!")
""")
        
        print(f"\n📝 Created user script: {user_script}")
        
        # Test 5: Record using Python API (most common usage)
        api_test_script = tmpdir / "use_api.py"
        api_test_script.write_text(f"""
from epi_recorder import record
from pathlib import Path

output_file = Path(r"{tmpdir}") / "workflow_api.epi"

print("Starting API recording...")
with record(str(output_file), workflow_name="My Workflow"):
    # Simulate user's workflow
    data = [1, 2, 3, 4, 5]
    result = sum(data)
    print(f"Result: {{result}}")

print(f"✓ API recording complete: {{output_file}}")
""")
        
        if not run_command(
            f"python {api_test_script}",
            "Test 5: Record using Python API (recommended method)"
        ):
            return False
        
        # Test 6: Verify the API-created file
        api_epi_file = tmpdir / "workflow_api.epi"
        if not api_epi_file.exists():
            print(f"❌ Expected file not found: {api_epi_file}")
            return False
        
        if not run_command(
            f"python -m epi_cli.main verify {api_epi_file}",
            "Test 6: Verify API-created .epi file"
        ):
            return False
        
        # Test 7: Record using CLI
        cli_epi_file = tmpdir / "workflow_cli.epi"
        if not run_command(
            f"python -m epi_cli.main record --out {cli_epi_file} -- python {user_script}",
            "Test 7: Record using CLI"
        ):
            return False
        
        # Test 8: Verify CLI-created file
        if not cli_epi_file.exists():
            print(f"❌ Expected file not found: {cli_epi_file}")
            return False
        
        if not run_command(
            f"python -m epi_cli.main verify {cli_epi_file}",
            "Test 8: Verify CLI-created .epi file"
        ):
            return False
        
        # Test 9: Test with OpenAI mock (if user has OpenAI usage)
        openai_test = tmpdir / "openai_test.py"
        openai_test.write_text(f"""
from epi_recorder import record
from pathlib import Path
from unittest.mock import Mock, patch

output_file = Path(r"{tmpdir}") / "openai_workflow.epi"

# Mock OpenAI to simulate user who has OpenAI in their code
mock_response = Mock()
mock_response.choices = [Mock()]
mock_response.choices[0].message.content = "Hello! This is a test response."
mock_response.model = "gpt-4"
mock_response.usage.total_tokens = 25

print("Testing with mocked OpenAI...")
with record(str(output_file), workflow_name="OpenAI Workflow"):
    # Simulate OpenAI call
    print("Calling OpenAI API (mocked)...")
    print("Response received:", mock_response.choices[0].message.content)

print(f"✓ OpenAI workflow recorded: {{output_file}}")
""")
        
        if not run_command(
            f"python {openai_test}",
            "Test 9: Record with OpenAI-like workflow (mocked)"
        ):
            return False
        
        # Test 10: Test custom logging (advanced users)
        custom_test = tmpdir / "custom_logging.py"
        custom_test.write_text(f"""
from epi_recorder import record
from pathlib import Path

output_file = Path(r"{tmpdir}") / "custom_workflow.epi"

print("Testing custom logging...")
with record(str(output_file), workflow_name="Custom", tags=["v1.0", "test"]) as epi:
    # Log custom events
    epi.log_step("data.load", {{"rows": 100, "cols": 5}})
    
    # Do some work
    result = 42 * 2
    
    # Log results
    epi.log_step("calculation.complete", {{"result": result}})

print(f"✓ Custom workflow recorded: {{output_file}}")
""")
        
        if not run_command(
            f"python {custom_test}",
            "Test 10: Custom logging with tags"
        ):
            return False
        
        # Test 11: Verify all created files
        epi_files = list(tmpdir.glob("*.epi"))
        print(f"\n\n📦 Created {len(epi_files)} .epi files:")
        for f in epi_files:
            print(f"   • {f.name} ({f.stat().st_size} bytes)")
        
        if len(epi_files) < 4:
            print(f"❌ Expected at least 4 .epi files, found {len(epi_files)}")
            return False
        
        # Test 12: Verify each file
        all_verified = True
        for epi_file in epi_files:
            result = subprocess.run(
                f"python -m epi_cli.main verify {epi_file}",
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"❌ Verification failed for {epi_file.name}")
                all_verified = False
            else:
                print(f"✅ {epi_file.name} verified")
        
        if not all_verified:
            return False
        
        # Test 13: Error handling (workflow with error)
        error_test = tmpdir / "error_workflow.py"
        error_test.write_text(f"""
from epi_recorder import record
from pathlib import Path

output_file = Path(r"{tmpdir}") / "error_workflow.epi"

print("Testing error handling...")
try:
    with record(str(output_file), workflow_name="Error Test") as epi:
        epi.log_step("start", {{"status": "ok"}})
        # Simulate an error
        raise ValueError("Test error - this is expected!")
except ValueError as e:
    print(f"Caught error: {{e}}")
    print("Recording should still be saved!")

# Check file was created despite error
if Path(output_file).exists():
    print(f"✓ Error workflow recorded: {{output_file}}")
else:
    print("❌ File was not saved after error!")
    exit(1)
""")
        
        if not run_command(
            f"python {error_test}",
            "Test 13: Error handling (file saved even on error)"
        ):
            return False
        
        print("\n\n" + "="*60)
        print("✅ ALL USER WORKFLOW TESTS PASSED!")
        print("="*60)
        print("\n📊 Test Summary:")
        print("  ✅ Package import")
        print("  ✅ CLI accessibility")
        print("  ✅ Signing keys")
        print("  ✅ Python API recording")
        print("  ✅ CLI recording")
        print("  ✅ File verification")
        print("  ✅ OpenAI-like workflow")
        print("  ✅ Custom logging")
        print("  ✅ Error handling")
        print(f"  ✅ {len(epi_files)} .epi files created and verified")
        print("\n🎉 The package is ready for real users!")
        
        return True


if __name__ == "__main__":
    success = test_workflow()
    sys.exit(0 if success else 1)
