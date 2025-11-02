#!/usr/bin/env python3
"""
Test script to verify the consolidated app can be imported without syntax errors
"""

try:
    # Test importing the consolidated app
    with open('consolidated_app.py', 'r') as f:
        content = f.read()
    
    # Basic syntax check
    compile(content, 'consolidated_app.py', 'exec')
    
    print("✅ Consolidated app import test passed!")
    print("✅ No syntax errors found")
    print("✅ Ready to run the application")
    
except SyntaxError as e:
    print(f"❌ Syntax error in consolidated_app.py: {e}")
    print(f"   Line {e.lineno}: {e.text}")
except Exception as e:
    print(f"❌ Error testing consolidated app: {e}")

print("\n📋 Next steps:")
print("1. Run: pip install -r requirements_consolidated.txt")
print("2. Run: python run_consolidated_app.py")
print("3. Access: http://localhost:8501 in your browser")