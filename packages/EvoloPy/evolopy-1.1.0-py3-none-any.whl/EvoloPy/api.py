"""
High-level API functions for EvoloPy.

This module provides simplified access to EvoloPy's core functionality
with a more Pythonic and user-friendly interface.
"""

import numpy as np
from typing import Union, List, Dict, Any, Callable, Optional
from EvoloPy.optimizer import run as optimizer_run
from EvoloPy.solution import solution
import importlib

def get_optimizer_map():
    """Get a dictionary mapping optimizer names to their functions."""
    optimizer_map = {}
    optimizer_modules = [
        "PSO", "GWO", "MVO", "MFO", "CS", "BAT", 
        "WOA", "FFA", "SSA", "GA", "HHO", "SCA", 
        "JAYA", "DE"
    ]
    
    for name in optimizer_modules:
        try:
            module = importlib.import_module(f"EvoloPy.optimizers.{name}")
            optimizer_function = getattr(module, name)
            optimizer_map[name] = optimizer_function
        except (ImportError, AttributeError):
            # Skip optimizers that aren't available
            pass
    
    return optimizer_map

def available_optimizers() -> List[str]:
    """
    Get a list of all available optimization algorithms.
    
    Returns:
        List[str]: List of optimizer names
        
    Example:
        >>> from EvoloPy.api import available_optimizers
        >>> print(available_optimizers())
        ['PSO', 'GWO', 'MVO', ...]
    """
    return list(get_optimizer_map().keys())

def available_benchmarks() -> List[str]:
    """
    Get a list of all available benchmark functions.
    
    Returns:
        List[str]: List of benchmark function names
        
    Example:
        >>> from EvoloPy.api import available_benchmarks
        >>> print(available_benchmarks())
        ['F1', 'F2', 'F3', ...]
    """
    # List of all benchmark functions
    return [
        "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10",
        "F11", "F12", "F13", "F14", "F15", "F16", "F17", "F18", "F19",
        "F20", "F21", "F22", "F23", "F24", "ackley", "rosenbrock", 
        "rastrigin", "griewank"
    ]

def run_optimizer(
    optimizer: str,
    objective_func: Union[str, Callable],
    lb: float = -100,
    ub: float = 100,
    dim: int = 30,
    population_size: int = 30,
    iterations: int = 50,
    num_runs: int = 1,
    export_results: bool = False,
    export_details: bool = False,
    export_convergence: bool = False,
    export_boxplot: bool = False,
    results_directory: Optional[str] = None
) -> Dict[str, Any]:
    """
    Run a single optimizer on a specified objective function.
    
    Parameters:
        optimizer (str): Name of the optimizer algorithm
        objective_func (str or callable): Either a benchmark name (e.g., "F1") 
                                         or a custom objective function
        lb (float): Lower bound for variables
        ub (float): Upper bound for variables
        dim (int): Problem dimension
        population_size (int): Size of the population
        iterations (int): Maximum number of iterations
        num_runs (int): Number of independent runs
        export_results (bool): Whether to export average results
        export_details (bool): Whether to export detailed results
        export_convergence (bool): Whether to export convergence plots
        export_boxplot (bool): Whether to export boxplots
        results_directory (str, optional): Directory to save results
        
    Returns:
        Dict[str, Any]: Results dictionary containing:
            - 'best_solution': Best solution found
            - 'best_fitness': Best fitness value
            - 'convergence': Convergence history
            - 'execution_time': Execution time
            
    Example:
        >>> from EvoloPy.api import run_optimizer
        >>> result = run_optimizer("PSO", "F1", population_size=50, iterations=100)
        >>> print(f"Best fitness: {result['best_fitness']}")
        >>> print(f"Execution time: {result['execution_time']} seconds")
    """
    optimizer_map = get_optimizer_map()
    
    # Check if optimizer exists
    if optimizer not in optimizer_map:
        raise ValueError(f"Optimizer '{optimizer}' not found. Available optimizers: {available_optimizers()}")
    
    # Handle string objective functions (benchmarks)
    if isinstance(objective_func, str):
        if objective_func not in available_benchmarks():
            raise ValueError(f"Benchmark '{objective_func}' not found. Available benchmarks: {available_benchmarks()}")
        
        # Run the optimization
        params = {"PopulationSize": population_size, "Iterations": iterations}
        export_flags = {
            "Export_avg": export_results,
            "Export_details": export_details,
            "Export_convergence": export_convergence,
            "Export_boxplot": export_boxplot
        }
        
        results = optimizer_run(
            [optimizer], 
            [objective_func], 
            num_runs, 
            params, 
            export_flags,
            results_directory
        )
        
        # Process and return results
        return {
            'best_solution': results.bestIndividual if hasattr(results, 'bestIndividual') else None,
            'best_fitness': results.best if hasattr(results, 'best') else None,
            'convergence': results.convergence if hasattr(results, 'convergence') else None,
            'execution_time': results.executionTime if hasattr(results, 'executionTime') else None
        }
    
    # Handle callable objective functions
    elif callable(objective_func):
        # Get the optimizer function
        optimizer_func = optimizer_map[optimizer]
        
        # Run the optimization directly
        result = optimizer_func(objective_func, lb, ub, dim, population_size, iterations)
        
        # Return the results
        return {
            'best_solution': result.bestIndividual,
            'best_fitness': objective_func(result.bestIndividual),
            'convergence': result.convergence,
            'execution_time': result.executionTime
        }
    
    else:
        raise TypeError("objective_func must be either a string (benchmark name) or a callable function")

