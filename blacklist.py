from config import BLACKLIST_CONFIG, BLOCKED_DOMAINS_PATH, BLOCKED_IPS_PATH
from utils import resolve_domain, read_file_lines, write_file_lines, write_ips
from pf_rules import reload_pf

def apply_blacklist():
    domains = read_file_lines(BLACKLIST_CONFIG)

    if not domains:
        print("⚠️ blacklist.config not found or empty. Skipping blacklist mode. | ⚠️ blacklist.config 未找到或为空。跳过黑名单模式。")
        write_file_lines(BLOCKED_IPS_PATH, domains)
        write_file_lines(BLOCKED_DOMAINS_PATH, domains)
        return

    print("[+] Applying blacklist mode: blocking listed domains | 应用黑名单模式：阻止列出的域名")
    all_ips = set()
    for domain in domains:
        all_ips.update(resolve_domain(domain))
    
    write_ips(all_ips, BLOCKED_IPS_PATH)

    # 🆕 Write domains list into BLOCKED_DOMAINS_PATH
    write_file_lines(BLOCKED_DOMAINS_PATH, domains)
    reload_pf()

def add_to_blacklist(domain):
    entries = set(read_file_lines(BLACKLIST_CONFIG))
    entries.add(domain)
    write_file_lines(BLACKLIST_CONFIG, sorted(entries))
    print(f"[+] {domain} added to blacklist. | 已添加到黑名单。")

def remove_from_blacklist(domain):
    entries = set(read_file_lines(BLACKLIST_CONFIG))
    if domain in entries:
        entries.remove(domain)
        write_file_lines(BLACKLIST_CONFIG, sorted(entries))
        print(f"[-] {domain} removed from blacklist. | 从黑名单中删除。")
    else:
        print(f"[!] {domain} not found in blacklist. | 未在黑名单中找到。")

def list_blacklist():
    entries = read_file_lines(BLACKLIST_CONFIG)
    print("[*] Blacklisted Domains: | 列入黑名单的域名：")
    if not entries:
        print(" - No domains in blacklist. | 黑名单中没有域名。")
    else:
        for d in entries:
            print(f" - {d}")
