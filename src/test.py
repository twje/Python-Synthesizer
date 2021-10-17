from concurrent import futures

data = [1, 2, 3, 4]


class Hello:
    def __init__(self):
        self.foo = 10

    def run(self, value):
        return value + self.foo


hello = Hello()

if __name__ == "__main__":
    executor = futures.ProcessPoolExecutor()
    to_do = {}
    for cc in data:
        future = executor.submit(hello.run, cc)
        to_do[future] = cc

    results = []
    for future in futures.as_completed(to_do):
        result = future.result()
        results.append(result)

    print(results)
