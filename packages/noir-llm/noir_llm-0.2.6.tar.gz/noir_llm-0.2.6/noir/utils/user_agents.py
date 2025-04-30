"""
User agent utilities for Noir package.

This module provides a collection of user agents and functions to work with them
for use in model implementations to help with rate limit bypassing.
"""

import random
import requests
from typing import List, Optional

# Default list of user agents to use if fetching from the source fails
DEFAULT_USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/135.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0"
]

# URL to fetch user agents from
USER_AGENTS_URL = "https://gist.githubusercontent.com/pzb/b4b6f57144aea7827ae4/raw/cf847b76a142955b1410c8bcef3aabe221a63db1/user-agents.txt"

# Cache for user agents
_user_agents_cache = None


def fetch_user_agents() -> List[str]:
    """Fetch user agents from the source URL.
    
    Returns:
        A list of user agent strings
    """
    global _user_agents_cache
    
    # Return cached user agents if available
    if _user_agents_cache is not None:
        return _user_agents_cache
    
    try:
        # Fetch user agents from the source
        response = requests.get(USER_AGENTS_URL, timeout=10)
        
        if response.status_code == 200:
            # Parse the response and filter out empty lines
            agents = [line.strip() for line in response.text.split('\n') if line.strip()]
            
            # Cache the result
            _user_agents_cache = agents
            
            return agents
        else:
            # Return default user agents if fetching fails
            return DEFAULT_USER_AGENTS
    except Exception:
        # Return default user agents if an exception occurs
        return DEFAULT_USER_AGENTS


def get_random_user_agent() -> str:
    """Get a random user agent.
    
    Returns:
        A random user agent string
    """
    agents = fetch_user_agents()
    return random.choice(agents)


def get_random_user_agents(count: int = 5) -> List[str]:
    """Get multiple random user agents.
    
    Args:
        count: The number of user agents to return
        
    Returns:
        A list of random user agent strings
    """
    agents = fetch_user_agents()
    
    # If count is greater than the number of available agents,
    # return all agents (with potential duplicates to match count)
    if count >= len(agents):
        # Return all agents and add random ones to reach the requested count
        result = agents.copy()
        while len(result) < count:
            result.append(random.choice(agents))
        return result
    
    # Otherwise, return a random sample of the requested size
    return random.sample(agents, count)


def get_desktop_user_agent() -> str:
    """Get a random desktop user agent.
    
    Returns:
        A random desktop user agent string
    """
    agents = fetch_user_agents()
    
    # Filter for desktop user agents (simple heuristic)
    desktop_agents = [
        agent for agent in agents 
        if "Windows" in agent or "Macintosh" in agent or "Linux" in agent
        and "Mobile" not in agent and "Android" not in agent and "iPhone" not in agent and "iPad" not in agent
    ]
    
    # If no desktop agents found, return any random agent
    if not desktop_agents:
        return random.choice(agents)
    
    return random.choice(desktop_agents)


def get_mobile_user_agent() -> str:
    """Get a random mobile user agent.
    
    Returns:
        A random mobile user agent string
    """
    agents = fetch_user_agents()
    
    # Filter for mobile user agents (simple heuristic)
    mobile_agents = [
        agent for agent in agents 
        if "Mobile" in agent or "Android" in agent or "iPhone" in agent or "iPad" in agent
    ]
    
    # If no mobile agents found, return any random agent
    if not mobile_agents:
        return random.choice(agents)
    
    return random.choice(mobile_agents)
