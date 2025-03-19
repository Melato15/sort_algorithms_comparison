import random
import codecs
from abc import ABC, abstractmethod
import time
from statistics import mean

# Seu código original
class RandomNumberStrategy(ABC):
    @abstractmethod
    def generate_numbers(self, num, start, end):
        pass

class UniqueRandomNumberStrategy(RandomNumberStrategy):
    def generate_numbers(self, num, start, end):
        arr = []
        tmp = random.randint(start, end)
        for x in range(num):
            while tmp in arr:
                tmp = random.randint(start, end)
            arr.append(tmp)
        arr.sort()
        return arr

class RandomNumberGenerator:
    def __init__(self, strategy: RandomNumberStrategy):
        self.strategy = strategy

    def create_random_number_list(self, num, start=1, end=100):
        arr = self.strategy.generate_numbers(num, start, end)
        with codecs.open("Data.txt", "w", "utf-8") as file:
            file.write(','.join(map(str, arr)))
        return arr

# Classe para métricas
class Metrics:
    def __init__(self):
        self.time_ms = 0
        self.comparisons = 0
        self.swaps = 0

# Função para carregar dados
def load_data():
    with codecs.open("Data.txt", "r", "utf-8") as file:
        return [int(x) for x in file.read().split(',')]

# Implementações dos algoritmos de ordenação
def bubble_sort(arr):
    metrics = Metrics()
    arr_copy = arr.copy()
    n = len(arr_copy)
    for i in range(n):
        for j in range(0, n-i-1):
            metrics.comparisons += 1
            if arr_copy[j] > arr_copy[j+1]:
                arr_copy[j], arr_copy[j+1] = arr_copy[j+1], arr_copy[j]
                metrics.swaps += 1
    return arr_copy, metrics

def bubble_sort_improved(arr):
    metrics = Metrics()
    arr_copy = arr.copy()
    n = len(arr_copy)
    for i in range(n):
        swapped = False
        for j in range(0, n-i-1):
            metrics.comparisons += 1
            if arr_copy[j] > arr_copy[j+1]:
                arr_copy[j], arr_copy[j+1] = arr_copy[j+1], arr_copy[j]
                metrics.swaps += 1
                swapped = True
        if not swapped:
            break
    return arr_copy, metrics

def insertion_sort(arr):
    metrics = Metrics()
    arr_copy = arr.copy()
    n = len(arr_copy)
    for i in range(1, n):
        key = arr_copy[i]
        j = i - 1
        while j >= 0:
            metrics.comparisons += 1
            if arr_copy[j] > key:
                arr_copy[j + 1] = arr_copy[j]
                metrics.swaps += 1
                j -= 1
            else:
                break
        arr_copy[j + 1] = key
        if j >= 0:
            metrics.swaps += 1
    return arr_copy, metrics

def selection_sort(arr):
    metrics = Metrics()
    arr_copy = arr.copy()
    n = len(arr_copy)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            metrics.comparisons += 1
            if arr_copy[j] < arr_copy[min_idx]:
                min_idx = j
        if min_idx != i:
            arr_copy[i], arr_copy[min_idx] = arr_copy[min_idx], arr_copy[i]
            metrics.swaps += 1
    return arr_copy, metrics

def quick_sort(arr):
    metrics = Metrics()
    arr_copy = arr.copy()
    
    def partition(low, high):
        pivot = arr_copy[high]
        i = low - 1
        for j in range(low, high):
            metrics.comparisons += 1
            if arr_copy[j] <= pivot:
                i += 1
                arr_copy[i], arr_copy[j] = arr_copy[j], arr_copy[i]
                metrics.swaps += 1
        arr_copy[i+1], arr_copy[high] = arr_copy[high], arr_copy[i+1]
        metrics.swaps += 1
        return i + 1

    def quick_sort_recursive(low, high):
        if low < high:
            pi = partition(low, high)
            quick_sort_recursive(low, pi-1)
            quick_sort_recursive(pi+1, high)

    quick_sort_recursive(0, len(arr_copy)-1)
    return arr_copy, metrics

