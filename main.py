"""
Main Entry Point for Telegram Trading Signal Matcher
Runs live parsing, pattern classification, and XAUS API price matching.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from src.matcher import SignalMatcher
from src.xaus_fetcher import XAUSFetcher


def run_demo():
    print("=" * 65)
    print("🚀 TELEGRAM TRADING SIGNAL & XAUS API MATCHER DEMO 🚀")
    print("=" * 65)

    sample_signal = """🚀 Oanda Trade Signal [DRY RUN] 🚀
Instrument: XAUUSD
Price: 4220.7
Time: 2026-09-30 09:45:08 UTC
------------------------
PHD (Last 2): 100.0, 100.0
RHD (Last 2): 20.0, 16.667
BUY Total: 1, 1
SELL Total: 4, 5
------------------------
Recent Verdict: sell
Verdict (1 Period Ago): sell
Verdict (2 Period Ago): sell
Verdict (3 Period Ago): sell
"""

    print("\n📩 Processing Sample Telegram Signal...")
    live_price = XAUSFetcher.get_live_gold_price()
    print(f"📊 Live XAUS Gold Price: ${live_price:,.2f}")

    result = SignalMatcher.evaluate_signal(sample_signal, live_price=live_price)

    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return

    print("\n--- ✅ EVALUATION RESULTS ---")
    print(f"Instrument      : {result['instrument']}")
    print(f"UTC Timestamp   : {result['timestamp_utc']}")
    print(f"Pattern Code    : {result['digit_code']} ({result['pattern_emoji']} {result['pattern_category']})")
    print(f"Move Type       : {result['move_type']}")
    print(f"Capital Share   : {int(result['capital_share']*100)}%")
    print(f"Signal Verdict  : {result['verdict']}")
    print(f"Entry Price     : ${result['entry_price']:,.2f}")
    print(f"Live Price      : ${result['live_price']:,.2f}")
    
    status_icon = "✅ PROFIT" if result['is_profit'] else "❌ LOSS"
    sign = "+" if result['pnl_dollars'] >= 0 else ""
    print(f"P&L Result      : {status_icon} -> {sign}${result['pnl_dollars']} ({sign}{result['pnl_pct']}%)")
    print("=" * 65)

if __name__ == "__main__":
    run_demo()
