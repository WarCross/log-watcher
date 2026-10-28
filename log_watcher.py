import sys

def analyze_logs(logs):
    stats = {}
    for log in logs:
        parts = log.split()
        ip, code = parts[0], parts[-2]
        stats.setdefault(ip, {"requests": 0, "errors": 0, "paths": set()})
        stats[ip]["requests"] += 1
        stats[ip]["paths"].add(parts[6])

        if code == "404":
            stats[ip]["errors"] += 1

    return stats

def make_report(stats):
    lines = []
    for ip, s in stats.items():
        status = "SCANNER" if s["errors"] >= 3 or len(s["paths"]) >= 4 else "OK"
        lines.append(f"{ip} - {status}, 404: {s['errors']}, unique paths: {len(s['paths'])}")
    return "\n".join(lines)
    
def read_logs(file_path):
    with open(file_path, encoding="utf-8") as f:
        logs = []
        for line in f:
            stripped = line.strip()
            if stripped:                    # пропускаем пустые
                logs.append(stripped)       # кладём уже почищенные
        return logs          
    
if len(sys.argv) < 2:
    print("Использование: python3 log_watcher.py <путь_к_файлу>")
    print("Пример: python3 log_watcher.py access.log")
    sys.exit(1)  # выход с кодом ошибки

file_path = sys.argv[1]  # берём первый аргумент
logs = read_logs(file_path)
report = make_report(analyze_logs(logs))
print(report)




