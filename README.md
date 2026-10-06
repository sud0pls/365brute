# 365brute

Microsoft 365 / Entra ID password sprayer with NetExec-style output. Updated for 2024+ Microsoft endpoints.

Performs password spraying against Microsoft Online accounts (Azure/O365/Entra ID). Detects valid credentials, MFA status, account lockouts, disabled accounts, conditional access policies, and expired passwords.

## Installation

```bash
git clone https://github.com/sud0pls/365brute.git
cd 365brute
pip3 install requests
```

## Usage

### Single password spray

```bash
python3 365brute.py -u userlist.txt -p 'Winter2025!'
```

### Password list with delay between rounds

```bash
python3 365brute.py -u userlist.txt -P passwords.txt -d 1800 -s 1 -v -o results.txt
```

### With FireProx (IP rotation)

```bash
python3 365brute.py -u userlist.txt -P passwords.txt -d 1800 --url https://api-gw.execute-api.us-east-1.amazonaws.com/fireprox -o results.txt
```

## Options

| Flag | Description |
|------|-------------|
| `-u`, `--userlist` | File with usernames one-per-line `user@domain.com` (required) |
| `-p`, `--password` | Single password to spray |
| `-P`, `--passlist` | File with passwords one-per-line (sprays in rounds) |
| `-o`, `--out` | Output file for valid results |
| `-d`, `--delay` | Seconds to wait between password rounds (default: 0) |
| `-s`, `--sleep` | Seconds to sleep between each attempt (default: 0) |
| `-v`, `--verbose` | Show usernames that exist on invalid password |
| `-f`, `--force` | Don't stop on multiple account lockouts |
| `--url` | Target URL (default: `https://login.microsoftonline.com`) |

> `-p` and `-P` are mutually exclusive. Use one or the other.

## Output

Output follows the NetExec format:

```
ENTRA  login.microsoftonline.com   443  [*] Spraying password 1/5: Winter2025!
ENTRA  login.microsoftonline.com   443  [-] user@domain.com:Winter2025!
ENTRA  login.microsoftonline.com   443  [+] admin@domain.com:Winter2025!
ENTRA  login.microsoftonline.com   443  [+] user2@domain.com:Winter2025! (MFA required)
ENTRA  login.microsoftonline.com   443  [!] user3@domain.com LOCKED
ENTRA  login.microsoftonline.com   443  [!] user4@domain.com:Winter2025! (Account disabled)
```

| Tag | Meaning |
|-----|---------|
| `[+]` | Valid credentials found |
| `[-]` | Invalid password (verbose mode) |
| `[*]` | Info / status |
| `[!]` | Warning (locked, disabled, tenant not found) |
| `[.]` | Unhandled error code |

## Evading Azure Smart Lockout

Microsoft Entra Smart Lockout tracks failed authentication attempts per-account and locks accounts after ~10 failed attempts from unknown IPs. Here's how to work around it:

### Timing

| Scenario | Recommended `-d` value |
|----------|----------------------|
| Conservative (production targets) | `-d 1800` (30 min) |
| Moderate (known test environments) | `-d 900` (15 min) |
| Aggressive (lab/CTF only) | `-d 60` (1 min) |

Smart Lockout resets its counter after a period of inactivity (typically 15-30 minutes). The lockout duration increases with repeated lockouts (exponential backoff).

### Strategies

**1. Use long delays between rounds**

```bash
python3 365brute.py -u userlist.txt -P passwords.txt -d 1800 -s 1
```

One password per round across all users, then wait 30 minutes. This keeps each account at 1 failed attempt per window.

**2. IP rotation with FireProx**

Smart Lockout tracks by IP. Rotating source IPs resets the per-IP counter:

```bash
python3 365brute.py -u userlist.txt -P passwords.txt -d 300 --url https://your-fireprox-url.amazonaws.com/fireprox
```

Setup: [https://github.com/ustayready/fireprox](https://github.com/ustayready/fireprox)

**3. Keep password lists short and targeted**

Instead of large wordlists, use 5-15 targeted passwords:
- `Season+Year!` (Summer2025!, Winter2025!)
- `CompanyName+123`
- `Welcome1`, `Password1`, `Changeme1`

**4. Sleep between individual attempts**

```bash
python3 365brute.py -u userlist.txt -p 'Summer2025!' -s 2
```

`-s 2` adds 2 seconds between each authentication request, reducing the chance of triggering rate limits.

**5. Avoid re-spraying locked accounts**

If you see `LOCKED` warnings, stop immediately (`-f` is NOT set by default). Wait 30+ minutes before retrying. Re-spraying locked accounts extends the lockout window.

### Smart Lockout Behavior Summary

- Lockout threshold: ~10 failed attempts from unfamiliar IPs
- Initial lockout: ~60 seconds
- Subsequent lockouts: exponential backoff (doubles each time)
- Counter reset: 15-30 minutes of inactivity
- Familiar IPs (e.g., corporate VPN): higher threshold or exempt
- Lockout applies per-account, not per-tenant

## Detections

| Response | Meaning |
|----------|---------|
| `[+] user:pass` | Valid credentials, no MFA |
| `[+] ... (MFA required)` | Valid creds, MFA enabled (AADSTS50076) |
| `[+] ... (MFA enrollment needed)` | Valid creds, MFA not yet registered (AADSTS50079) |
| `[+] ... (Conditional Access / DUO MFA)` | Valid creds, external MFA like DUO (AADSTS50158) |
| `[+] ... (Conditional Access blocks token)` | Valid creds, CA policy blocks (AADSTS53003) |
| `[+] ... (Password expired)` | Valid creds, password needs reset (AADSTS50055) |
| `[!] ... LOCKED` | Account locked by Smart Lockout (AADSTS50053) |
| `[!] ... (Account disabled)` | Account disabled in Entra ID (AADSTS50057) |
| `[-] ... (User not found)` | User does not exist (AADSTS50034) |

## Disclaimer

This tool is intended for authorized security testing only. Only use it against accounts you have explicit permission to test. Unauthorized access to computer systems is illegal.

## Author

[Sud0pls](https://github.com/sud0pls)
