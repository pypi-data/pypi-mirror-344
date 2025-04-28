# Levox - GDPR Compliance Tool

A comprehensive tool for scanning, fixing, and reporting GDPR compliance issues in code.

## Features

- **GDPR Compliance Scanning**: Detect potential GDPR violations in your codebase
- **PII Detection**: Identify personally identifiable information in your code
- **Data Flow Analysis**: Track how data moves through your application
- **Automated Remediation**: Get suggestions for fixing compliance issues
- **Detailed Reporting**: Generate reports in multiple formats

## Installation

Install the package using pip:

```bash
pip install levox
```

## Additional Requirements

For the AI-powered fix suggestions to work, you'll need:

1. Install Ollama from https://ollama.com
2. Pull the required model:
   ```bash
   ollama pull deepseek-r1:1.5b
   ```

Ollama must be running when you use the fix functionality. If you're on Windows, make sure to start Ollama before running Levox.

## Usage

### Command Line Interface

```bash
# Scan a directory for GDPR compliance issues
levox scan [directory]

# Fix GDPR compliance issues in a directory
levox fix [directory]

# Show benchmarks and information
levox about

# Run benchmarks
levox benchmark --run
```

### As a Library

```python
from levox.scanner import Scanner
from levox.fixer import Fixer

# Scan a directory
scanner = Scanner("path/to/your/code")
issues = scanner.scan_directory()

# Get suggestions for fixing issues
fixer = Fixer()
for issue in issues:
    fix = fixer.generate_fix(issue)
    print(fix)
```

## Configuration

Levox can be configured using a `levox_config.json` file in your project directory or in the user's home directory (`~/.levox/config.json`).

Example configuration:

```json
{
  "exclude": [
    "**/test/**",
    "**/node_modules/**",
    "**/__pycache__/**"
  ],
  "severity_threshold": "medium"
}
```

## Path Handling

Levox supports both relative and absolute paths on all platforms. If you encounter "Directory not found" errors:

1. Make sure the directory exists and is readable
2. Try using absolute paths instead of relative paths
3. Check file system permissions
4. For Windows paths with spaces, enclose the path in quotes

## License

This is proprietary software. All rights reserved.

Usage is permitted according to the terms in the LICENSE file. This software is licensed, not sold, and may only be used in accordance with the license terms provided.

For licensing inquiries, please contact: info@levox.io 