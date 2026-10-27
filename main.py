"""RAM usage reporter: parse /proc/meminfo on Linux (stdlib + platform files)."""
import os
import sys


def parse_meminfo(text):
    vals = {}
    for line in text.splitlines():
        if ":" in line:
            key, rest = line.split(":", 1)
            parts = rest.strip().split()
            if parts and parts[0].isdigit():
                vals[key.strip()] = int(parts[0])  # kB
    total = vals.get("MemTotal")
    avail = vals.get("MemAvailable", vals.get("MemFree"))
    if not total:
        return {"available": False, "error": "MemTotal not found in meminfo"}
    used = total - avail if avail is not None else None
    pct = round(used / total * 100, 1) if used is not None else None
    return {"available": True, "total_kb": total, "available_kb": avail,
            "used_kb": used, "used_percent": pct}


def report(meminfo_path="/proc/meminfo"):
    if not os.path.exists(meminfo_path):
        return {"available": False, "platform": sys.platform,
                "error": f"{meminfo_path} not found; RAM reporting via /proc/meminfo "
                         "is Linux-only and no psutil fallback is used."}
    with open(meminfo_path, encoding="utf-8") as fh:
        result = parse_meminfo(fh.read())
    result["platform"] = sys.platform
    return result


def main():
    r = report()
    if not r["available"]:
        print(f"RAM report unavailable: {r['error']}")
        return 0
    print(f"Total RAM: {r['total_kb']} kB")
    print(f"Available: {r['available_kb']} kB")
    print(f"Used: {r['used_kb']} kB ({r['used_percent']}%)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
