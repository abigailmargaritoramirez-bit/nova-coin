#!/usr/bin/env python3
"""
Universal Resource Code (URC) Generator
Generates unified master identifiers for NOVA ecosystem resources

URC Format: SHA-256 hash of unified resource data
Compact Format: URC-NOVA-RID{ID}-NTK{ID}-NWA{ID}-NCT{ID}

Usage:
    python3 generate-urc.py --type token --rid RID-8A92F1 --token NTK-4B11C8 --wallet NWA-7F92D1
    python3 generate-urc.py --config resource.json
"""

import hashlib
import json
import sys
import argparse
from datetime import datetime
from typing import Dict, List, Optional

class URCGenerator:
    """Universal Resource Code Generator"""
    
    # Resource prefixes
    PREFIXES = {
        "urc": "URC",
        "ecosystem": "NOVA",
        "resource": "RID",
        "token": "NTK",
        "wallet": "NWA",
        "contract": "NCT",
        "governance": "NDAO"
    }
    
    def __init__(self):
        self.resources: List[Dict] = []
    
    def generate_urc(
        self,
        resource_id: str,
        token_id: Optional[str] = None,
        wallet_id: Optional[str] = None,
        contract_id: Optional[str] = None,
        governance_id: Optional[str] = None,
        name: str = "Nova Resource",
        resource_type: str = "digital_asset"
    ) -> Dict:
        """
        Generate URC and compact representation
        
        Args:
            resource_id: RID-XXXXXX
            token_id: NTK-XXXXXX (optional)
            wallet_id: NWA-XXXXXX (optional)
            contract_id: NCT-XXXXXX (optional)
            governance_id: NDAO-XXXX (optional)
            name: Resource name
            resource_type: Resource type
            
        Returns:
            Dict with URC, compact format, and metadata
        """
        # Build unified data string
        components = [
            resource_id,
            token_id or "",
            wallet_id or "",
            contract_id or "",
            governance_id or "",
            self.PREFIXES["ecosystem"]
        ]
        
        unified_data = "|".join(components)
        
        # Generate SHA-256 hash
        urc_hash = hashlib.sha256(unified_data.encode()).hexdigest()
        
        # Create compact format
        compact_parts = [
            self.PREFIXES["urc"],
            self.PREFIXES["ecosystem"],
            f"{self.PREFIXES['resource']}{resource_id.split('-')[1] if '-' in resource_id else resource_id[:6]}",
        ]
        
        if token_id:
            compact_parts.append(f"{self.PREFIXES['token']}{token_id.split('-')[1] if '-' in token_id else token_id[:6]}")
        
        if wallet_id:
            compact_parts.append(f"{self.PREFIXES['wallet']}{wallet_id.split('-')[1] if '-' in wallet_id else wallet_id[:6]}")
        
        compact_urc = "-".join(compact_parts)
        
        # Build full resource object
        resource = {
            "urc": {
                "master": urc_hash,
                "compact": compact_urc,
                "version": "1.0"
            },
            "identifiers": {
                "resource_id": resource_id,
                "token_id": token_id or None,
                "wallet_id": wallet_id or None,
                "contract_id": contract_id or None,
                "governance_id": governance_id or None
            },
            "metadata": {
                "name": name,
                "type": resource_type,
                "created_at": datetime.now().isoformat(),
                "verified": False
            },
            "verification": {
                "algorithm": "SHA-256",
                "data_hash": hashlib.sha256(unified_data.encode()).hexdigest(),
                "data_components": unified_data
            },
            "blockchain": {
                "network": "Ethereum",
                "consensus": "ProofOfStake"
            }
        }
        
        self.resources.append(resource)
        return resource
    
    def generate_batch(self, config: List[Dict]) -> List[Dict]:
        """
        Generate multiple URCs from configuration
        
        Args:
            config: List of resource configurations
            
        Returns:
            List of generated resources
        """
        results = []
        
        for item in config:
            resource = self.generate_urc(
                resource_id=item.get("resource_id"),
                token_id=item.get("token_id"),
                wallet_id=item.get("wallet_id"),
                contract_id=item.get("contract_id"),
                governance_id=item.get("governance_id"),
                name=item.get("name", "Nova Resource"),
                resource_type=item.get("type", "digital_asset")
            )
            results.append(resource)
        
        return results
    
    def export_json(self, filename: str = "urc_registry.json") -> None:
        """Export generated URCs to JSON"""
        with open(filename, "w") as f:
            json.dump(self.resources, f, indent=2)
        print(f"✓ Exported {len(self.resources)} URCs to {filename}")
    
    def display_resource(self, resource: Dict) -> None:
        """Pretty print resource information"""
        print("\n" + "="*70)
        print("UNIVERSAL RESOURCE CODE (URC) - NOVA ECOSYSTEM")
        print("="*70 + "\n")
        
        # Master URC
        print("📋 MASTER IDENTIFIERS:")
        print(f"  URC (Master):     {resource['urc']['master']}")
        print(f"  URC (Compact):    {resource['urc']['compact']}")
        print(f"  Version:          {resource['urc']['version']}")
        print()
        
        # Component IDs
        print("🔗 COMPONENT IDS:")
        ids = resource['identifiers']
        print(f"  Resource ID:      {ids['resource_id']}")
        print(f"  Token ID:         {ids['token_id'] or 'N/A'}")
        print(f"  Wallet ID:        {ids['wallet_id'] or 'N/A'}")
        print(f"  Contract ID:      {ids['contract_id'] or 'N/A'}")
        print(f"  Governance ID:    {ids['governance_id'] or 'N/A'}")
        print()
        
        # Metadata
        print("📝 METADATA:")
        meta = resource['metadata']
        print(f"  Name:             {meta['name']}")
        print(f"  Type:             {meta['type']}")
        print(f"  Created:          {meta['created_at']}")
        print(f"  Verified:         {meta['verified']}")
        print()
        
        # Verification
        print("✓ VERIFICATION:")
        verify = resource['verification']
        print(f"  Algorithm:        {verify['algorithm']}")
        print(f"  Data Hash:        {verify['data_hash']}")
        print()
        
        # Blockchain
        print("⛓️  BLOCKCHAIN:")
        blockchain = resource['blockchain']
        print(f"  Network:          {blockchain['network']}")
        print(f"  Consensus:        {blockchain['consensus']}")
        print()
        
        # Hierarchy
        print("📊 RESOURCE HIERARCHY:")
        print(f"  RESOURCE")
        print(f"    ↓ {ids['resource_id']}")
        print(f"    ↓ TOKEN: {ids['token_id'] or 'None'}")
        print(f"    ↓ WALLET: {ids['wallet_id'] or 'None'}")
        print(f"    ↓ CONTRACT: {ids['contract_id'] or 'None'}")
        print(f"    ↓ GOVERNANCE: {ids['governance_id'] or 'None'}")
        print(f"    ↓ SHA-256")
        print(f"    ↓ URC (MASTER)")
        print()

