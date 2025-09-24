"""
Jerasoft rates exporter (functions-only)

Usage (example):
    export_rates_by_query(
        target_query="Quickcom tel PRM trunk Prefix:1001 USD",
        output_path="quickcom_rates.xlsx",
    )

The entrypoint `export_rates_by_query()`:
- Finds the best-matching TERM* rate table for `target_query`.
- Fetches active current & future rates from that table.
- Saves a tidy Excel file at `output_path`.
- Returns a small result dict with table_id, score, and counts.

Configuration:
- API URL & KEY are read from env by default: JERA_SOFT_API_KEY, JERASOFT_API_URL
- You can also pass `api_url` / `api_key` explicitly to any function.
"""

from __future__ import annotations
import os
import re
import json
from pathlib import Path
from datetime import datetime
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Optional
import pandas as pd
import requests
from dotenv import load_dotenv
from json import JSONDecodeError

load_dotenv()

# -------------------------------------------------------------------
# Defaults / Env
# -------------------------------------------------------------------
DEFAULT_API_URL = os.getenv("JERASOFT_API_URL", "http://billing.voipsystem.org:3080")
DEFAULT_API_KEY = os.getenv("JERA_SOFT_API_KEY")
DEFAULT_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# _session = requests.Session()

# --- robust session with retries for transient upstream issues ---
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_session = requests.Session()
_retry = Retry(
    total=4,
    backoff_factor=0.4,
    status_forcelist=[502, 503, 504],
    allowed_methods=["POST"],
)
_session.mount("http://", HTTPAdapter(max_retries=_retry))
_session.mount("https://", HTTPAdapter(max_retries=_retry))

#__________________________Enforce prefix_____________________________
# --- prefix utilities (add near your string utils) ---
_prefix_in_name_pat = re.compile(r'(?:prefix|prfx)[:\s-]*(\d+)\b', re.I)

def normalize_prefix(prefix) -> Optional[str]:
    if prefix is None:
        return None
    try:
        return str(int(str(prefix).strip()))
    except Exception:
        return None

def table_prefix_from_name(name: str) -> Optional[str]:
    """Extract numeric prefix from a table name like '... PREFIX:33' or 'PRFX-33'."""
    m = _prefix_in_name_pat.search(name or "")
    return str(int(m.group(1))) if m else None

def table_has_prefix(name: str, prefix_code: str) -> bool:
    """True if table name contains the exact prefix number."""
    tp = table_prefix_from_name(name)
    return tp == normalize_prefix(prefix_code)

#_____________________________________________________________________________________

# -------------------------------------------------------------------
# String utils
# -------------------------------------------------------------------
_norm_space = re.compile(r"\s+")
_norm_hashes = re.compile(r"[#]+")

def normalize(s: str) -> str:
    s = s or ""
    s = s.lower().strip()
    s = _norm_hashes.sub("", s)
    s = s.replace(".", " ")
    s = _norm_space.sub(" ", s)
    return s.strip()

def fuzzy_score(a: str, b: str) -> float:
    """Blend of SequenceMatcher and Jaccard, in [0,1]."""
    a_n, b_n = normalize(a), normalize(b)
    base = SequenceMatcher(None, a_n, b_n).ratio()
    a_tokens, b_tokens = set(a_n.split()), set(b_n.split())
    jacc = (len(a_tokens & b_tokens) / len(a_tokens | b_tokens)) if (a_tokens and b_tokens) else 0.0
    return 0.85 * base + 0.15 * jacc

def name_starts_with_term(name: str) -> bool:
    return str(name).lstrip().upper().startswith("TERM")

def name_contains_company(name: str, company_kw: str) -> bool:
    return company_kw in normalize(name)

def extract_company_keyword(query: str) -> str:
    """Derive company keyword from the first token (alnum, ., _, -)."""
    m = re.search(r"[A-Za-z0-9._-]+", query or "")
    return (m.group(0).lower() if m else "").strip()

