# # example showing foreign function interface rs <-> py
# import oxiida
# import threading
# from time import time, perf_counter
#
# def count_duration(t0: float) -> float:
#     return perf_counter() - t0
#
# # Heavy CPU call to show the GIL still hold and cannot be surpass
# def cpu_work():
#     total = 0
#     for i in range(10_000_0000):     # ← purely CPU, no I/O, no sleep
#         total += i * i
#
# # 1) How long does one run take?
# pt0 = perf_counter()
# _ = cpu_work()
# duration = count_duration(pt0)
# print(f"single thread: {duration:.2f} s")
#
# # 2) Now run two of exactly the same job in “parallel” threads
# pt0 = perf_counter()
#
# t1 = threading.Thread(target=cpu_work)
# t2 = threading.Thread(target=cpu_work)
# t3 = threading.Thread(target=cpu_work)
# t1.start()
# t2.start()
# t3.start()
# t1.join()
# t2.join()
# t3.join()
#
# duration = count_duration(pt0)
# print(f"triple threads: {duration:.2f} s")
#
# # language = oxiida
# workflow = """
# require cpu_work, count_duration, perf_counter;
# require time;
#
# print "-- multiple tasks (multithreading with gil) --";
# t0 = perf_counter();
# para {
#     seq {
#         cpu_work();
#     }
#
#     seq {
#         cpu_work();
#     }
#
#     seq {
#         cpu_work();
#     }
# }
# print count_duration(t0);
#
# print "-- multiple tasks (multiprocessing) --";
# t0 = perf_counter();
# para {
#     seq {
#         =cpu_work=();
#     }
#
#     seq {
#         =cpu_work=();
#     }
#
#     seq {
#         =cpu_work=();
#     }
# }
# print count_duration(t0);
# """
#
# if __name__ == '__main__':
#     print("-- running workflow --")
#     pt0 = perf_counter()
#     oxiida.run(workflow)
#     _ = count_duration(pt0)
import oxiida
from time import time, perf_counter, sleep

def count_duration(t0: float) -> float:
    return perf_counter() - t0

def cpu_work(idx: str):
    total = 0
    for i in range(10_000_0000):
        total += i * i
    print(f"finish! task #{idx}")

# language = oxiida
workflow = """
require cpu_work, count_duration, perf_counter;
require time;

print "-- multiple tasks (multiprocessing) --";
t0 = perf_counter();
para {
    =cpu_work=("1st");
    =cpu_work=("2nd");
}
print count_duration(t0);
"""

if __name__ == '__main__':
    print("-- running workflow --")
    pt0 = perf_counter()
    oxiida.run(workflow)
    _ = count_duration(pt0)
