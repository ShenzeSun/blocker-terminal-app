# Directory Structure:
# ├── __init__.py
# ├── config.py             # Shared config paths
# ├── utils.py              # Helpers: resolve_domain, write_ips, etc.
# ├── blacklist.py          # Blacklist domain logic
# ├── whitelist.py          # Whitelist domain logic
# ├── pf_rules.py           # pf rule handling (ensure_pf_rules, reload_pf)
# └── main.py               # Menu CLI

# Step 1: config.py
# ------------------

# Path to domain and IP block/allow lists
WHITELIST_DOMAINS_PATH = "/etc/pf.whitelist_domains"
BLOCKED_DOMAINS_PATH = "/etc/pf.blocked_domains"
BLOCKED_IPS_PATH = "/etc/pf.blocklist"
WHITELIST_IPS_PATH = "/etc/pf.whitelist"  # ✅ used in pf_rules.py

# PF system config and plist location
PF_CONF = "/etc/pf.conf"
LAUNCHD_PLIST_PATH = "/Library/LaunchDaemons/com.pf.start.plist"

# Internal config files
BLACKLIST_CONFIG = "blacklist.config"
WHITELIST_CONFIG = "whitelist.config"

# NEW: default network interface
NETWORK_INTERFACE = "en0"

PF_ANCHOR_FILE_PATH = "/private/etc/pf.anchors/org.user.block.out"
