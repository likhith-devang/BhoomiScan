from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.constants import LEDGER_GENESIS_HASH
from app.models.report import FinalReport, LedgerRecord
from app.services.hashing import hash_payload


def _timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).strftime("%Y-%m-%dT%H:%M:%SZ")


def ledger_material(report_id, report_hash: str, previous_hash: str, timestamp: str) -> dict[str, Any]:
    return {
        "previous_hash": previous_hash,
        "report_hash": report_hash,
        "report_id": str(report_id),
        "timestamp": timestamp,
    }


def latest_record(db: Session, property_case_id=None) -> LedgerRecord | None:
    query = select(LedgerRecord).join(FinalReport)
    if property_case_id is not None:
        query = query.where(FinalReport.property_case_id == property_case_id)
    return db.scalar(query.order_by(FinalReport.version.desc()).limit(1))


def append_ledger(db: Session, report: FinalReport) -> LedgerRecord:
    previous = latest_record(db, report.property_case_id)
    previous_hash = previous.record_hash if previous else LEDGER_GENESIS_HASH
    timestamp = _timestamp()
    material = ledger_material(report.id, report.report_hash, previous_hash, timestamp)
    record = LedgerRecord(
        report_id=report.id,
        report_hash=report.report_hash,
        previous_hash=previous_hash,
        record_hash=hash_payload(material),
        hashed_at=timestamp,
    )
    db.add(record)
    db.flush()
    write_ledger_files(report, record)
    return record


def ledger_dir() -> Path:
    path = get_settings().STORAGE_DIR.parent / "ledger"
    path.mkdir(parents=True, exist_ok=True)
    return path


def ledger_entry(report: FinalReport, record: LedgerRecord) -> dict[str, Any]:
    return {
        "what_this_is": (
            "BhoomiScan local hash-chain record. Not Bitcoin or Ethereum. "
            "The same values are stored in PostgreSQL tables final_reports and ledger_records."
        ),
        "version": report.version,
        "risk_score": report.risk_score,
        "risk_level": report.risk_level,
        "report_id": str(report.id),
        "property_case_id": str(report.property_case_id),
        "report_hash_sha256": record.report_hash,
        "previous_hash": record.previous_hash,
        "record_hash": record.record_hash,
        "hashed_at": record.hashed_at,
    }


def write_ledger_files(report: FinalReport, record: LedgerRecord) -> Path:
    folder = ledger_dir()
    entry = ledger_entry(report, record)
    single = folder / f"report_v{report.version}.json"
    single.write_text(json.dumps(entry, indent=2), encoding="utf-8")

    chain_path = folder / "CHAIN.json"
    by_key: dict[str, dict[str, Any]] = {}
    if chain_path.exists():
        try:
            loaded = json.loads(chain_path.read_text(encoding="utf-8"))
            if isinstance(loaded, list):
                for item in loaded:
                    key = f"{item.get('property_case_id')}:{item.get('version')}"
                    by_key[key] = item
        except json.JSONDecodeError:
            pass
    by_key[f"{entry['property_case_id']}:{entry['version']}"] = entry
    chain = sorted(by_key.values(), key=lambda item: (str(item.get("property_case_id")), int(item.get("version") or 0)))
    chain_path.write_text(json.dumps(chain, indent=2), encoding="utf-8")
    return single


def verify_record(record: LedgerRecord) -> bool:
    material = ledger_material(record.report_id, record.report_hash, record.previous_hash, record.hashed_at)
    return record.record_hash == hash_payload(material)


def verify_chain(db: Session, record: LedgerRecord) -> bool:
    report = record.report or db.get(FinalReport, record.report_id)
    if report is None:
        return False
    previous = db.scalar(
        select(LedgerRecord)
        .join(FinalReport)
        .where(
            FinalReport.property_case_id == report.property_case_id,
            FinalReport.version < report.version,
        )
        .order_by(FinalReport.version.desc())
        .limit(1)
    )
    expected = previous.record_hash if previous else LEDGER_GENESIS_HASH
    return record.previous_hash == expected
