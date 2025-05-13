# Step 2: utils.py
# ------------------
import socket

def resolve_domain(domain):
    try:
        return list(set(socket.gethostbyname_ex(domain)[2]))
    except Exception as e:
        print(f"[!] Failed to resolve {domain}: {e}")
        return []

def write_ips(all_ips, path):
    with open(path, "w") as f:
        f.write("\n".join(sorted(all_ips)) + "\n")

def read_file_lines(path):
    try:
        with open(path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[!] Failed to read {path}: {e}")
        return []

def write_file_lines(path, lines):
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")

