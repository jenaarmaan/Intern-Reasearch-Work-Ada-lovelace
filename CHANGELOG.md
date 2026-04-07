# Changelog - KALI Optimization & UI Refactor

## UI/UX Improvements (F1)

- Removed NASA terminal UI and all monospace neon themes.
- Implemented a clean, friendly educational interface with a soft blue (#4A90D9) accent.
- Switched to standard Streamlit components (buttons, headers, titles) for maximum readability.
- Replaced the complex 3D Neural Orb with a simple, modern pulse avatar.
- Removed all glassmorphism, scanlines, and rotating rings.
- Standardized typography using default Streamlit sans-serif.

## Data & Content Cleanup (F2)

- Removed all satellite data references and node L-PK synchronization.
- Removed NASA datasets and space-themed telemetry.
- Deleted all US stock data (S&P, NYSE, NASDAQ, USD, DOW) from the codebase.
- Replaced USD exchange rates with INR-based metrics in all research nodes.
- Updated ticker universes to focus exclusively on Indian market equivalents (NSE).
- Removed `kali_boot_sequence.py` and boot animations for faster, direct loading.
- Verified system integrity: zero raw HTML or terminal-style text in the UI.

*Date: 2026-04-07 | Status: Verified Deliverable*
