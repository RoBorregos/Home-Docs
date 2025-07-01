# Tailscale Installation & Usage Guide

**Tailscale** is a simple, secure mesh VPN that uses [WireGuard®](https://www.wireguard.com/) to securely connect your devices wherever they are.

## Prerequisites

- A [Tailscale account](https://login.tailscale.com/start) (sign in with Google, GitHub, or Microsoft. For Roborregos, log in with the Roborregos Google Account).
- Admin rights on your device.

## Install Tailscale

### macOS

1. **Download & Install**
   - [Download the macOS installer](https://tailscale.com/download)
   - Run the `.pkg` file and follow the steps.

2. **Start Tailscale**
   - Open **Tailscale** from Applications.
   - Click **Log In** — your browser will open.
   - Log in with your Tailscale account and approve the connection.
   - Sometimes a reboot is required for it to work.

### Windows

1. **Download & Install**
   - [Download the Windows installer](https://tailscale.com/download)
   - Run the `.msi` file and follow the setup wizard.

2. **Start Tailscale**
   - Open **Tailscale** from the Start Menu.
   - Click **Log In** — your browser will open.
   - Log in with your Tailscale account and approve the connection.

### Linux

1. **Install**

**Debian/Ubuntu:**

  ``` bash
  curl -fsSL https://tailscale.com/install.sh | sh
  ```

Or install via APT:

``` bash
sudo apt-get install tailscale
```

**Fedora/RHEL:**

``` bash
curl -fsSL https://tailscale.com/install.sh | sh
```

2. **Start & Log In**

  ``` bash
  sudo tailscale up
  ```

Follow the link provided to log in and authorize your device.

## Use Tailscale

* After login, your device gets a **Tailscale IP** (e.g. `100.x.x.x`).
* Devices on your network can now securely connect.

## Common Commands (Linux/macOS Terminal)

| Command                   | Description                         |
| ------------------------- | ----------------------------------- |
| `tailscale status`        | See all connected devices           |
| `tailscale ip`            | Show your Tailscale IP              |
| `tailscale ping <device>` | Test connectivity to another device |
| `tailscale up`            | Connect to Tailscale                |
| `tailscale down`          | Disconnect from Tailscale           |

## Test It

* **Ping a device**

  ```bash
  ping 100.x.x.x
  ```

* **SSH into a device**

  ```bash
  ssh user@100.x.x.x
  ```

## Tips

* Manage devices at [Tailscale Admin Console](https://login.tailscale.com/admin/machines)
* Use **MagicDNS** to connect via hostnames instead of IPs.
* The free plan is enough for most personal use cases.

**Useful Links:**

* [Official Docs](https://tailscale.com/kb/)
* [Download Page](https://tailscale.com/download)
