import os
from config import WHITELIST_CONFIG, BLOCKED_IPS_PATH, WHITELIST_IPS_PATH
from utils import resolve_domain, read_file_lines, write_file_lines, write_ips
from pf_rules import ensure_pf_rules, reload_pf
import subprocess
from config import WHITELIST_IPS_PATH, PF_ANCHOR_FILE_PATH

def update_whitelist_anchor():
    if not os.path.exists(WHITELIST_IPS_PATH):
        print(f"⚠️ Whitelist file {WHITELIST_IPS_PATH} not found!")
        return

    # Read domains
    with open(WHITELIST_IPS_PATH, "r") as f:
        domains = [line.strip() for line in f if line.strip()]

    if not domains:
        print("⚠️ No domains found in whitelist file.")
        return

    # Prepare mygoodhosts list
    mygoodhosts = "{ " + ", ".join(domains) + " }"

    # Generate anchor file content
    anchor_content = f"""# Whitelist domains
mygoodhosts = "{mygoodhosts}"
myports = "{{ 80, 443, 8080 }}"
block drop out proto {{ tcp, udp }} from any to any port $myports
pass out proto {{ tcp, udp }} from any to $mygoodhosts port $myports
"""

    # Write to anchor file
    with open(PF_ANCHOR_FILE_PATH, "w") as f:
        f.write(anchor_content)

    print(f"✅ Successfully updated whitelist anchor at {PF_ANCHOR_FILE_PATH}.")

    # Reload pfctl
    subprocess.run(["sudo", "pfctl", "-f", "/etc/pf.conf"], check=True)
    print("✅ Reloaded pfctl with new anchor rules.")

def apply_whitelist():
    domains = read_file_lines(WHITELIST_CONFIG)

    if not domains:
        print("⚠️ whitelist.config not found or empty. Skipping whitelist mode. ⚠️ whitelist.config 未找到或为空。跳过白名单模式。")
        write_file_lines(WHITELIST_IPS_PATH, domains)
        return

    print("[+] Applying whitelist mode: only listed domains allowed | 应用白名单模式：仅允许列出的域")

    write_file_lines(WHITELIST_IPS_PATH, domains)
    update_whitelist_anchor()  # <--- ADD THIS
    ensure_pf_rules()
    reload_pf()

def add_to_whitelist(domain):
    entries = set(read_file_lines(WHITELIST_CONFIG))
    entries.add(domain)
    write_file_lines(WHITELIST_CONFIG, sorted(entries))
    print(f"[+] {domain} added to whitelist. | 已添加到白名单。")

def remove_from_whitelist(domain):
    entries = set(read_file_lines(WHITELIST_CONFIG))
    if domain in entries:
        entries.remove(domain)
        write_file_lines(WHITELIST_CONFIG, sorted(entries))
        print(f"[-] {domain} removed from whitelist. | 从白名单中删除。")
    else:
        print(f"[!] {domain} not found in whitelist. | 在白名单中未找到。")

def list_whitelist():
    entries = read_file_lines(WHITELIST_CONFIG)
    print("[*] Whitelisted Domains: | 白名单域名：")
    if not entries:
        print(" - No domains in whitelist. | 白名单中没有域名。")
    else:
        for d in entries:
            print(f" - {d}")
