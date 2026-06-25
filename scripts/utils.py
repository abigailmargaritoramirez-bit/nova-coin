#!/usr/bin/env python3
"""
NOVA COIN Utilities Package
Comprehensive toolkit for NOVA COIN ecosystem management

Includes:
- Contract deployment helpers
- ABI management
- Transaction utilities
- Contract interaction wrappers
"""

import json
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum

class ContractType(Enum):
    """Supported contract types"""
    TOKEN = "token"
    STAKING = "staking"
    GOVERNANCE = "governance"
    URC = "urc"

class TokenDecimals:
    """Standard token decimals"""
    WEI = 0
    GWEI = 9
    ETHER = 18
    NOVA = 18

class ContractUtilities:
    """Utility functions for contract management"""
    
    @staticmethod
    def to_wei(amount: float, decimals: int = 18) -> int:
        """Convert amount to Wei"""
        return int(amount * (10 ** decimals))
    
    @staticmethod
    def from_wei(amount: int, decimals: int = 18) -> float:
        """Convert from Wei to readable amount"""
        return amount / (10 ** decimals)
    
    @staticmethod
    def format_address(address: str) -> str:
        """Format Ethereum address with checksum"""
        from eth_utils import to_checksum_address
        return to_checksum_address(address)
    
    @staticmethod
    def is_valid_address(address: str) -> bool:
        """Check if address is valid Ethereum address"""
        return len(address) == 42 and address.startswith('0x')
    
    @staticmethod
    def create_urc_hash(components: Dict[str, str]) -> str:
        """Create URC hash from components"""
        data = "|".join([
            components.get("resource_id", ""),
            components.get("token_id", ""),
            components.get("wallet_id", ""),
            components.get("contract_id", ""),
            components.get("governance_id", ""),
            "NOVA"
        ])
        return hashlib.sha256(data.encode()).hexdigest()

class DeploymentHelper:
    """Helpers for contract deployment"""
    
    def __init__(self, network: str = "sepolia"):
        self.network = network
        self.deployed_contracts = {}
        self.deployment_log = []
    
    def log_deployment(
        self,
        contract_name: str,
        address: str,
        tx_hash: str,
        block: int
    ) -> None:
        """Log deployment information"""
        entry = {
            "contract": contract_name,
            "address": address,
            "tx_hash": tx_hash,
            "block": block,
            "network": self.network,
            "timestamp": datetime.now().isoformat()
        }
        self.deployment_log.append(entry)
        self.deployed_contracts[contract_name] = address
    
    def export_deployment_info(self, filename: str = "deployment.json") -> None:
        """Export deployment information to JSON"""
        data = {
            "network": self.network,
            "timestamp": datetime.now().isoformat(),
            "contracts": self.deployed_contracts,
            "log": self.deployment_log
        }
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)
        print(f"✓ Deployment info exported to {filename}")
    
    def load_deployment_info(self, filename: str = "deployment.json") -> Dict:
        """Load deployment information from JSON"""
        with open(filename, "r") as f:
            return json.load(f)

