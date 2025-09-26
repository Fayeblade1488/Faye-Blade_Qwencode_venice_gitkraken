#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
External API Integrator Module for Qwen CLI
This module handles integration with external API providers like Venice.ai
based on configurations from Raycast or other external sources.
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests

# Try to import yaml, with a fallback if not available
try:
    import yaml
except ImportError:
    print("Warning: PyYAML is not installed. Install it with 'pip install PyYAML' to use external API providers functionality.", file=sys.stderr)
    yaml = None


class ExternalAPIIntegrator:
    """Integrates with external AI providers using configuration files.

    This class loads provider details, such as API endpoints and models, from
    a YAML configuration file (e.g., from Raycast). It provides methods to
    list available providers and models, and to perform chat completions
    using a specified provider.

    Attributes:
        providers_config_path (Optional[str]): The path to the provider
            configuration YAML file.
        providers (Dict[str, Any]): A dictionary holding the configuration
            for all loaded providers, keyed by provider ID.
    """

    def __init__(self, providers_config_path: Optional[str] = None):
        """Initializes the ExternalAPIIntegrator.

        Args:
            providers_config_path: An optional path to the providers'
                configuration file. If not provided, it will search in the
                default Raycast config locations.
        """
        self.providers_config_path = providers_config_path or self._find_raycast_providers_config()
        self.providers = {}
        if self.providers_config_path:
            self.load_providers_from_config()
    
    def _find_raycast_providers_config(self) -> Optional[str]:
        """Finds the Raycast providers configuration file in common locations.

        Returns:
            The path to the configuration file if found, otherwise None.
        """
        possible_paths = [
            os.path.expanduser("~/.config/raycast/ai/providers.yaml"),
            os.path.expanduser("~/.config/raycast/ai/providers.yml"),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        return None
    
    def load_providers_from_config(self) -> bool:
        """Loads provider configurations from the YAML file.

        Parses the YAML file specified in `providers_config_path` and populates
        the `providers` dictionary.

        Returns:
            True if providers were loaded successfully, False otherwise.
        """
        if not self.providers_config_path or not os.path.exists(self.providers_config_path):
            return False
        
        try:
            with open(self.providers_config_path, 'r') as f:
                config_data = yaml.safe_load(f)
            
            if 'providers' in config_data:
                for provider in config_data['providers']:
                    provider_id = provider.get('id')
                    if provider_id:
                        self.providers[provider_id] = provider
                return True
            else:
                print(f"Warning: No 'providers' key found in {self.providers_config_path}", file=sys.stderr)
                return False
        except Exception as e:
            print(f"Error loading providers from config: {e}", file=sys.stderr)
            return False
    
    def get_available_providers(self) -> List[str]:
        """Gets a list of available provider IDs from the loaded configuration.

        Returns:
            A list of strings, where each string is a provider ID.
        """
        return list(self.providers.keys())
    
    def get_provider_info(self, provider_id: str) -> Optional[Dict[str, Any]]:
        """Gets the configuration information for a specific provider.

        Args:
            provider_id: The ID of the provider to retrieve information for.

        Returns:
            A dictionary containing the provider's configuration, or None if
            the provider ID is not found.
        """
        return self.providers.get(provider_id)
    
    def get_provider_models(self, provider_id: str) -> List[Dict[str, Any]]:
        """Gets the list of models available for a specific provider.

        Args:
            provider_id: The ID of the provider.

        Returns:
            A list of model dictionaries for the specified provider. Returns
            an empty list if the provider is not found.
        """
        provider_info = self.get_provider_info(provider_id)
        if not provider_info:
            return []
        
        return provider_info.get('models', [])
    
    def get_default_provider_api_key(self, provider_id: str) -> Optional[str]:
        """Retrieves the API key for a provider from the configuration.

        It prioritizes keys of type 'openai' but will return the first key
        it finds. Note that keys may be placeholders that reference
        environment variables (e.g., "${VENICE_API_KEY}").

        Args:
            provider_id: The ID of the provider.

        Returns:
            The API key string or placeholder, or None if not found.
        """
        provider_info = self.get_provider_info(provider_id)
        if not provider_info or 'api_keys' not in provider_info:
            return None
        
        # Get the first API key from the api_keys dict
        api_keys = provider_info['api_keys']
        for key_type, key_value in api_keys.items():
            # If it's an OpenAI-compatible key, use it
            if key_type == 'openai':
                return key_value
            # If there are multiple keys, return the first non-empty one
            if key_value:
                return key_value
        
        return None
    
    def chat_completion(
        self,
        provider_id: str,
        model_id: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Performs a chat completion using a specified external provider.

        This method constructs and sends a request to the provider's chat
        completion endpoint and returns the response.

        Args:
            provider_id: The ID of the provider to use (e.g., 'venice').
            model_id: The ID of the model to use for the completion.
            messages: A list of message dictionaries, following the standard
                OpenAI format (e.g., `[{'role': 'user', 'content': '...'}]`).
            temperature: The temperature for the generation (creativity).
            max_tokens: The maximum number of tokens to generate.
            **kwargs: Any other parameters to pass to the provider's API.

        Returns:
            A dictionary containing the API response. On success, this will
            include the 'response' key with the provider's JSON response.
            On failure, it will include an 'error' key with details.
        """
        provider_info = self.get_provider_info(provider_id)
        if not provider_info:
            return {
                'success': False,
                'error': f'Provider {provider_id} not found in configuration'
            }
        
        base_url = provider_info.get('base_url')
        if not base_url:
            return {
                'success': False,
                'error': f'No base_url found for provider {provider_id}'
            }
        
        # Get API key
        api_key_placeholder = self.get_default_provider_api_key(provider_id)
        if not api_key_placeholder:
            return {
                'success': False,
                'error': f'No API key found for provider {provider_id}'
            }
        
        # Resolve API key from environment variable if it's a placeholder
        if api_key_placeholder.startswith('${') and api_key_placeholder.endswith('}'):
            env_var_name = api_key_placeholder[2:-1]
            api_key = os.environ.get(env_var_name)
            if not api_key:
                return {
                    'success': False,
                    'error': f'Environment variable {env_var_name} for API key not set'
                }
        else:
            api_key = api_key_placeholder

        # Validate model exists
        available_models = [m['id'] for m in self.get_provider_models(provider_id)]
        if model_id not in available_models:
            return {
                'success': False,
                'error': f'Model {model_id} not available for provider {provider_id}. Available: {available_models}'
            }
        
        # Prepare the request
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': model_id,
            'messages': messages,
            'temperature': temperature
        }
        
        if max_tokens:
            data['max_tokens'] = max_tokens
        
        # Add any additional parameters
        for key, value in kwargs.items():
            if value is not None:
                data[key] = value
        
        try:
            # Make the request to the provider
            response = requests.post(f"{base_url}/chat/completions", headers=headers, json=data, timeout=30)
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'response': response.json()
                }
            else:
                return {
                    'success': False,
                    'error': f'API request failed with status {response.status_code}: {response.text}'
                }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': f'Request failed: {str(e)}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def list_all_models(self) -> Dict[str, List[Dict[str, Any]]]:
        """Lists all models for all configured providers.

        Returns:
            A dictionary mapping each provider ID to a list of its
            available model dictionaries.
        """
        all_models = {}
        for provider_id in self.providers:
            all_models[provider_id] = self.get_provider_models(provider_id)
        return all_models


def main():
    """Main function to test the ExternalAPIIntegrator."""
    parser = argparse.ArgumentParser(description="External API Integrator for Qwen CLI")
    parser.add_argument(
        "--config-path",
        type=str,
        help="Path to providers configuration file"
    )
    parser.add_argument(
        "--list-providers",
        action="store_true",
        help="List available providers"
    )
    parser.add_argument(
        "--list-models",
        action="store_true",
        help="List models for all providers"
    )
    parser.add_argument(
        "--provider",
        type=str,
        help="Provider ID to use for operations"
    )
    parser.add_argument(
        "--model",
        type=str,
        help="Model ID to use for operations"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.7,
        help="Temperature for generation"
    )
    parser.add_argument(
        "--message",
        type=str,
        help="Single message to send to the model"
    )
    
    args = parser.parse_args()
    
    # Initialize the integrator
    integrator = ExternalAPIIntegrator(providers_config_path=args.config_path)
    
    if args.list_providers:
        providers = integrator.get_available_providers()
        print("Available providers:")
        for provider in providers:
            print(f"  - {provider}")
    
    elif args.list_models:
        all_models = integrator.list_all_models()
        for provider_id, models in all_models.items():
            print(f"\nModels for provider '{provider_id}':")
            for model in models:
                print(f"  - {model.get('id', 'unknown')} ({model.get('name', 'unnamed')})")
    
    elif args.provider and args.message:
        if not args.model:
            print("Error: --model is required when using --provider and --message", file=sys.stderr)
            return 1
        
        # Format the message as a chat message
        messages = [{"role": "user", "content": args.message}]
        
        # Call the chat completion
        result = integrator.chat_completion(
            provider_id=args.provider,
            model_id=args.model,
            messages=messages,
            temperature=args.temperature
        )
        
        print(json.dumps(result, indent=2))
    
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())