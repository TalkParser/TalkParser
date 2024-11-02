import statistics
from time import time
from unittest import TestCase

ITER_NUM = 100


class KakaoTalkParserTest(TestCase):
    def test_large_process_time(self):
        process_times = []
        for iline in range(ITER_NUM):
            with self.subTest(line=iline):
                start = time()

                process_times.append(time() - start)
                self.assertEqual(len(data.data), 1158705)
        average_time = statistics.mean(process_times)
        print(f"Average process time over {ITER_NUM} runs: {average_time}")

    def test_middle_process_time(self):
        process_times = []
        for iline in range(ITER_NUM):
            with self.subTest(line=iline):
                start = time()

                process_times.append(time() - start)
                self.assertEqual(len(data.data), 247234)
        average_time = statistics.mean(process_times)
        print(f"Average process time over {ITER_NUM} runs: {average_time}")

    def test_small_process_time(self):
        process_times = []
        for iline in range(ITER_NUM):
            with self.subTest(line=iline):
                start = time()

                process_times.append(time() - start)
                self.assertEqual(len(data.data), 5773)
        average_time = statistics.mean(process_times)
        print(f"Average process time over {ITER_NUM} runs: {average_time}")
