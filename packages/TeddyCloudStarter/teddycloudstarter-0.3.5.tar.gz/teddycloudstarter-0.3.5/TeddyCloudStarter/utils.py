#!/usr/bin/env python3
"""
Utility functions for TeddyCloudStarter.
"""
import socket
import re
import ipaddress
import os
import dns.resolver
from pathlib import Path


def check_port_available(port: int) -> bool:
    """Check if a port is available on the system.
    
    Args:
        port: The port number to check
        
    Returns:
        bool: True if port is available, False otherwise
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return True
        except socket.error:
            return False


def validate_domain_name(domain: str) -> bool:
    """Validate a domain name format.
    
    Args:
        domain: The domain name to validate
        
    Returns:
        bool: True if valid domain, False otherwise
    """
    domain_pattern = r'^[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?)*$'
    return bool(re.match(domain_pattern, domain))


def check_domain_resolvable(domain: str) -> bool:
    """Check if a domain is publicly resolvable using Quad9 DNS.
    
    Args:
        domain: The domain to check
        
    Returns:
        bool: True if resolvable, False otherwise
    """
    try:
        # Configure resolver to use Quad9 DNS servers
        resolver = dns.resolver.Resolver(configure=False)
        resolver.nameservers = ['9.9.9.9', '149.112.112.112']  # Quad9 DNS servers
        
        # Attempt to resolve the domain
        answers = resolver.resolve(domain, 'A')
        
        # If we get here, the domain is resolvable
        return True
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, 
            dns.resolver.NoNameservers, dns.exception.Timeout):
        # Domain doesn't exist or cannot be resolved
        return False
    except Exception:
        # Fallback to standard socket resolution in case of other errors
        try:
            socket.gethostbyname(domain)
            return True
        except socket.gaierror:
            return False


def validate_ip_address(ip_str: str) -> bool:
    """Validate an IP address or CIDR notation.
    
    Args:
        ip_str: The string to validate as IP or CIDR
        
    Returns:
        bool: True if valid IP or CIDR, False otherwise
    """
    try:
        ipaddress.ip_network(ip_str)
        return True
    except ValueError:
        return False


def get_project_path(config_manager=None):
    """
    Get the project path from config or return None if not set.
    
    Args:
        config_manager: The configuration manager instance
        
    Returns:
        str: The project path, or None if not set
    """
    try:
        if config_manager and config_manager.config:
            return config_manager.config.get("environment", {}).get("path")
        return None
    except Exception:
        return None


def ensure_project_directories(project_path=None):
    """
    Create necessary directories in the project path if provided, otherwise in current working directory.
    
    Args:
        project_path: The path to the project directory
    """
    base_path = Path(project_path) if project_path else Path(".")
    (base_path / "data").mkdir(exist_ok=True)
    (base_path / "data" / "configurations").mkdir(exist_ok=True)
    (base_path / "data" / "backup").mkdir(exist_ok=True)