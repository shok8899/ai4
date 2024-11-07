import logging
import json
from datetime import datetime
import os

class TradeLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = log_dir
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Set up file handler for trade logs
        self.trade_log_file = os.path.join(log_dir, "trades.log")
        
        # Configure logging
        self.logger = logging.getLogger("trade_logger")
        self.logger.setLevel(logging.INFO)
        
        # File handler for all trades
        file_handler = logging.FileHandler(self.trade_log_file)
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def log_trade(self, trade_data):
        """Log trade information"""
        try:
            # Format trade data
            trade_info = {
                "timestamp": datetime.now().isoformat(),
                "symbol": trade_data.get("symbol"),
                "side": trade_data.get("side"),
                "leverage": trade_data.get("leverage"),
                "margin": trade_data.get("margin"),
                "stop_loss": trade_data.get("stop_loss"),
                "take_profit": trade_data.get("take_profit"),
                "tx_hash": trade_data.get("tx_hash"),
                "status": trade_data.get("status")
            }
            
            # Log as JSON
            self.logger.info(json.dumps(trade_info))
            return True
        except Exception as e:
            self.logger.error(f"Error logging trade: {str(e)}")
            return False

    def get_recent_trades(self, limit=10):
        """Get recent trades from log file"""
        try:
            trades = []
            with open(self.trade_log_file, 'r') as f:
                lines = f.readlines()
                for line in lines[-limit:]:
                    # Parse log entry
                    timestamp = line.split(" - ")[0]
                    trade_data = json.loads(line.split(" - ")[1])
                    trade_data["log_timestamp"] = timestamp
                    trades.append(trade_data)
            return trades
        except FileNotFoundError:
            return []
        except Exception as e:
            self.logger.error(f"Error reading trades: {str(e)}")
            return []

    def get_trades_by_symbol(self, symbol, limit=10):
        """Get trades filtered by symbol"""
        try:
            trades = []
            with open(self.trade_log_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    trade_data = json.loads(line.split(" - ")[1])
                    if trade_data.get("symbol") == symbol:
                        trades.append(trade_data)
                        if len(trades) >= limit:
                            break
            return trades
        except FileNotFoundError:
            return []
        except Exception as e:
            self.logger.error(f"Error filtering trades: {str(e)}")
            return []