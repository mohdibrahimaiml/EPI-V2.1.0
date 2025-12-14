"""
Test steps recording to see actual format
"""
from epi_recorder import record
from pathlib import Path
import time
import zipfile
import json

test_file = Path(f"test_steps_{int(time.time())}.epi")

with record(test_file, auto_sign=False) as session:
    session.log_step("step1", {"data": "first"})
    session.log_step("step2", {"data": "second"})

# Read steps from ZIP
with zipfile.ZipFile(test_file) as zf:
    steps_data = zf.read("steps.jsonl").decode('utf-8')

print("Steps content:")
print(steps_data)
print("\nParsing steps:")

lines = [line for line in steps_data.strip().split('\n') if line]
for i, line in enumerate(lines):
    step = json.loads(line)
    print(f"Step {i}: kind='{step['kind']}', content={step['content']}")

test_file.unlink()
