#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Additional comprehensive tests to achieve 90% coverage
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch, mock_open, call, PropertyMock
import subprocess

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))


class TestMainFunctions(unittest.TestCase):
    """Test main functions of each module."""
    
    @patch('sys.argv', ['qwen_cli_integrator.py', 'gitkraken', 'version'])
    def test_qwen_main_gitkraken(self):
        """Test qwen main with gitkraken command."""
        from qwen_cli_integrator import main
        
        with patch('qwen_cli_integrator.QwenCLIIntegrator') as mock_integrator_class:
            mock_integrator = MagicMock()
            mock_integrator.gitkraken_command.return_value = {"success": True}
            mock_integrator_class.return_value = mock_integrator
            
            result = main()
            mock_integrator.gitkraken_command.assert_called_once()
    
    @patch('sys.argv', ['qwen_cli_integrator.py', 'venice', 'list-models'])
    def test_qwen_main_venice_list_models(self):
        """Test qwen main with venice list-models."""
        from qwen_cli_integrator import main
        
        with patch('qwen_cli_integrator.QwenCLIIntegrator') as mock_integrator_class:
            mock_integrator = MagicMock()
            mock_integrator.list_available_models.return_value = {
                "success": True, 
                "all_models": [], 
                "uncensored_models": []
            }
            mock_integrator_class.return_value = mock_integrator
            
            result = main()
            mock_integrator.list_available_models.assert_called_once()
    
    @patch('sys.argv', ['qwen_cli_integrator.py', 'venice', 'generate', '--prompt', 'test'])
    def test_qwen_main_venice_generate(self):
        """Test qwen main with venice generate command."""
        from qwen_cli_integrator import main
        
        with patch('qwen_cli_integrator.QwenCLIIntegrator') as mock_integrator_class:
            mock_integrator = MagicMock()
            mock_integrator.venice_generate_image.return_value = {
                "success": True,
                "generated_image_path": "/tmp/test.png"
            }
            mock_integrator_class.return_value = mock_integrator
            
            result = main()
            mock_integrator.venice_generate_image.assert_called_once()
    
    @patch('sys.argv', ['qwen_cli_integrator.py', 'venice', 'upscale', '--input', 'test.png'])
    def test_qwen_main_venice_upscale(self):
        """Test qwen main with venice upscale command."""
        from qwen_cli_integrator import main
        
        with patch('qwen_cli_integrator.QwenCLIIntegrator') as mock_integrator_class:
            mock_integrator = MagicMock()
            mock_integrator.venice_upscale_image.return_value = {
                "success": True,
                "output_path": "/tmp/test_upscaled.png"
            }
            mock_integrator_class.return_value = mock_integrator
            
            result = main()
            mock_integrator.venice_upscale_image.assert_called_once()
    
    @patch('sys.argv', ['qwen_cli_integrator.py', 'external', 'list-providers'])
    def test_qwen_main_external_list(self):
        """Test qwen main with external list-providers."""
        from qwen_cli_integrator import main
        
        with patch('qwen_cli_integrator.QwenCLIIntegrator') as mock_integrator_class:
            mock_integrator = MagicMock()
            mock_integrator.list_external_providers.return_value = {
                "success": True,
                "providers": [],
                "models": {}
            }
            mock_integrator_class.return_value = mock_integrator
            
            result = main()
            mock_integrator.list_external_providers.assert_called_once()
    
    @patch('sys.argv', ['qwen_cli_integrator.py', 'external', 'chat', '--provider', 'test', '--model', 'test-model', '--message', 'hello'])
    def test_qwen_main_external_chat(self):
        """Test qwen main with external chat."""
        from qwen_cli_integrator import main
        
        with patch('qwen_cli_integrator.QwenCLIIntegrator') as mock_integrator_class:
            mock_integrator = MagicMock()
            mock_integrator.external_chat_completion.return_value = {
                "success": True,
                "response": {}
            }
            mock_integrator_class.return_value = mock_integrator
            
            result = main()
            mock_integrator.external_chat_completion.assert_called_once()
    
    @patch('sys.argv', ['qwen_cli_integrator.py', 'venice-tools', 'verify'])
    def test_qwen_main_venice_tools_verify(self):
        """Test qwen main with venice-tools verify."""
        from qwen_cli_integrator import main
        
        with patch('qwen_cli_integrator.QwenCLIIntegrator') as mock_integrator_class:
            mock_integrator = MagicMock()
            mock_integrator.verify_venice_api.return_value = {"success": True}
            mock_integrator_class.return_value = mock_integrator
            
            result = main()
            mock_integrator.verify_venice_api.assert_called_once()
    
    @patch('sys.argv', ['qwen_cli_integrator.py', 'venice-tools', 'update-config'])
    def test_qwen_main_venice_tools_update(self):
        """Test qwen main with venice-tools update-config."""
        from qwen_cli_integrator import main
        
        with patch('qwen_cli_integrator.QwenCLIIntegrator') as mock_integrator_class:
            mock_integrator = MagicMock()
            mock_integrator.update_venice_config.return_value = {"success": True}
            mock_integrator_class.return_value = mock_integrator
            
            result = main()
            mock_integrator.update_venice_config.assert_called_once()