# def _post_json(api_url: str, payload: Dict, timeout: int = 500) -> Dict:
#     resp = _session.post(api_url, headers=DEFAULT_HEADERS, json=payload, timeout=timeout)
#     resp.raise_for_status()
#     ctype = resp.headers.get("Content-Type", "")
#     try:
#         return resp.json()
#     except JSONDecodeError as e:
#         head = resp.text[:1000]
#         tail = resp.text[-500:] if len(resp.text) > 1500 else ""
#         raise RuntimeError(
#             f"JSON decode failed at pos {e.pos}: {e.msg}. "
#             f"status={resp.status_code} content_type={ctype}. "
#             f"body_start={head!r} body_end={tail!r}"
#         )

def _post_json(api_url: str, payload: Dict, timeout: int = 500) -> Dict:
    resp = _session.post(api_url, headers=DEFAULT_HEADERS, json=payload, timeout=timeout)
    resp.raise_for_status()
    ctype = resp.headers.get("Content-Type", "")
    try:
        return resp.json()
    except JSONDecodeError as e:
        body = resp.text or ""
        clen = resp.headers.get("Content-Length")
        raise RuntimeError(
            f"JSON decode failed at pos {e.pos}: {e.msg}. "
            f"status={resp.status_code} content_type={ctype} content_length={clen} "
            f"body_len={len(body)} body_start={body[:1000]!r} body_end={body[-500:]!r}"
        )


def fetch_all_tables(api_url: Optional[str] = None, api_key: Optional[str] = None, page_size: int = 500) -> List[Dict]:
    """Fetch all rate tables via pagination."""
    api_url = api_url or DEFAULT_API_URL
    api_key = api_key or DEFAULT_API_KEY
    if not api_key:
        raise ValueError("Missing API key (env JERA_SOFT_API_KEY or pass api_key).")

    all_tables: List[Dict] = []
    offset = 0
    while True:
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "rates.tables.search",
            "params": {"AUTH": api_key, "limit": page_size, "offset": offset},
        }
        data = _post_json(api_url, payload)
        if "result" not in data:
            raise RuntimeError(f"API error: {data.get('error')}")
        page = data["result"]
        if not page:
            break
        all_tables.extend(page)
        offset += page_size
    return all_tables

def find_best_term_table(
    target_query: str,
    subject: str,
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
    top_k: int = 5,
    prefix_code: Optional[str] = None,   # <--- NEW
) -> Tuple[int, Dict, List[Tuple[float, Dict]]]:

    if not target_query:
        raise ValueError("target_query must be non-empty")

    company_kw = extract_company_keyword(target_query)
    if not company_kw:
        raise ValueError("Could not extract a company keyword from target_query.")

    tables = fetch_all_tables(api_url=api_url, api_key=api_key)
    candidates = [
        t for t in tables
        if name_starts_with_term(t.get("name", "")) and name_contains_company(t.get("name", ""), company_kw)
    ]
    if not candidates:
        return f"No TERM* tables found containing company '{company_kw}'.", "", ""

    # Enforce explicit prefix if provided
    norm_pref = normalize_prefix(prefix_code)
    if norm_pref:
        exact_prefix = [t for t in candidates if table_has_prefix(t.get("name", ""), norm_pref)]
        if not exact_prefix:
            return (f"No TERM* tables found for company '{company_kw}' with PREFIX:{norm_pref}.",
                    "", "")
        candidates = exact_prefix

    # Score, with small tie-break boost for explicit prefix match (in case of duplicates)
    scored: List[Tuple[float, Dict]] = []
    for t in candidates:
        name = t.get("name", "")
        score = fuzzy_score(name, subject)
        if norm_pref:
            tp = table_prefix_from_name(name)
            if tp == norm_pref:
                score += 0.25  # gentle nudge for deterministic ordering
        scored.append((score, t))

    scored.sort(key=lambda x: x[0], reverse=True)
    best_score, best_table = scored[0]
    best_id = best_table.get("id")
    if best_id is None:
        raise KeyError("Best table did not include an 'id' field")

    return int(best_id), best_table, scored[:top_k]


