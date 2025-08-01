import subprocess
import sys
import os

def run_tests():
    """Run all tests using pytest"""
    try:
        # Change to project root directory
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        os.chdir(project_root)
        
        print("Running tests with pytest...")
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short"
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
            sys.exit(result.returncode)
            
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)