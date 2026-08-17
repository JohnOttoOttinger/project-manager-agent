"""Google Analytics 4 + Search Console client — stdlib and `cryptography` only.

The machine has no google-auth / googleapiclient, so this signs its own RS256
JWT assertion and exchanges it for an access token. Read-only scopes.

Credentials come from the environment, never from this file:
    GOOGLE_APPLICATION_CREDENTIALS  path to the service-account JSON
    GA4_ODDTOE_PROPERTY_ID          numeric GA4 property id
    GSC_ODDTOE_SITE_URL             Search Console property URL

The private key is loaded to sign and is never logged or printed.
"""

from __future__ import annotations

import base64
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

SCOPES = (
    "https://www.googleapis.com/auth/analytics.readonly "
    "https://www.googleapis.com/auth/webmasters.readonly"
)

REPO_ROOT = Path(__file__).resolve().parents[3]


class ConfigError(RuntimeError):
    """Raised when credentials or ids are missing, with a fix in the message."""


def _load_dotenv() -> None:
    """Populate os.environ from the repo .env for anything not already set."""
    env_path = REPO_ROOT / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip())


def config() -> dict:
    _load_dotenv()
    key_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
    prop = os.environ.get("GA4_ODDTOE_PROPERTY_ID", "")
    site = os.environ.get("GSC_ODDTOE_SITE_URL", "")
    missing = [
        name
        for name, value in (
            ("GOOGLE_APPLICATION_CREDENTIALS", key_path),
            ("GA4_ODDTOE_PROPERTY_ID", prop),
            ("GSC_ODDTOE_SITE_URL", site),
        )
        if not value
    ]
    if missing:
        raise ConfigError(
            "Missing in .env: " + ", ".join(missing) + ". "
            "See skills/analytics/SKILL.md for what each one is."
        )
    if not Path(key_path).expanduser().exists():
        raise ConfigError(
            f"Service-account key not found at {key_path}. "
            "Check GOOGLE_APPLICATION_CREDENTIALS in .env."
        )
    return {"key_path": str(Path(key_path).expanduser()), "property_id": prop, "site_url": site}


def _b64(raw: bytes) -> bytes:
    return base64.urlsafe_b64encode(raw).rstrip(b"=")


_token_cache: dict = {}


def get_token() -> str:
    """Return a bearer token, reusing it until five minutes before expiry."""
    now = int(time.time())
    if _token_cache.get("expires_at", 0) > now + 300:
        return _token_cache["token"]

    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding

    with open(config()["key_path"]) as fh:
        sa = json.load(fh)

    header = {"alg": "RS256", "typ": "JWT", "kid": sa["private_key_id"]}
    claims = {
        "iss": sa["client_email"],
        "scope": SCOPES,
        "aud": sa["token_uri"],
        "iat": now,
        "exp": now + 3600,
    }
    signing_input = _b64(json.dumps(header).encode()) + b"." + _b64(json.dumps(claims).encode())

    key = serialization.load_pem_private_key(sa["private_key"].encode(), password=None)
    signature = key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    assertion = (signing_input + b"." + _b64(signature)).decode()

    body = urllib.parse.urlencode(
        {
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": assertion,
        }
    ).encode()
    request = urllib.request.Request(
        sa["token_uri"],
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        raise ConfigError(
            "Token exchange rejected by Google "
            f"({exc.code}). The key may have been revoked, or the clock is skewed. "
            f"Detail: {exc.read().decode()[:300]}"
        ) from exc

    _token_cache["token"] = payload["access_token"]
    _token_cache["expires_at"] = now + int(payload.get("expires_in", 3600))
    return _token_cache["token"]


def _call(url: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {get_token()}",
            "Content-Type": "application/json",
        },
        method="POST" if data else "GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=90) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode()[:400]
        if exc.code == 403:
            raise ConfigError(
                "Google returned 403. The service account is probably missing access: "
                "GA4 needs it as a Viewer under Property access management, "
                "Search Console under Settings -> Users and permissions. "
                f"Detail: {detail}"
            ) from exc
        raise ConfigError(f"Google API error {exc.code}: {detail}") from exc


# --- GA4 -------------------------------------------------------------------

def ga4_report(
    metrics: list[str],
    dimensions: list[str] | None = None,
    start: str = "28daysAgo",
    end: str = "yesterday",
    limit: int = 25,
    order_by_metric: str | None = None,
) -> list[dict]:
    """Run a GA4 report and return rows as flat dicts."""
    body: dict = {
        "dateRanges": [{"startDate": start, "endDate": end}],
        "metrics": [{"name": m} for m in metrics],
        "limit": limit,
    }
    if dimensions:
        body["dimensions"] = [{"name": d} for d in dimensions]
    if order_by_metric:
        body["orderBys"] = [{"metric": {"metricName": order_by_metric}, "desc": True}]

    url = (
        "https://analyticsdata.googleapis.com/v1beta/properties/"
        f"{config()['property_id']}:runReport"
    )
    response = _call(url, body)

    rows = []
    for row in response.get("rows", []):
        record: dict = {}
        for header, value in zip(response.get("dimensionHeaders", []), row.get("dimensionValues", [])):
            record[header["name"]] = value["value"]
        for header, value in zip(response.get("metricHeaders", []), row.get("metricValues", [])):
            raw = value["value"]
            record[header["name"]] = float(raw) if "." in raw else int(raw)
        rows.append(record)
    return rows


# --- Search Console --------------------------------------------------------

def gsc_query(
    dimensions: list[str],
    start: str,
    end: str,
    contains: str | None = None,
    page_equals: str | None = None,
    limit: int = 50,
) -> list[dict]:
    """Query Search Console analytics and return rows as flat dicts."""
    body: dict = {
        "startDate": start,
        "endDate": end,
        "dimensions": dimensions,
        "rowLimit": limit,
    }
    filters = []
    if contains:
        filters.append({"dimension": "query", "operator": "contains", "expression": contains})
    if page_equals:
        filters.append({"dimension": "page", "operator": "equals", "expression": page_equals})
    if filters:
        body["dimensionFilterGroups"] = [{"filters": filters}]

    site = urllib.parse.quote(config()["site_url"], safe="")
    url = f"https://searchconsole.googleapis.com/webmasters/v3/sites/{site}/searchAnalytics/query"
    response = _call(url, body)

    rows = []
    for row in response.get("rows", []):
        record = dict(zip(dimensions, row["keys"]))
        record["clicks"] = int(row["clicks"])
        record["impressions"] = int(row["impressions"])
        record["ctr"] = round(row["ctr"] * 100, 2)
        record["position"] = round(row["position"], 1)
        rows.append(record)
    return rows


def gsc_inspect(page_url: str) -> dict:
    """Ask Search Console how it currently sees one URL."""
    url = "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect"
    response = _call(url, {"inspectionUrl": page_url, "siteUrl": config()["site_url"]})
    result = response.get("inspectionResult", {}).get("indexStatusResult", {})
    return {
        "url": page_url,
        "verdict": result.get("verdict", "UNKNOWN"),
        "coverage": result.get("coverageState", "unknown"),
        "last_crawl": (result.get("lastCrawlTime") or "never")[:10],
        "indexing_allowed": result.get("indexingState", "unknown"),
        "canonical": result.get("googleCanonical", ""),
    }
