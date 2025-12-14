"""
FIXED: Test metadata handling correctly
"""
from epi_recorder import record
from epi_core.container import EPIContainer
from pathlib import Path
import time

test_file = Path(f"test_metadata_{int(time.time())}.epi")

with record(test_file, 
            goal="Test Goal",
            notes="Test Notes",
            metrics={"accuracy": 0.95},
            approved_by="tester@test.com",
            metadata_tags=["tag1", "tag2"],
            auto_sign=False) as session:
    session.log_step("test", {"x": 1})

# Read manifest
manifest = EPIContainer.read_manifest(test_file)

print(f"Goal: {manifest.goal}")
print(f"Notes: {manifest.notes}")
print(f"Metrics: {manifest.metrics}")
print(f"Approved by: {manifest.approved_by}")
print(f"Tags: {manifest.tags}")

# Verify
assert manifest.goal == "Test Goal", f"Goal mismatch: {manifest.goal}"
assert manifest.notes == "Test Notes", f"Notes mismatch: {manifest.notes}"
assert manifest.metrics == {"accuracy": 0.95}, f"Metrics mismatch: {manifest.metrics}"
assert manifest.approved_by == "tester@test.com", f"approved_by mismatch: {manifest.approved_by}"
assert manifest.tags == ["tag1", "tag2"], f"Tags mismatch: {manifest.tags}"

test_file.unlink()
print("\n[PASS] Metadata handling works correctly!")
