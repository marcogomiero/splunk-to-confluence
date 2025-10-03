#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Splunk → Confluence Alert Action
--------------------------------
Questo script viene eseguito da Splunk quando scatta un alert che utilizza
la custom alert action "Send to Confluence".

- Legge i parametri configurati in alert_actions.conf
- Prende i risultati della ricerca Splunk (stdin in JSON)
- Costruisce una tabella HTML
- Inserisce la tabella e un timestamp in un template HTML esterno
- Aggiorna la pagina Confluence con il contenuto
"""

import sys
import os
import json
import urllib.request
import urllib.error
import base64
from datetime import datetime


def http_request(url, method="GET", data=None, auth_user=None, auth_token=None, headers=None):
    """Wrapper HTTP usando urllib con basic auth e supporto JSON."""
    if headers is None:
        headers = {}

    if auth_user and auth_token:
        auth_str = f"{auth_user}:{auth_token}"
        b64_auth = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
        headers["Authorization"] = f"Basic {b64_auth}"

    if data is not None and isinstance(data, (dict, list)):
        data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
            if resp.headers.get("Content-Type", "").startswith("application/json"):
                return json.loads(content.decode("utf-8"))
            return content.decode("utf-8")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"HTTP {e.code} error for {url}: {err_body}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"Connection error for {url}: {e}")


def update_page(base_url, page_id, space_key, page_title, auth_user, auth_token, content_html):
    """Aggiorna una pagina Confluence sostituendo completamente il contenuto."""
    version_url = f"{base_url}/rest/api/content/{page_id}?expand=version"
    version_data = http_request(version_url, auth_user=auth_user, auth_token=auth_token)
    current_version = version_data["version"]["number"]
    new_version = current_version + 1

    payload = {
        "id": page_id,
        "type": "page",
        "title": page_title,
        "space": {"key": space_key},
        "body": {
            "storage": {
                "value": content_html,
                "representation": "storage"
            }
        },
        "version": {"number": new_version}
    }

    update_url = f"{base_url}/rest/api/content/{page_id}"
    http_request(update_url, method="PUT", data=payload, auth_user=auth_user, auth_token=auth_token)
    print(f"✓ Pagina aggiornata con successo! Versione {new_version}")


def create_html_table(results):
    """Crea una tabella HTML dai risultati Splunk, con formattazione Confluence-friendly."""
    if not results:
        return "<p><em>Nessun risultato</em></p>"

    headers = results[0].keys()
    header_html = "".join([f"<th>{h}</th>" for h in headers])

    rows_html = ""
    for i, r in enumerate(results, 1):
        bg = "#f4f5f7" if i % 2 == 0 else "white"
        cells = "".join([f"<td>{r.get(h, '')}</td>" for h in headers])
        rows_html += f"<tr style='background-color:{bg}'>{cells}</tr>"

    return f"""
    <table data-layout="wide" style="border-collapse:collapse;width:100%">
      <thead>
        <tr style="background-color:#0052cc;color:white;">{header_html}</tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    """


def load_template(timestamp, table_html):
    """Carica il template HTML esterno e sostituisce i segnaposti."""
    template_path = os.path.join(os.path.dirname(__file__), "../templates/confluence_template.html")
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        return template.replace("{{TIMESTAMP}}", timestamp).replace("{{TABLE_HTML}}", table_html)
    except FileNotFoundError:
        # fallback: inline template minimale
        return f"""
        <h1 style="color:#0052cc;">🚀 Risultati Alert Splunk</h1>
        <p><strong>📅 Ultimo aggiornamento:</strong> {timestamp}</p>
        {table_html}
        """


def main():
    payload = sys.stdin.read()
    if not payload:
        print("No payload from Splunk", file=sys.stderr)
        return 1

    event = json.loads(payload)
    config = event.get("configuration", {})
    results = event.get("result", [])

    # Parametri Confluence
    BASE_URL   = config.get("BASE_URL")
    PAGE_ID    = config.get("PAGE_ID")
    SPACE_KEY  = config.get("SPACE_KEY")
    PAGE_TITLE = config.get("PAGE_TITLE")
    AUTH_USER  = config.get("AUTH_USER")
    AUTH_TOKEN = config.get("AUTH_TOKEN")

    if isinstance(results, dict):
        results = [results]

    table_html = create_html_table(results)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content_html = load_template(timestamp, table_html)
    update_page(BASE_URL, PAGE_ID, SPACE_KEY, PAGE_TITLE, AUTH_USER, AUTH_TOKEN, content_html)

    return 0


if __name__ == "__main__":
    sys.exit(main())
