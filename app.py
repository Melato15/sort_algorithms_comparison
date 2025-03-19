import random
import codecs
from abc import ABC, abstractmethod
import time
from statistics import mean
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

# Configurar o recurso com o nome do serviço
resource = Resource(attributes={
    ResourceAttributes.SERVICE_NAME: "sorting_algorithms"
})

# Configurar o provedor de rastreamento
trace.set_tracer_provider(TracerProvider(resource=resource))

# Configurar o exporter do Jaeger
jaeger_exporter = JaegerExporter(
    collector_endpoint="http://localhost:14268/api/traces"
)

# Adicionar o processador de spans
span_processor = BatchSpanProcessor(jaeger_exporter)
trace.get_tracer_provider().add_span_processor(span_processor)

# Criar o tracer
tracer = trace.get_tracer("sorting_algorithms_tracer")

# Classes e funções do código original
class RandomNumberStrategy(ABC):
    @abstractmethod
    def generate_numbers(self, num, start, end):
        pass

class UniqueRandomNumberStrategy(RandomNumberStrategy):
    def generate_numbers(self, num, start, end):
        with tracer.start_as_current_span("generate_unique_numbers") as span:
            arr = []
            tmp = random.randint(start, end)
            for x in range(num):
                while tmp in arr:
                    tmp = random.randint(start, end)
                arr.append(tmp)
            arr.sort()
            span.set_attribute("generated_numbers_count", len(arr))
            return arr

class RandomNumberGenerator:
    def __init__(self, strategy: RandomNumberStrategy):
        self.strategy = strategy

    def create_random_number_list(self, num, start=1, end=100):
        with tracer.start_as_current_span("create_random_number_list") as span:
            arr = self.strategy.generate_numbers(num, start, end)
            with codecs.open("Data.txt", "w", "utf-8") as file:
                file.write(','.join(map(str, arr)))
            span.set_attribute("list_size", len(arr))
            return arr

class Metrics:
    def __init__(self):
        self.time_ms = 0
        self.comparisons = 0
        self.swaps = 0

def load_data():
    with tracer.start_as_current_span("load_data") as span:
        with codecs.open("Data.txt", "r", "utf-8") as file:
            data = [int(x) for x in file.read().split(',')]
            span.set_attribute("loaded_numbers_count", len(data))
            return data

# Algoritmos de ordenação com tracing
def bubble_sort(arr):
    metrics = Metrics()
    arr_copy = arr.copy()
    with tracer.start_as_current_span("bubble_sort") as span:
        n = len(arr_copy)
        for i in range(n):
            for j in range(0, n-i-1):
                metrics.comparisons += 1
                if arr_copy[j] > arr_copy[j+1]:
                    arr_copy[j], arr_copy[j+1] = arr_copy[j+1], arr_copy[j]
                    metrics.swaps += 1
        span.set_attributes({
            "comparisons": metrics.comparisons,
            "swaps": metrics.swaps,
            "array_size": n
        })
    return arr_copy, metrics

def bubble_sort_improved(arr):
    metrics = Metrics()
    arr_copy = arr.copy()
    with tracer.start_as_current_span("bubble_sort_improved") as span:
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
        span.set_attributes({
            "comparisons": metrics.comparisons,
            "swaps": metrics.swaps,
            "array_size": n
        })
    return arr_copy, metrics

def insertion_sort(arr):
    metrics = Metrics()
    arr_copy = arr.copy()
    with tracer.start_as_current_span("insertion_sort") as span:
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
        span.set_attributes({
            "comparisons": metrics.comparisons,
            "swaps": metrics.swaps,
            "array_size": n
        })
    return arr_copy, metrics

def selection_sort(arr):
    metrics = Metrics()
    arr_copy = arr.copy()
    with tracer.start_as_current_span("selection_sort") as span:
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
        span.set_attributes({
            "comparisons": metrics.comparisons,
            "swaps": metrics.swaps,
            "array_size": n
        })
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

    with tracer.start_as_current_span("quick_sort") as span:
        quick_sort_recursive(0, len(arr_copy)-1)
        span.set_attributes({
            "comparisons": metrics.comparisons,
            "swaps": metrics.swaps,
            "array_size": len(arr_copy)
        })
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

    with tracer.start_as_current_span("merge_sort") as span:
        sorted_arr = merge_sort_recursive(arr_copy)
        span.set_attributes({
            "comparisons": metrics.comparisons,
            "swaps": metrics.swaps,
            "array_size": len(arr_copy)
        })
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

    with tracer.start_as_current_span("tim_sort") as span:
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
        span.set_attributes({
            "comparisons": metrics.comparisons,
            "swaps": metrics.swaps,
            "array_size": n
        })
    return arr_copy, metrics

def shell_sort(arr):
    metrics = Metrics()
    arr_copy = arr.copy()
    with tracer.start_as_current_span("shell_sort") as span:
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
        span.set_attributes({
            "comparisons": metrics.comparisons,
            "swaps": metrics.swaps,
            "array_size": n
        })
    return arr_copy, metrics

# Função de comparação com tracing
def run_comparison(algorithms, num_executions=5):
    with tracer.start_as_current_span("run_comparison") as span:
        strategy = UniqueRandomNumberStrategy()
        generator = RandomNumberGenerator(strategy)
        generator.create_random_number_list(10, 100, 100000)
        
        original_data = load_data()
        results = {algo.__name__: {'times': [], 'comparisons': [], 'swaps': []} 
                  for algo in algorithms}
        
        for algo in algorithms:
            for i in range(num_executions):
                with tracer.start_as_current_span(f"{algo.__name__}_execution_{i+1}") as exec_span:
                    start_time = time.perf_counter()
                    _, metrics = algo(original_data)
                    end_time = time.perf_counter()
                    
                    execution_time = (end_time - start_time) * 1000
                    results[algo.__name__]['times'].append(execution_time)
                    results[algo.__name__]['comparisons'].append(metrics.comparisons)
                    results[algo.__name__]['swaps'].append(metrics.swaps)
                    
                    exec_span.set_attributes({
                        "execution_time_ms": execution_time,
                        "comparisons": metrics.comparisons,
                        "swaps": metrics.swaps,
                        "execution_number": i+1
                    })
        
        span.set_attribute("num_executions", num_executions)
        span.set_attribute("algorithms_tested", len(algorithms))
        
        print("\nResultados (médias de", num_executions, "execuções):")
        print("-" * 60)
        for algo_name, metrics in results.items():
            print(f"\n{algo_name}:")
            print(f"Tempo de execução: {mean(metrics['times']):.2f} ms")
            print(f"Comparações: {mean(metrics['comparisons']):.0f}")
            print(f"Trocas: {mean(metrics['swaps']):.0f}")

# Executar
if __name__ == "__main__":
    with tracer.start_as_current_span("main"):
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
    
    # Forçar envio dos traces e encerrar
    trace.get_tracer_provider().force_flush()
    trace.get_tracer_provider().shutdown()