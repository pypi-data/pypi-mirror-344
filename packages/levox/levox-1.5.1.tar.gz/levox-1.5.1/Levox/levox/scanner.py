from pathlib import Path
import os
import sys
import re
import time
import threading
from typing import List, Optional, Dict, Any, Tuple

class GDPRIssue:
    """Class representing a GDPR compliance issue in code."""
    
    def __init__(
            self,
            file_path: str,
            line_number: int,
            issue_type: str,
            description: str = None,
            remediation: str = None,
            severity: str = "medium"
        ):
        self.file_path = file_path
        self.line_number = line_number
        self.issue_type = issue_type
        self.description = description
        self.remediation = remediation
        self.severity = severity
    
    def to_dict(self) -> dict:
        """Convert to dictionary format."""
        return {
            "file_path": self.file_path,
            "line_number": self.line_number,
            "issue_type": self.issue_type,
            "description": self.description,
            "remediation": self.remediation,
            "severity": self.severity
        }

class Scanner:
    def __init__(self, target_dir: str, exclude_dirs=None):
        """Initialize scanner with target directory and exclusions.
        
        Args:
            target_dir: Path to directory to scan
            exclude_dirs: List of directory names to exclude from scanning
        """
        # Resolve path to handle both relative and absolute paths
        self.target_dir = self._resolve_path(target_dir)
        
        # Validate directory exists and is accessible
        if not self._validate_directory(self.target_dir):
            self.valid = False
            return
            
        self.valid = True
        self.exclude_dirs = exclude_dirs or ["node_modules", "venv", ".git", "__pycache__"]
        self.issues = []
    
    def _resolve_path(self, path_str: str) -> str:
        """Resolve a path to handle relative and absolute paths across platforms.
        
        Args:
            path_str: Path string to resolve
            
        Returns:
            Resolved absolute path as string
        """
        # Handle special case of '.' (current directory)
        if path_str == '.':
            return os.path.abspath('.')
            
        # Use pathlib to resolve the path properly
        try:
            path = Path(path_str)
            resolved_path = path.resolve()
            return str(resolved_path)
        except Exception as e:
            print(f"Error resolving path: {e}")
            return path_str  # Return original if resolution fails
    
    def _validate_directory(self, directory: str) -> bool:
        """Validate that a directory exists and is accessible.
        
        Args:
            directory: Directory path to validate
            
        Returns:
            True if directory exists and is accessible, False otherwise
        """
        try:
            if not os.path.exists(directory):
                print(f"Error: Directory does not exist: {directory}")
                return False
                
            if not os.path.isdir(directory):
                print(f"Error: Path is not a directory: {directory}")
                return False
                
            # Check if directory is readable
            if not os.access(directory, os.R_OK):
                print(f"Error: Directory is not readable: {directory}")
                return False
                
            return True
        except Exception as e:
            print(f"Error validating directory: {e}")
            return False
    
    def should_scan_file(self, file_path: Path) -> bool:
        """Check if file should be scanned."""
        # Skip non-text files or known binary files
        binary_extensions = ['.zip', '.gz', '.exe', '.dll', '.jpg', '.png', '.pdf']
        if file_path.suffix.lower() in binary_extensions:
            return False
            
        # Skip known resource directories
        resource_dirs = ['node_modules', 'venv', 'dist', 'build', '.git', '__pycache__']
        for part in file_path.parts:
            if part in resource_dirs or part in self.exclude_dirs:
                return False
                
        return True
    
    def scan_file(self, file_path: Path) -> List[GDPRIssue]:
        """Scan a single file for GDPR compliance issues."""
        issues = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
                
            # Example pattern for PII detection - in real implementation this would be more complex
            pii_patterns = {
                'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                'phone': r'\b(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}\b',
                'credit_card': r'\b(?:\d{4}[- ]?){3}\d{4}\b'
            }
            
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                for pii_type, pattern in pii_patterns.items():
                    if re.search(pattern, line):
                        issues.append(GDPRIssue(
                            file_path=str(file_path),
                            line_number=i,
                            issue_type="pii_" + pii_type,
                            description=f"Possible {pii_type} found in code",
                            severity="medium"
                        ))
        except Exception as e:
            print(f"Error scanning file {file_path}: {e}")
            
        return issues
    
    def _collect_files(self) -> List[Path]:
        """Collect all files to scan."""
        files_to_scan = []
        try:
            for root, dirs, files in os.walk(self.target_dir):
                # Skip excluded directories
                dirs[:] = [d for d in dirs if d not in self.exclude_dirs]
                
                for file in files:
                    file_path = Path(os.path.join(root, file))
                    if self.should_scan_file(file_path):
                        files_to_scan.append(file_path)
        except Exception as e:
            print(f"Error collecting files: {e}")
            
        print(f"Found {len(files_to_scan)} files to scan")
        return files_to_scan
    
    def scan_directory(self) -> List[GDPRIssue]:
        """Scan the directory for GDPR compliance issues.
        
        Returns:
            List of GDPR issues found
        """
        # First verify directory is valid
        if not hasattr(self, 'valid') or not self.valid:
            print("Cannot scan - directory invalid or inaccessible")
            return []
        
        # Clear any previous issues
        self.issues = []
        
        # Collect all files to scan
        start_time = time.time()
        files_to_scan = self._collect_files()
        
        # Scan each file
        scanned_files = 0
        try:
            for file_path in files_to_scan:
                file_issues = self.scan_file(file_path)
                self.issues.extend(file_issues)
                scanned_files += 1
                
                # Progress update
                if scanned_files % 100 == 0:
                    print(f"Scanned {scanned_files}/{len(files_to_scan)} files...")
        except Exception as e:
            print(f"Error during scan: {e}")
        
        # Finishing report
        elapsed = time.time() - start_time
        if elapsed > 0:
            files_per_second = scanned_files / elapsed
            print(f"Scan completed in {elapsed:.2f} seconds")
            print(f"Performance: {files_per_second:.1f} files/second")
            print(f"Found {len(self.issues)} potential GDPR compliance issues")
        
        return self.issues 