# def fetch_active_current_future_rates(
#     table_id: int,
#     api_url: Optional[str] = None,
#     api_key: Optional[str] = None,
#     when_utc: Optional[datetime] = None,
#     page_limit: int = 5000,  # server may cap this; we’ll still paginate safely
# ) -> pd.DataFrame:
#     """
#     Fetch active current & future rates into a tidy DataFrame.
#     - Uses stable server-side ordering for consistent pagination.
#     - V1-style pagination: increment by len(result); stop only on empty page.
#     """
#     api_url = api_url or DEFAULT_API_URL
#     api_key = api_key or DEFAULT_API_KEY
#     if not api_key:
#         raise ValueError("Missing API key (env JERA_SOFT_API_KEY or pass api_key).")

#     when_utc = when_utc or datetime.utcnow()

#     offset = 0
#     all_records: List[Dict] = []

#     base_params = {
#         "AUTH": api_key,
#         "rate_tables_id": table_id,
#         "state": "current_future",
#         "status": "active",
#         "__tz": "UTC",
#         "dt": when_utc.strftime("%Y-%m-%d %H:%M:%S"),
#         "limit": page_limit,
#         "order": ["+code", "-effective_from"],  # stable ordering for paging parity
#     }

#     while True:
#         params = dict(base_params, offset=offset)

#         payload = {
#             "jsonrpc": "2.0",
#             "id": 1,
#             "method": "rates.search",
#             "params": params,
#         }

#         data = _post_json(api_url, payload)
#         result = data.get("result")
#         if not isinstance(result, list):
#             raise RuntimeError(f"Unexpected response or error: {str(data)[:400]}")

#         if not result:
#             break

#         all_records.extend(result)
#         # V1-style: move offset by what we actually got; don't assume server honors 'limit'
#         offset += len(result)

#     if not all_records:
#         return pd.DataFrame(columns=[
#             "Dst Code", "Dst Code Name", "Rate", "Effective Date", "Billing Increment"
#         ])

#     df = pd.DataFrame(all_records)

#     # Billing Increment (robust to missing)
#     min_vol = df.get("min_volume")
#     pay_int = df.get("pay_interval")
#     min_vol_str = min_vol.where(min_vol.notna(), "").astype(str) if min_vol is not None else ""
#     pay_int_str = pay_int.where(pay_int.notna(), "").astype(str) if pay_int is not None else ""
#     df["Billing Increment"] = (
#         (min_vol_str if isinstance(min_vol_str, pd.Series) else "") + "/" +
#         (pay_int_str if isinstance(pay_int_str, pd.Series) else "")
#     ).str.strip("/")

#     keep = ["code", "code_name", "value", "effective_from", "Billing Increment"]
#     keep_existing = [c for c in keep if c in df.columns]
#     df_selected = df[keep_existing].rename(columns={
#         "code": "Dst Code",
#         "code_name": "Dst Code Name",
#         "value": "Rate",
#         "effective_from": "Effective Date",
#     })

#     return df_selected.reset_index(drop=True)

