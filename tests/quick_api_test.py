"""Quick API validation test."""
from pathlib import Path
import tempfile
from epi_recorder import record

temp = Path(tempfile.mktemp(suffix='.epi'))
try:
    with record(temp, workflow_name='test'):
        pass
    print(f'✓ API works: Created {temp.exists()}')
    if temp.exists():
        print(f'✓ File size: {temp.stat().st_size} bytes')
        temp.unlink()
except Exception as e:
    print(f'✗ API error: {e}')
