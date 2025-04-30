#!/bin/bash
# Build script for StalmarckPy Python extension

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$SCRIPT_DIR"

# Clean previous builds first
rm -rf build dist *.egg-info src

# Create source directories
mkdir -p src/{core,parser,solver}

# Copy C++ source files
echo "Copying source files..."
cp "$PROJECT_ROOT"/src/core/*.{cpp,hpp} src/core/
cp "$PROJECT_ROOT"/src/parser/*.{cpp,hpp} src/parser/
cp "$PROJECT_ROOT"/src/solver/*.{cpp,hpp} src/solver/

# Install build dependencies
pip install -U pip build twine scikit-build-core pybind11 cmake auditwheel

# Build distributions
python -m build

# Repair the wheel with auditwheel
echo "Repairing wheel with auditwheel..."
auditwheel repair dist/*.whl --plat manylinux_2_17_x86_64 -w dist/
# Remove the original wheel
rm dist/*-linux_x86_64.whl

echo "Build complete! Distribution files created in dist/"
echo "To upload to PyPI, run:"
echo "python -m twine upload dist/*"