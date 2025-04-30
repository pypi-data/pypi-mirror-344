import time
import hashlib
import math
from typing import Union, Optional

def _generate_enhanced_seed() -> tuple:
    """Generate enhanced seed with multiple hash values"""
    current_time = time.time_ns()
    seed_hash1 = hashlib.sha256(str(current_time).encode()).hexdigest()
    seed_hash2 = hashlib.sha512(str(current_time + 42).encode()).hexdigest()
    
    return (
        int(seed_hash1[:16], 16),
        int(seed_hash2[:16], 16),
        current_time % (2**32)
    )

def _apply_random_transformations(seed_tuple: tuple) -> float:
    """Apply various mathematical operations to increase entropy"""
    seed1, seed2, time_component = seed_tuple
    
    # Convert to a 0-1 range directly mimicking Python's random.random()
    # Use both seed components and time component for better randomness
    base_value = ((seed1 & 0xFFFFFF) ^ (seed2 & 0xFFFFFF) ^ (time_component & 0xFFFFFF))
    max_val = 0xFFFFFF
    
    # Create a value between 0 and 1 with high precision
    return base_value / max_val

def _random_from_seed(seed_tuple: tuple, start: float, end: float, decimal_places: int = 0) -> Union[int, float]:
    """Generate random number between start and end with specified decimal places"""
    # Get normalized random value [0, 1)
    normalized_value = _apply_random_transformations(seed_tuple)
    
    # For default 0-1 range, return the direct value
    if start == 0 and end == 1 and decimal_places == 0:
        return normalized_value
    
    # Scale to range [start, end]
    scaled_value = start + normalized_value * (end - start)
    
    if decimal_places > 0:
        # Apply decimal places constraint
        multiplier = 10 ** decimal_places
        return math.floor(scaled_value * multiplier) / multiplier
    else:
        # Return integer for non-default ranges
        return int(scaled_value)

def rannumber(
    start: Union[int, float, str] = 0, 
    end: Union[int, float, str] = 1, 
    decimal_option: Optional[str] = None
) -> Union[int, float]:
    """
    Generate a random number.
    
    Args:
        start: Lower bound (default: 0)
        end: Upper bound (default: 1)
        decimal_option: Format "dX" where X is decimal places (up to 20)
    
    Returns:
        Random number within the specified range
    """
    # Handle string inputs (expressions)
    if isinstance(start, str):
        try:
            start = eval(start)
        except Exception:
            raise ValueError(f"ranpickError: Invalid start expression: {start}.")
    if isinstance(end, str):
        try:
            end = eval(end)
        except Exception:
            raise ValueError(f"ranpickError: Invalid end expression: {end}.")

    # Parse decimal places option
    decimal_places = 0
    if decimal_option and decimal_option.startswith("d"):
        try:
            decimal_places = int(decimal_option[1:])
            if decimal_places < 0 or decimal_places > 20:  # Increased from 10 to 20
                raise ValueError(f"ranpickError: Decimal places must be between 0 and 20.")
        except ValueError as e:
            if "ranpickError" in str(e):
                raise e
            raise ValueError(f"ranpickError: Invalid decimal option format: {decimal_option}.")

    # Validate range
    if start >= end:
        raise ValueError("ranpickError: Start value must be less than end value.")

    # Generate random number
    seed_tuple = _generate_enhanced_seed()
    return _random_from_seed(seed_tuple, start, end, decimal_places)
