import logging
from web3 import Web3
from config_kiloex import BASE, BASE12, kiloconfigs
import time
import usdt_kiloex
import api_kiloex

with open('./abi/MarketOrderWithTriggerOrder.abi', 'r') as f:
    abi = f.read()

def open_market_trigger_position(config, product_id, margin, leverage, is_long, acceptable_price, referral_code, stop_loss_price, take_profit_price):
    """
    Open a market position with stop loss and take profit triggers.
    """
    try:
        # Automatically authorize USDT limit
        usdt_kiloex.approve_usdt_allowance(config, config.market_trigger_contract, margin)

        w3 = Web3(Web3.HTTPProvider(config.rpc))
        
        # Convert addresses to checksum format
        wallet_address = w3.to_checksum_address(config.wallet)
        trigger_address = w3.to_checksum_address(config.market_trigger_contract)
        
        nonce = w3.eth.get_transaction_count(wallet_address)
        gas_price = w3.eth.gas_price
        execution_fee = config.execution_fee * 3  # Higher fee for trigger orders

        tx = {
            'from': wallet_address,
            'nonce': nonce,
            'gas': config.gas * 2,  # Higher gas for trigger orders
            'gasPrice': gas_price,
            'value': execution_fee,
            'chainId': config.chain_id
        }

        trade_contract_w3 = w3.eth.contract(address=trigger_address, abi=abi)
        txn = trade_contract_w3.functions.createIncreasePositionWithCloseTriggerOrders(
            product_id,
            int(margin * BASE),
            int(leverage * BASE),
            is_long,
            int(acceptable_price * BASE),
            config.execution_fee,
            referral_code,
            int(stop_loss_price * BASE),
            int(take_profit_price * BASE)
        ).build_transaction(tx)

        signed_txn = w3.eth.account.sign_transaction(txn, private_key=config.private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        logging.info(f"Market trigger position tx_hash: {tx_hash.hex()}")
        return tx_hash

    except Exception as e:
        logging.error(f'Market trigger position error: {str(e)}')
        raise