def main():
    parser = argparse.ArgumentParser(
        description="Universal Resource Code (URC) Generator for NOVA Ecosystem"
    )
    
    parser.add_argument(
        "--type",
        choices=["token", "contract", "resource", "wallet", "governance"],
        default="token",
        help="Resource type to generate"
    )
    
    parser.add_argument(
        "--rid",
        required=True,
        help="Resource ID (RID-XXXXXX)"
    )
    
    parser.add_argument(
        "--token",
        help="Token ID (NTK-XXXXXX)"
    )
    
    parser.add_argument(
        "--wallet",
        help="Wallet ID (NWA-XXXXXX)"
    )
    
    parser.add_argument(
        "--contract",
        help="Contract ID (NCT-XXXXXX)"
    )
    
    parser.add_argument(
        "--governance",
        help="Governance ID (NDAO-XXXX)"
    )
    
    parser.add_argument(
        "--name",
        default="Nova Resource",
        help="Resource name"
    )
    
    parser.add_argument(
        "--config",
        help="JSON config file for batch generation"
    )
    
    parser.add_argument(
        "--export",
        action="store_true",
        help="Export results to JSON file"
    )
    
    parser.add_argument(
        "--count",
        type=int,
        default=1,
        help="Number of URCs to generate (for demo)"
    )
    
    args = parser.parse_args()
    
    generator = URCGenerator()
    
    print("\n" + "="*70)
    print("  NOVA COIN - Universal Resource Code (URC) Generator")
    print("="*70 + "\n")
    
    # Batch mode from config file
    if args.config:
        try:
            with open(args.config, 'r') as f:
                config = json.load(f)
            
            resources = generator.generate_batch(config)
            
            for idx, resource in enumerate(resources, 1):
                print(f"\n[{idx}] Generated URC: {resource['urc']['master'][:16]}...")
            
            if args.export:
                generator.export_json()
        
        except FileNotFoundError:
            print(f"Error: Config file '{args.config}' not found")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in config file")
            sys.exit(1)
    
    # Single or multiple generation
    else:
        for i in range(args.count):
            resource = generator.generate_urc(
                resource_id=args.rid,
                token_id=args.token,
                wallet_id=args.wallet,
                contract_id=args.contract,
                governance_id=args.governance,
                name=args.name,
                resource_type=args.type
            )
            
            generator.display_resource(resource)
        
        if args.export:
            generator.export_json()
    
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
