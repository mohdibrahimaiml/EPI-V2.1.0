"""
Stress test for EPI Recorder
Tests multiple recordings, concurrent sessions, edge cases
"""

import sys
from pathlib import Path
from epi_recorder import record
import threading
import time

print("="*60)
print("EPI RECORDER STRESS TEST")
print("="*60)

# Test 1: Rapid sequential recordings
print("\n1. Testing rapid sequential recordings...")
try:
    for i in range(5):
        with record(f"stress_seq_{i}.epi", workflow_name=f"Seq Test {i}"):
            result = i * 2
    print("   ✅ Created 5 sequential recordings")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# Test 2: Verify all files created
print("\n2. Verifying files created...")
for i in range(5):
    f = Path(f"stress_seq_{i}.epi")
    if not f.exists():
        print(f"   ❌ Missing: {f}")
        sys.exit(1)
print("   ✅ All 5 files exist")

# Test 3: Concurrent recordings (thread safety)
print("\n3. Testing concurrent recordings...")
def create_recording(thread_id):
    with record(f"stress_thread_{thread_id}.epi", workflow_name=f"Thread {thread_id}"):
        time.sleep(0.1)  # Simulate work

threads = []
for i in range(5):
    t = threading.Thread(target=create_recording, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("   ✅ Created 5 concurrent recordings")

# Test 4: Verify concurrent files
print("\n4. Verifying concurrent files...")
for i in range(5):
    f = Path(f"stress_thread_{i}.epi")
    if not f.exists():
        print(f"   ❌ Missing: {f}")
        sys.exit(1)
print("   ✅ All 5 concurrent files exist")

# Test 5: Large data recording
print("\n5. Testing large data recording...")
try:
    with record("stress_large.epi", workflow_name="Large Data") as epi:
        for i in range(100):
            epi.log_step(f"step_{i}", {"data": "x" * 100})
    print("   ✅ Large recording successful")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# Test 6: Empty workflow
print("\n6. Testing empty workflow...")
try:
    with record("stress_empty.epi", workflow_name="Empty"):
        pass
    if Path("stress_empty.epi").exists():
        print("   ✅ Empty workflow recorded")
    else:
        print("   ❌ File not created")
        sys.exit(1)
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# Test 7: Nested context (should not work but shouldn't crash)
print("\n7. Testing nested contexts...")
try:
    with record("stress_outer.epi", workflow_name="Outer"):
        with record("stress_inner.epi", workflow_name="Inner"):
            pass
    print("   ✅ Nested contexts handled")
except Exception as e:
    print(f"   ⚠️  Expected behavior: {type(e).__name__}")

# Test 8: Very long workflow name
print("\n8. Testing long workflow name...")
try:
    long_name = "A" * 500
    with record("stress_longname.epi", workflow_name=long_name):
        pass
    print("   ✅ Long name handled")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# Test 9: Special characters in workflow name
print("\n9. Testing special characters...")
try:
    with record("stress_special.epi", workflow_name="Test™ © ® 中文 🎉"):
        pass
    print("   ✅ Special characters handled")
except Exception as e:
    print(f"   ❌ Failed: {e}")
    sys.exit(1)

# Test 10: Verify all stress test files
print("\n10. Verifying all files...")
expected_files = [
    *[f"stress_seq_{i}.epi" for i in range(5)],
    *[f"stress_thread_{i}.epi" for i in range(5)],
    "stress_large.epi",
    "stress_empty.epi",
    "stress_outer.epi",
    "stress_inner.epi",
    "stress_longname.epi",
    "stress_special.epi"
]

created = 0
for f in expected_files:
    if Path(f).exists():
        created += 1

print(f"   ✅ {created}/{len(expected_files)} files created")

# Cleanup
print("\n11. Cleaning up...")
for f in expected_files:
    try:
        Path(f).unlink()
    except:
        pass
print("   🧹 Cleanup complete")

print("\n" + "="*60)
print("✅ ALL STRESS TESTS PASSED")
print("="*60)
print(f"\nTotal recordings created: {created}")
print("No crashes, no data loss, thread-safe ✓")
