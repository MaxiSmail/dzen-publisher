"""
VK Auto Publisher — entry point.

Usage:
    python main.py              # Start the recurring scheduler
    python main.py --run-once   # Run one publishing cycle and exit
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import signal
import sys

from config import get_settings, setup_logging
from database import init_db
from scheduler import run_pipeline, scheduler_loop

logger = logging.getLogger(__name__)

# Global event for graceful shutdown
_shutdown_event = asyncio.Event()


def _register_signals() -> None:
    """Register SIGINT / SIGTERM handlers for graceful shutdown."""
    loop = asyncio.get_running_loop()

    def _handle_signal(sig: int) -> None:
        name = signal.Signals(sig).name
        logger.info("Received %s — initiating graceful shutdown", name)
        _shutdown_event.set()

    for sig in (signal.SIGINT, signal.SIGTERM):
        try:
            loop.add_signal_handler(sig, _handle_signal, sig)
        except NotImplementedError:
            # Windows doesn't support add_signal_handler for all signals
            pass


async def _run_service() -> None:
    """Main async entrypoint: init DB and start the scheduler loop."""
    _register_signals()
    await init_db()
    logger.info("Service started. Press Ctrl+C to stop.")

    scheduler_task = asyncio.create_task(scheduler_loop())

    # Wait until shutdown is requested or the scheduler crashes
    done, _ = await asyncio.wait(
        [scheduler_task, asyncio.create_task(_shutdown_event.wait())],
        return_when=asyncio.FIRST_COMPLETED,
    )

    # Cancel whatever is still running
    scheduler_task.cancel()
    try:
        await scheduler_task
    except asyncio.CancelledError:
        pass

    logger.info("Service stopped gracefully.")


async def _run_once() -> None:
    """Run a single pipeline cycle (for testing)."""
    await init_db()
    logger.info("Running single pipeline cycle...")
    await run_pipeline()
    logger.info("Single cycle completed.")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="VK Auto Publisher — automated fact card generator",
    )
    parser.add_argument(
        "--run-once",
        action="store_true",
        help="Run one publishing cycle and exit (for testing).",
    )
    args = parser.parse_args()

    settings = get_settings()
    setup_logging(settings.log_level)

    logger.info("VK Auto Publisher v1.0")
    logger.info("VK Group ID: %d", settings.vk_group_id)
    logger.info("LLM Model: %s", settings.llm_model)
    logger.info("Image Model: %s", settings.image_model)
    logger.info("Post interval: %d hours", settings.post_interval_hours)
    logger.info("Card size: %dx%d", settings.card_width, settings.card_height)

    try:
        if args.run_once:
            asyncio.run(_run_once())
        else:
            asyncio.run(_run_service())
    except KeyboardInterrupt:
        logger.info("Interrupted by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
