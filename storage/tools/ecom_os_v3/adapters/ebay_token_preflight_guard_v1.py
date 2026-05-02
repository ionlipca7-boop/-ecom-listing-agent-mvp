from __future__ import annotations

import base64
import json
import os
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class EbayTokenPreflightResult:
    status: str
    env_present: bool
    token_refreshed: bool
    expires_in: int | None
    http_status: int | None
    blocked_reasons: List[str]
    secret_scan_status: str
    next_allowed_action: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class EbayTokenPreflightGuardV1:
    """eBay OAuth token preflight guard.

    This guard may refresh an access token if env variables are present.
    It never publishes, revises, deletes, uploads EPS images, or changes listings.

    Required env:
    - EBAY_CLIENT_ID
    - EBAY_CLIENT_SECRET
    - EBAY_REFRESH_TOKEN

    Optional env:
    - EBAY_ENV=production|sandbox
    - EBAY_SCOPES
    """

    DEFAULT_SCOPES = "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory"

    def run(self, output_path: Path | None = None, do_refresh: bool = True) -> EbayTokenPreflightResult:
        client_id = os.environ.get("EBAY_CLIENT_ID")
        client_secret = os.environ.get("EBAY_CLIENT_SECRET")
        refresh_token = os.environ.get("EBAY_REFRESH_TOKEN")
        env = (os.environ.get("EBAY_ENV") or "production").lower()
        scopes = os.environ.get("EBAY_SCOPES") or self.DEFAULT_SCOPES

        missing = [k for k, v in {
            "EBAY_CLIENT_ID": client_id,
            "EBAY_CLIENT_SECRET": client_secret,
            "EBAY_REFRESH_TOKEN": refresh_token,
        }.items() if not v]

        if missing:
            result = EbayTokenPreflightResult(
                status="BLOCKED_EBAY_ENV_MISSING",
                env_present=False,
                token_refreshed=False,
                expires_in=None,
                http_status=None,
                blocked_reasons=[f"missing:{x}" for x in missing],
                secret_scan_status="NOT_RUN",
                next_allowed_action="SET_EBAY_ENV_IN_LOCAL_OR_SERVER_SECRETS",
            )
            self.write_result(output_path, result)
            return result

        if not do_refresh:
            result = EbayTokenPreflightResult(
                status="PASS_EBAY_ENV_PRESENT_REFRESH_NOT_RUN",
                env_present=True,
                token_refreshed=False,
                expires_in=None,
                http_status=None,
                blocked_reasons=[],
                secret_scan_status="NOT_RUN",
                next_allowed_action="RUN_REFRESH_PREFLIGHT_BEFORE_LIVE_GATE",
            )
            self.write_result(output_path, result)
            return result

        token_url = "https://api.ebay.com/identity/v1/oauth2/token" if env == "production" else "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
        basic = base64.b64encode(f"{client_id}:{client_secret}".encode("utf-8")).decode("ascii")
        body = urllib.parse.urlencode({
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "scope": scopes,
        }).encode("utf-8")
        req = urllib.request.Request(
            token_url,
            data=body,
            headers={
                "Authorization": f"Basic {basic}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                payload = json.loads(raw)
                expires_in = int(payload.get("expires_in") or 0)
                access_token = payload.get("access_token")
                token_refreshed = bool(access_token and expires_in > 0)
                status = "PASS_EBAY_TOKEN_REFRESHED" if token_refreshed else "BLOCKED_EBAY_TOKEN_REFRESH_NO_ACCESS_TOKEN"
                blocked = [] if token_refreshed else ["access_token_missing_in_response"]
                if output_path and access_token:
                    token_file = output_path.parent / "ebay_access_token_runtime_local.txt"
                    token_file.write_text(access_token, encoding="utf-8")
                result = EbayTokenPreflightResult(
                    status=status,
                    env_present=True,
                    token_refreshed=token_refreshed,
                    expires_in=expires_in,
                    http_status=resp.status,
                    blocked_reasons=blocked,
                    secret_scan_status="NOT_RUN",
                    next_allowed_action="MARKETPLACE_ACCESS_GATE" if token_refreshed else "FIX_EBAY_TOKEN_REFRESH",
                )
                self.write_result(output_path, result)
                return result
        except Exception as e:
            result = EbayTokenPreflightResult(
                status="BLOCKED_EBAY_TOKEN_REFRESH_ERROR",
                env_present=True,
                token_refreshed=False,
                expires_in=None,
                http_status=None,
                blocked_reasons=[type(e).__name__],
                secret_scan_status="NOT_RUN",
                next_allowed_action="FIX_EBAY_TOKEN_PREFLIGHT_ERROR",
            )
            self.write_result(output_path, result)
            return result

    def write_result(self, output_path: Path | None, result: EbayTokenPreflightResult) -> None:
        if output_path:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(json.dumps(result.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    import sys
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("ebay_token_preflight_result_v1.json")
    do_refresh = "--no-refresh" not in sys.argv
    result = EbayTokenPreflightGuardV1().run(output, do_refresh=do_refresh).to_dict()
    safe = dict(result)
    print(json.dumps(safe, ensure_ascii=False, indent=2))
    return 0 if str(result["status"]).startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
