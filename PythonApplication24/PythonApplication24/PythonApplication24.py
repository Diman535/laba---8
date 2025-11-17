import random
import time

MAX_VERTICES = 100

# ----------------------------- Безопасный ввод -----------------------------
def safe_int_input(prompt, min_value=None, max_value=None):
    while True:
        value = input(prompt).strip()
        if not value.isdigit():
            print("Ошибка: нужно ввести целое число!\n")
            continue
        value = int(value)
        if min_value is not None and value < min_value:
            print(f"Ошибка: число должно быть не меньше {min_value}!\n")
            continue
        if max_value is not None and value > max_value:
            print(f"Ошибка: число должно быть не больше {max_value}!\n")
            continue
        return value

# ----------------------------- Генерация матрицы -----------------------------
def generate_adjacency_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    random.seed(time.time())
    for i in range(n):
        for j in range(i, n):
            if i == j:
                matrix[i][j] = 0
            else:
                has_edge = random.randint(0, 99) < 30
                matrix[i][j] = has_edge
                matrix[j][i] = has_edge
    return matrix

def print_matrix(matrix, n):
    print(f"Матрица смежности ({n}x{n}):")
    print("   ", end="")
    for i in range(n):
        print(f"{i:2d} ", end="")
    print()
    for i in range(n):
        print(f"{i:2d} ", end="")
        for j in range(n):
            print(f"{matrix[i][j]:2d} ", end="")
        print()
    print()

# ----------------------------- Очередь (стандартная) -----------------------------
class Queue:
    def __init__(self):
        self.data = []
    def is_empty(self):
        return len(self.data) == 0
    def enqueue(self, x):
        self.data.append(x)
    def dequeue(self):
        if self.is_empty():
            return -1
        return self.data.pop(0)

# ----------------------------- BFS по матрице -----------------------------
def bfs_matrix(matrix, n, start):
    visited = [0] * n
    q = Queue()
    print(f"Обход в ширину (матрица смежности), начиная с вершины {start}: ", end="")
    visited[start] = 1
    q.enqueue(start)
    while not q.is_empty():
        current = q.dequeue()
        print(current, end=" ")
        for i in range(n):
            if matrix[current][i] == 1 and not visited[i]:
                visited[i] = 1
                q.enqueue(i)
    print()

def bfs_matrix_silent(matrix, n, start):
    visited = [0] * n
    q = Queue()
    visited[start] = 1
    q.enqueue(start)
    while not q.is_empty():
        current = q.dequeue()
        for i in range(n):
            if matrix[current][i] == 1 and not visited[i]:
                visited[i] = 1
                q.enqueue(i)

# ----------------------------- Список смежности -----------------------------
class AdjListNode:
    def __init__(self, dest):
        self.dest = dest
        self.next = None

class Graph:
    def __init__(self, n):
        self.numVertices = n
        self.array = [None] * n

def matrix_to_adjlist(matrix, n):
    graph = Graph(n)
    for i in range(n):
        head = None
        for j in range(n):
            if matrix[i][j] == 1:
                new_node = AdjListNode(j)
                new_node.next = head
                head = new_node
        graph.array[i] = head
    return graph

def print_adjlist(graph):
    print("Списки смежности:")
    for i in range(graph.numVertices):
        print(f"Вершина {i}: ", end="")
        temp = graph.array[i]
        while temp:
            print(temp.dest, end=" ")
            temp = temp.next
        print()
    print()

# ----------------------------- BFS по спискам смежности -----------------------------
def bfs_adjlist(graph, start):
    visited = [0] * graph.numVertices
    q = Queue()
    print(f"Обход в ширину (списки смежности), начиная с вершины {start}: ", end="")
    visited[start] = 1
    q.enqueue(start)
    while not q.is_empty():
        current = q.dequeue()
        print(current, end=" ")
        temp = graph.array[current]  # <-- исправлено!
        while temp:
            if not visited[temp.dest]:
                visited[temp.dest] = 1
                q.enqueue(temp.dest)
            temp = temp.next
    print()

# ----------------------------- Собственная очередь -----------------------------
class CustomQueue:
    def __init__(self, capacity):
        self.items = [0] * capacity
        self.front = 0
        self.rear = -1
        self.capacity = capacity
    def is_empty(self):
        return self.rear < self.front
    def enqueue(self, x):
        if self.rear == self.capacity - 1:
            print("Очередь переполнена!")
            return
        self.rear += 1
        self.items[self.rear] = x
    def dequeue(self):
        if self.is_empty():
            return -1
        x = self.items[self.front]
        self.front += 1
        return x

def bfs_custom(matrix, n, start):
    visited = [0] * n
    q = CustomQueue(n * n)
    print(f"Обход в ширину (собственная очередь), начиная с вершины {start}: ", end="")
    visited[start] = 1
    q.enqueue(start)
    while not q.is_empty():
        current = q.dequeue()
        print(current, end=" ")
        for i in range(n):
            if matrix[current][i] == 1 and not visited[i]:
                visited[i] = 1
                q.enqueue(i)
    print()

def bfs_custom_silent(matrix, n, start):
    visited = [0] * n
    q = CustomQueue(n * n)
    visited[start] = 1
    q.enqueue(start)
    while not q.is_empty():
        current = q.dequeue()
        for i in range(n):
            if matrix[current][i] == 1 and not visited[i]:
                visited[i] = 1
                q.enqueue(i)

# ----------------------------- Измерение времени -----------------------------
def measure_time(func, *args):
    start = time.time()
    func(*args)
    end = time.time()
    return end - start

# ----------------------------- MAIN -----------------------------
def main():
    n = safe_int_input("Введите количество вершин графа: ", 1, MAX_VERTICES)
    print("=== ЗАДАНИЕ 1 ===")
    matrix = generate_adjacency_matrix(n)
    print_matrix(matrix, n)
    start = safe_int_input(f"Введите начальную вершину для обхода (0-{n - 1}): ", 0, n - 1)
    graph = matrix_to_adjlist(matrix, n)
    print_adjlist(graph)
    bfs_matrix(matrix, n, start)
    bfs_adjlist(graph, start)
    print("\n=== ЗАДАНИЕ 2 ===")
    bfs_custom(matrix, n, start)
    print("\n=== СРАВНЕНИЕ ВРЕМЕНИ РАБОТЫ ===")
    t1 = measure_time(bfs_matrix_silent, matrix, n, start)
    t2 = measure_time(bfs_custom_silent, matrix, n, start)
    print(f"Время выполнения со стандартной очередью: {t1:.6f} секунд")
    print(f"Время выполнения с собственной очередью: {t2:.6f} секунд")
    print(f"Разница: {t2 - t1:.6f} секунд")

if __name__ == "__main__":
    main()

