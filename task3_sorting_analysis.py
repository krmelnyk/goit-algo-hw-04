import random
import timeit
from typing import Callable


SortFunction = Callable[[list[int]], list[int]]


def insertion_sort(items: list[int]) -> list[int]:
    """Sort a list using insertion sort."""
    sorted_items = items.copy()

    for i in range(1, len(sorted_items)):
        current_value = sorted_items[i]
        j = i - 1

        while j >= 0 and sorted_items[j] > current_value:
            sorted_items[j + 1] = sorted_items[j]
            j -= 1

        sorted_items[j + 1] = current_value

    return sorted_items


def merge_sort(items: list[int]) -> list[int]:
    """Sort a list using merge sort."""
    if len(items) <= 1:
        return items.copy()

    middle = len(items) // 2
    left = merge_sort(items[:middle])
    right = merge_sort(items[middle:])

    return merge(left, right)


def merge(left: list[int], right: list[int]) -> list[int]:
    """Merge two sorted lists into one sorted list."""
    result = []
    left_index = 0
    right_index = 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] <= right[right_index]:
            result.append(left[left_index])
            left_index += 1
        else:
            result.append(right[right_index])
            right_index += 1

    result.extend(left[left_index:])
    result.extend(right[right_index:])
    return result


def timsort(items: list[int]) -> list[int]:
    """Sort a list using Python's built-in Timsort implementation."""
    return sorted(items)


def generate_datasets(size: int) -> dict[str, list[int]]:
    """Generate datasets with different initial ordering."""
    random_data = [random.randint(0, size * 10) for _ in range(size)]
    sorted_data = list(range(size))
    reversed_data = list(range(size, 0, -1))
    nearly_sorted_data = list(range(size))

    # Add a small amount of disorder to test adaptive sorting behavior.
    swaps_count = max(1, size // 100)
    for _ in range(swaps_count):
        first_index = random.randint(0, size - 1)
        second_index = random.randint(0, size - 1)
        nearly_sorted_data[first_index], nearly_sorted_data[second_index] = (
            nearly_sorted_data[second_index],
            nearly_sorted_data[first_index],
        )

    return {
        "random": random_data,
        "sorted": sorted_data,
        "reversed": reversed_data,
        "nearly sorted": nearly_sorted_data,
    }


def measure_time(sort_function: SortFunction, data: list[int]) -> float:
    """Measure sorting time with the timeit module."""
    return timeit.timeit(lambda: sort_function(data), number=1)


def validate_sorting(sort_functions: dict[str, SortFunction]) -> None:
    """Check that all sorting functions return the same sorted result."""
    test_data = [5, 3, 8, 3, 1, -4, 0]
    expected = sorted(test_data)

    for name, sort_function in sort_functions.items():
        if sort_function(test_data) != expected:
            raise ValueError(f"{name} returned an incorrect sorting result.")


def print_results_table(
    sizes: list[int],
    sort_functions: dict[str, SortFunction],
) -> None:
    """Print empirical timing results for all datasets and algorithms."""
    header = (
        f"{'Size':>6} | {'Dataset':<13} | {'Insertion':>10} | "
        f"{'Merge':>10} | {'Timsort':>10}"
    )
    print(header)
    print("-" * len(header))

    for size in sizes:
        datasets = generate_datasets(size)

        for dataset_name, data in datasets.items():
            timings = {
                name: measure_time(sort_function, data)
                for name, sort_function in sort_functions.items()
            }
            print(
                f"{size:>6} | {dataset_name:<13} | "
                f"{timings['Insertion sort']:>10.6f} | "
                f"{timings['Merge sort']:>10.6f} | "
                f"{timings['Timsort']:>10.6f}"
            )


def print_conclusions() -> None:
    """Print conclusions based on theoretical and empirical comparison."""
    print("\nConclusions:")
    print("- Insertion sort has O(n^2) average and worst-case complexity.")
    print(
        "- Merge sort has stable O(n log n) complexity "
        "for all input orders."
    )
    print("- Timsort also has O(n log n) worst-case complexity.")
    print("- Timsort is adaptive and works especially fast on sorted data.")
    print(
        "- Built-in sorted() is usually the best practical choice "
        "in Python."
    )


def main() -> None:
    random.seed(42)

    sort_functions = {
        "Insertion sort": insertion_sort,
        "Merge sort": merge_sort,
        "Timsort": timsort,
    }
    sizes = [1000, 5000, 10000]

    validate_sorting(sort_functions)
    print_results_table(sizes, sort_functions)
    print_conclusions()


if __name__ == "__main__":
    main()