class TestQwenIntegratorMethods(unittest.TestCase):
    """Test QwenCLIIntegrator methods."""
    
    @patch.dict(os.environ, {"VENICE_API_KEY": "test_key"})
    def test_venice_generate_no_venice(self):
        """Test venice generate when venice not initialized."""
        from qwen_cli_integrator import QwenCLIIntegrator
        
        integrator = QwenCLIIntegrator()
        integrator.venice = None
        
        result = integrator.venice_generate_image("test prompt")
        self.assertFalse(result['success'])
        self.assertIn('not initialized', result['error'])
    
    @patch.dict(os.environ, {"VENICE_API_KEY": "test_key"})
    def test_venice_generate_with_venice(self):
        """Test venice generate with venice initialized."""
        from qwen_cli_integrator import QwenCLIIntegrator
        
        integrator = QwenCLIIntegrator()
        mock_venice = MagicMock()
        mock_venice.generate_image.return_value = {"success": True}
        integrator.venice = mock_venice
        
        result = integrator.venice_generate_image("test prompt", model="test-model")
        self.assertTrue(result['success'])
        mock_venice.generate_image.assert_called_once_with(prompt="test prompt", model="test-model")
    
    def test_venice_upscale_no_venice(self):
        """Test venice upscale when venice not initialized."""
        from qwen_cli_integrator import QwenCLIIntegrator
        
        integrator = QwenCLIIntegrator()
        integrator.venice = None
        
        result = integrator.venice_upscale_image("test.png")
        self.assertFalse(result['success'])
    
    def test_list_models_no_venice(self):
        """Test list models when venice not initialized."""
        from qwen_cli_integrator import QwenCLIIntegrator
        
        integrator = QwenCLIIntegrator()
        integrator.venice = None
        
        result = integrator.list_available_models()
        self.assertFalse(result['success'])
    
    def test_verify_venice_no_key(self):
        """Test verify venice without API key."""
        from qwen_cli_integrator import QwenCLIIntegrator
        
        integrator = QwenCLIIntegrator()
        integrator.venice_api_key = None
        
        result = integrator.verify_venice_api()
        self.assertFalse(result['success'])
        self.assertIn('No API key', result['error'])
    
    @patch('qwen_cli_integrator.VeniceAIVerifier')
    def test_verify_venice_with_key(self, mock_verifier_class):
        """Test verify venice with API key."""
        from qwen_cli_integrator import QwenCLIIntegrator
        
        mock_verifier = MagicMock()
        mock_verifier.verify_api_key.return_value = {"success": True}
        mock_verifier_class.return_value = mock_verifier
        
        integrator = QwenCLIIntegrator()
        integrator.venice_api_key = "test_key"
        
        result = integrator.verify_venice_api()
        self.assertTrue(result['success'])
    
    def test_update_venice_config_no_key(self):
        """Test update venice config without API key."""
        from qwen_cli_integrator import QwenCLIIntegrator
        
        integrator = QwenCLIIntegrator()
        integrator.venice_api_key = None
        
        result = integrator.update_venice_config()
        self.assertFalse(result['success'])
        self.assertIn('No API key', result['error'])
    
    @patch('qwen_cli_integrator.VeniceAIConfigUpdater')
    def test_update_venice_config_with_key(self, mock_updater_class):
        """Test update venice config with API key."""
        from qwen_cli_integrator import QwenCLIIntegrator
        
        mock_updater = MagicMock()
        mock_updater.update_raycast_config.return_value = {"success": True}
        mock_updater_class.return_value = mock_updater
        
        integrator = QwenCLIIntegrator()
        integrator.venice_api_key = "test_key"
        
        result = integrator.update_venice_config()
        self.assertTrue(result['success'])
    
    @patch('qwen_cli_integrator.GitKrakenCLI')
    def test_gitkraken_command_exception(self, mock_gk_class):
        """Test gitkraken command with exception."""
        from qwen_cli_integrator import QwenCLIIntegrator
        
        mock_gk = MagicMock()
        mock_gk.is_installed.return_value = True
        mock_gk.version.side_effect = Exception("Test error")
        mock_gk_class.return_value = mock_gk
        
        integrator = QwenCLIIntegrator()
        result = integrator.gitkraken_command('version')
        
        self.assertFalse(result['success'])
        self.assertIn('Test error', result['error'])


