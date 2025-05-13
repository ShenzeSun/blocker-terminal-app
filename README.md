# 🛡️ Blocker Terminal App
### Blocker is a whitelisting, blacklisting outbound restrict terminal app, work only in MacOS.

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


# 🛡️ 使用 pf 和 Python 在 macOS 上的网站封锁器

这份指南会带你先用 `pf.conf` 手动封锁网站，然后转向使用 Python 编写的 `main.py`脚本。

## ✨ 前置条件

- macOS（在 macOS 12+测试通过）
- 根权限（使用 `sudo`）
- Python 3
- 用于 DNS 解析的网络连接

## 🔒 第一步：添加 ⚠️ 额外权限设置

1. **打开终端输入：**

   ```bash
   sudo bash -c 'touch /private/etc/pf.anchors/org.user.block.out /etc/pf.whitelist /etc/pf.blocklist /etc/pf.blocked_domains /etc/pf.whitelist_domains && chmod 600 /private/etc/pf.anchors/org.user.block.out /etc/pf.whitelist /etc/pf.blocklist /etc/pf.blocked_domains /etc/pf.whitelist_domains'
   ```

2. **启用防火墙：**

   ```bash
   sudo pfctl -f /etc/pf.conf
   sudo pfctl -e
   ```

## 🐍 第二步：安装 `blocker.zip`

1. **下载或备份 `blocker.zip` 脚本**至一个安全的目录：

   ```bash
   mkdir -p ~/scripts
   cd ~/scripts
   upzip blocker.zip ./blocker
   ```

2. **解压 `blocker.zip` 内容，然后转到该目录：**

   ```bash
   upzip blocker.zip -d ./blocker
   cd ./blocker
   ```

3. **使脚本可执行：**

   ```bash
   chmod +x main.py
   ```

## ⚙️ 第三步：运行脚本

使用根权限启动基于菜单的封锁器：

```bash
sudo python3 ~/scripts/blocker/main.py
```

## 📋 脚本菜单选项

1. **封锁域名**  
   输入一个域名，如 `example.com`，将其封锁。

2. **解除封锁域名**  
   从列表中选择一个域名，将其移除。

3. **列出已封锁域名**  
   查看目前所有封锁记录。

4. **退出**  
   关闭脚本。

## 🧐 它如何工作

- 将域名解析为一个或多个 IP 地址；
- 将这些 IP 存入 `/etc/pf.blocklist`；
- 使用 `pfctl` 应用规则；
- 将已封锁域名保存在 `/etc/pf.blocked_domains`中，以保持持久记录。

## 🔄 更新防火墙规则

通过 `blocker.py` 进行任何更改后，脚本会自动执行：

```bash
sudo pfctl -f /etc/pf.conf
```

所以不需要手动重新加载，除非你直接编辑了 `pf.conf`。

## 🧬 卸载 / 恢复指南

1. **从 `/etc/pf.conf` 移除相关规则**

   ```bash
   sudo nano /etc/pf.conf
   ```

2. **删除数据文件：**

   ```bash
   sudo bash -c 'rm /private/etc/pf.anchors/org.user.block.out /etc/pf.whitelist /etc/pf.blocklist /etc/pf.blocked_domains /etc/pf.whitelist_domains'
   ```

3. **重新加载防火墙：**

   ```bash
   sudo pfctl -f /etc/pf.conf
   ```

4. **(可选)** 删除脚本：

   ```bash
   rm -rf ~/scripts/blocker
   ```
