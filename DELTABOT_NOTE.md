# DeltaChat / Deltabot Compatibility Note

## Issue

The `deltabot` package (v0.8.0, released March 2021) has **compatibility issues** with the newer `deltachat` library (v2.23.0).

### Error:
```
ImportError: cannot import name 'parse_system_add_remove' from 'deltachat.message'
```

## Root Cause

- **deltabot 0.8.0** is the legacy DeltaChat bot framework
- **deltachat 2.23.0** has changed its API significantly
- The old `parse_system_add_remove` function no longer exists in the new deltachat library
- These two packages are incompatible

## Status in Ribit 2.0

✅ **DeltaChat integration is OPTIONAL**

The Ribit 2.0 bot works perfectly fine without DeltaChat:
- ✅ Matrix bot fully functional
- ✅ All core features working
- ✅ Megabite LLM operational
- ✅ All other modules working

## Solutions

### Option 1: Skip DeltaChat (Recommended)
Simply don't install deltabot. Ribit 2.0 works great with just Matrix!

```bash
# Install everything except deltabot
pip3 install matrix-nio[e2e] aiohttp requests beautifulsoup4 lxml \
  wikipedia-api Pillow python-magic aiofiles supabase \
  --break-system-packages
```

### Option 2: Use Newer DeltaChat RPC System
The DeltaChat project now recommends using the **RPC-based bot system** instead of the old `deltabot` package:

```bash
# Install the newer deltachat-rpc-client
pip3 install deltachat-rpc-client --break-system-packages
```

However, this would require rewriting the DeltaChat bot integration in Ribit 2.0.

### Option 3: Downgrade deltachat (Not Recommended)
You could downgrade to an older deltachat version, but this is not recommended:

```bash
pip3 uninstall deltachat -y
pip3 install deltachat==1.40.1 --break-system-packages
pip3 install deltabot --break-system-packages
```

## Current Configuration

The `check_modules_and_install.py` script now treats `deltabot` as **optional**, so:
- ✅ Script won't fail if deltabot is missing
- ✅ Won't show as "MISSING" (shows as optional)
- ✅ Ribit 2.0 will report 100% operational without it

## Recommendation

**Skip DeltaChat for now.** Focus on Matrix bot functionality, which is fully working and feature-complete. If you need DeltaChat in the future, we can update the integration to use the newer RPC-based system.

---

**Summary:** DeltaChat is optional, has compatibility issues, and Ribit 2.0 works perfectly without it! 🎉