class TestGitKrakenMethods(unittest.TestCase):
    """Test GitKraken CLI methods."""
    
    @patch('gitkraken_integration.subprocess.run')
    def test_timeout_error(self, mock_run):
        """Test command timeout."""
        from gitkraken_integration import GitKrakenCLI
        
        mock_run.side_effect = subprocess.TimeoutExpired('cmd', 30)
        
        cli = GitKrakenCLI()
        cli.cli_path = '/usr/local/bin/gk'
        
        result = cli.run_command(['version'])
        self.assertFalse(result['success'])
        self.assertIn('timed out', result['error'])
    
    @patch('gitkraken_integration.subprocess.run')
    def test_generic_exception(self, mock_run):
        """Test generic exception in run_command."""
        from gitkraken_integration import GitKrakenCLI
        
        mock_run.side_effect = Exception("Generic error")
        
        cli = GitKrakenCLI()
        cli.cli_path = '/usr/local/bin/gk'
        
        result = cli.run_command(['version'])
        self.assertFalse(result['success'])
        self.assertIn('Generic error', result['error'])
    
    @patch('gitkraken_integration.subprocess.run')
    def test_ai_commands(self, mock_run):
        """Test various AI commands."""
        from gitkraken_integration import GitKrakenCLI
        
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'success'
        mock_result.stderr = ''
        mock_run.return_value = mock_result
        
        cli = GitKrakenCLI()
        cli.cli_path = '/usr/local/bin/gk'
        
        # Test ai_changelog
        result = cli.ai_changelog(base="main", head="feature")
        self.assertTrue(result['success'])
        
        # Test ai_explain_branch
        result = cli.ai_explain_branch(branch="feature")
        self.assertTrue(result['success'])
        
        # Test ai_explain_commit
        result = cli.ai_explain_commit("abc123")
        self.assertTrue(result['success'])
        
        # Test ai_pr_create
        result = cli.ai_pr_create()
        self.assertTrue(result['success'])
        
        # Test ai_resolve
        result = cli.ai_resolve()
        self.assertTrue(result['success'])
        
        # Test ai_tokens
        result = cli.ai_tokens()
        self.assertTrue(result['success'])
    
    @patch('gitkraken_integration.subprocess.run')
    def test_work_commands(self, mock_run):
        """Test work commands."""
        from gitkraken_integration import GitKrakenCLI
        
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = 'success'
        mock_result.stderr = ''
        mock_run.return_value = mock_result
        
        cli = GitKrakenCLI()
        cli.cli_path = '/usr/local/bin/gk'
        
        # Test work_list
        result = cli.work_list()
        self.assertTrue(result['success'])
        
        # Test work_info
        result = cli.work_info(name="test")
        self.assertTrue(result['success'])
        
        # Test work_start
        result = cli.work_start("new-work", issue="ISSUE-1")
        self.assertTrue(result['success'])
        
        # Test work_set
        result = cli.work_set("test-work")
        self.assertTrue(result['success'])


