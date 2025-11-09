#!/usr/bin/env python3
"""
Start the DeltaChat-Matrix Bridge

This script initializes and runs the unified bridge between DeltaChat
and Matrix platforms, enabling cross-platform communication through Ribit 2.0.

Usage:
    python run_deltachat_matrix_bridge.py

Environment Variables Required:
    SUPABASE_URL - Supabase project URL
    SUPABASE_ANON_KEY - Supabase anonymous key
    MATRIX_HOMESERVER - Matrix homeserver URL
    MATRIX_USERNAME - Matrix bot username
    MATRIX_PASSWORD - Matrix bot password
    DELTACHAT_EMAIL - DeltaChat bot email
    DELTACHAT_PASSWORD - DeltaChat bot password

Author: Manus AI
Date: November 2025
"""

import asyncio
import logging
import os
import sys
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def validate_environment():
    """Validate required environment variables."""
    required_vars = [
        "MATRIX_HOMESERVER",
        "MATRIX_USERNAME",
        "MATRIX_PASSWORD",
        "DELTACHAT_EMAIL",
        "DELTACHAT_PASSWORD",
    ]

    missing = []
    for var in required_vars:
        if not os.getenv(var):
            missing.append(var)

    if missing:
        print("❌ Missing required environment variables:")
        for var in missing:
            print(f"   - {var}")
        print("\nPlease set these variables or create a .env file")
        print("See .env.example for configuration template")
        return False

    optional_vars = ["SUPABASE_URL", "SUPABASE_ANON_KEY"]
    missing_optional = [v for v in optional_vars if not os.getenv(v)]

    if missing_optional:
        print("⚠️  Optional Supabase variables not set:")
        for var in missing_optional:
            print(f"   - {var}")
        print("   Bridge will run with in-memory state (no persistence)")
        print()

    return True


async def main():
    """Main entry point."""
    print("=" * 70)
    print("🌉 DeltaChat-Matrix Bridge - Ribit 2.0")
    print("=" * 70)
    print()

    if not validate_environment():
        sys.exit(1)

    try:
        from ribit_2_0.deltachat_matrix_bridge import DeltaChatMatrixBridge
        from ribit_2_0.matrix_bot import RibitMatrixBot
        from ribit_2_0.deltachat_bot import DeltaChatRibotBot, DeltaChatBotConfig
        from ribit_2_0.mock_llm_wrapper import MockRibit20LLM

        logger.info("✅ All modules imported successfully")

    except ImportError as e:
        logger.error(f"❌ Failed to import required modules: {e}")
        print("\nPlease ensure all dependencies are installed:")
        print("   pip install -r requirements.txt")
        sys.exit(1)

    try:
        from supabase import create_client

        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_ANON_KEY")

        supabase_client = None
        if supabase_url and supabase_key:
            supabase_client = create_client(supabase_url, supabase_key)
            logger.info("✅ Supabase client initialized")
        else:
            logger.warning("⚠️  Supabase not configured - using in-memory state")

    except ImportError:
        logger.warning("⚠️  Supabase client not available - using in-memory state")
        supabase_client = None
    except Exception as e:
        logger.warning(f"⚠️  Supabase initialization failed: {e}")
        supabase_client = None

    try:
        logger.info("Initializing LLM...")
        llm = MockRibit20LLM()
        logger.info("✅ LLM initialized")

    except Exception as e:
        logger.warning(f"Could not initialize LLM: {e}")
        llm = None

    print()
    logger.info("Initializing Matrix Bot...")
    matrix_bot = RibitMatrixBot(
        homeserver=os.getenv("MATRIX_HOMESERVER"),
        username=os.getenv("MATRIX_USERNAME"),
        password=os.getenv("MATRIX_PASSWORD"),
    )
    logger.info("✅ Matrix Bot initialized")

    print()
    logger.info("Initializing DeltaChat Bot...")
    deltachat_config = DeltaChatBotConfig(
        email=os.getenv("DELTACHAT_EMAIL"),
        password=os.getenv("DELTACHAT_PASSWORD"),
        smtp_server=os.getenv("DELTACHAT_SMTP", ""),
        imap_server=os.getenv("DELTACHAT_IMAP", ""),
    )

    deltachat_bot = DeltaChatRibotBot(deltachat_config, llm=llm, enable_bridge=True)
    logger.info("✅ DeltaChat Bot initialized")

    print()
    logger.info("Initializing Bridge...")
    bridge = DeltaChatMatrixBridge(
        matrix_bot=matrix_bot,
        deltachat_bot=deltachat_bot,
        supabase_client=supabase_client,
    )
    logger.info("✅ Bridge initialized")

    print()
    print("=" * 70)
    print("🚀 Starting Bridge...")
    print("=" * 70)
    print()

    try:
        await bridge.start()

    except KeyboardInterrupt:
        print()
        print()
        logger.info("🛑 Bridge interrupted by user")

    except Exception as e:
        logger.error(f"❌ Bridge error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)

    finally:
        logger.info("Performing cleanup...")
        await bridge.shutdown()
        logger.info("✅ Cleanup complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Bridge stopped")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
