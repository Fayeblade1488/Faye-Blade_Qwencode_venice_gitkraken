#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen Code Integration Module
This module combines GitKraken CLI and Venice AI image generation capabilities
for use within the Qwen Code environment.
"""

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional

# Import our integration modules
from gitkraken_integration import GitKrakenCLI
from venice_integration import VeniceAIImageGenerator


class QwenCLIIntegrator:
    """
    Main class that integrates both GitKraken and Venice AI capabilities
    for use within the Qwen Code environment.
    """
    
    def __init__(self):
        self.gitkraken = GitKrakenCLI()
        self.venice_api_key = os.environ.get("VENICE_API_KEY")
        self.venice = None
        
        # Initialize Venice if API key is available
        if self.venice_api_key:
            try:
                self.venice = VeniceAIImageGenerator(api_key=self.venice_api_key)
            except ValueError as e:
                print(f"Warning: Venice AI not initialized: {e}", file=sys.stderr)
    
    def gitkraken_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a GitKraken CLI command.
        
        Args:
            command: The command to execute (e.g., 'ai_commit', 'graph', 'workspace_list')
            **kwargs: Arguments to pass to the command
            
        Returns:
            Dictionary containing the command result
        """
        if not self.gitkraken.is_installed():
            return {
                'success': False,
                'error': 'GitKraken CLI (gk) is not installed or not in PATH'
            }
        
        # Map command to the appropriate method
        method_map = {
            # AI commands
            'ai_changelog': self.gitkraken.ai_changelog,
            'ai_commit': self.gitkraken.ai_commit,
            'ai_explain_branch': self.gitkraken.ai_explain_branch,
            'ai_explain_commit': self.gitkraken.ai_explain_commit,
            'ai_pr_create': self.gitkraken.ai_pr_create,
            'ai_resolve': self.gitkraken.ai_resolve,
            'ai_tokens': self.gitkraken.ai_tokens,
            
            # Auth commands
            'auth_login': self.gitkraken.auth_login,
            'auth_logout': self.gitkraken.auth_logout,
            
            # Graph commands
            'graph': self.gitkraken.graph,
            
            # Issue commands
            'issue_assign': self.gitkraken.issue_assign,
            'issue_list': self.gitkraken.issue_list,
            
            # MCP commands
            'mcp_start': self.gitkraken.mcp_start,
            'mcp_install': self.gitkraken.mcp_install,
            'mcp_uninstall': self.gitkraken.mcp_uninstall,
            
            # Organization commands
            'organization_list': self.gitkraken.organization_list,
            'organization_set': self.gitkraken.organization_set,
            'organization_unset': self.gitkraken.organization_unset,
            
            # Provider commands
            'provider_add': self.gitkraken.provider_add,
            'provider_list': self.gitkraken.provider_list,
            'provider_remove': self.gitkraken.provider_remove,
            
            # Version command
            'version': self.gitkraken.version,
            
            # Work commands
            'work_list': self.gitkraken.work_list,
            'work_info': self.gitkraken.work_info,
            'work_start': self.gitkraken.work_start,
            'work_set': self.gitkraken.work_set,
            'work_branch': self.gitkraken.work_branch,
            'work_commit': self.gitkraken.work_commit,
            'work_push': self.gitkraken.work_push,
            'work_pr_create': self.gitkraken.work_pr_create,
            'work_pr_merge': self.gitkraken.work_pr_merge,
            'work_delete': self.gitkraken.work_delete,
            'work_update': self.gitkraken.work_update,
            
            # Workspace commands
            'workspace_list': self.gitkraken.workspace_list,
            'workspace_info': self.gitkraken.workspace_info,
            'workspace_create': self.gitkraken.workspace_create,
            'workspace_set': self.gitkraken.workspace_set,
            'workspace_unset': self.gitkraken.workspace_unset,
            'workspace_update': self.gitkraken.workspace_update,
            'workspace_delete': self.gitkraken.workspace_delete,
            'workspace_refresh': self.gitkraken.workspace_refresh,
            'workspace_clone': self.gitkraken.workspace_clone,
        }
        
        if command not in method_map:
            return {
                'success': False,
                'error': f'Unknown GitKraken command: {command}'
            }
        
        try:
            method = method_map[command]
            result = method(**kwargs)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def venice_generate_image(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Generate an image using Venice AI.
        
        Args:
            prompt: The prompt for image generation
            **kwargs: Additional parameters for image generation
            
        Returns:
            Dictionary containing the generation result
        """
        if not self.venice:
            return {
                'success': False,
                'error': 'Venice AI not initialized - please set VENICE_API_KEY environment variable'
            }
        
        try:
            result = self.venice.generate_image(prompt=prompt, **kwargs)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def venice_upscale_image(self, image_path: str, **kwargs) -> Dict[str, Any]:
        """
        Upscale an image using Venice AI.
        
        Args:
            image_path: Path to the input image file
            **kwargs: Additional parameters for upscaling
            
        Returns:
            Dictionary containing the upscaling result
        """
        if not self.venice:
            return {
                'success': False,
                'error': 'Venice AI not initialized - please set VENICE_API_KEY environment variable'
            }
        
        try:
            result = self.venice.upscale_image_file(image_path, **kwargs)
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def list_available_models(self) -> Dict[str, Any]:
        """
        List available Venice AI models, especially uncensored ones.
        
        Returns:
            Dictionary containing the model listing result
        """
        if not self.venice:
            return {
                'success': False,
                'error': 'Venice AI not initialized - please set VENICE_API_KEY environment variable'
            }
        
        try:
            models = self.venice.list_models()
            uncensored_models = self.venice.get_uncensored_models()
            return {
                'success': True,
                'all_models': models,
                'uncensored_models': uncensored_models
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """Main function to handle command line interface."""
    parser = argparse.ArgumentParser(description="Qwen Code Integration Tool")
    subparsers = parser.add_subparsers(dest="tool", help="Available tools")
    
    # GitKraken subcommands
    gk_parser = subparsers.add_parser("gitkraken", help="GitKraken CLI integration")
    gk_subparsers = gk_parser.add_subparsers(dest="gk_command", help="GitKraken commands")
    
    # Common arguments for GitKraken commands
    common_gk_args = {
        "path": {"type": str, "help": "Repository path", "required": False},
    }
    
    # AI commands
    ai_changelog = gk_subparsers.add_parser("ai_changelog", help="Generate changelog with AI")
    ai_changelog.add_argument("--base", type=str, help="Base branch or commit")
    ai_changelog.add_argument("--head", type=str, help="Head branch or commit")
    ai_changelog.add_argument("--path", type=str, help="Repository path")
    
    ai_commit = gk_subparsers.add_parser("ai_commit", help="Generate commit with AI")
    ai_commit.add_argument("--add-description", action="store_true", help="Add description to commit message")
    ai_commit.add_argument("--path", type=str, help="Repository path")
    
    ai_explain_branch = gk_subparsers.add_parser("ai_explain_branch", help="Explain branch changes with AI")
    ai_explain_branch.add_argument("--branch", type=str, help="Branch to explain (default: HEAD)")
    ai_explain_branch.add_argument("--path", type=str, help="Repository path")
    
    ai_explain_commit = gk_subparsers.add_parser("ai_explain_commit", help="Explain commit changes with AI")
    ai_explain_commit.add_argument("commit_sha", type=str, help="Commit SHA to explain")
    ai_explain_commit.add_argument("--path", type=str, help="Repository path")
    
    ai_pr_create = gk_subparsers.add_parser("ai_pr_create", help="Create PR with AI")
    ai_pr_create.add_argument("--path", type=str, help="Repository path")
    
    ai_resolve = gk_subparsers.add_parser("ai_resolve", help="Resolve conflicts with AI")
    ai_resolve.add_argument("--path", type=str, help="Repository path")
    
    gk_subparsers.add_parser("ai_tokens", help="Show GitKraken AI tokens used")
    
    # Common commands
    gk_subparsers.add_parser("version", help="Show GitKraken CLI version")
    
    # Work commands
    work_list = gk_subparsers.add_parser("work_list", help="List work items")
    
    work_start = gk_subparsers.add_parser("work_start", help="Start a new work item")
    work_start.add_argument("name", type=str, help="Name for the work item")
    work_start.add_argument("--issue", type=str, help="Issue key to link")
    work_start.add_argument("--branch", type=str, help="Branch name")
    work_start.add_argument("--base-branch", type=str, help="Base branch")
    work_start.add_argument("--include-repos", type=str, help="Include repos (comma-separated)")
    work_start.add_argument("--exclude-repos", type=str, help="Exclude repos (comma-separated)")
    
    # Workspace commands
    ws_list = gk_subparsers.add_parser("workspace_list", help="List workspaces")
    ws_info = gk_subparsers.add_parser("workspace_info", help="Show workspace info")
    ws_info.add_argument("--name", type=str, help="Workspace name")
    
    # Venice AI subcommands
    venice_parser = subparsers.add_parser("venice", help="Venice AI integration")
    venice_subparsers = venice_parser.add_subparsers(dest="venice_command", help="Venice commands")
    
    # Image generation command
    gen_parser = venice_subparsers.add_parser("generate", help="Generate an image")
    gen_parser.add_argument("--prompt", type=str, required=True, help="Prompt for image generation")
    gen_parser.add_argument("--model", type=str, default="lustify-sdxl", help="Model to use")
    gen_parser.add_argument("--aspect-ratio", type=str, default="tall", choices=["square", "tall", "wide"], 
                            help="Aspect ratio for output")
    gen_parser.add_argument("--output-dir", type=str, default="generated", help="Output directory")
    gen_parser.add_argument("--output-name", type=str, help="Output filename")
    gen_parser.add_argument("--steps", type=int, default=30, help="Number of inference steps")
    gen_parser.add_argument("--cfg-scale", type=float, default=5.0, help="Classifier-free guidance scale")
    gen_parser.add_argument("--seed", type=int, help="Random seed")
    gen_parser.add_argument("--format", type=str, default="png", choices=["png", "webp"], help="Output format")
    gen_parser.add_argument("--safe-mode", action="store_true", help="Enable safe mode")
    gen_parser.add_argument("--no-safe-mode", action="store_true", help="Disable safe mode")
    gen_parser.add_argument("--no-watermark", action="store_true", help="Hide watermark")
    gen_parser.add_argument("--upscale", action="store_true", help="Auto-upscale generated images")
    gen_parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    # Upscale command
    upscale_parser = venice_subparsers.add_parser("upscale", help="Upscale an image")
    upscale_parser.add_argument("--input", type=str, required=True, help="Input image path")
    upscale_parser.add_argument("--output", type=str, help="Output image path")
    upscale_parser.add_argument("--scale", type=int, default=4, help="Upscale scale factor")
    upscale_parser.add_argument("--enhance", action="store_true", help="Enhance details")
    upscale_parser.add_argument("--creativity", type=float, default=0.15, help="Enhance creativity")
    upscale_parser.add_argument("--replication", type=float, default=0.35, help="Replication factor")
    upscale_parser.add_argument("--prompt", type=str, help="Enhancement prompt")
    upscale_parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    # List models command
    venice_subparsers.add_parser("list-models", help="List available Venice AI models")
    
    args = parser.parse_args()
    
    # Initialize the integrator
    integrator = QwenCLIIntegrator()
    
    if args.tool == "gitkraken":
        if args.gk_command is None:
            parser.print_help()
            return 1
            
        # Prepare arguments for the command
        kwargs = {}
        for key, value in vars(args).items():
            if key not in ["tool", "gk_command"]:
                kwargs[key] = value
        
        # Execute GitKraken command
        result = integrator.gitkraken_command(args.gk_command, **kwargs)
        print(json.dumps(result, indent=2))
        
    elif args.tool == "venice":
        if args.venice_command is None:
            parser.print_help()
            return 1
            
        if args.venice_command == "generate":
            # Determine safe mode
            if args.no_safe_mode:
                safe_mode = False
            elif args.safe_mode:
                safe_mode = True
            else:
                safe_mode = False  # Default to False for uncensored
            
            result = integrator.venice_generate_image(
                prompt=args.prompt,
                model=args.model,
                aspect_ratio=args.aspect_ratio,
                steps=args.steps,
                cfg_scale=args.cfg_scale,
                seed=args.seed,
                output_format=args.format,
                safe_mode=safe_mode,
                hide_watermark=args.no_watermark,
                auto_upscale=args.upscale,
                output_dir=args.output_dir,
                output_name=args.output_name,
                verbose=args.verbose
            )
            print(json.dumps(result, indent=2))
            
        elif args.venice_command == "upscale":
            result = integrator.venice_upscale_image(
                image_path=args.input,
                output_path=args.output,
                scale=args.scale,
                enhance=args.enhance,
                enhance_creativity=args.creativity,
                enhance_prompt=args.prompt,
                replication=args.replication,
                verbose=args.verbose
            )
            print(json.dumps(result, indent=2))
            
        elif args.venice_command == "list-models":
            result = integrator.list_available_models()
            print(json.dumps(result, indent=2))
    
    else:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())