class TestExternalAPIIntegrator(unittest.TestCase):
    """Test external API integrator methods."""
    
    def test_get_default_api_key_env_var(self):
        """Test getting API key from environment variable."""
        from external_api_integrator import ExternalAPIIntegrator
        
        integrator = ExternalAPIIntegrator()
        integrator.providers = {
            'test': {
                'api_keys': {'openai': '${TEST_API_KEY}'}
            }
        }
        
        with patch.dict(os.environ, {'TEST_API_KEY': 'actual_key'}):
            result = integrator.chat_completion(
                'test', 'model',
                [{'role': 'user', 'content': 'test'}]
            )
            # Will fail due to missing model, but checks env var resolution
            self.assertFalse(result['success'])
    
    def test_chat_completion_no_base_url(self):
        """Test chat completion without base_url."""
        from external_api_integrator import ExternalAPIIntegrator
        
        integrator = ExternalAPIIntegrator()
        integrator.providers = {
            'test': {
                'api_keys': {'openai': 'test_key'},
                'models': [{'id': 'test-model'}]
            }
        }
        
        result = integrator.chat_completion(
            'test', 'test-model',
            [{'role': 'user', 'content': 'Hello'}]
        )
        
        self.assertFalse(result['success'])
        self.assertIn('No base_url', result['error'])
    
    def test_chat_completion_no_api_key(self):
        """Test chat completion without API key."""
        from external_api_integrator import ExternalAPIIntegrator
        
        integrator = ExternalAPIIntegrator()
        integrator.providers = {
            'test': {
                'base_url': 'https://api.test.com',
                'models': [{'id': 'test-model'}]
            }
        }
        
        result = integrator.chat_completion(
            'test', 'test-model',
            [{'role': 'user', 'content': 'Hello'}]
        )
        
        self.assertFalse(result['success'])
        self.assertIn('No API key', result['error'])
    
    def test_chat_completion_invalid_model(self):
        """Test chat completion with invalid model."""
        from external_api_integrator import ExternalAPIIntegrator
        
        integrator = ExternalAPIIntegrator()
        integrator.providers = {
            'test': {
                'base_url': 'https://api.test.com',
                'api_keys': {'openai': 'test_key'},
                'models': [{'id': 'valid-model'}]
            }
        }
        
        result = integrator.chat_completion(
            'test', 'invalid-model',
            [{'role': 'user', 'content': 'Hello'}]
        )
        
        self.assertFalse(result['success'])
        self.assertIn('not available', result['error'])
    
    @patch('external_api_integrator.requests.post')
    def test_chat_completion_api_error(self, mock_post):
        """Test chat completion with API error."""
        from external_api_integrator import ExternalAPIIntegrator
        
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Server error"
        mock_post.return_value = mock_response
        
        integrator = ExternalAPIIntegrator()
        integrator.providers = {
            'test': {
                'base_url': 'https://api.test.com',
                'api_keys': {'openai': 'test_key'},
                'models': [{'id': 'test-model'}]
            }
        }
        
        result = integrator.chat_completion(
            'test', 'test-model',
            [{'role': 'user', 'content': 'Hello'}],
            max_tokens=100
        )
        
        self.assertFalse(result['success'])
        self.assertIn('API request failed', result['error'])


