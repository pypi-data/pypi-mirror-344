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
    run_multiple_optimizers,
    get_hardware_info,
    PARALLEL_AVAILABLE
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
    
    # Parallel processing options
    parallel_group = parser.add_argument_group('Parallel Processing')
    
    parallel_group.add_argument(
        "--parallel", action="store_true",
        help="Enable parallel processing for multiple runs"
    )
    
    parallel_group.add_argument(
        "--backend", type=str, default="auto", choices=["auto", "multiprocessing", "cuda"],
        help="Parallel processing backend to use"
    )
    
    parallel_group.add_argument(
        "--processes", type=int, default=None,
        help="Number of parallel processes to use (default: auto-detect)"
    )
    
    parallel_group.add_argument(
        "--hw-info", action="store_true",
        help="Display hardware information and exit"
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


def display_hardware_info() -> None:
    """Display hardware information for parallel processing."""
    if not PARALLEL_AVAILABLE:
        print("Error: Hardware detection requires the psutil package.")
        print("Install with: pip install psutil")
        sys.exit(1)
        
    try:
        hw_info = get_hardware_info()
        
        print("Hardware Information:")
        print(f"CPU cores: {hw_info['cpu_count']}")
        print(f"CPU threads: {hw_info['cpu_threads']}")
        print(f"RAM: {hw_info['ram_gb']:.2f} GB")
        
        if hw_info['gpu_available']:
            print(f"CUDA GPUs available: {hw_info['gpu_count']}")
            for i, (name, mem) in enumerate(zip(hw_info['gpu_names'], hw_info['gpu_memory'])):
                print(f"  GPU {i}: {name} ({mem:.2f} GB)")
        else:
            print("CUDA GPUs: None detected")
    except Exception as e:
        print(f"Error detecting hardware: {e}")
        sys.exit(1)


def run_cli() -> None:
    """Run the command-line interface for EvoloPy."""
    args = parse_args()
    
    # Handle hardware info display
    if args.hw_info:
        display_hardware_info()
        sys.exit(0)
    
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
        
        # Display parallel processing info if enabled
        if args.parallel:
            print(f"Parallel processing enabled with {args.backend} backend")
            if args.processes:
                print(f"Using {args.processes} processes")
            else:
                print("Auto-detecting optimal number of processes")
        
        start_time = time.time()
        
        results = run_multiple_optimizers(
            optimizers=optimizers,
            objective_funcs=functions,
            population_size=args.pop_size,
            iterations=args.iterations,
            dim=args.dim,
            lb=args.lb,
            ub=args.ub,
            num_runs=args.runs,
            enable_parallel=args.parallel,
            parallel_backend=args.backend,
            num_processes=args.processes
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
        
        # Display parallel processing info if enabled
        if args.parallel:
            print(f"Parallel processing enabled with {args.backend} backend")
            if args.processes:
                print(f"Using {args.processes} processes")
            else:
                print("Auto-detecting optimal number of processes")
        
        start_time = time.time()
        
        result = run_optimizer(
            optimizer=args.optimizer,
            objective_func=args.function,
            population_size=args.pop_size,
            iterations=args.iterations,
            dim=args.dim,
            lb=args.lb,
            ub=args.ub,
            num_runs=args.runs,
            enable_parallel=args.parallel,
            parallel_backend=args.backend,
            num_processes=args.processes
        )
        
        elapsed = time.time() - start_time
        
        print("\nOptimization completed!")
        print(f"Best fitness: {result['best_fitness']}")
        print(f"Execution time: {result['execution_time']:.2f} seconds")
        print(f"Total wall time: {elapsed:.2f} seconds")
        
        # Save result to file
        with open(args.output, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"Result saved to {args.output}")


if __name__ == "__main__":
    run_cli() 