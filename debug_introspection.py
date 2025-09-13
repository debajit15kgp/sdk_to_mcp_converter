#!/usr/bin/env python3
"""
Debug script to test SDK introspection.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from introspector import SDKIntrospector

def test_github_introspection():
    """Test GitHub SDK introspection."""
    print("Testing GitHub SDK introspection...")
    
    introspector = SDKIntrospector()
    
    try:
        sdk_info = introspector.introspect_sdk("github", include_private=False)
        
        print(f"Module: {sdk_info['module_name']}")
        print(f"Classes found: {len(sdk_info['classes'])}")
        print(f"Methods found: {len(sdk_info['methods'])}")
        print(f"Functions found: {len(sdk_info['functions'])}")
        
        if sdk_info['classes']:
            print("\nFirst few classes:")
            for i, cls in enumerate(sdk_info['classes'][:5]):
                print(f"  {i+1}. {cls['name']} - {len(cls['methods'])} methods")
        
        if sdk_info['methods']:
            print("\nFirst few methods:")
            for i, method in enumerate(sdk_info['methods'][:5]):
                print(f"  {i+1}. {method['name']} ({method.get('class_name', 'standalone')})")
        
        return sdk_info
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_github_introspection()
