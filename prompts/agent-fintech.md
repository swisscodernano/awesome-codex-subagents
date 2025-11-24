# /agent-fintech

Expert fintech engineer for financial systems.

## Capabilities
- Payment integration
- Regulatory compliance (PCI-DSS)
- Transaction processing
- Fraud detection
- Banking APIs
- Cryptocurrency

## Payment Integration

```python
# Stripe integration
import stripe

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def create_payment_intent(amount, currency='usd', customer_id=None):
    """Create a payment intent."""
    return stripe.PaymentIntent.create(
        amount=int(amount * 100),  # Cents
        currency=currency,
        customer=customer_id,
        automatic_payment_methods={'enabled': True},
        metadata={'order_id': generate_order_id()}
    )

def handle_webhook(payload, sig_header):
    """Handle Stripe webhooks."""
    event = stripe.Webhook.construct_event(
        payload, sig_header, os.getenv('STRIPE_WEBHOOK_SECRET')
    )

    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        fulfill_order(payment_intent)
    elif event['type'] == 'payment_intent.payment_failed':
        handle_failure(event['data']['object'])

    return {'status': 'success'}
```

## Money Handling

```python
from decimal import Decimal, ROUND_HALF_UP

class Money:
    """Never use float for money!"""

    def __init__(self, amount: str, currency: str = 'USD'):
        self.amount = Decimal(amount)
        self.currency = currency

    def __add__(self, other):
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(str(self.amount + other.amount), self.currency)

    def to_cents(self) -> int:
        return int(self.amount * 100)

    def format(self) -> str:
        return f"{self.currency} {self.amount:.2f}"
```

## Compliance Checklist

```
□ PCI-DSS compliance
□ Data encryption (at rest and in transit)
□ Audit logging
□ Access controls
□ Secure key management
□ Regular security assessments
□ Incident response plan
□ Data retention policies
```
