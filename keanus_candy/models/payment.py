import random
import time

class PaymentMethod:
    """Base class for payment types with shared logging."""
    
    def __init__(self, method_name: str):
        self.method_name = method_name
        self.transaction_history = []  # NEW: track all transactions

    def log_transaction(self, amount: float, status: str):
        """Record a transaction attempt."""
        entry = {
            "method": self.method_name,
            "amount": amount,
            "status": status,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        self.transaction_history.append(entry)
        print(f"[{entry['timestamp']}] {self.method_name} — ${amount:.2f} → {status}")

    def process_payment(self, amount: float) -> bool:
        """Abstract method to process payments."""
        raise NotImplementedError


class CreditCard(PaymentMethod):
    """Implements credit card payment with mock validation."""
    
    def __init__(self, card_number: str, holder_name: str, expiration_date: str = "12/29"):
        super().__init__("Credit Card")
        self.card_number = card_number
        self.holder_name = holder_name
        self.expiration_date = expiration_date  # NEW attribute

    def validate_card(self) -> bool:
        """Simple mock validation for demonstration."""
        return len(self.card_number) in (15, 16) and self.card_number.isdigit()

    def process_payment(self, amount: float) -> bool:
        """Process a credit card payment with basic validation and randomness."""
        if amount <= 0:
            print("Invalid amount. Must be greater than zero.")
            self.log_transaction(amount, "Failed")
            return False

        if not self.validate_card():
            print("Invalid card number. Transaction declined.")
            self.log_transaction(amount, "Declined")
            return False

        print(f"Charging ${amount:.2f} to card ending in {self.card_number[-4:]} ({self.holder_name})...")
        success = random.choice([True, True, True, False])  # 75% success rate
        status = "Approved" if success else "Declined"
        self.log_transaction(amount, status)
        return success


class PayPal(PaymentMethod):
    """Implements PayPal payment with simulated network latency."""
    
    def __init__(self, email: str):
        super().__init__("PayPal")
        self.email = email
        self.balance = 500.00  # NEW: mock balance

    def process_payment(self, amount: float) -> bool:
        """Process a PayPal payment with balance check and delay."""
        if amount <= 0:
            print("Payment failed: Amount must be positive.")
            self.log_transaction(amount, "Failed")
            return False
        if amount > self.balance:
            print(f"Payment failed: Insufficient balance (${self.balance:.2f}).")
            self.log_transaction(amount, "Insufficient Funds")
            return False

        print(f"Connecting to PayPal account {self.email}...")
        time.sleep(1)  # simulate API delay
        self.balance -= amount
        print(f"Processed PayPal payment of ${amount:.2f}. Remaining balance: ${self.balance:.2f}")
        self.log_transaction(amount, "Completed")
        return True