def run_multiple_optimizers(
    optimizers: List[str],
    objective_funcs: List[Union[str, Callable]],
    lb: float = -100,
    ub: float = 100,
    dim: int = 30,
    population_size: int = 30,
    iterations: int = 50,
    num_runs: int = 1,
    export_results: bool = True,
    export_details: bool = False,
    export_convergence: bool = True,
    export_boxplot: bool = True,
    results_directory: Optional[str] = None
) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    Run multiple optimizers on multiple objective functions.
    
    This function allows running multiple optimization algorithms on multiple benchmark
    functions and returns structured results.
    
    Parameters:
        optimizers (List[str]): List of optimizer names
        objective_funcs (List[str]): List of benchmark function names
        lb (float): Lower bound for variables
        ub (float): Upper bound for variables
        dim (int): Problem dimension
        population_size (int): Size of the population
        iterations (int): Maximum number of iterations
        num_runs (int): Number of independent runs
        export_results (bool): Whether to export average results
        export_details (bool): Whether to export detailed results
        export_convergence (bool): Whether to export convergence plots
        export_boxplot (bool): Whether to export boxplots
        results_directory (str, optional): Directory to save results
        
    Returns:
        Dict[str, Dict[str, Dict[str, Any]]]: Nested dictionary of results:
            {optimizer_name: {objective_name: {result_data}}}
            
    Example:
        >>> from EvoloPy.api import run_multiple_optimizers
        >>> results = run_multiple_optimizers(
        ...     optimizers=["PSO", "GWO"], 
        ...     objective_funcs=["F1", "F5"],
        ...     population_size=30,
        ...     iterations=50
        ... )
        >>> # Access specific results
        >>> for opt_name, opt_results in results.items():
        ...     for func_name, func_results in opt_results.items():
        ...         print(f"{opt_name} on {func_name}: {func_results}")
    """
    optimizer_map = get_optimizer_map()
    
    # Validate inputs
    for opt in optimizers:
        if opt not in optimizer_map:
            raise ValueError(f"Optimizer '{opt}' not found. Available optimizers: {available_optimizers()}")
    
    for func in objective_funcs:
        if isinstance(func, str) and func not in available_benchmarks():
            raise ValueError(f"Benchmark '{func}' not found. Available benchmarks: {available_benchmarks()}")
    
    # Only support string benchmark functions for now
    if not all(isinstance(func, str) for func in objective_funcs):
        raise TypeError("For multiple optimizers, all objective_funcs must be benchmark names (strings)")
    
    # Set up parameters
    params = {"PopulationSize": population_size, "Iterations": iterations}
    export_flags = {
        "Export_avg": export_results,
        "Export_details": export_details,
        "Export_convergence": export_convergence,
        "Export_boxplot": export_boxplot
    }
    
    # Initialize results dictionary
    results = {}
    
    # Run each optimizer on each objective function
    for opt in optimizers:
        results[opt] = {}
        for func in objective_funcs:
            # Run the optimizer on the current function
            result = run_optimizer(
                optimizer=opt,
                objective_func=func,
                lb=lb,
                ub=ub,
                dim=dim,
                population_size=population_size,
                iterations=iterations,
                num_runs=num_runs,
                export_results=export_results,
                export_details=export_details,
                export_convergence=export_convergence,
                export_boxplot=export_boxplot,
                results_directory=results_directory
            )
            
            # Store the result
            results[opt][func] = result
    
    return results 