#!/usr/bin/env python3
"""Quick test to verify Chronyx structure"""
import os
import sys

print("🌀 CHRONYX - Structure Test\n")
print("="*60)
print(f"✅ Python version: {sys.version.split()[0]}")

files_to_check = [
    "cli.py", "core/agent_base.py", "core/single_agent.py",
    "templates/restaurant.py", "templates/consulting.py",
    "config/settings.py", "requirements.txt", "README.md"
]

print("\n📁 Files:")
all_good = True
for file in files_to_check:
    exists = os.path.exists(file)
    status = "✅" if exists else "❌"
    print(f"  {status} {file}")
    all_good = all_good and exists

print("\n" + "="*60)
if all_good:
    print("✅ ALL CHECKS PASSED!")
    print("\n🚀 Next: pip install -r requirements.txt")
else:
    print("❌ SOME FILES MISSING!")
print("="*60)
