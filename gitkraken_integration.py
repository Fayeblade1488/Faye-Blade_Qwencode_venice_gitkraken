#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitKraken CLI Integration Module for Qwen Code
This module provides integration with the GitKraken CLI using the OpenAPI specification.
It allows Qwen to interact with GitKraken's features including AI capabilities,
workspace management, git operations, and more.
"""

import subprocess
import json
import os
import sys
from typing import Optional, Dict, Any, List
from pathlib import Path


class GitKrakenCLI:
    """
    A class to interact with the GitKraken CLI.
    """
    
    def __init__(self):
        self.cli_path = self._find_gk_cli()
        
    def _find_gk_cli(self) -> Optional[str]:
        """Find the GitKraken CLI executable"""
        try:
            # Try to locate gk command
            result = subprocess.run(['which', 'gk'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
            
            # If not found in PATH, try common installation locations
            possible_paths = [
                '/usr/local/bin/gk',
                '/opt/homebrew/bin/gk',  # macOS with homebrew
                os.path.expanduser('~/bin/gk'),
                os.path.expanduser('~/.local/bin/gk')
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    return path
        except Exception:
            pass
        
        return None
    
    def is_installed(self) -> bool:
        """Check if GitKraken CLI is installed"""
        return self.cli_path is not None
    
    def run_command(self, args: List[str]) -> Dict[str, Any]:
        """
        Run a GitKraken CLI command and return the result.
        
        Args:
            args: List of arguments to pass to the gk command
            
        Returns:
            Dictionary containing the command result
        """
        if not self.is_installed():
            return {
                'success': False,
                'error': 'GitKraken CLI (gk) is not installed or not in PATH',
                'output': ''
            }
        
        try:
            cmd = [self.cli_path] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            return {
                'success': result.returncode == 0,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'command': ' '.join(cmd)
            }
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Command timed out',
                'output': ''
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'output': ''
            }
    
    # AI-related commands
    def ai_changelog(self, base: Optional[str] = None, head: Optional[str] = None, path: Optional[str] = None) -> Dict[str, Any]:
        """Generate a changelog between two commits or branches using AI"""
        args = ['ai', 'changelog']
        if base:
            args.extend(['--base', base])
        if head:
            args.extend(['--head', head])
        if path:
            args.extend(['--path', path])
        
        return self.run_command(args)
    
    def ai_commit(self, add_description: bool = False, path: Optional[str] = None) -> Dict[str, Any]:
        """Generate a new commit message with AI"""
        args = ['ai', 'commit']
        if add_description:
            args.append('--add-description')
        if path:
            args.extend(['--path', path])
        
        return self.run_command(args)
    
    def ai_explain_branch(self, branch: Optional[str] = None, path: Optional[str] = None) -> Dict[str, Any]:
        """Use AI to explain what changes a branch has"""
        args = ['ai', 'explain', 'branch']
        if branch:
            args.extend(['--branch', branch])
        if path:
            args.extend(['--path', path])
        
        return self.run_command(args)
    
    def ai_explain_commit(self, commit_sha: str, path: Optional[str] = None) -> Dict[str, Any]:
        """Use AI to explain changes in a commit"""
        args = ['ai', 'explain', 'commit', commit_sha]
        if path:
            args.extend(['--path', path])
        
        return self.run_command(args)
    
    def ai_pr_create(self, path: Optional[str] = None) -> Dict[str, Any]:
        """Generate a new PR with AI"""
        args = ['ai', 'pr', 'create']
        if path:
            args.extend(['--path', path])
        
        return self.run_command(args)
    
    def ai_resolve(self, path: Optional[str] = None) -> Dict[str, Any]:
        """Use AI to resolve git conflicts"""
        args = ['ai', 'resolve']
        if path:
            args.extend(['--path', path])
        
        return self.run_command(args)
    
    def ai_tokens(self) -> Dict[str, Any]:
        """Output GitKraken AI tokens used"""
        return self.run_command(['ai', 'tokens'])
    
    # Auth-related commands
    def auth_login(self, token: Optional[str] = None) -> Dict[str, Any]:
        """Login to GitKraken account"""
        args = ['auth', 'login']
        if token:
            args.extend(['--token', token])
        
        return self.run_command(args)
    
    def auth_logout(self) -> Dict[str, Any]:
        """Logout from GitKraken account"""
        return self.run_command(['auth', 'logout'])
    
    # Graph-related commands
    def graph(self, gitkraken: bool = False, gitlens: bool = False, gitlens_codium: bool = False, gitlens_insiders: bool = False, path: Optional[str] = None) -> Dict[str, Any]:
        """Display commit graph in current repository"""
        args = ['graph']
        if gitkraken:
            args.append('--gitkraken')
        if gitlens:
            args.append('--gitlens')
        if gitlens_codium:
            args.append('--gitlens-codium')
        if gitlens_insiders:
            args.append('--gitlens-insiders')
        if path:
            args.extend(['--path', path])
        
        return self.run_command(args)
    
    # Issue-related commands
    def issue_assign(self, provider: str, issue_id: str, organization_name: str, repo_name: str, email: Optional[str] = None, nickname: Optional[str] = None) -> Dict[str, Any]:
        """Assign an issue to a user"""
        args = ['issue', 'assign', provider, '--issue-id', issue_id, '--organization-name', organization_name, '--repo-name', repo_name]
        if email:
            args.extend(['--email', email])
        if nickname:
            args.extend(['--nickname', nickname])
        
        return self.run_command(args)
    
    def issue_list(self, provider: str) -> Dict[str, Any]:
        """Show list of issues"""
        return self.run_command(['issue', 'list', provider])
    
    # MCP-related commands
    def mcp_start(self, readonly: bool = False) -> Dict[str, Any]:
        """Start a local MCP server"""
        args = ['mcp']
        if readonly:
            args.append('--readonly')
        
        return self.run_command(args)
    
    def mcp_install(self, platform: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Install the GitKraken MCP server in an MCP client"""
        args = ['mcp', 'install', platform]
        if file_path:
            args.extend(['--file-path', file_path])
        
        return self.run_command(args)
    
    def mcp_uninstall(self, platform: str, file_path: Optional[str] = None) -> Dict[str, Any]:
        """Uninstall GitKraken MCP server"""
        args = ['mcp', 'uninstall', platform]
        if file_path:
            args.extend(['--file-path', file_path])
        
        return self.run_command(args)
    
    # Organization-related commands
    def organization_list(self) -> Dict[str, Any]:
        """List all GitKraken organizations"""
        return self.run_command(['organization', 'list'])
    
    def organization_set(self, name: str) -> Dict[str, Any]:
        """Set your default GitKraken organization"""
        return self.run_command(['organization', 'set', name])
    
    def organization_unset(self) -> Dict[str, Any]:
        """Clear your default GitKraken organization"""
        return self.run_command(['organization', 'unset'])
    
    # Provider-related commands
    def provider_add(self, provider: str, token: str) -> Dict[str, Any]:
        """Add a provider token"""
        return self.run_command(['provider', 'add', provider, '--token', token])
    
    def provider_list(self) -> Dict[str, Any]:
        """List all provider tokens"""
        return self.run_command(['provider', 'list'])
    
    def provider_remove(self, provider: str) -> Dict[str, Any]:
        """Remove a provider token"""
        return self.run_command(['provider', 'remove', provider])
    
    # Version command
    def version(self) -> Dict[str, Any]:
        """Print the version number of GK CLI"""
        return self.run_command(['version'])
    
    # Work-related commands
    def work_list(self) -> Dict[str, Any]:
        """List all work items"""
        return self.run_command(['work', 'list'])
    
    def work_info(self, name: Optional[str] = None) -> Dict[str, Any]:
        """View information about a work item"""
        args = ['work', 'info']
        if name:
            args.extend(['--name', name])
        
        return self.run_command(args)
    
    def work_start(self, name: str, issue: Optional[str] = None, branch: Optional[str] = None, base_branch: Optional[str] = None, 
                   include_repos: Optional[str] = None, exclude_repos: Optional[str] = None) -> Dict[str, Any]:
        """Start a new work item"""
        args = ['work', 'start', name]
        if issue:
            args.extend(['--issue', issue])
        if branch:
            args.extend(['--branch', branch])
        if base_branch:
            args.extend(['--base-branch', base_branch])
        if include_repos:
            args.extend(['--include-repos', include_repos])
        if exclude_repos:
            args.extend(['--exclude-repos', exclude_repos])
        
        return self.run_command(args)
    
    def work_set(self, name: str) -> Dict[str, Any]:
        """Set the active work item"""
        return self.run_command(['work', 'set', name])
    
    def work_branch(self, base_branch: Optional[str] = None, include_repos: Optional[str] = None, 
                    exclude_repos: Optional[str] = None) -> Dict[str, Any]:
        """Create a new branch for the work item"""
        args = ['work', 'branch']
        if base_branch:
            args.extend(['--base-branch', base_branch])
        if include_repos:
            args.extend(['--include-repos', include_repos])
        if exclude_repos:
            args.extend(['--exclude-repos', exclude_repos])
        
        return self.run_command(args)
    
    def work_commit(self, add_description: bool = False, ai: bool = False, 
                    include_repos: Optional[str] = None, exclude_repos: Optional[str] = None) -> Dict[str, Any]:
        """Commit changes for the work item"""
        args = ['work', 'commit']
        if add_description:
            args.append('--add-description')
        if ai:
            args.append('--ai')
        if include_repos:
            args.extend(['--include-repos', include_repos])
        if exclude_repos:
            args.extend(['--exclude-repos', exclude_repos])
        
        return self.run_command(args)
    
    def work_push(self, force: bool = False, create_pr: bool = False, 
                  include_repos: Optional[str] = None, exclude_repos: Optional[str] = None) -> Dict[str, Any]:
        """Push repository changes for the work item"""
        args = ['work', 'push']
        if force:
            args.append('--force')
        if create_pr:
            args.append('--create-pr')
        if include_repos:
            args.extend(['--include-repos', include_repos])
        if exclude_repos:
            args.extend(['--exclude-repos', exclude_repos])
        
        return self.run_command(args)
    
    def work_pr_create(self, title: Optional[str] = None, body: Optional[str] = None, ai: bool = False, push: bool = False,
                       include_repos: Optional[str] = None, exclude_repos: Optional[str] = None) -> Dict[str, Any]:
        """Create a new PR for the work item"""
        args = ['work', 'pr', 'create']
        if title:
            args.extend(['--title', title])
        if body:
            args.extend(['--body', body])
        if ai:
            args.append('--ai')
        if push:
            args.append('--push')
        if include_repos:
            args.extend(['--include-repos', include_repos])
        if exclude_repos:
            args.extend(['--exclude-repos', exclude_repos])
        
        return self.run_command(args)
    
    def work_pr_merge(self, include_repos: Optional[str] = None, exclude_repos: Optional[str] = None) -> Dict[str, Any]:
        """Merge existing PRs for the work item"""
        args = ['work', 'pr', 'merge']
        if include_repos:
            args.extend(['--include-repos', include_repos])
        if exclude_repos:
            args.extend(['--exclude-repos', exclude_repos])
        
        return self.run_command(args)
    
    def work_delete(self, name: str, force: bool = False) -> Dict[str, Any]:
        """Delete a work item"""
        args = ['work', 'delete', name]
        if force:
            args.append('--force')
        
        return self.run_command(args)
    
    def work_update(self) -> Dict[str, Any]:
        """Update a work item"""
        return self.run_command(['work', 'update'])
    
    # Workspace-related commands
    def workspace_list(self) -> Dict[str, Any]:
        """List all workspaces"""
        return self.run_command(['workspace', 'list'])
    
    def workspace_info(self, name: Optional[str] = None) -> Dict[str, Any]:
        """View information about a workspace"""
        args = ['workspace', 'info']
        if name:
            args.extend(['--name', name])
        
        return self.run_command(args)
    
    def workspace_create(self, name: Optional[str] = None, cloud: bool = False, description: Optional[str] = None,
                         add_repos: Optional[str] = None, add_members: Optional[str] = None, add_teams: Optional[str] = None,
                         organization_name: Optional[str] = None, root_path: Optional[str] = None) -> Dict[str, Any]:
        """Create a new workspace"""
        args = ['workspace', 'create']
        if name:
            args.extend(['--name', name])
        if cloud:
            args.append('--cloud')
        if description:
            args.extend(['--description', description])
        if add_repos:
            args.extend(['--add-repos', add_repos])
        if add_members:
            args.extend(['--add-members', add_members])
        if add_teams:
            args.extend(['--add-teams', add_teams])
        if organization_name:
            args.extend(['--organization-name', organization_name])
        if root_path:
            args.extend(['--root-path', root_path])
        
        return self.run_command(args)
    
    def workspace_set(self, name: str) -> Dict[str, Any]:
        """Set your default workspace"""
        return self.run_command(['workspace', 'set', name])
    
    def workspace_unset(self) -> Dict[str, Any]:
        """Clear active workspace"""
        return self.run_command(['workspace', 'unset'])
    
    def workspace_update(self, name: str, new_name: Optional[str] = None, description: Optional[str] = None,
                         cloud: Optional[bool] = None, add_repos: Optional[str] = None, remove_repos: Optional[str] = None,
                         add_members: Optional[str] = None, remove_members: Optional[str] = None,
                         add_teams: Optional[str] = None, remove_teams: Optional[str] = None,
                         azure_org: Optional[str] = None, azure_project: Optional[str] = None) -> Dict[str, Any]:
        """Update a workspace"""
        args = ['workspace', 'update', name]
        if new_name:
            args.extend(['--name', new_name])
        if description:
            args.extend(['--description', description])
        if cloud is not None:
            if cloud:
                args.append('--cloud')
            else:
                args.append('--no-cloud')
        if add_repos:
            args.extend(['--add-repos', add_repos])
        if remove_repos:
            args.extend(['--remove-repos', remove_repos])
        if add_members:
            args.extend(['--add-members', add_members])
        if remove_members:
            args.extend(['--remove-members', remove_members])
        if add_teams:
            args.extend(['--add-teams', add_teams])
        if remove_teams:
            args.extend(['--remove-teams', remove_teams])
        if azure_org:
            args.extend(['--azure-org', azure_org])
        if azure_project:
            args.extend(['--azure-project', azure_project])
        
        return self.run_command(args)
    
    def workspace_delete(self, name: str, force: bool = False) -> Dict[str, Any]:
        """Delete a workspace"""
        args = ['workspace', 'delete', name]
        if force:
            args.append('--force')
        
        return self.run_command(args)
    
    def workspace_refresh(self, name: Optional[str] = None, fetch_only: bool = False,
                          include_repos: Optional[str] = None, exclude_repos: Optional[str] = None) -> Dict[str, Any]:
        """Synchronize the state of your workspace"""
        args = ['workspace', 'refresh']
        if name:
            args.extend(['--name', name])
        if fetch_only:
            args.append('--fetch-only')
        if include_repos:
            args.extend(['--include-repos', include_repos])
        if exclude_repos:
            args.extend(['--exclude-repos', exclude_repos])
        
        return self.run_command(args)
    
    def workspace_clone(self, name: str, root_path: str) -> Dict[str, Any]:
        """Clone a workspace"""
        return self.run_command(['workspace', 'clone', name, root_path])


# Example usage
if __name__ == "__main__":
    gk = GitKrakenCLI()
    
    if gk.is_installed():
        print("GitKraken CLI is installed!")
        result = gk.version()
        print(f"Version: {result}")
    else:
        print("GitKraken CLI is not installed or not in PATH")