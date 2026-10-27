import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import main

SAMPLE = ("MemTotal:       16384000 kB\nMemFree:         4096000 kB\n"
          "MemAvailable:   8192000 kB\nBuffers:         1024000 kB\n")


class TestRAM(unittest.TestCase):
    def test_parse_sample_meminfo(self):
        r = main.parse_meminfo(SAMPLE)
        self.assertTrue(r["available"])
        self.assertEqual(r["total_kb"], 16384000)
        self.assertEqual(r["used_kb"], 8192000)
        self.assertEqual(r["used_percent"], 50.0)

    def test_missing_file_is_honest(self):
        r = main.report("/nonexistent/meminfo")
        self.assertFalse(r["available"])

    def test_real_proc_if_present(self):
        if os.path.exists("/proc/meminfo"):
            r = main.report()
            self.assertTrue(r["available"])
            self.assertGreater(r["total_kb"], 0)


if __name__ == "__main__":
    unittest.main()
