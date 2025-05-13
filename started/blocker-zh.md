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
