import os
from pf_rules import ensure_pf_rules, create_launchd_plist
from blacklist import (
    apply_blacklist,
    add_to_blacklist,
    remove_from_blacklist,
    list_blacklist
)
from whitelist import (
    apply_whitelist,
    add_to_whitelist,
    remove_from_whitelist,
    list_whitelist
)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("⚠️ Must run as root (sudo)")
        exit(1)

    ensure_pf_rules()
    create_launchd_plist()
    apply_whitelist()
    apply_blacklist()

    while True:
        print("\n--- Website Blocker --- | --- 网站拦截器 ---")
        print("1. Block domain - 拦截域名")
        print("2. Unblock domain - 解除拦截域名")
        print("3. List blocked domains - 列出已拦截域名")
        print("4. Add whitelist domain - 添加白名单域名")
        print("5. Remove whitelist domain - 移除白名单域名")
        print("6. List whitelist domains - 列出白名单域名")
        print("7. Exit - 退出")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            domain = input("Enter domain to block: ").strip()
            add_to_blacklist(domain)
            apply_blacklist()
        elif choice == "2":
            domain = input("Enter domain to unblock: ").strip()
            remove_from_blacklist(domain)
            apply_blacklist()
        elif choice == "3":
            list_blacklist()
        elif choice == "4":
            domain = input("Enter domain to whitelist: ").strip()
            add_to_whitelist(domain)
            apply_whitelist()
        elif choice == "5":
            domain = input("Enter domain to remove from whitelist: ").strip()
            remove_from_whitelist(domain)
            apply_whitelist()
        elif choice == "6":
            list_whitelist()
        elif choice == "7":
            break
        else:
            print("Invalid choice.")
