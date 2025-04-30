import requests
from typing import Optional, Dict, Any

class YouCanPayError(Exception):
    """Custom exception for YouCanPay SDK."""
    pass

class YouCanPay:
    def __init__(self, private_key: str, public_key: str, sandbox: bool = True):
        """
        Initialize the YouCanPay SDK client.
        
        :param private_key: Your YouCan Pay private API key (starts with 'pri_')
        :param public_key: Your YouCan Pay public API key (starts with 'pub_')
        :param sandbox: True for sandbox mode, False for production
        """
        self.private_key = private_key
        self.public_key = public_key
        self.base_url = "https://api.youcanpay.com" if not sandbox else "https://api-sandbox.youcanpay.com"

    def _request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make a request to the YouCanPay API.
        
        :param method: HTTP method (GET, POST, etc.)
        :param endpoint: API endpoint
        :param data: Request data
        :return: API response
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.private_key}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        response = requests.request(method, url, headers=headers, json=data)
        if response.status_code >= 400:
            raise YouCanPayError(f"API Error ({response.status_code}): {response.text}")
        return response.json()

    def create_payment_token(
        self,
        order_id: str,
        amount: int,
        currency: str,
        customer_ip: str,
        success_url: str,
        error_url: str,
        customer_info: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a payment token for a new transaction.
        
        :param order_id: Identifier of the order
        :param amount: Amount in smallest currency unit (e.g., cents)
        :param currency: Currency code (e.g., 'USD', 'MAD')
        :param customer_ip: Customer's IP address
        :param success_url: URL to redirect after successful payment
        :param error_url: URL to redirect after failed payment
        :param customer_info: Optional customer information
        :param metadata: Optional metadata
        :return: Token information
        """
        data = {
            "order_id": order_id,
            "amount": amount,
            "currency": currency,
            "customer_ip": customer_ip,
            "success_url": success_url,
            "error_url": error_url,
        }
        
        if customer_info:
            data["customer_info"] = customer_info
        if metadata:
            data["metadata"] = metadata
            
        return self._request("POST", "/tokens", data)

    def get_transaction(self, transaction_id: str) -> Dict[str, Any]:
        """
        Get transaction details.
        
        :param transaction_id: Transaction ID
        :return: Transaction information
        """
        return self._request("GET", f"/transactions/{transaction_id}")

    def refund_transaction(self, transaction_id: str, amount: Optional[int] = None) -> Dict[str, Any]:
        """
        Refund a transaction.
        
        :param transaction_id: Transaction ID
        :param amount: Optional amount to refund (partial refund)
        :return: Refund information
        """
        data = {}
        if amount is not None:
            data["amount"] = amount
        return self._request("POST", f"/transactions/{transaction_id}/refund", data) 