def fetch_active_current_future_rates(
    table_id: int,
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
    when_utc: Optional[datetime] = None,
    page_limit: int = 500,  # start conservative; adaptive logic will adjust
) -> pd.DataFrame:
    """
    Fetch active current & future rates with adaptive pagination.
    If the server returns truncated JSON with HTTP 200, we retry the same page,
    and if needed, halve the page size until it parses.
    """
    api_url = api_url or DEFAULT_API_URL
    api_key = api_key or DEFAULT_API_KEY
    if not api_key:
        raise ValueError("Missing API key (env JERA_SOFT_API_KEY or pass api_key).")

    when_utc = when_utc or datetime.utcnow()

    offset = 0
    all_records: List[Dict] = []

    # never go below this; below 100 is just suffering
    MIN_LIMIT = 100
    current_limit = max(MIN_LIMIT, int(page_limit))

    base_params = {
        "AUTH": api_key,
        "rate_tables_id": table_id,
        "state": "current_future",
        "status": "active",
        "__tz": "UTC",
        "dt": when_utc.strftime("%Y-%m-%d %H:%M:%S"),
        "order": ["+code", "-effective_from"],
    }

    while True:
        params = dict(base_params, limit=current_limit, offset=offset)
        payload = {"jsonrpc": "2.0", "id": 1, "method": "rates.search", "params": params}

        # retry decode at this offset/limit before shrinking
        attempts = 0
        while True:
            attempts += 1
            try:
                data = _post_json(api_url, payload, timeout=500)
                break  # parsed ok
            except RuntimeError as e:
                # Our _post_json wraps JSONDecodeError in RuntimeError with a clear message
                if "JSON decode failed" in str(e):
                    if attempts < 2:
                        # try once more at the same limit, could be a hiccup
                        continue
                    if current_limit > MIN_LIMIT:
                        # shrink page and retry same offset
                        current_limit = max(MIN_LIMIT, current_limit // 2)
                        attempts = 0
                        continue
                # not a truncation case or can't shrink further — bubble up
                raise

        result = data.get("result")
        if not isinstance(result, list):
            raise RuntimeError(f"Unexpected response or error: {str(data)[:400]}")

        if not result:
            break  # all done

        all_records.extend(result)
        offset += len(result)
        # keep current_limit as adapted; if the server handled it, we keep using it

    if not all_records:
        return pd.DataFrame(columns=[
            "Dst Code", "Dst Code Name", "Rate", "Effective Date", "Billing Increment"
        ])

    df = pd.DataFrame(all_records)

    min_vol = df.get("min_volume")
    pay_int = df.get("pay_interval")
    min_vol_str = min_vol.where(min_vol.notna(), "").astype(str) if min_vol is not None else ""
    pay_int_str = pay_int.where(pay_int.notna(), "").astype(str) if pay_int is not None else ""
    df["Billing Increment"] = (
        (min_vol_str if isinstance(min_vol_str, pd.Series) else "") + "/" +
        (pay_int_str if isinstance(pay_int_str, pd.Series) else "")
    ).str.strip("/")

    keep = ["code", "code_name", "value", "effective_from", "Billing Increment"]
    keep_existing = [c for c in keep if c in df.columns]
    df_selected = df[keep_existing].rename(columns={
        "code": "Dst Code",
        "code_name": "Dst Code Name",
        "value": "Rate",
        "effective_from": "Effective Date",
    })

    return df_selected.reset_index(drop=True)


def save_rates_to_excel(df: pd.DataFrame, output_path: str) -> str:
    """Save DataFrame to Excel, ensuring parent folder exists. Returns absolute path."""
    if not output_path:
        raise ValueError("output_path must be provided")

    out_path = Path(output_path).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Let pandas pick a writer engine that's available (xlsxwriter/openpyxl)
    df.to_excel(out_path, index=False)
    return str(out_path)

def export_rates_by_query(
    target_query: str,
    output_path: str,
    subject: str,
    prefix_code: Optional[str] = None,
    *,
    api_url: Optional[str] = None,
    api_key: Optional[str] = None,
    return_debug: bool = True,
) -> Dict:
    """
    High-level convenience function.

    1) Find best TERM* table for `target_query`.
    2) Fetch active current & future rates for that table.
    3) Save to `output_path`.

    Returns a dict with summary info.
    """
    table_id, best_table, top_scored = find_best_term_table(
        target_query=target_query, api_url=api_url, api_key=api_key, subject=subject, prefix_code=prefix_code
    )

    if best_table == "" and top_scored == "":
        return table_id # error message from find_best_term_table

    df = fetch_active_current_future_rates(
        table_id=table_id, api_url=api_url, api_key=api_key
    )

    saved_to = save_rates_to_excel(df, output_path)

    result = {
        "table_id": table_id,
        "rows": int(df.shape[0]),
        "saved_to": saved_to,
    }

    if return_debug:
        result.update({
            "best_table_name": best_table.get("name"),
            "top_candidates": [
                {"score": round(score, 3), "id": t.get("id"), "name": t.get("name")}
                for score, t in top_scored
            ],
        })

    return result

if __name__ == "__main__":
    # Example quick-start (reads API key from env):
    info = export_rates_by_query(
        subject="Quickcom tel com PRM trunk Prefix:001 USD",
        target_query="Quickcom tel com PRM trunk Prefix:001 USD",
        output_path="quickcom_rates.xlsx",
    )
    print(json.dumps(info, indent=2))
