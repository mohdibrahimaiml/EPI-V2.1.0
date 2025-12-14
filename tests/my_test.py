# -*- coding: utf-8 -*-
"""
Your First EPI Recording - Simple Test

Run this to see the Python API in action!
"""

import sys
import io

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from epi_recorder import record

print("🎯 Creating your first EPI recording...")
print()

with record("my_first_recording.epi", workflow_name="My First Test"):
    print("✅ Recording started!")
    print()
    
    # Do some simple calculations
    print("📊 Running calculations...")
    result = sum(range(1, 101))
    print(f"   Sum of 1-100: {result}")
    
    # Simulate some work
    squares = [x**2 for x in range(1, 11)]
    print(f"   First 10 squares: {squares}")
    
    print()
    print("✅ Recording completed!")

print()
print("🎉 Success! Your .epi file has been created.")
print()
print("📁 File created: my_first_recording.epi")
print()
print("Next steps:")
print("1. Verify it:")
print("   python -m epi_cli.main verify my_first_recording.epi")
print()
print("2. View it:")
print("   python -m epi_cli.main view my_first_recording.epi")
