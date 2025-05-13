# 🛡️ macOS Website Blocker with pf and Python

This guide walks you through manually blocking websites with `pf.conf`, then transitioning to using the Python-based `main.py`.

## ✨ Prerequisites

- macOS (tested on macOS 12+)
- Root access (`sudo`)
- Python 3
- Internet connection for DNS resolution

## 🔒 Step 1: Add ⚠️ Additional Permissions Setup

1. **Open terminal and type:**

   ```bash
   sudo bash -c 'touch /private/etc/pf.anchors/org.user.block.out /etc/pf.whitelist /etc/pf.blocklist /etc/pf.blocked_domains /etc/pf.whitelist_domains && chmod 600 /private/etc/pf.anchors/org.user.block.out /etc/pf.whitelist /etc/pf.blocklist /etc/pf.blocked_domains /etc/pf.whitelist_domains'
   ```

2. **Enable the firewall:**

   ```bash
   sudo pfctl -f /etc/pf.conf
   sudo pfctl -e
   ```

## 🐍 Step 2: Install `blocker.zip`

1. **Download or copy the `blocker.zip` script** to a safe directory:

   ```bash
   mkdir -p ~/scripts
   cd ~/scripts
   upzip blocker.zip ./blocker
   ```

2. **Upzip the contents of `blocker.zip`** go to terminal and paste it.

   ```bash
   upzip blocker.zip -d ./blocker
   cd ./blocker
   ```

3. **Make the script executable:**

   ```bash
   chmod +x main.py
   ```

## ⚙️ Step 3: Run the Script

Use root privileges to start the menu-based blocker:

```bash
sudo python3 ~/scripts/blocker/main.py
```

## 📋 Script Menu Options

1. **Block a domain**  
   Enter a domain like `example.com` to block it.

2. **Unblock a domain**  
   Choose a domain from the list to remove it.

3. **List blocked domains**  
   See all currently blocked entries.

4. **Exit**  
   Close the script.

## 🧠 How It Works

- Resolves the domain name to one or more IP addresses.
- Stores those IPs in `/etc/pf.blocklist`.
- Applies rules using `pfctl`.
- Keeps a persistent record of blocked domains in `/etc/pf.blocked_domains`.

## 🔄 Updating Firewall Rules

After any change via `blocker.py`, the script automatically:

```bash
sudo pfctl -f /etc/pf.conf
```

So no need to manually reload unless you edit `pf.conf` directly.

## 🧼 Uninstall / Reset Instructions

1. **Remove rules from `/etc/pf.conf`**

   ```bash
   sudo nano /etc/pf.conf
   ```

2. **Delete the data files:**

   ```bash
   sudo bash -c 'rm /private/etc/pf.anchors/org.user.block.out /etc/pf.whitelist /etc/pf.blocklist /etc/pf.blocked_domains /etc/pf.whitelist_domains
   ```

3. **Reload the firewall:**

   ```bash
   sudo pfctl -f /etc/pf.conf
   ```

4. **(Optional)** Delete the script:

   ```bash
   rm -rf ~/scripts/blocker
   ```
