#!/usr/bin/env python
"""
File cleanup and security test
"""

import os
import sys
from pathlib import Path

def check_sensitive_files_exposed():
    """Check that sensitive files are not exposed"""
    project_root = Path(__file__).parent
    
    # Files that should never be exposed
    sensitive_files = [
        '.env',
        '.env.local',
        '.env.production',
        'db.sqlite3',
        '*.log',
        '*.pyc',
        '__pycache__/',
    ]
    
    # Check if these files are in .gitignore
    gitignore_path = project_root / '.gitignore'
    if gitignore_path.exists():
        with open(gitignore_path, 'r') as f:
            gitignore_content = f.read()
        
        missing_from_gitignore = []
        for sensitive_file in sensitive_files:
            if sensitive_file not in gitignore_content:
                missing_from_gitignore.append(sensitive_file)
        
        if missing_from_gitignore:
            print(f"❌ Missing from .gitignore: {missing_from_gitignore}")
            return False
        else:
            print("✅ All sensitive files properly excluded in .gitignore")
            return True
    else:
        print("❌ .gitignore file not found")
        return False

def check_empty_files():
    """Check for empty files that should be removed"""
    project_root = Path(__file__).parent
    
    empty_files = []
    for root, dirs, files in os.walk(project_root):
        # Skip virtual environments and other ignored directories
        dirs[:] = [d for d in dirs if d not in ['venv', 'env', '__pycache__', '.git']]
        
        for file in files:
            file_path = Path(root) / file
            if file_path.stat().st_size == 0:
                # Skip __init__.py files as they can be legitimately empty
                if file != '__init__.py':
                    empty_files.append(str(file_path.relative_to(project_root)))
    
    if empty_files:
        print(f"⚠️ Empty files found (consider removing):")
        for file in empty_files:
            print(f"  - {file}")
        return False
    else:
        print("✅ No unnecessary empty files found")
        return True

def check_unused_static_files():
    """Check for unused static files"""
    project_root = Path(__file__).parent
    static_dir = project_root / 'static'
    
    if not static_dir.exists():
        print("⚠️ Static directory not found")
        return True
    
    # Check if images directory has only the README
    images_dir = static_dir / 'images'
    if images_dir.exists():
        files = list(images_dir.iterdir())
        if len(files) == 1 and files[0].name == 'README.txt':
            print("⚠️ Static images directory only contains README.txt")
            print("   Add your actual images or remove the directory if not needed")
            return False
        elif len(files) == 0:
            print("⚠️ Static images directory is empty")
            return False
    
    print("✅ Static files directory structure looks good")
    return True

def check_unused_templates():
    """Check for unused template files"""
    project_root = Path(__file__).parent
    templates_dir = project_root / 'templates'
    
    if not templates_dir.exists():
        print("❌ Templates directory not found")
        return False
    
    # All expected template files
    expected_templates = {
        'base.html',
        'main/about.html',
        'main/contact.html',
        'main/home.html',
        'main/resume.html',
        'main/security_dashboard.html',
        'portfolio/portfolio_list.html',
        'portfolio/project_detail.html',
        'blog/blog_list.html',
        'blog/post_detail.html'
    }
    
    # Check if all expected templates exist
    missing_templates = []
    for template in expected_templates:
        template_path = templates_dir / template
        if not template_path.exists():
            missing_templates.append(template)
    
    if missing_templates:
        print(f"❌ Missing expected templates: {missing_templates}")
        return False
    else:
        print("✅ All expected templates are present")
        return True

def run_file_cleanup_tests():
    """Run all file cleanup and security tests"""
    print("🧹 FILE CLEANUP AND SECURITY TEST")
    print("=" * 50)
    
    tests = [
        check_sensitive_files_exposed,
        check_empty_files,
        check_unused_static_files,
        check_unused_templates,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with error: {e}")
            print()
    
    print("=" * 50)
    print(f"File Cleanup Score: {passed}/{total} ({(passed/total)*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL FILE CLEANUP TESTS PASSED!")
        print("\n✅ Your project files are properly organized and secured.")
    else:
        print("⚠️ Some file cleanup tests had issues.")
        print("Please review the warnings and fix as needed.")
    
    return passed == total

if __name__ == '__main__':
    run_file_cleanup_tests()