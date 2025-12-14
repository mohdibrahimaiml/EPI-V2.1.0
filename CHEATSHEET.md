╔══════════════════════════════════════════════════════════════════════════╗
║                     EPI RECORDER - CHEAT SHEET                           ║
║                  Run These Commands in PowerShell                        ║
╚══════════════════════════════════════════════════════════════════════════╝

📍 WHERE TO RUN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Open PowerShell:
  • Press Win + X → Click "Windows Terminal" or "PowerShell"
  • Or press Win + R → Type "powershell" → Press Enter
  
  Navigate to project:
  cd C:\Users\dell\epi-recorder

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔑 KEY MANAGEMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  List all keys:
  python -m epi_cli.main keys list

  Generate new key:
  python -m epi_cli.main keys generate --name mykey

  Export public key:
  python -m epi_cli.main keys export --name default

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📹 RECORDING (Not fully implemented yet - stub only)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Record a Python script:
  python -m epi_cli.main record --out demo.epi -- python your_script.py

  Run demo workflow:
  python demo_workflow.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ VERIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Verify a .epi file:
  python -m epi_cli.main verify demo.epi

  Verify with verbose output:
  python -m epi_cli.main verify demo.epi --verbose

  Verify with JSON output:
  python -m epi_cli.main verify demo.epi --json

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

👁️  VIEWING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  View in browser:
  python -m epi_cli.main view demo.epi

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧪 TESTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Run all tests:
  python -m pytest tests\

  Run tests with coverage:
  python -m pytest tests\ -q

  View coverage report:
  start htmlcov\index.html

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 HELP & DOCS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Get help:
  python -m epi_cli.main --help

  Command-specific help:
  python -m epi_cli.main keys --help
  python -m epi_cli.main verify --help
  python -m epi_cli.main view --help

  Read documentation:
  • QUICKSTART.md      - 5-minute overview
  • USAGE_GUIDE.md     - Complete guide with examples
  • WHERE_TO_RUN.md    - Where to run these commands
  • COVERAGE_REPORT.md - Test suite details

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 QUICK START (Copy-Paste This!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  # Test installation
  python -c "import epi_cli; print('✅ EPI is ready!')"

  # List your keys
  python -m epi_cli.main keys list

  # Run the demo
  python demo_workflow.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 PROJECT STATUS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ✅ Core modules:        99.7% coverage (container, crypto, redactor)
  ✅ CLI commands:        78.5% coverage (keys, verify, view)
  ✅ Test suite:          174 tests, all passing
  ⏸️  Recording feature:   Stub implementation (future work)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 REMEMBER
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  • Run commands in PowerShell (the terminal you're using now)
  • No special application needed
  • Keys stored at: C:\Users\dell\.epi\keys\
  • All commands start with: python -m epi_cli.main

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Need help? Read WHERE_TO_RUN.md for detailed visual guide!
