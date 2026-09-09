"""Prevent downstream consumers from silently loading a failed refresh's leftovers."""
import json
from pathlib import Path


def require_successful_run(processed: Path) -> dict:
    try:
        run=json.loads((processed/'run.json').read_text())
    except (OSError,ValueError) as error:
        raise ValueError('A successful pipeline run is required before consuming processed data') from error
    if not isinstance(run,dict) or run.get('status')!='success':
        raise ValueError('A successful pipeline run is required before consuming processed data')
    return run
