#!/usr/bin/env python3
"""
Command-line interface for PyCodeLens.
"""

import sys
import os
import argparse
import json
from .analyzer import analyze_file, extract_code_elements

def print_functions(functions, verbose=False):
    """Print function information."""
    print("\nFUNCTIONS:")
    for func in functions:
        print(f"  {func['name']} (lines {func['line_start']}-{func['line_end']})")
        if verbose and func['decorators']:
            print(f"    Decorators: {', '.join('@' + d['name'] for d in func['decorators'])}")

def print_decorators(decorators):
    """Print decorator information."""
    print("\nDECORATORS:")
    # Group by decorator name
    decorator_names = {}
    for dec in decorators:
        decorator_names.setdefault(dec['name'], []).append(dec['line'])
        
    for name, lines in decorator_names.items():
        print(f"  @{name}: {len(lines)} occurrences (lines: {', '.join(map(str, lines))})")

def print_classes(classes, verbose=False):
    """Print class information."""
    print("\nCLASSES:")
    for cls in classes:
        print(f"  {cls['name']} (lines {cls['line_start']}-{cls['line_end']})")
        if verbose and 'methods' in cls and cls['methods']:
            print(f"    Methods:")
            for method in cls['methods']:
                print(f"      {method['name']} (lines {method['line_start']}-{method['line_end']})")

def print_prints(print_calls):
    """Print information about print statements."""
    print("\nPRINT STATEMENTS:")
    for p in print_calls:
        print(f"  Line {p['line']}: print with {p['args']} arguments")

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='PyCodeLens: Extract and analyze code elements from Python files'
    )
    parser.add_argument('file', help='Path to the Python file')
    parser.add_argument('--functions', '-f', action='store_true', help='List functions')
    parser.add_argument('--decorators', '-d', action='store_true', help='List decorators')
    parser.add_argument('--classes', '-c', action='store_true', help='List classes')
    parser.add_argument('--prints', '-p', action='store_true', help='List print statements')
    parser.add_argument('--counts', '-n', action='store_true', help='Show only counts')
    parser.add_argument('--all', '-a', action='store_true', help='Show all information')
    parser.add_argument('--json', '-j', action='store_true', help='Output in JSON format')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed information')
    
    args = parser.parse_args()
    
    try:
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found.", file=sys.stderr)
            return 1
            
        analysis = analyze_file(args.file)
        results = analysis['raw_results']
        summary = analysis['summary']
        
        # JSON output
        if args.json:
            if args.counts:
                print(json.dumps({
                    'file': args.file,
                    'functions': len(results['functions']),
                    'decorators': len(results['decorators']),
                    'classes': len(results['classes']),
                    'print_statements': len(results['print_calls'])
                }, indent=2))
            else:
                print(json.dumps(analysis, indent=2))
            return 0
        
        # Default to showing counts if no specific options
        if not (args.functions or args.decorators or args.classes or args.prints) and not args.all:
            args.counts = True
        
        # Show counts
        if args.counts:
            print(f"File: {args.file}")
            print(f"  Functions: {len(results['functions'])}")
            print(f"  Decorators: {len(results['decorators'])}")
            print(f"  Classes: {len(results['classes'])}")
            print(f"  Print statements: {len(results['print_calls'])}")
        
        # Show detailed information
        if args.functions or args.all:
            print_functions(results['functions'], args.verbose)
        
        if args.decorators or args.all:
            print_decorators(results['decorators'])
        
        if args.classes or args.all:
            print_classes(results['classes'], args.verbose)
        
        if args.prints or args.all:
            print_prints(results['print_calls'])
            
    except Exception as e:
        print(f"Error analyzing file: {e}", file=sys.stderr)
        return 1
        
    return 0

if __name__ == "__main__":
    sys.exit(main())
