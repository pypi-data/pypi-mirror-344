#!/usr/bin/env python
import argparse
import json
import sys
import time
from typing import Dict, List, Any, Optional

from EvoloPy.api import (
    available_optimizers,
    available_benchmarks,
    run_optimizer,
    run_multiple_optimizers
)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for the EvoloPy CLI."""
    parser = argparse.ArgumentParser(
        description="EvoloPy: A Python library for nature-inspired optimization algorithms",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Add required arguments
    parser.add_argument(
        "--optimizer", "-o", type=str, 
        help="Optimizer to use. Use 'list' to see available optimizers."
    )
    
    parser.add_argument(
        "--function", "-f", type=str, 
        help="Objective function to optimize. Use 'list' to see available functions."
    )
    
    # Add optional arguments with defaults
    parser.add_argument(
        "--pop-size", "-p", type=int, default=30,
        help="Population size"
    )
    
    parser.add_argument(
        "--iterations", "-i", type=int, default=50,
        help="Number of iterations"
    )
    
    parser.add_argument(
        "--dim", "-d", type=int, default=10,
        help="Problem dimension"
    )
    
    parser.add_argument(
        "--lb", type=float, default=-100,
        help="Lower bound of search space"
    )
    
    parser.add_argument(
        "--ub", type=float, default=100,
        help="Upper bound of search space"
    )
    
    parser.add_argument(
        "--runs", "-r", type=int, default=1,
        help="Number of independent runs"
    )
    
    parser.add_argument(
        "--output", type=str, default="results.json",
        help="Output file to save results"
    )
    
    parser.add_argument(
        "--list", action="store_true",
        help="List available optimizers and benchmark functions"
    )
    
    # Multi-optimizer and multi-function mode
    parser.add_argument(
        "--multi", action="store_true",
        help="Run multiple optimizers and/or functions (comma-separated lists)"
    )
    
    return parser.parse_args()


def display_available_options() -> None:
    """Display available optimizers and benchmark functions."""
    print("Available Optimizers:")
    for opt in available_optimizers():
        print(f"  - {opt}")
    
    print("\nAvailable Benchmark Functions:")
    for func in available_benchmarks():
        print(f"  - {func}")


def run_cli() -> None:
    """Run the command-line interface for EvoloPy."""
    args = parse_args()
    
    # Handle listing available options
    if args.list:
        display_available_options()
        sys.exit(0)
    
    # Check for required arguments
    if args.optimizer == "list" or args.function == "list":
        display_available_options()
        sys.exit(0)
    
    if not args.optimizer:
        print("Error: Optimizer must be specified. Use --list to see options.")
        sys.exit(1)
    
    if not args.function:
        print("Error: Objective function must be specified. Use --list to see options.")
        sys.exit(1)
    
    # Handle multi-mode
    if args.multi:
        optimizers = [o.strip() for o in args.optimizer.split(",")]
        functions = [f.strip() for f in args.function.split(",")]
        
        print(f"Running {len(optimizers)} optimizer(s) on {len(functions)} function(s)...")
        start_time = time.time()
        
        results = run_multiple_optimizers(
            optimizers=optimizers,
            objective_funcs=functions,
            population_size=args.pop_size,
            iterations=args.iterations,
            dim=args.dim,
            lb=args.lb,
            ub=args.ub,
            num_runs=args.runs
        )
        
        elapsed = time.time() - start_time
        print(f"All optimizations completed in {elapsed:.2f} seconds.")
        
        # Save results to file
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Results saved to {args.output}")
        
    else:
        # Handle single optimizer and function
        print(f"Running {args.optimizer} on {args.function}...")
        
        result = run_optimizer(
            optimizer=args.optimizer,
            objective_func=args.function,
            population_size=args.pop_size,
            iterations=args.iterations,
            dim=args.dim,
            lb=args.lb,
            ub=args.ub
        )
        
        print("\nOptimization completed!")
        print(f"Best fitness: {result['best_fitness']}")
        print(f"Execution time: {result['execution_time']:.2f} seconds")
        
        # Save result to file
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"Result saved to {args.output}")


if __name__ == "__main__":
    run_cli() 