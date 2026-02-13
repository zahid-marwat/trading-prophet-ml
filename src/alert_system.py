"""Alert system placeholders."""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def send_email_alert(subject: str, message: str) -> None:
    logger.info("Email alert placeholder: %s", subject)


def send_telegram_alert(message: str) -> None:
    logger.info("Telegram alert placeholder")


def send_sms_alert(message: str) -> None:
    logger.info("SMS alert placeholder")


def send_desktop_notification(message: str) -> None:
    logger.info("Desktop notification placeholder")
