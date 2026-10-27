# ram-usage-reporter

Report memory usage by parsing `/proc/meminfo` on Linux, using only the
standard library and platform files. No psutil, no invented numbers — on a
system without `/proc/meminfo` it says so instead of guessing.

## How to run

```bash
python3 main.py
```

## Example output (sample from test fixture data)

```text
Total RAM: 16384000 kB
Available: 8192000 kB
Used: 8192000 kB (50.0%)
```

Standard library only. No network access.
