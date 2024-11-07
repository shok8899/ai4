from flask import Flask, request, jsonify
from trade_handler import TradeHandler
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
trade_handler = TradeHandler()

def validate_trade_data(data):
    """Validate trading data"""
    required_fields = ['symbol', 'side', 'leverage', 'margin']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
    
    if data['side'].lower() not in ['buy', 'sell']:
        raise ValueError("Side must be 'buy' or 'sell'")
    
    if not isinstance(data['leverage'], (int, float)) or data['leverage'] <= 0:
        raise ValueError("Invalid leverage value")
    
    if not isinstance(data['margin'], (int, float)) or data['margin'] <= 0:
        raise ValueError("Invalid margin value")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get trading data
        data = request.json
        logger.info(f"Received trading signal: {data}")
        
        # Validate trading data
        validate_trade_data(data)
        
        # Execute trade
        result = trade_handler.execute_trade(data)
        
        # Log success
        logger.info(f"Trade executed successfully: {result}")
        
        return jsonify({
            'status': 'success',
            'data': result,
            'message': f"{'Long' if data['side'].lower() == 'buy' else 'Short'} position executed"
        })

    except ValueError as e:
        logger.error(f"Validation error: {str(e)}")
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 400
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return jsonify({
            'status': 'error',
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)