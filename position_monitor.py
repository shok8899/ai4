import time
import logging
from trade_handler import TradeHandler
import api_kiloex
from config import SYMBOL_TO_PRODUCT_ID

logger = logging.getLogger(__name__)

class PositionMonitor:
    def __init__(self):
        self.trade_handler = TradeHandler()
        
    def monitor_position(self, symbol):
        """Monitor position and execute trades based on strategy signals"""
        try:
            product_id = SYMBOL_TO_PRODUCT_ID.get(symbol.upper())
            if not product_id:
                raise ValueError(f"Unsupported symbol: {symbol}")
                
            while True:
                # Get current price
                current_price = api_kiloex.index_price(product_id, 'OPBNB')
                logger.info(f"Current price for {symbol}: {current_price}")
                
                # Wait for next strategy signal
                time.sleep(30)  # Check every 30 seconds
                
        except Exception as e:
            logger.error(f"Error monitoring position: {str(e)}")
            raise

def main():
    logging.basicConfig(level=logging.INFO)
    monitor = PositionMonitor()
    
    # Example usage
    symbol = "BTCUSD"
    monitor.monitor_position(symbol)

if __name__ == "__main__":
    main()