class ABIManager:
    """Manage contract ABIs"""
    
    @staticmethod
    def get_erc20_abi() -> List[Dict]:
        """Get standard ERC-20 ABI"""
        return [
            {
                "constant": False,
                "inputs": [{"name": "to", "type": "address"}, {"name": "value", "type": "uint256"}],
                "name": "transfer",
                "outputs": [{"name": "", "type": "bool"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [{"name": "who", "type": "address"}],
                "name": "balanceOf",
                "outputs": [{"name": "", "type": "uint256"}],
                "type": "function"
            },
            {
                "constant": False,
                "inputs": [{"name": "spender", "type": "address"}, {"name": "value", "type": "uint256"}],
                "name": "approve",
                "outputs": [{"name": "", "type": "bool"}],
                "type": "function"
            },
            {
                "constant": True,
                "inputs": [],
                "name": "totalSupply",
                "outputs": [{"name": "", "type": "uint256"}],
                "type": "function"
            }
        ]
    
    @staticmethod
    def save_abi(abi: List[Dict], filename: str) -> None:
        """Save ABI to JSON file"""
        with open(filename, "w") as f:
            json.dump(abi, f, indent=2)
        print(f"✓ ABI saved to {filename}")
    
    @staticmethod
    def load_abi(filename: str) -> List[Dict]:
        """Load ABI from JSON file"""
        with open(filename, "r") as f:
            return json.load(f)

class TransactionBuilder:
    """Build and manage transactions"""
    
    def __init__(self):
        self.transactions = []
    
    def create_transfer_tx(
        self,
        to_address: str,
        amount: int,
        gas_limit: int = 100000,
        gas_price: int = 20
    ) -> Dict:
        """Create a transfer transaction"""
        tx = {
            "to": to_address,
            "amount": amount,
            "gasLimit": gas_limit,
            "gasPrice": gas_price,
            "data": "0x",
            "type": "transfer",
            "timestamp": datetime.now().isoformat()
        }
        self.transactions.append(tx)
        return tx
    
    def create_contract_call_tx(
        self,
        contract_address: str,
        function_name: str,
        params: List[Any],
        gas_limit: int = 200000,
        gas_price: int = 20
    ) -> Dict:
        """Create a contract call transaction"""
        tx = {
            "to": contract_address,
            "function": function_name,
            "params": params,
            "gasLimit": gas_limit,
            "gasPrice": gas_price,
            "type": "contract_call",
            "timestamp": datetime.now().isoformat()
        }
        self.transactions.append(tx)
        return tx
    
    def export_transactions(self, filename: str = "transactions.json") -> None:
        """Export transactions to JSON"""
        with open(filename, "w") as f:
            json.dump(self.transactions, f, indent=2)
        print(f"✓ Exported {len(self.transactions)} transactions to {filename}")

class ContractInteraction:
    """Wrapper for common contract interactions"""
    
    def __init__(self, contract_address: str, contract_type: ContractType):
        self.contract_address = contract_address
        self.contract_type = contract_type
    
    def prepare_stake_tx(self, amount: int) -> Dict:
        """Prepare staking transaction"""
        return {
            "function": "stake",
            "params": [amount],
            "description": f"Stake {ContractUtilities.from_wei(amount)} NVC"
        }
    
    def prepare_claim_rewards_tx(self) -> Dict:
        """Prepare claim rewards transaction"""
        return {
            "function": "claimRewards",
            "params": [],
            "description": "Claim accumulated staking rewards"
        }
    
    def prepare_vote_tx(self, proposal_id: int, support: int) -> Dict:
        """Prepare voting transaction"""
        vote_types = {0: "Against", 1: "For", 2: "Abstain"}
        return {
            "function": "castVote",
            "params": [proposal_id, support],
            "description": f"Vote {vote_types.get(support, 'Unknown')} on proposal {proposal_id}"
        }
    
    def prepare_propose_tx(
        self,
        title: str,
        description: str
    ) -> Dict:
        """Prepare proposal creation transaction"""
        return {
            "function": "propose",
            "params": [title, description],
            "description": f"Create proposal: {title}"
        }

class TokenomicsCalculator:
    """Calculate tokenomics metrics"""
    
    @staticmethod
    def calculate_staking_reward(
        principal: int,
        annual_rate: float = 0.08,
        days: int = 365
    ) -> int:
        """Calculate staking rewards"""
        return int(principal * annual_rate * (days / 365))
    
    @staticmethod
    def calculate_apy(
        principal: int,
        reward: int,
        days: int = 365
    ) -> float:
        """Calculate APY"""
        return ((reward / principal) / days) * 365
    
    @staticmethod
    def calculate_supply_after_burn(
        initial_supply: int,
        burn_amount: int
    ) -> int:
        """Calculate circulating supply after burns"""
        return initial_supply - burn_amount
    
    @staticmethod
    def calculate_distribution(
        total_supply: int,
        allocation: Dict[str, float]
    ) -> Dict[str, int]:
        """Calculate token allocation"""
        return {
            key: int(total_supply * percentage)
            for key, percentage in allocation.items()
        }

class VerificationHelper:
    """Help with contract verification"""
    
    @staticmethod
    def generate_verification_command(
        network: str,
        contract_address: str,
        contract_name: str,
        constructor_args: List[Any] = None
    ) -> str:
        """Generate Etherscan verification command"""
        cmd = f"npx hardhat verify --network {network} {contract_address}"
        if constructor_args:
            cmd += f" {' '.join(map(str, constructor_args))}"
        return cmd
    
    @staticmethod
    def create_verification_json(
        contracts: List[Dict]
    ) -> Dict:
        """Create verification information JSON"""
        return {
            "timestamp": datetime.now().isoformat(),
            "contracts": contracts
        }

# Example usage
if __name__ == "__main__":
    print("NOVA COIN Utilities Package loaded successfully!")
    print("\nAvailable utilities:")
    print("  - ContractUtilities: Wei conversion, address validation")
    print("  - DeploymentHelper: Track deployments")
    print("  - ABIManager: Manage contract ABIs")
    print("  - TransactionBuilder: Build transactions")
    print("  - ContractInteraction: Prepare contract calls")
    print("  - TokenomicsCalculator: Calculate rewards and APY")
    print("  - VerificationHelper: Etherscan verification")
