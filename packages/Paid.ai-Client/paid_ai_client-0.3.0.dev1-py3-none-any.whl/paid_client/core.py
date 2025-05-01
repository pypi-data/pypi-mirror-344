import requests
import logging
import threading
import json
from typing import Any, List, TypeVar, Generic, Optional, Dict
from datetime import datetime, timezone
from .models.account import Account, CreateAccountRequest, UpdateAccountRequest
from .models.signal import Signal
from .models.order import Order, OrderLine, OrderLineAttribute, CreateOrderRequest, UpdateOrderRequest
from .models.agent import Agent, ProductAttribute, CreateAgentRequest, UpdateAgentRequest
from .models.contact import Contact
from dataclasses import asdict

# Setup logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

T = TypeVar('T')

class PaidClient:
    """
    Client for the AgentPaid API.
    Collects signals and flushes them to the API periodically or when the buffer is full.
    """

    DUMMY_ORG_ID = 'dummy-org-id'  # or any string, it doesn't matter

    def __init__(self, api_key: str, api_url: str = 'https://api.agentpaid.io'):
        """
        Initialize the client with an API key and optional API URL.
        
        Args:
            api_key: The API key for authentication
            api_url: The base URL for the API (defaults to 'https://api.agentpaid.io')
        """
        if not api_key:
            raise ValueError("API key is required")
        
        self.api_key = api_key
        self.api_url = api_url.rstrip('/')
        self.logger = logging.getLogger(__name__)
        self.signals: List[Signal[Any]] = []
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
        
        # Start the periodic flush timer
        self._start_timer()
        
        logger.info(f"ApClient initialized with endpoint: {self.api_url}")

    def _start_timer(self):
        """Start a timer to flush signals every 30 seconds"""
        self.timer = threading.Timer(30.0, self._timer_callback)
        self.timer.daemon = True  # Allow the program to exit even if timer is running
        self.timer.start()
        
    def _timer_callback(self):
        """Callback for the timer to flush signals and restart the timer"""
        try:
            self.flush()
        except Exception as e:
            logger.error(f"Error during automatic flush: {str(e)}")
        finally:
            self._start_timer()  # Restart the timer
            
    def flush(self):
        """
        Send all collected signals to the API and clear the buffer.
        """
        if not self.signals:
            logger.debug("No signals to flush")
            return
        
        url = f"{self.api_url}/api/entries/bulk"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        body = {
            "transactions": [vars(signal) for signal in self.signals]
        }
        
        try:
            response = requests.post(
                url,
                headers=headers,
                json=body,
                timeout=10
            )
            response.raise_for_status()
            logger.info(f"Successfully flushed {len(self.signals)} signals")
            self.signals = []
        except requests.RequestException as e:
            logger.error(f"Failed to flush signals: {str(e)}")
            raise RuntimeError(f"Failed to flush signals: {str(e)}")
    
    def record_usage(self, agent_id: str, external_user_id: str, signal_name: str, data: Any):
        """
        Record a usage signal.
        
        Args:
            agent_id: The ID of the agent
            external_user_id: The external user ID (customer)
            signal_name: The name of the signal event
            data: The data to include with the signal
        """
        signal = Signal(
            event_name=signal_name,
            agent_id=agent_id,
            customer_id=external_user_id,
            data=data
        )
        
        self.signals.append(signal)
        logger.debug(f"Recorded signal: {signal_name} for agent {agent_id}")
        
        # If buffer reaches 100 signals, flush immediately
        if len(self.signals) >= 100:
            logger.info("Signal buffer reached 100, flushing")
            self.flush()
    
    def __del__(self):
        """
        Cleanup method to flush remaining signals when the object is garbage collected.
        """
        try:
            # Cancel the timer
            if hasattr(self, 'timer'):
                self.timer.cancel()
            
            # Flush any remaining signals
            if self.signals:
                logger.info("Flushing signals during cleanup")
                self.flush()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

    # Account methods
    def create_account(self, data: CreateAccountRequest) -> Account:
        """
        Create a new account.
        
        Args:
            data: Account data including name, email, etc.
        """
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/customers"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, json=data.to_dict())
            response.raise_for_status()
            return Account.from_dict(response.json()['data'])
        except requests.exceptions.HTTPError as e:
            error_data = e.response.json() if e.response.text else {}
            error_message = error_data.get('error', {}).get('message', str(e))
            raise RuntimeError(f"Failed to create account: {error_message}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to create account: {str(e)}")

    def get_account(self, account_id: str) -> Account:
        """Get a specific account."""
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/customer/{account_id}"
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return Account.from_dict(response.json()['data'])
        except requests.exceptions.HTTPError as e:
            error_data = e.response.json() if e.response.text else {}
            error_message = error_data.get('error', {}).get('message', str(e))
            raise RuntimeError(f"Failed to get account: {error_message}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to get account: {str(e)}")

    def list_accounts(self) -> List[Account]:
        """List all accounts for an organization."""
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/customers"
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return [Account.from_dict(account) for account in response.json()['data']]
        except requests.exceptions.HTTPError as e:
            error_data = e.response.json() if e.response.text else {}
            error_message = error_data.get('error', {}).get('message', str(e))
            raise RuntimeError(f"Failed to list accounts: {error_message}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to list accounts: {str(e)}")

    def update_account(self, account_id: str, data: UpdateAccountRequest) -> Account:
        """
        Update an existing account.
        
        Args:
            account_id: The account ID
            data: Fields to update
        """
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/customer/{account_id}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.put(url, headers=headers, json=data.to_dict())
            response.raise_for_status()
            response_data = response.json()
            if 'data' in response_data:
                return Account.from_dict(response_data['data'])
            return Account.from_dict(response_data)
        except requests.exceptions.HTTPError as e:
            error_data = e.response.json() if e.response.text else {}
            error_message = error_data.get('error', {}).get('message', str(e))
            raise RuntimeError(f"Failed to update account: {error_message}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to update account: {str(e)}")

    def delete_account(self, account_id: str) -> None:
        """Delete an account."""
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/customer/{account_id}"
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error_data = e.response.json() if e.response.text else {}
            error_message = error_data.get('error', {}).get('message', str(e))
            raise RuntimeError(f"Failed to delete account: {error_message}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to delete account: {str(e)}")

    def get_account_by_external_id(self, external_id: str) -> Account:
        """
        Get an account by its external ID.
        """
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/customer/external/{external_id}"
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            if 'data' in response_data:
                return Account.from_dict(response_data['data'])
            return Account.from_dict(response_data)
        except requests.exceptions.HTTPError as e:
            error_data = e.response.json() if e.response.text else {}
            error_message = error_data.get('error', {}).get('message', str(e))
            raise RuntimeError(f"Failed to get account by external ID: {error_message}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to get account by external ID: {str(e)}")

    # Order methods
    def create_order(self, data: CreateOrderRequest) -> Order:
        """
        Create a new order.
        
        Args:
            data: Order data including accountId, OrderLine, etc.
        """
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/orders"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            # Convert the dataclass to a dict and remove None values
            request_data = {k: v for k, v in data.__dict__.items() if v is not None}
            
            # Format startDate to ISO-8601 with timezone
            if 'startDate' in request_data and request_data['startDate']:
                if isinstance(request_data['startDate'], datetime):
                    # Ensure datetime has timezone info, default to UTC if none
                    if request_data['startDate'].tzinfo is None:
                        request_data['startDate'] = request_data['startDate'].replace(tzinfo=timezone.utc)
                    request_data['startDate'] = request_data['startDate'].isoformat()
                elif isinstance(request_data['startDate'], str):
                    # If it's already a string, ensure it's in ISO format with timezone
                    try:
                        dt = datetime.fromisoformat(request_data['startDate'].replace('Z', '+00:00'))
                        if dt.tzinfo is None:
                            dt = dt.replace(tzinfo=timezone.utc)
                        request_data['startDate'] = dt.isoformat()
                    except ValueError:
                        pass
            
            # Handle nested OrderLine data
            if 'OrderLine' in request_data and request_data['OrderLine']:
                request_data['OrderLine'] = [
                    {
                        'productId': line['productId'],
                        'description': line['description'],
                        'OrderLineAttribute': [
                            {
                                'productAttributeId': attr['productAttributeId'],
                                'pricing': {
                                    'eventName': attr['pricing']['eventName'],
                                    'chargeType': attr['pricing']['chargeType'],
                                    'pricePoint': attr['pricing']['pricePoint'],
                                    'pricingModel': attr['pricing']['pricingModel'],
                                    'billingFrequency': attr['pricing']['billingFrequency']
                                }
                            }
                            for attr in line['OrderLineAttribute']
                        ]
                    }
                    for line in request_data['OrderLine']
                ]
            
            # Log the request data for debugging
            logger.debug(f"Creating order with data: {json.dumps(request_data, indent=2)}")
            
            response = requests.post(url, headers=headers, json=request_data)
            response.raise_for_status()
            return Order.from_dict(response.json()['data'])
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to create order: {error_message}")
            raise RuntimeError(f"Failed to create order: {error_message}")

    def get_order(self, order_id: str) -> Order:
        """Get a specific order."""
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/orders/{order_id}"
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            response_data = response.json()
            logger.debug(f"API Response: {json.dumps(response_data, indent=2)}")
            return Order.from_dict(response_data['data'])
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to get order: {error_message}")
            raise RuntimeError(f"Failed to get order: {error_message}")

    def update_order(self, order_id: str, data: UpdateOrderRequest) -> Order:
        """
        Update an existing order.
        
        Args:
            order_id: The order ID
            data: Fields to update
        """
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/orders/{order_id}/v2"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            # Convert the dataclass to a dict and remove None values
            request_data = {k: v for k, v in data.__dict__.items() if v is not None}
            
            # Log the request data for debugging
            logger.debug(f"Updating order with data: {json.dumps(request_data, indent=2)}")
            
            response = requests.put(url, headers=headers, json=request_data)
            response.raise_for_status()
            return Order.from_dict(response.json()['data'])
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to update order: {error_message}")
            raise RuntimeError(f"Failed to update order: {error_message}")

    def delete_order(self, order_id: str) -> None:
        """Delete an order."""
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/orders/{order_id}"
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to delete order: {error_message}")
            raise RuntimeError(f"Failed to delete order: {error_message}")

    def list_orders(self) -> List[Order]:
        """List all orders for an organization."""
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/orders"
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return [Order.from_dict(order) for order in response.json()['data']]
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to list orders: {error_message}")
            raise RuntimeError(f"Failed to list orders: {error_message}")

    def add_order_lines(self, order_id: str, lines: List[Dict[str, Any]]) -> List[OrderLine]:
        """
        Add order lines to an existing order.
        
        Args:
            order_id: The order ID
            lines: List of order lines to add
        """
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/orders/{order_id}/lines"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, json=lines)
            response.raise_for_status()
            return [OrderLine.from_dict(line) for line in response.json()['data']]
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to add order lines: {error_message}")
            raise RuntimeError(f"Failed to add order lines: {error_message}")

    # Agent methods
    def create_agent(self, data: CreateAgentRequest) -> Agent:
        """
        Create a new agent.
        
        Args:
            data: Agent data including name, description, ProductAttribute, etc.
        """
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/products"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, json=data.__dict__)
            response.raise_for_status()
            return Agent.from_dict(response.json()['data'])
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to create agent: {error_message}")
            raise RuntimeError(f"Failed to create agent: {error_message}")

    def get_agent(self, agent_id: str) -> Agent:
        """Get a specific agent."""
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/products/{agent_id}"
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return Agent.from_dict(response.json()['data'])
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to get agent: {error_message}")
            raise RuntimeError(f"Failed to get agent: {error_message}")

    def list_agents(self) -> List[Agent]:
        """List all agents for an organization."""
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/products"
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return [Agent.from_dict(agent) for agent in response.json()['data']]
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to list agents: {error_message}")
            raise RuntimeError(f"Failed to list agents: {error_message}")

    def update_agent(self, agent_id: str, data: Dict[str, Any]) -> Agent:
        """
        Update an existing agent.
        
        Args:
            agent_id: The agent ID
            data: Fields to update
        """
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/products/{agent_id}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.put(url, headers=headers, json=data)
            response.raise_for_status()
            return Agent.from_dict(response.json())
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to update agent: {error_message}")
            raise RuntimeError(f"Failed to update agent: {error_message}")

    def delete_agent(self, agent_id: str) -> None:
        """Delete an agent."""
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/products/{agent_id}"
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to delete agent: {error_message}")
            raise RuntimeError(f"Failed to delete agent: {error_message}")

    # Contact methods
    def create_contact(self, data: Dict[str, Any]) -> Contact:
        """
        Create a new contact.
        
        Args:
            data: Contact data including customerId, firstName, lastName, etc.
        """
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/contacts"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return Contact.from_dict(response.json()['data'])
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to create contact: {error_message}")
            raise RuntimeError(f"Failed to create contact: {error_message}")

    def get_contact(self, contact_id: str) -> Contact:
        """
        Get a specific contact.
        
        Args:
            contact_id: The contact ID
        """
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/contacts/{contact_id}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return Contact.from_dict(response.json()['data'])
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to get contact: {error_message}")
            raise RuntimeError(f"Failed to get contact: {error_message}")

    def list_contacts(self, customer_id: Optional[str] = None) -> List[Contact]:
        """
        List all contacts for an organization, optionally filtered by customer.
        
        Args:
            customer_id: Optional customer ID to filter contacts
        """
        url = f"{self.api_url}/api/organizations/{self.DUMMY_ORG_ID}/contacts"
        if customer_id:
            url += f"?customer_id={customer_id}"
            
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return [Contact.from_dict(contact) for contact in response.json()['data']]
        except requests.RequestException as e:
            error_message = str(e)
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_message = error_data.get('error', {}).get('message', str(e))
                except:
                    error_message = f"{str(e)} - Response: {e.response.text}"
            logger.error(f"Failed to list contacts: {error_message}")
            raise RuntimeError(f"Failed to list contacts: {error_message}")