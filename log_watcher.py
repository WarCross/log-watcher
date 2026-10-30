import sys

def analyze_logs(logs):
    stats = {}
    broken = 0
    processed = 0
    for n, log in enumerate(logs, 1):
        try: 
            parts = log.split()
            ip, code, path = parts[0], parts[-2], parts[6]
        except IndexError:
            broken += 1
            print(f"Пропущена битая строка {n}")
            continue
        stats.setdefault(ip, {"requests": 0, "errors": 0, "paths": set()})
        stats[ip]["requests"] += 1
        stats[ip]["paths"].add(path)

        if code == "404":
            stats[ip]["errors"] += 1
        processed += 1

    print(f"Всего обработано: {processed} строк, пропущено битых: {broken}")
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
            if stripped:                    
                logs.append(stripped)       
        return logs          
    
if len(sys.argv) < 2:
    print("Использование: python3 log_watcher.py <путь_к_файлу>")
    print("Пример: python3 log_watcher.py access.log")
    sys.exit(1)  

file_path = sys.argv[1]
try:
    logs = read_logs(file_path)
    report = make_report(analyze_logs(logs))
    print(report)
except FileNotFoundError:
    print(f"Ошибка: файл '{file_path}' не найден")
    sys.exit(1)
except PermissionError:
    print(f"Ошибка: нет прав на чтение '{file_path}'")
    sys.exit(1)
except UnicodeDecodeError:
    print(f"Ошибка: файл '{file_path}' повреждён или в неизвестной кодировке")
    sys.exit(1)


