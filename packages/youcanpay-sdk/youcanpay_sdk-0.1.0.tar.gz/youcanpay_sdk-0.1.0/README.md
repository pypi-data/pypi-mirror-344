# YouCanPay SDK

A Python SDK for integrating with the YouCan Pay payment gateway.

## Installation

```bash
pip install youcanpay-sdk
```

## Usage

```python
from youcanpay import YouCanPay

# Initialize the client
client = YouCanPay(
    private_key="pri_your_private_key",
    public_key="pub_your_public_key",
    sandbox=True  # Set to False for production
)

# Create a payment token
try:
    token = client.create_payment_token(
        order_id="order_123",
        amount=1000,  # 10.00 MAD (in cents)
        currency="MAD",
        customer_ip="123.123.123.123",
        success_url="https://yourdomain.com/success",
        error_url="https://yourdomain.com/error",
        customer_info={
            "name": "John Doe",
            "email": "john@example.com",
            "phone": "+212600000000"
        },
        metadata={
            "description": "Test payment"
        }
    )
    print(f"Payment token: {token['id']}")
    print(f"Redirect URL: {token['redirect_url']}")
except YouCanPayError as e:
    print(f"Error: {e}")

# Get transaction details
try:
    transaction = client.get_transaction("transaction_id")
    print(f"Transaction status: {transaction['status']}")
except YouCanPayError as e:
    print(f"Error: {e}")

# Refund a transaction
try:
    refund = client.refund_transaction("transaction_id", amount=500)  # Partial refund of 5.00 MAD
    print(f"Refund status: {refund['status']}")
except YouCanPayError as e:
    print(f"Error: {e}")
```

## Features

- Create payment tokens
- Get transaction details
- Process refunds
- Support for sandbox and production environments
- Type hints for better IDE support

## Requirements

- Python 3.6+
- requests>=2.25.1

## License

MIT License 