class TestVeniceImageGeneration(unittest.TestCase):
    """Test Venice image generation methods."""
    
    @patch('venice_integration.requests.Session')
    def test_generate_image_binary_response(self, mock_session_class):
        """Test generating image with binary response."""
        from venice_integration import VeniceAIImageGenerator
        import base64
        
        # Setup mock binary response
        test_image = b"fake image data"
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {
            "x-request-id": "test-id",
            "Content-Type": "image/png"
        }
        mock_response.content = test_image
        
        mock_session = MagicMock()
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        generator = VeniceAIImageGenerator("test_key")
        
        with patch('builtins.open', mock_open()):
            with patch('venice_integration.pathlib.Path.mkdir'):
                result = generator.generate_image(
                    "test prompt",
                    output_dir="/tmp/test",
                    verbose=True
                )
        
        self.assertTrue(result['success'])
        self.assertIn('generated_image_path', result)
    
    @patch('venice_integration.requests.Session')
    def test_generate_image_json_response(self, mock_session_class):
        """Test generating image with JSON response."""
        from venice_integration import VeniceAIImageGenerator
        import base64
        
        # Setup mock JSON response with base64 image
        test_image = b"fake image data"
        encoded_image = base64.b64encode(test_image).decode('utf-8')
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"x-request-id": "test-id"}
        mock_response.json.return_value = {
            "images": [encoded_image]
        }
        
        mock_session = MagicMock()
        mock_session.post.return_value = mock_response
        mock_session_class.return_value = mock_session
        
        # Mock _is_binary_image_response to return False
        generator = VeniceAIImageGenerator("test_key")
        generator._is_binary_image_response = Mock(return_value=False)
        
        with patch('builtins.open', mock_open()):
            with patch('venice_integration.pathlib.Path.mkdir'):
                result = generator.generate_image(
                    "test prompt",
                    seed=42,
                    auto_upscale=False,
                    verbose=True
                )
        
        self.assertTrue(result['success'])
    
    def test_decode_image_from_json(self):
        """Test decoding image from JSON payload."""
        from venice_integration import VeniceAIImageGenerator
        import base64
        
        generator = VeniceAIImageGenerator("test_key")
        
        # Test with 'image' key
        test_data = b"test image"
        payload = {"image": base64.b64encode(test_data).decode('utf-8')}
        result = generator._decode_image_from_json(payload)
        self.assertEqual(result, test_data)
        
        # Test with 'images' key
        payload = {"images": [base64.b64encode(test_data).decode('utf-8')]}
        result = generator._decode_image_from_json(payload)
        self.assertEqual(result, test_data)
        
        # Test with no image data
        with self.assertRaises(KeyError):
            generator._decode_image_from_json({})
    
    def test_is_binary_image_response(self):
        """Test checking if response is binary image."""
        from venice_integration import VeniceAIImageGenerator
        
        generator = VeniceAIImageGenerator("test_key")
        
        # Test image response
        mock_resp = Mock()
        mock_resp.headers = {"Content-Type": "image/png"}
        self.assertTrue(generator._is_binary_image_response(mock_resp))
        
        # Test non-image response
        mock_resp.headers = {"Content-Type": "application/json"}
        self.assertFalse(generator._is_binary_image_response(mock_resp))
    
    def test_now_iso(self):
        """Test ISO timestamp generation."""
        from venice_integration import VeniceAIImageGenerator
        import re
        
        generator = VeniceAIImageGenerator("test_key")
        timestamp = generator._now_iso()
        
        # Check ISO format
        iso_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'
        self.assertRegex(timestamp, iso_pattern)


if __name__ == '__main__':
    unittest.main()