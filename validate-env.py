#!/usr/bin/env python3
"""
Ribit 2.0 Environment Configuration Validator

This script validates your .env file and identifies common configuration errors.
"""

import os
import re
from pathlib import Path

def validate_env():
    """Validate the .env configuration file."""
    
    print("🔍 Ribit 2.0 Configuration Validator")
    print("=" * 60)
    print()
    
    env_file = Path(".env")
    
    if not env_file.exists():
        print("❌ ERROR: .env file not found!")
        print()
        print("Create one by copying the template:")
        print("  cp .env.template .env")
        print("  nano .env")
        print()
        return False
    
    # Load .env file
    config = {}
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip().strip('"\'')
    
    print("📄 Configuration loaded from .env")
    print()
    
    # Validation checks
    issues = []
    warnings = []
    
    # Check 1: MATRIX_HOMESERVER
    if 'MATRIX_HOMESERVER' in config:
        homeserver = config['MATRIX_HOMESERVER']
        print(f"✓ MATRIX_HOMESERVER: {homeserver}")
        
        if 'matrix.envs.net' in homeserver:
            issues.append({
                'field': 'MATRIX_HOMESERVER',
                'current': homeserver,
                'should_be': 'https://envs.net',
                'reason': 'Should not include "matrix." prefix'
            })
        elif not homeserver.startswith('https://'):
            warnings.append(f"MATRIX_HOMESERVER should start with https://")
    else:
        issues.append({
            'field': 'MATRIX_HOMESERVER',
            'current': 'MISSING',
            'should_be': 'https://envs.net',
            'reason': 'Required field is missing'
        })
    
    # Check 2: MATRIX_USERNAME
    if 'MATRIX_USERNAME' in config:
        username = config['MATRIX_USERNAME']
        print(f"✓ MATRIX_USERNAME: {username}")
        
        # Check for wrong format (periods instead of colon)
        if re.match(r'@[^:]+\.[^:]+\.', username):
            # Extract what should be the correct format
            parts = username.split('.')
            if len(parts) >= 3:
                correct_username = f"@{parts[0][1:]}:{parts[-2]}.{parts[-1]}"
                issues.append({
                    'field': 'MATRIX_USERNAME',
                    'current': username,
                    'should_be': correct_username,
                    'reason': 'Uses periods (.) instead of colon (:) - Matrix usernames MUST use colon!'
                })
        
        # Check if starts with @
        if not username.startswith('@'):
            issues.append({
                'field': 'MATRIX_USERNAME',
                'current': username,
                'should_be': f'@{username}',
                'reason': 'Must start with @ symbol'
            })
        
        # Check if has colon
        if ':' not in username:
            warnings.append(f"MATRIX_USERNAME should contain : to separate username from homeserver")
    else:
        issues.append({
            'field': 'MATRIX_USERNAME',
            'current': 'MISSING',
            'should_be': '@ribit:envs.net',
            'reason': 'Required field is missing'
        })
    
    # Check 3: MATRIX_PASSWORD
    if 'MATRIX_PASSWORD' in config:
        password = config['MATRIX_PASSWORD']
        if password:
            print(f"✓ MATRIX_PASSWORD: {'*' * len(password)}")
            
            if password in ['your_password_here', 'your-secure-password', 'password']:
                issues.append({
                    'field': 'MATRIX_PASSWORD',
                    'current': '[default placeholder]',
                    'should_be': '[your actual bot password]',
                    'reason': 'Still using placeholder password - must use actual bot password'
                })
        else:
            issues.append({
                'field': 'MATRIX_PASSWORD',
                'current': 'EMPTY',
                'should_be': '[your actual bot password]',
                'reason': 'Password cannot be empty'
            })
    else:
        issues.append({
            'field': 'MATRIX_PASSWORD',
            'current': 'MISSING',
            'should_be': '[your actual bot password]',
            'reason': 'Required field is missing'
        })
    
    # Check 4: Username and Homeserver match
    if 'MATRIX_USERNAME' in config and 'MATRIX_HOMESERVER' in config:
        username = config['MATRIX_USERNAME']
        homeserver = config['MATRIX_HOMESERVER']
        
        if ':' in username:
            username_domain = username.split(':')[1]
            homeserver_domain = homeserver.replace('https://', '').replace('http://', '')
            
            if username_domain != homeserver_domain:
                warnings.append(
                    f"Username domain ({username_domain}) doesn't match homeserver ({homeserver_domain})"
                )
    
    print()
    print("=" * 60)
    print()
    
    # Report issues
    if issues:
        print(f"❌ Found {len(issues)} CRITICAL issue(s):")
        print()
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue['field']}")
            print(f"   Current:   {issue['current']}")
            print(f"   Should be: {issue['should_be']}")
            print(f"   Reason:    {issue['reason']}")
            print()
    
    if warnings:
        print(f"⚠️  Found {len(warnings)} warning(s):")
        print()
        for i, warning in enumerate(warnings, 1):
            print(f"{i}. {warning}")
        print()
    
    if not issues and not warnings:
        print("✅ All checks passed! Configuration looks good.")
        print()
        print("🚀 You can now start the bot:")
        print("   python3 run_matrix_bot.py")
        print()
        return True
    
    if issues:
        print("=" * 60)
        print()
        print("🔧 TO FIX:")
        print()
        print("1. Edit your .env file:")
        print("   nano .env")
        print()
        print("2. Make the changes shown above")
        print()
        print("3. Run this validator again:")
        print("   python3 validate-env.py")
        print()
        print("=" * 60)
        return False
    
    return True

if __name__ == "__main__":
    try:
        success = validate_env()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        exit(1)

