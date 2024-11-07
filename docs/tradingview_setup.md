# TradingView Alert Configuration Guide

## 1. Create New Alert

1. Click "Alerts" button on TradingView chart
2. Click "Create Alert"

## 2. Alert Settings

### Webhook URL Settings
In the "Notifications" section:
1. Check "Webhook URL"
2. Enter your server address:
```
http://your_server/webhook
```

### Message Body Settings
In the "Message" section, select "JSON format" and enter:
```json
{
    "symbol": "{{ticker}}",
    "side": "{{strategy.order.action}}",
    "leverage": 2,
    "margin": 20,
    "stop_loss": 45000,  // Direct stop loss price
    "take_profit": 55000 // Direct take profit price
}
```

## 3. Supported Trading Pairs

Please use the correct trading pair format:
- ETHUSD
- BTCUSD
- BNBUSD

## 4. Important Notes

1. Stop loss and take profit prices are optional
2. For long positions:
   - Stop loss must be lower than entry price
   - Take profit must be higher than entry price
3. For short positions:
   - Stop loss must be higher than entry price
   - Take profit must be lower than entry price
4. Test with small amounts first