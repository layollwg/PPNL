#!/usr/bin/env python3
import json
import glob
from pathlib import Path

def summarize():
    metric_files = glob.glob("outputs/*_metrics.json")
    
    print("| Model | Parse Rate | Feasibility | Success Rate | Optimality |")
    print("|---|---|---|---|---|")
    
    for file_path in sorted(metric_files):
        model_name = Path(file_path).stem.replace('_metrics', '')
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            agg = data.get("aggregate", {})
            
            parse_rate = agg.get("parse_rate", 0)
            feasibility = agg.get("feasibility", 0)
            success = agg.get("success_rate", 0)
            optimality = agg.get("optimality", 0)
            
            print(f"| {model_name} | {parse_rate:.4f} | {feasibility:.4f} | {success:.4f} | {optimality:.4f} |")

if __name__ == "__main__":
    summarize()
