# funds/services/fund_importer.py
import csv
from decimal import Decimal, InvalidOperation
from datetime import datetime
from django.db import transaction
from funds.models import Fund
import logging

logger = logging.getLogger("funds")

def parse_decimal(value):
    try:
        value = value.strip().replace("$", "").replace(",", "")
        return Decimal(value) if value else None
    except (InvalidOperation, AttributeError):
        return None

def parse_date(value):
    value = value.strip()
    if not value:
        return None

    formats = [
        "%d/%m/%Y", 
        "%m/%d/%Y", 
        "%Y-%m-%d",  
        "%b. %d, %Y",  
        "%B %d, %Y",  
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    logger.warning(f"Unrecognized date format: '{value}'")
    return None

# Parses a CSV file and imports fund records.
# - Deduplicates by fund `name`
# - Updates existing funds with new strategy, AUM, and inception_date
# - Skips rows missing critical fields
@transaction.atomic
def import_funds_from_csv(file_obj):
    reader = csv.DictReader(file_obj)
    seen_names = set()
    created = 0
    updated = 0

    for i, row in enumerate(reader, start=1):
        try:
            # Clean and normalize strings
            name = row.get("Name", "").strip()
            strategy = row.get("Strategy", "").strip().title()
            aum = parse_decimal(row.get("AUM (USD)", "").strip())
            inception_date = parse_date(row.get("Inception Date", "").strip())

            if not name:
                logger.warning(f"Row {i} skipped — missing fund name: {row}")
                continue

            if name in seen_names:
                logger.debug(f"Row {i} skipped — duplicate fund name in same file: {name}")
                continue
            seen_names.add(name)

            fund, is_created = Fund.objects.update_or_create(
                name=name,
                defaults={
                    "strategy": strategy,
                    "aum": aum,
                    "inception_date": inception_date
                },
            )

            if is_created:
                created += 1
                logger.info(f"Created: {name}")
            else:
                updated += 1
                logger.info(f"Updated: {name}")

        except Exception as e:
            logger.exception(f"Row {i} failed to import: {row} — {e}")

    return created, updated