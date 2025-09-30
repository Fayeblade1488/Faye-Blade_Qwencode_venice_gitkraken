# Tests

This directory contains the test suite for the Qwen CLI Integration project.

## Test Files

- **test_integration.py** - Core integration tests for all modules
- **test_comprehensive_coverage.py** - Comprehensive test coverage for critical paths
- **test_coverage_improvement.py** - Additional coverage improvements
- **test_bug_fixes.py** - Regression tests for bug fixes

## Running Tests

### Run all tests:
```bash
pytest tests/
```

### Run with coverage:
```bash
pytest tests/ --cov=. --cov-report=html
```

### Run specific test file:
```bash
pytest tests/test_integration.py
```

### Run verbose:
```bash
pytest tests/ -v
```

## Test Requirements

Tests require the main dependencies plus:
- pytest
- pytest-cov
- pytest-mock

Install test dependencies:
```bash
pip install pytest pytest-cov pytest-mock
```