#!/usr/bin/env python3
"""
Tool to inventory public API symbols in Python files.

This script parses Python files using the ast module and catalogs all public
classes, functions, and methods. It outputs both JSON and Markdown formats.
"""

import argparse
import ast
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional


class APIInventory:
    """Catalogs public API symbols from Python source files."""
    
    def __init__(self):
        """Initialize the API inventory."""
        self.inventory: List[Dict[str, Any]] = []
    
    def is_public(self, name: str) -> bool:
        """Check if a symbol name is public (no leading underscore).
        
        Args:
            name: The symbol name to check.
            
        Returns:
            True if the name is public, False otherwise.
        """
        return not name.startswith("_")
    
    def has_docstring(self, node: ast.AST) -> bool:
        """Check if an AST node has a docstring.
        
        Args:
            node: The AST node to check.
            
        Returns:
            True if the node has a docstring, False otherwise.
        """
        if not hasattr(node, "body") or not node.body:
            return False
        first = node.body[0]
        return isinstance(first, ast.Expr) and isinstance(first.value, ast.Constant)
    
    def get_docstring(self, node: ast.AST) -> Optional[str]:
        """Extract docstring from an AST node.
        
        Args:
            node: The AST node to extract from.
            
        Returns:
            The docstring text if present, None otherwise.
        """
        return None if not self.has_docstring(node) else node.body[0].value.value
    
    def process_file(self, filepath: Path) -> None:
        """Process a single Python file and extract public API symbols.
        
        Args:
            filepath: Path to the Python file to process.
        """
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                source = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}", file=sys.stderr)
            return
        
        try:
            tree = ast.parse(source, filepath.name)
        except SyntaxError as e:
            print(f"Syntax error in {filepath}: {e}", file=sys.stderr)
            return
        
        for node in tree.body:
            # Process module-level functions
            if isinstance(node, ast.FunctionDef):
                if self.is_public(node.name) and hasattr(node, "lineno"):
                    self.inventory.append({
                        "file": str(filepath),
                        "type": "function",
                        "name": node.name,
                        "line": node.lineno,
                        "has_docstring": self.has_docstring(node),
                        "docstring_preview": (self.get_docstring(node) or "")[:100],
                        "is_async": False
                    })
            
            # Process async functions
            elif isinstance(node, ast.AsyncFunctionDef):
                if self.is_public(node.name) and hasattr(node, "lineno"):
                    self.inventory.append({
                        "file": str(filepath),
                        "type": "async_function",
                        "name": node.name,
                        "line": node.lineno,
                        "has_docstring": self.has_docstring(node),
                        "docstring_preview": (self.get_docstring(node) or "")[:100],
                        "is_async": True
                    })
            
            # Process classes and their methods
            elif isinstance(node, ast.ClassDef):
                if self.is_public(node.name) and hasattr(node, "lineno"):
                    self.inventory.append({
                        "file": str(filepath),
                        "type": "class",
                        "name": node.name,
                        "line": node.lineno,
                        "has_docstring": self.has_docstring(node),
                        "docstring_preview": (self.get_docstring(node) or "")[:100]
                    })
                    
                    # Process class methods
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if self.is_public(item.name):
                                method_info = {
                                    "file": str(filepath),
                                    "type": "method",
                                    "class": node.name,
                                    "name": item.name,
                                    "line": item.lineno,
                                    "has_docstring": self.has_docstring(item),
                                    "docstring_preview": (self.get_docstring(item) or "")[:100],
                                    "is_async": isinstance(item, ast.AsyncFunctionDef)
                                }
                                self.inventory.append(method_info)
    
    def generate_stats(self) -> Dict[str, Any]:
        """Generate statistics about the inventory.
        
        Returns:
            Dictionary containing statistics about documented symbols.
        """
        total = len(self.inventory)
        documented = sum(1 for item in self.inventory if item["has_docstring"])
        
        by_type = {}
        for item in self.inventory:
            item_type = item["type"]
            if item_type not in by_type:
                by_type[item_type] = {"total": 0, "documented": 0}
            by_type[item_type]["total"] += 1
            if item["has_docstring"]:
                by_type[item_type]["documented"] += 1
        
        return {
            "total_symbols": total,
            "documented_symbols": documented,
            "documentation_coverage": f"{(documented/total*100):.1f}%" if total > 0 else "0%",
            "by_type": by_type
        }
    
    def to_json(self, output_path: Path) -> None:
        """Write inventory to JSON file.
        
        Args:
            output_path: Path to the output JSON file.
        """
        data = {
            "inventory": self.inventory,
            "statistics": self.generate_stats()
        }
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    
    def to_markdown(self, output_path: Path) -> None:
        """Write inventory to Markdown file.
        
        Args:
            output_path: Path to the output Markdown file.
        """
        stats = self.generate_stats()
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("# Public API Inventory\n\n")
            f.write("## Statistics\n\n")
            f.write(f"- **Total symbols:** {stats['total_symbols']}\n")
            f.write(f"- **Documented:** {stats['documented_symbols']}\n")
            f.write(f"- **Coverage:** {stats['documentation_coverage']}\n\n")
            
            f.write("### By Type\n\n")
            for symbol_type, counts in stats['by_type'].items():
                f.write(f"- **{symbol_type}:** {counts['documented']}/{counts['total']} documented\n")
            f.write("\n")
            
            f.write("## Symbols\n\n")
            
            # Group by file
            by_file = {}
            for item in self.inventory:
                filepath = item["file"]
                if filepath not in by_file:
                    by_file[filepath] = []
                by_file[filepath].append(item)
            
            for filepath in sorted(by_file.keys()):
                f.write(f"### {filepath}\n\n")
                items = sorted(by_file[filepath], key=lambda x: x["line"])
                
                for item in items:
                    doc_status = "✅" if item["has_docstring"] else "❌"
                    if item["type"] == "method":
                        f.write(f"- {doc_status} **{item['class']}.{item['name']}** "
                               f"(line {item['line']}, {item['type']})\n")
                    else:
                        f.write(f"- {doc_status} **{item['name']}** "
                               f"(line {item['line']}, {item['type']})\n")
                    if item["has_docstring"] and item["docstring_preview"]:
                        docstring_flat = item["docstring_preview"].replace("\n", " ")
                        if len(docstring_flat) > 80:
                            preview = docstring_flat[:80]
                            f.write(f"  - Preview: `{preview}...`\n")
                        else:
                            f.write(f"  - Preview: `{docstring_flat}`\n")
                f.write("\n")


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Inventory public API symbols in Python files"
    )
    parser.add_argument(
        "--paths-file",
        type=str,
        help="File containing list of Python file paths (one per line)"
    )
    parser.add_argument(
        "--out-json",
        type=str,
        help="Output JSON file path"
    )
    parser.add_argument(
        "--out-md",
        type=str,
        help="Output Markdown file path"
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Python files to process (if --paths-file not specified)"
    )
    
    args = parser.parse_args()
    
    # Determine which files to process
    files_to_process = []
    if args.paths_file:
        with open(args.paths_file, "r") as f:
            files_to_process = [line.strip() for line in f if line.strip()]
    elif args.files:
        files_to_process = args.files
    else:
        print("Error: No files specified. Use --paths-file or provide file arguments.", file=sys.stderr)
        sys.exit(1)
    
    # Process files
    inventory = APIInventory()

    def is_python_file(path):
        if not path.exists():
            return False
        if path.suffix == ".py":
            return True
        try:
            with path.open("r", encoding="utf-8") as f:
                first_line = f.readline()
                if first_line.startswith("#!"):
                    if "python" in first_line:
                        return True
            # Try parsing as Python
            with path.open("r", encoding="utf-8") as f:
                source = f.read()
                ast.parse(source)
            return True
        except Exception:
            return False

    for filepath in files_to_process:
        path = Path(filepath)
        if is_python_file(path):
            print(f"Processing {path}...", file=sys.stderr)
            inventory.process_file(path)
        else:
            print(f"Warning: Skipping {filepath} (not found or not a Python file)", file=sys.stderr)
    
    # Generate outputs
    if args.out_json:
        inventory.to_json(Path(args.out_json))
        print(f"JSON inventory written to {args.out_json}", file=sys.stderr)
    
    if args.out_md:
        inventory.to_markdown(Path(args.out_md))
        print(f"Markdown inventory written to {args.out_md}", file=sys.stderr)
    
    # Print summary
    stats = inventory.generate_stats()
    print(f"\nSummary: {stats['documented_symbols']}/{stats['total_symbols']} "
          f"symbols documented ({stats['documentation_coverage']})", file=sys.stderr)


if __name__ == "__main__":
    main()