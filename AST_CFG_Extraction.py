import os
import time
import psutil
import csv
import esprima  # Install with: pip install esprima
import tracemalloc

# Set the directory path for JavaScript files Users    \OU\Data sets\ProjectDatset
INPUT_DIRECTORY = r'C:\Users\batai\Documents\Qasim Stuff\OU\Data sets\ProjectDatset'
OUTPUT_DIRECTORY = r'.\output'
RESULTS_CSV = os.path.join(OUTPUT_DIRECTORY, 'results.csv')
SUMMARY_REPORT = os.path.join(OUTPUT_DIRECTORY, 'summary_report.txt')

# Ensure output directory exists
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

def generate_ast(js_code):
    """Generate Abstract Syntax Tree from JavaScript code"""
    return esprima.parseScript(js_code, tolerant=True)

def generate_cfg(js_code):
    """Dummy CFG generation (simulate control flow extraction)"""
    # Real CFG generation would need full control flow analysis
    # Here we simulate it by parsing and extracting 'control' keywords
    keywords = ['if', 'else', 'for', 'while', 'switch', 'case', 'break', 'continue', 'function']
    cfg = []
    lines = js_code.split('\n')
    for idx, line in enumerate(lines):
        if any(keyword in line for keyword in keywords):
            cfg.append((idx + 1, line.strip()))
    return cfg

def measure_resources(function, *args):
    """Measure time and memory usage of a function"""
    tracemalloc.start()
    start_time = time.time()
    result = function(*args)
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    time_taken = end_time - start_time
    space_used = peak / 1024  # in KB
    return result, time_taken, space_used

def process_files():
    results = []
    
    for filename in os.listdir(INPUT_DIRECTORY):
        if filename.endswith('.js'):
            print("Processing file ... " + filename)
            filepath = os.path.join(INPUT_DIRECTORY, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                js_code = f.read()

            ast, ast_time, ast_space = measure_resources(generate_ast, js_code)
            cfg, cfg_time, cfg_space = measure_resources(generate_cfg, js_code)

            # Write AST and CFG to text files
            with open(os.path.join(OUTPUT_DIRECTORY, f'{filename}_ast.txt'), 'w', encoding='utf-8') as f_ast:
                f_ast.write(str(ast))
            with open(os.path.join(OUTPUT_DIRECTORY, f'{filename}_cfg.txt'), 'w', encoding='utf-8') as f_cfg:
                for node in cfg:
                    f_cfg.write(f'Line {node[0]}: {node[1]}\n')

            results.append({
                'Filename': filename,
                'AST Time (s)': round(ast_time, 5),
                'AST Space (KB)': round(ast_space, 2),
                'CFG Time (s)': round(cfg_time, 5),
                'CFG Space (KB)': round(cfg_space, 2)
            })

    # Save results to CSV
    with open(RESULTS_CSV, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Filename', 'AST Time (s)', 'AST Space (KB)', 'CFG Time (s)', 'CFG Space (KB)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    return results

def generate_summary(results):
    """Generate a readable summary report"""
    with open(SUMMARY_REPORT, 'w', encoding='utf-8') as f:
        f.write('Summary Report: AST vs CFG Performance\n\n')
        for r in results:
            f.write(f"File: {r['Filename']}\n")
            f.write(f"  AST Time: {r['AST Time (s)']}s | AST Space: {r['AST Space (KB)']}KB\n")
            f.write(f"  CFG Time: {r['CFG Time (s)']}s | CFG Space: {r['CFG Space (KB)']}KB\n\n")

if __name__ == '__main__':
    results = process_files()
    generate_summary(results)
    print(f"Processing completed. Results saved to {OUTPUT_DIRECTORY}")
