# import modules
import time, random, requests, psutil, math
from PIL import Image
from io import BytesIO

# Remove characters from a string
def clean(string, chars):
    return "".join([c for c in string if c not in chars])

# Merge multiple lists or dictionaries
def merge(*args, duplicate=False):
    """
    Merge multiple lists or dictionaries of the same type.

    Parameters:
        *args: Variable number of list or dict arguments to merge.
        duplicate (bool): Applicable for lists. If True, duplicates are retained; if False, duplicates are removed.

    Returns:
        Merged list or dictionary if all inputs are of the same type.
        False if input types are mixed or unsupported.
    """
    if not args:
        return False

    first_type = type(args[0])
    if not all(isinstance(arg, first_type) for arg in args):
        return False

    if first_type is list:
        if duplicate:
            # Retain duplicates; concatenate all lists
            result = []
            for lst in args:
                result.extend(lst)
            return result
        else:
            # Remove duplicates while preserving order
            result = args[0]
            args = args[1:]
            for lst in args:
                for item in lst:
                    if item not in result:
                        result.append(item)
            return result

    elif first_type is dict:
        # Merge dictionaries; prefer values from the first dictionary in case of key conflicts
        result = {}
        for d in args:
            for key, value in d.items():
                if key not in result:
                    result[key] = value
        return result

    else:
        # Unsupported type
        return False

# Measure execution time
def timer(func):
    # Decorator
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        needed_time = end_time - start_time
        return needed_time, result
    return wrapper

# Remove duplicates
def unique(lst):
    return list(dict.fromkeys(lst))

# Flatten a nested list
def flatten(lst):
    flat_list = []
    for element in lst:
        if isinstance(element, list):
            flat_list.extend(flatten(element))
        else:
            flat_list.append(element)
    return flat_list

# Generate a random string
def random_string(length, charset):
    return ''.join(random.choice(charset) for _ in range(length))

# Download a file
def download(url, path):
    try:
        response = requests.get(url)
        with open(path, 'wb') as file:
            file.write(response.content)
    except Exception as e:
        print(f"Error downloading file: {e}")

# Check if any item in a is in b
def any_in(a, b):
    return any(item in b for item in a)

# Check if all items in a are in b
def all_in(a, b):
    return all(item in b for item in a)

# Download an image
def download_image(url):
    try:
        response = requests.get(url)
        return Image.open(BytesIO(response.content))
    except Exception as e:
        print(f"Error downloading image: {e}")

# Format duration
def format_duration(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

# Get memory usage
def memory_usage():
    process = psutil.Process()
    return process.memory_info().rss

# Check if connected to the internet
def isnetwork():
    import socket
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

# Get n-th prime
def nprime(n):
    def sieve_of_eratosthenes(limit):
        sieve = [True] * (limit + 1)
        sieve[0] = sieve[1] = False
        for start in range(2, int(limit ** 0.5) + 1):
            if sieve[start]:
                for i in range(start * start, limit + 1, start):
                    sieve[i] = False
        return [num for num, is_prime in enumerate(sieve) if is_prime]
    limit = int(n * math.log(n) * 1.2)
    while True:
        primes = sieve_of_eratosthenes(limit)
        if len(primes) >= n:
            return primes[n - 1]
        limit *= 2

# Check if a number is prime
def isprime(n):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True