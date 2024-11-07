#!/usr/bin/env python3
from trade_logger import TradeLogger
import argparse

def main():
    parser = argparse.ArgumentParser(description='View trading logs')
    parser.add_argument('--symbol', help='Filter trades by symbol (e.g., BTCUSD)')
    parser.add_argument('--limit', type=int, default=10, help='Number of trades to show')
    args = parser.parse_args()

    logger = TradeLogger()
    
    if args.symbol:
        trades = logger.get_trades_by_symbol(args.symbol, args.limit)
        print(f"\nShowing last {args.limit} trades for {args.symbol}:")
    else:
        trades = logger.get_recent_trades(args.limit)
        print(f"\nShowing last {args.limit} trades:")
    
    if not trades:
        print("No trades found.")
        return

    # Print trades in a formatted table
    print("\n{:<25} {:<8} {:<6} {:<8} {:<12} {:<12} {:<12}".format(
        "Timestamp", "Symbol", "Side", "Leverage", "Margin", "Stop Loss", "Take Profit"))
    print("-" * 90)
    
    for trade in trades:
        print("{:<25} {:<8} {:<6} {:<8} {:<12} {:<12} {:<12}".format(
            trade['timestamp'][:19],
            trade['symbol'],
            trade['side'],
            str(trade['leverage']) + "x",
            str(trade['margin']),
            str(trade['stop_loss'] or '-'),
            str(trade['take_profit'] or '-')
        ))

if __name__ == "__main__":
    main()