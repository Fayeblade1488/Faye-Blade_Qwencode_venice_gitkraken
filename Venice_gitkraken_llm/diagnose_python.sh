#!/bin/bash

echo "Python Diagnostics"
echo "=================="
echo ""

# Check Python installations
echo "1. Python installations:"
echo "   Homebrew Python3:"
/opt/homebrew/bin/python3 --version 2>&1 || echo "   ERROR: Cannot run Homebrew Python"

echo ""
echo "   System Python3:"
/usr/bin/python3 --version 2>&1 || echo "   ERROR: Cannot run system Python"

# Check if venv module exists
echo ""
echo "2. Checking venv module:"
/opt/homebrew/bin/python3 -c "import venv; print('   venv module: OK')" 2>&1 || echo "   ERROR: venv module not available"

# Check if ensurepip exists
echo ""
echo "3. Checking ensurepip:"
/opt/homebrew/bin/python3 -c "import ensurepip; print('   ensurepip: OK')" 2>&1 || echo "   ERROR: ensurepip not available"

# Try creating a test venv with verbose output
echo ""
echo "4. Attempting venv creation with verbose output:"
/opt/homebrew/bin/python3 -m venv --help 2>&1 | head -5

echo ""
echo "5. Trying to create test venv with system Python:"
/usr/bin/python3 -m venv ~/test_venv 2>&1
if [ -d ~/test_venv ]; then
    echo "   SUCCESS: System Python can create venvs"
    ls -la ~/test_venv/
    rm -rf ~/test_venv
else
    echo "   FAILED: System Python cannot create venvs"
fi

echo ""
echo "6. Check disk space:"
df -h ~ | head -2

echo ""
echo "7. Check directory permissions:"
ls -ld ~/.venvs

echo ""
echo "ALTERNATIVE SOLUTION:"
echo "===================="
echo "Since venv creation is failing, we have alternatives:"
echo ""
echo "Option 1: Use pipx to install Poetry globally, then use Poetry's built-in venv:"
echo "   brew install pipx"
echo "   pipx ensurepath"
echo "   pipx install poetry"
echo "   cd ~/Desktop/26082025/Gemini2.5Pro/CSAM_GUARD_PROJECT"
echo "   poetry install"
echo "   poetry shell"
echo ""
echo "Option 2: Use conda/miniconda:"
echo "   brew install miniconda"
echo "   conda create -n sd-env python=3.10"
echo "   conda activate sd-env"
echo ""
echo "Option 3: Try virtualenv (older tool):"
echo "   /opt/homebrew/bin/python3 -m pip install --user virtualenv"
echo "   ~/.local/bin/virtualenv ~/.venvs/sd-env"
echo ""
