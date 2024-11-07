import os
from web3 import Web3
import market_trigger_trade_kiloex
import api_kiloex
from config import SYMBOL_TO_PRODUCT_ID, SLIPPAGE
import logging
from config_kiloex import kiloconfigs, BASE
from dotenv import load_dotenv
from trade_logger import TradeLogger
import perp_kiloex

logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class TradeHandler:
    def __init__(self):
        self.config = kiloconfigs['OPBNB']
        self.trade_logger = TradeLogger()
    
    def get_product_id(self, symbol):
        """Get product ID from symbol"""
        product_id = SYMBOL_TO_PRODUCT_ID.get(symbol.upper())
        if not product_id:
            raise ValueError(f"Unsupported symbol: {symbol}")
        return product_id
    
    def get_current_position(self, product_id):
        """Get current position for the product"""
        try:
            position = perp_kiloex.get_position(self.config, product_id)
            if position and position.margin > 0:
                return {
                    'margin': position.margin,
                    'is_long': position.isTrue,
                    'leverage': position.leverage
                }
            return None
        except Exception as e:
            logger.error(f"Error getting position: {str(e)}")
            return None
    
    def execute_trade(self, trade_data):
        """Execute market trade based on strategy signal"""
        try:
            # Get product ID
            product_id = self.get_product_id(trade_data['symbol'])
            
            # Get current market price
            market_price = api_kiloex.index_price(product_id, 'OPBNB')
            logger.info(f"Current market price for {trade_data['symbol']}: {market_price}")
            
            # Trade parameters
            is_long = trade_data['side'].lower() == 'buy'
            leverage = float(trade_data['leverage'])
            margin = float(trade_data['margin'])
            
            # Get current position
            current_position = self.get_current_position(product_id)
            if current_position:
                logger.info(f"Current position: {current_position}")
                
                # If position exists in opposite direction, log warning and skip
                if current_position['is_long'] != is_long:
                    logger.warning("Skipping trade as opposite position exists")
                    return {
                        'status': 'skipped',
                        'reason': 'opposite_position_exists',
                        'symbol': trade_data['symbol']
                    }
            
            # Set acceptable price with slippage
            acceptable_price = (
                market_price * (1 + SLIPPAGE) if is_long 
                else market_price * (1 - SLIPPAGE)
            )
            
            # Execute position
            tx_hash = market_trigger_trade_kiloex.open_market_trigger_position(
                config=self.config,
                product_id=product_id,
                margin=margin,
                leverage=leverage,
                is_long=is_long,
                acceptable_price=acceptable_price,
                referral_code=bytearray(32),
                stop_loss_price=0,
                take_profit_price=0
            )
            
            trade_result = {
                'tx_hash': tx_hash.hex(),
                'symbol': trade_data['symbol'],
                'side': 'LONG' if is_long else 'SHORT',
                'market_price': market_price,
                'leverage': leverage,
                'margin': margin,
                'status': 'submitted'
            }
            
            # Log the trade
            self.trade_logger.log_trade(trade_result)
            
            logger.info(f"Trade executed successfully: {trade_result}")
            return trade_result
            
        except Exception as e:
            logger.error(f"Error executing trade: {str(e)}", exc_info=True)
            raise