def merge_sort(arr):
    metrics = Metrics()
    arr_copy = arr.copy()
    
    def merge(left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            metrics.comparisons += 1
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
            metrics.swaps += 1
        result.extend(left[i:])
        result.extend(right[j:])
        return result

    def merge_sort_recursive(arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = merge_sort_recursive(arr[:mid])
        right = merge_sort_recursive(arr[mid:])
        return merge(left, right)

    sorted_arr = merge_sort_recursive(arr_copy)
    return sorted_arr, metrics

def tim_sort(arr):
    metrics = Metrics()
    arr_copy = arr.copy()
    min_run = 32

    def insertion_sort_tim(start, end):
        for i in range(start + 1, end + 1):
            key = arr_copy[i]
            j = i - 1
            while j >= start:
                metrics.comparisons += 1
                if arr_copy[j] > key:
                    arr_copy[j + 1] = arr_copy[j]
                    metrics.swaps += 1
                    j -= 1
                else:
                    break
            arr_copy[j + 1] = key
            if j >= start:
                metrics.swaps += 1

    def merge_tim(left, mid, right):
        left_arr = arr_copy[left:mid + 1]
        right_arr = arr_copy[mid + 1:right + 1]
        i = j = 0
        k = left
        while i < len(left_arr) and j < len(right_arr):
            metrics.comparisons += 1
            if left_arr[i] <= right_arr[j]:
                arr_copy[k] = left_arr[i]
                i += 1
            else:
                arr_copy[k] = right_arr[j]
                j += 1
            metrics.swaps += 1
            k += 1
        while i < len(left_arr):
            arr_copy[k] = left_arr[i]
            i += 1
            k += 1
            metrics.swaps += 1
        while j < len(right_arr):
            arr_copy[k] = right_arr[j]
            j += 1
            k += 1
            metrics.swaps += 1

    n = len(arr_copy)
    for i in range(0, n, min_run):
        insertion_sort_tim(i, min(i + min_run - 1, n - 1))
    
    size = min_run
    while size < n:
        for left in range(0, n, size * 2):
            mid = min(left + size - 1, n - 1)
            right = min(left + 2 * size - 1, n - 1)
            if mid < right:
                merge_tim(left, mid, right)
        size *= 2
    
    return arr_copy, metrics

def shell_sort(arr):
    metrics = Metrics()
    arr_copy = arr.copy()
    n = len(arr_copy)
    gap = n // 2
    
    while gap > 0:
        for i in range(gap, n):
            temp = arr_copy[i]
            j = i
            while j >= gap:
                metrics.comparisons += 1
                if arr_copy[j - gap] > temp:
                    arr_copy[j] = arr_copy[j - gap]
                    metrics.swaps += 1
                    j -= gap
                else:
                    break
            arr_copy[j] = temp
            if j >= gap:
                metrics.swaps += 1
        gap //= 2
    return arr_copy, metrics

# Função de comparação
def run_comparison(algorithms, num_executions=5):
    strategy = UniqueRandomNumberStrategy()
    generator = RandomNumberGenerator(strategy)
    generator.create_random_number_list(10, 100, 100000)
    
    original_data = load_data()
    results = {algo.__name__: {'times': [], 'comparisons': [], 'swaps': []} 
              for algo in algorithms}
    
    for algo in algorithms:
        for _ in range(num_executions):
            start_time = time.perf_counter()
            _, metrics = algo(original_data)
            end_time = time.perf_counter()
            
            execution_time = (end_time - start_time) * 1000
            results[algo.__name__]['times'].append(execution_time)
            results[algo.__name__]['comparisons'].append(metrics.comparisons)
            results[algo.__name__]['swaps'].append(metrics.swaps)
    
    print("\nResultados (médias de", num_executions, "execuções):")
    print("-" * 60)
    for algo_name, metrics in results.items():
        print(f"\n{algo_name}:")
        print(f"Tempo de execução: {mean(metrics['times']):.2f} ms")
        print(f"Comparações: {mean(metrics['comparisons']):.0f}")
        print(f"Trocas: {mean(metrics['swaps']):.0f}")

# Executar
if __name__ == "__main__":
    algorithms = [
        bubble_sort,
        bubble_sort_improved,
        insertion_sort,
        selection_sort,
        quick_sort,
        merge_sort,
        tim_sort,
        shell_sort
    ]
    run_comparison(algorithms, num_executions=5)