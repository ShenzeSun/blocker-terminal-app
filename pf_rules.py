# pf_rules.py
import subprocess
import re
import os
import shutil
from utils import resolve_domain, read_file_lines, write_file_lines, write_ips
from config import NETWORK_INTERFACE, PF_ANCHOR_FILE_PATH, PF_CONF, BLOCKED_IPS_PATH, LAUNCHD_PLIST_PATH, WHITELIST_CONFIG, BLACKLIST_CONFIG

def backup_pf_conf():
    """Backup the pf.conf before modifying."""
    backup_path = PF_CONF + ".bak"
    shutil.copy(PF_CONF, backup_path)
    print(f"🛡️  Backup created: {backup_path}")

def ensure_pf_rules():
    """Ensure PF rules are correctly set up based on configs."""
    backup_pf_conf()

    # Define basic anchor rules
    anchor_rule = 'anchor "org.user.block.out"'
    load_anchor_rule = f'load anchor "org.user.block.out" from "{PF_ANCHOR_FILE_PATH}"'
    whitelist_domains = read_file_lines(WHITELIST_CONFIG)

    # Define blacklist rules
    rule_table = f'table <blocked_sites> persist file "{BLOCKED_IPS_PATH}"'
    rule_in = f'block in quick on {NETWORK_INTERFACE} from any to <blocked_sites>'
    rule_out = f'block out quick on {NETWORK_INTERFACE} from any to <blocked_sites>'
    blacklist_domains = read_file_lines(BLACKLIST_CONFIG)

    # Rules to ensure based on configs
    rules_to_ensure = []
    if whitelist_domains:
        rules_to_ensure += [anchor_rule, load_anchor_rule]
    if blacklist_domains:
        rules_to_ensure += [rule_table, rule_in, rule_out]

    # Read current pf.conf
    with open(PF_CONF, "r") as f:
        conf_content = f.read()

    # Clean anchor rules if whitelist empty
    if not whitelist_domains:
        if anchor_rule in conf_content or load_anchor_rule in conf_content:
            print("⚠️  Whitelist missing or empty. Cleaning anchor rules from pf.conf...")
            conf_content = re.sub(r'^.*anchor "org\.user\.block\.out".*\n?', '', conf_content, flags=re.MULTILINE)
            conf_content = re.sub(r'^.*load anchor "org\.user\.block\.out" from ".*".*\n?', '', conf_content, flags=re.MULTILINE)

    # Clean blacklist rules if blacklist empty
    if not blacklist_domains:
        if rule_table in conf_content or rule_in in conf_content or rule_out in conf_content:
            print("⚠️  Blacklist missing or empty. Cleaning block rules from pf.conf...")
            conf_content = re.sub(r'^.*table <blocked_sites> persist file ".*".*\n?', '', conf_content, flags=re.MULTILINE)
            conf_content = re.sub(r'^.*block in quick on .* from any to <blocked_sites>.*\n?', '', conf_content, flags=re.MULTILINE)
            conf_content = re.sub(r'^.*block out quick on .* from any to <blocked_sites>.*\n?', '', conf_content, flags=re.MULTILINE)

    # Remove any double blank lines
    conf_content = "\n".join(line for line in conf_content.splitlines() if line.strip())

    # Save cleaned conf
    with open(PF_CONF, "w") as f:
        f.write(conf_content + "\n")  # Always end with newline

    # Now read again to check for missing rules
    with open(PF_CONF, "r") as f:
        conf_content = f.read()

    # Find missing rules
    missing_rules = []
    for rule in rules_to_ensure:
        if rule not in conf_content:
            missing_rules.append(rule)

    # Append missing rules
    if missing_rules:
        with open(PF_CONF, "a") as f:
            f.write("\n" + "\n".join(missing_rules) + "\n")
        subprocess.run(["sudo", "pfctl", "-f", PF_CONF], check=True)
        print(f"✅ Added missing pf rules: {missing_rules} and reloaded pfctl.")
    else:
        subprocess.run(["sudo", "pfctl", "-f", PF_CONF], check=True)
        print("✅ All pf rules already exist. No changes made.")

def reload_pf():
    """Reload pfctl and enable if necessary."""
    pf_status = subprocess.run(["sudo", "pfctl", "-s", "info"], capture_output=True, text=True)
    if "Status: Enabled" not in pf_status.stdout:
        subprocess.run(["sudo", "pfctl", "-e"], check=True)
    subprocess.run(["sudo", "pfctl", "-f", PF_CONF], check=True)
    print("✅ pfctl reloaded.")

def create_launchd_plist():
    """Create launchd plist for auto-start pf."""
    plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.pf.start</string>
  <key>ProgramArguments</key>
  <array>
    <string>/sbin/pfctl</string>
    <string>-e</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
</dict>
</plist>
"""
    with open(LAUNCHD_PLIST_PATH, "w") as f:
        f.write(plist_content)
    subprocess.run(["sudo", "launchctl", "load", "-w", LAUNCHD_PLIST_PATH], check=True)
    print(f"✅ launchd plist created and loaded: {LAUNCHD_PLIST_PATH}")

def reload_pf():
    """Reload pfctl and enable if necessary."""
    pf_status = subprocess.run(["sudo", "pfctl", "-s", "info"], capture_output=True, text=True)
    if "Status: Enabled" not in pf_status.stdout:
        subprocess.run(["sudo", "pfctl", "-e"], check=True)
    subprocess.run(["sudo", "pfctl", "-f", PF_CONF], check=True)
    print("✅ pfctl reloaded.")

def create_launchd_plist():
    """Create launchd plist for auto-start pf."""
    plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.pf.start</string>
  <key>ProgramArguments</key>
  <array>
    <string>/sbin/pfctl</string>
    <string>-e</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
</dict>
</plist>
"""
    with open(LAUNCHD_PLIST_PATH, "w") as f:
        f.write(plist_content)
    subprocess.run(["sudo", "launchctl", "load", "-w", LAUNCHD_PLIST_PATH], check=True)
    print(f"✅ launchd plist created and loaded: {LAUNCHD_PLIST_PATH}")

def reload_pf():
    pf_status = subprocess.run(["sudo", "pfctl", "-s", "info"], capture_output=True, text=True)
    if "Status: Enabled" not in pf_status.stdout:
        subprocess.run(["sudo", "pfctl", "-e"], check=True)
    subprocess.run(["sudo", "pfctl", "-f", PF_CONF], check=True)

def create_launchd_plist():
    plist_content = """<?xml version="1.0" encoding="UTF-8"?>
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.pf.start</string>
  <key>ProgramArguments</key>
  <array>
    <string>/sbin/pfctl</string>
    <string>-e</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
</dict>
</plist>
"""
    with open(LAUNCHD_PLIST_PATH, "w") as f:
        f.write(plist_content)
    subprocess.run(["sudo", "launchctl", "load", "-w", LAUNCHD_PLIST_PATH], check=True)
