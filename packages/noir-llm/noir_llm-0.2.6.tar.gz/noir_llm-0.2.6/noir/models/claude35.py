"""
Claude 3.5 model implementation for Noir package.

This module provides a client for accessing Claude 3.5 model through a proxy API.
"""

import json
import time
import hashlib
import requests
from typing import Dict, List, Any, Optional
from colorama import Fore, Style

from noir.models.base import BaseModel
from noir.utils import get_random_user_agent

class Claude35Client:
    """Client for accessing Claude 3.5 model through a proxy API."""

    def __init__(self, debug: bool = False):
        """Initialize a Claude 3.5 client.

        Args:
            debug: Whether to print debug information
        """
        self.base_url = "https://claude3.free2gpt.xyz"
        self.api_url = f"{self.base_url}/api/generate"
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br, zstd",
            "accept-language": "en-US,en;q=0.9,en-IN;q=0.8",
            "content-type": "text/plain;charset=UTF-8",
            "dnt": "1",
            "origin": "https://claude3.free2gpt.xyz",
            "referer": "https://claude3.free2gpt.xyz",
            "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Microsoft Edge";v="128"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": get_random_user_agent()
        }
        self.session = requests.Session()
        self.debug = debug
        self.max_retries = 3
        self.retry_delay = 2
        self.conversation_history = []
        self.last_refresh_time = 0
        self.refresh_interval = 300  # Refresh tokens every 5 minutes

    def _generate_sign(self, time_val: int, text: str, secret: str = "") -> str:
        """Generate a signature for the request.
        
        Args:
            time_val: Timestamp value
            text: Text to sign
            secret: Optional secret value
            
        Returns:
            The generated signature
        """
        message = f"{time_val}:{text}:{secret}"
        return hashlib.sha256(message.encode()).hexdigest()

    def _generate_conversation_prompt(self, message: str) -> str:
        """Generate a complete conversation prompt including history.
        
        Args:
            message: The new message to add
            
        Returns:
            The complete conversation prompt
        """
        # If no history, just return the message
        if not self.conversation_history:
            return message
            
        # Build conversation context from history
        context = []
        for entry in self.conversation_history:
            role = entry["role"]
            content = entry["content"]
            if role == "user":
                context.append(f"Human: {content}")
            elif role == "assistant": 
                context.append(f"Assistant: {content}")
        
        # Add the new message
        context.append(f"Human: {message}")
        
        # Join with newlines
        return "\n".join(context)

    def send_message(self, message: str, system_message: str = "") -> str:
        """Send a message to the Claude 3.5 model.

        Args:
            message: The message to send
            system_message: Optional system message to set context

        Returns:
            The response from the model
        """
        # Generate conversation prompt
        conversation_prompt = self._generate_conversation_prompt(message)
        
        # Generate timestamp
        timestamp = int(time.time() * 1000)
        
        # Construct messages list
        messages = []
        if system_message:
            messages.append({"role": "system", "content": system_message})
        messages.append({"role": "user", "content": conversation_prompt})

        # Generate signature using conversation prompt
        sign = self._generate_sign(timestamp, conversation_prompt)

        # Prepare payload
        payload = {
            "messages": messages,
            "time": timestamp,
            "pass": None,
            "sign": sign
        }

        # Try to send the message with retries
        for attempt in range(self.max_retries):
            try:
                if self.debug:
                    print(f"{Fore.YELLOW}Sending message to Claude 3.5 (attempt {attempt + 1}/{self.max_retries})...{Style.RESET_ALL}")
                    print(f"{Fore.YELLOW}Payload: {json.dumps(payload, indent=2)}{Style.RESET_ALL}")

                # Rotate user agent
                self.headers["user-agent"] = get_random_user_agent()

                # Convert payload to string since content-type is text/plain
                payload_str = json.dumps(payload)

                # Send the request
                response = self.session.post(
                    self.api_url,
                    headers=self.headers,
                    data=payload_str,
                    timeout=60
                )

                if self.debug:
                    print(f"{Fore.YELLOW}Response status: {response.status_code}{Style.RESET_ALL}")

                if response.status_code == 200:
                    try:
                        response_text = response.text
                        if self.debug:
                            print(f"{Fore.GREEN}Successfully received response{Style.RESET_ALL}")
                            print(f"{Fore.YELLOW}Response: {response_text[:200]}...{Style.RESET_ALL}")

                        # Store the conversation history
                        self.conversation_history.extend(messages)
                        self.conversation_history.append({
                            "role": "assistant",
                            "content": response_text
                        })

                        return response_text

                    except Exception as e:
                        if self.debug:
                            print(f"{Fore.RED}Error parsing response: {str(e)}{Style.RESET_ALL}")
                        if attempt == self.max_retries - 1:
                            return "I encountered an error processing your request. Please try again."
                else:
                    if self.debug:
                        print(f"{Fore.RED}Request failed with status code {response.status_code}{Style.RESET_ALL}")
                        print(f"{Fore.RED}Response: {response.text}{Style.RESET_ALL}")

                    if attempt == self.max_retries - 1:
                        return "I'm currently experiencing high demand. Please try again in a moment."

                    # Wait before retrying
                    time.sleep(self.retry_delay)

            except Exception as e:
                if self.debug:
                    print(f"{Fore.RED}Error sending message: {str(e)}{Style.RESET_ALL}")
                if attempt == self.max_retries - 1:
                    return "I encountered an error processing your request. Please try again."
                time.sleep(self.retry_delay)

        return "Failed to get a response after multiple attempts. Please try again later."

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []


class Claude35Model(BaseModel):
    """Wrapper class for the Claude client for Claude 3.5 model."""

    def __init__(self, debug: bool = False):
        """Initialize the Claude 3.5 client.

        Args:
            debug: Whether to print debug information
        """
        super().__init__("Claude 3.5", "claude-3-5", False, debug)
        self.client = Claude35Client(debug=debug)
        self.system_prompt = "You are Claude, an AI assistant by Anthropic that is helpful, harmless, and honest."

    def send_message(self, message: str, websearch: bool = False) -> str:
        """Send a message to the model.

        Args:
            message: The message to send
            websearch: Whether to enable web search (not supported)

        Returns:
            The response from the model
        """
        if websearch:
            if self.debug:
                print(f"{Fore.YELLOW}Warning: Web search is not supported by {self.model_name}. Ignoring websearch parameter.{Style.RESET_ALL}")

        return self.client.send_message(message, system_message=self.system_prompt)

    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.client.clear_history()

    def set_system_prompt(self, prompt: str) -> None:
        """Set the system prompt for the model.

        Args:
            prompt: The system prompt to set
        """
        self.system_prompt = prompt

    def get_system_prompt(self) -> str:
        """Get the current system prompt.

        Returns:
            The current system prompt
        """
        return self.system_prompt
