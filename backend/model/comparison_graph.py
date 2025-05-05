import matplotlib.pyplot as plt

# Data
concurrent_requests = [1, 2, 3, 4]
response_times = [54.18, 47.05, 49.76, 52.82]

# Plot
plt.figure(figsize=(8, 5))
plt.plot(concurrent_requests, response_times, marker='o', linestyle='-', color='blue')

plt.title('Concurrency Test: Response Time vs Number of Concurrent Requests')
plt.xlabel('Number of Concurrent Requests')
plt.ylabel('Response Time (seconds)')
plt.grid(True)
plt.xticks(concurrent_requests)

plt.show()
