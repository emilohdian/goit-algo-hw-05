import sys
import re


def parse_log_line(line: str) -> dict:
    pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) (\w+) (.+)$'
    match = re.match(pattern, line)
    if match:
        return {
            "datetime": match.group(1),
            "level": match.group(2),
            "message": match.group(3)
        }
    else:
        return None


def load_logs(file_path: str) -> list:
    logs = []
    try:
        with open(file_path, 'r') as file:
            for line in file:
                log_data = parse_log_line(line.strip())
                if log_data:
                    logs.append(log_data)
    except FileNotFoundError:
        print("File not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading log file: {e}")
        sys.exit(1)
    return logs


def filter_logs_by_level(logs: list, level: str) -> list:
    return [log for log in logs if log['level'].upper() == level.upper()]


def count_logs_by_level(logs: list) -> dict:
    counts = {}
    for log in logs:
        level = log['level']
        if level in counts:
            counts[level] += 1
        else:
            counts[level] = 1
    return counts


def display_log_counts(counts: dict):
    print("Рівень логування | Кількість")
    print("-----------------|----------")
    for level, count in counts.items():
        print(f"{level:<17} | {count}")


def display_logs(logs: list):
    print("Рівень логування | Повідомлення")
    print("-----------------|--------------")
    for log in logs:
        print(f"{log['level']:<17} | {log['message']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py /path/to/logfile.log [log_level]")
        sys.exit(1)

    log_file = sys.argv[1]
    log_level = sys.argv[2].upper() if len(sys.argv) > 2 else None

    logs = load_logs(log_file)

    if log_level:
        filtered_logs = filter_logs_by_level(logs, log_level)
        display_logs(filtered_logs)
    else:
        counts = count_logs_by_level(logs)
        display_log_counts(counts)
