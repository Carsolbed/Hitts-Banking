"""Logging estructurado (JSON) con correlación por run_id / request_id.

Los logs van a Azure Monitor. Nunca se registran datos personales en claro.
"""

from __future__ import annotations

import logging
import sys

import structlog

PII_FIELDS = {"documento", "nombre", "telefono", "email", "direccion"}


def _mask_pii(_, __, event_dict: dict) -> dict:
    for field in PII_FIELDS & event_dict.keys():
        event_dict[field] = "***"
    return event_dict


def get_logger(name: str) -> structlog.BoundLogger:
    logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(message)s")
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            _mask_pii,
            structlog.processors.JSONRenderer(),
        ]
    )
    return structlog.get_logger(name)
