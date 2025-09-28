#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test cases for bug fixes
"""

import sys
import unittest
from unittest.mock import patch, MagicMock, Mock
import importlib
import builtins


class TestBugFixes(unittest.TestCase):
    """Test suite for specific bug fixes."""

    def test_bug1_sys_not_imported_in_external_api(self):
        """Test that sys.stderr is accessible when PyYAML import fails."""
        # Save the original import function
        real_import = builtins.__import__
        
        def mock_import(name, *args, **kwargs):
            if name == "yaml":
                raise ImportError("Mock PyYAML import failure")
            return real_import(name, *args, **kwargs)
        
        # Test that importing works even when yaml fails
        with patch('builtins.__import__', side_effect=mock_import):
            # Clear any cached module
            if 'external_api_integrator' in sys.modules:
                del sys.modules['external_api_integrator']
            
            # This should not raise NameError for sys.stderr
            try:
                import external_api_integrator
                # If import succeeds, the bug is fixed
                self.assertTrue(True)
            except NameError as e:
                if 'sys' in str(e):
                    self.fail(f"Bug 1 not fixed: sys.stderr is undefined when yaml import fails: {e}")
                raise
    
    def test_bug2_mutually_exclusive_flags(self):
        """Test that --verify and --update-config flags are mutually exclusive."""
        # This tests the fix for incorrect control flow with multiple if statements
        import venice_integration
        
        # Create mocks for both verifier and updater
        mock_verifier = MagicMock()
        mock_verifier.verify_api_key = MagicMock(return_value={"success": True})
        mock_updater = MagicMock()
        mock_updater.update_raycast_config = MagicMock(return_value={"success": True})
        
        # Patch both classes
        with patch('venice_integration.VeniceAIVerifier', return_value=mock_verifier):
            with patch('venice_integration.VeniceAIConfigUpdater', return_value=mock_updater):
                # Try running with both flags
                with patch('sys.argv', ['venice_integration.py', '--verify', '--update-config', '--api-key', 'test_key']):
                    with patch('venice_integration.json.dumps'):
                        # Run main
                        result = venice_integration.main()
                        
                        # Bug exists if BOTH were called (they should be mutually exclusive)
                        if mock_verifier.verify_api_key.called and mock_updater.update_raycast_config.called:
                            self.fail("Bug 2 not fixed: Both --verify and --update-config were executed when they should be mutually exclusive")
    
    def test_bug3_missing_timeout_in_external_api(self):
        """Test that HTTP requests have timeout parameter."""
        import external_api_integrator
        
        # Create an integrator instance
        integrator = external_api_integrator.ExternalAPIIntegrator()
        
        # Mock the configuration
        integrator.providers = {
            'test_provider': {
                'base_url': 'https://api.test.com',
                'api_keys': {'openai': 'test_key'},
                'models': [{'id': 'test-model'}]
            }
        }
        
        # Mock requests.post to check if timeout is passed
        with patch('external_api_integrator.requests.post') as mock_post:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.json.return_value = {'choices': [{'message': {'content': 'test'}}]}
            mock_post.return_value = mock_response
            
            # Call chat_completion
            result = integrator.chat_completion(
                provider_id='test_provider',
                model_id='test-model', 
                messages=[{'role': 'user', 'content': 'test'}]
            )
            
            # Check that post was called with a timeout
            mock_post.assert_called_once()
            call_kwargs = mock_post.call_args[1]
            
            # Bug is fixed if timeout parameter exists
            if 'timeout' not in call_kwargs:
                self.fail("Bug 3 not fixed: requests.post called without timeout parameter")
            else:
                # Verify reasonable timeout value
                timeout = call_kwargs['timeout']
                self.assertIsNotNone(timeout)
                self.assertGreater(timeout, 0)
                self.assertLessEqual(timeout, 120)  # Should be reasonable, not too long


if __name__ == '__main__':
    unittest.main()