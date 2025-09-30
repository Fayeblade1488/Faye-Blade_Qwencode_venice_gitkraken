#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script for Qwen CLI Integration
This script tests both GitKraken and Venice AI integration functionality.
"""

import os
import sys
from pathlib import Path

# Add the current directory to the path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent))

from qwen_cli_integrator import QwenCLIIntegrator


def test_gitkraken_integration():
    """Test GitKraken CLI integration"""
    print("Testing GitKraken CLI Integration...")
    
    integrator = QwenCLIIntegrator()
    
    # Check if GitKraken is installed
    if integrator.gitkraken.is_installed():
        print("✓ GitKraken CLI is installed")
        
        # Try to get the version
        result = integrator.gitkraken_command('version')
        if result['success']:
            print(f"✓ GitKraken version: {result.get('stdout', 'Unknown')[:50]}")
        else:
            print(f"✗ Failed to get GitKraken version: {result.get('error', 'Unknown error')}")
        
        # Try to list workspaces
        result = integrator.gitkraken_command('workspace_list')
        if result['success']:
            print("✓ Workspace list command executed successfully")
        else:
            print(f"⚠ Workspace list command failed: {result.get('error', 'Unknown error')}")
            print("  (This is normal if you don't have any workspaces)")
    else:
        print("⚠ GitKraken CLI is not installed or not in PATH")
    
    print()


def test_venice_integration():
    """Test Venice AI integration"""
    print("Testing Venice AI Integration...")
    
    integrator = QwenCLIIntegrator()
    
    # Check if Venice API key is available
    if integrator.venice:
        print("✓ Venice AI is configured with API key")
        
        # Try to list models
        try:
            result = integrator.list_available_models()
            if result['success']:
                print(f"✓ Model listing successful. Found {len(result.get('all_models', []))} total models")
                
                # Show uncensored models if any
                uncensored = result.get('uncensored_models', [])
                if uncensored:
                    print(f"✓ Found {len(uncensored)} uncensored models:")
                    for model in uncensored[:3]:  # Show first 3
                        print(f"  - {model.get('id', 'Unknown ID')}")
                else:
                    print("⚠ No uncensored models found (this may be normal)")
            else:
                print(f"✗ Model listing failed: {result.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"✗ Error listing models: {e}")
    else:
        print("⚠ Venice AI not configured - please set VENICE_API_KEY environment variable")
    
    print()


def test_help_output():
    """Test that help output works"""
    print("Testing help output...")
    
    # Test main help
    import subprocess
    result = subprocess.run([sys.executable, 'qwen_cli_integrator.py', '--help'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0 and 'usage:' in result.stdout.lower():
        print("✓ Main help output works correctly")
    else:
        print("✗ Main help output failed")
        if result.stderr:
            print(f"  Error: {result.stderr}")
    
    # Test GitKraken help
    result = subprocess.run([sys.executable, 'qwen_cli_integrator.py', 'gitkraken', '--help'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0 and 'usage:' in result.stdout.lower():
        print("✓ GitKraken help output works correctly")
    else:
        print("✗ GitKraken help output failed")
        if result.stderr:
            print(f"  Error: {result.stderr}")
    
    # Test Venice help
    result = subprocess.run([sys.executable, 'qwen_cli_integrator.py', 'venice', '--help'], 
                          capture_output=True, text=True)
    
    if result.returncode == 0 and 'usage:' in result.stdout.lower():
        print("✓ Venice help output works correctly")
    else:
        print("✗ Venice help output failed")
        if result.stderr:
            print(f"  Error: {result.stderr}")
    
    print()


def main():
    """Run all tests"""
    print("Qwen CLI Integration - Test Suite")
    print("=" * 50)
    print()
    
    test_gitkraken_integration()
    test_venice_integration()
    test_help_output()
    
    print("Test suite completed!")


if __name__ == "__main__":
    main()