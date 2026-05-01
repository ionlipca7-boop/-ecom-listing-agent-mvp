# ECOM OS V3 Local Sandbox V1

## Status
EXECUTABLE_SANDBOX_DRAFT_V1

## Purpose
Run the new ECOM OS V3 listing pipeline locally on Windows before any server deployment.

This sandbox creates project artifacts only. It does not publish, revise, delete, upload to EPS, or call eBay live APIs.

## Included Files

- `run_local_sandbox_v1.bat`
- `local_sandbox_runner_v1.py`
- `agents/url_intake_agent_v1.py`
- `agents/product_passport_agent_v1.py`
- `agents/photo_blueprint_agent_v1.py`
- `agents/title_agent_v1.py`
- `agents/item_specifics_agent_v1.py`
- `agents/html_agent_v1.py`
- `agents/critic_agent_v1.py`
- `templates/ebay_description_template_v1.html`

## What It Produces

For each test product, the runner writes:

- source packet JSON
- product passport JSON
- evidence map JSON
- photo blueprint JSON
- title candidates JSON
- item specifics JSON
- HTML description file
- critic report JSON
- run summary JSON

## Output Folder

Default:

`storage/outputs/ecom_os_v3/local_sandbox/<RUN_ID>/`

## Current Limits

This package is deterministic/local only.
It does not yet call OpenAI image generation, Canva, Photoshop, Telegram, n8n, or eBay.

Those are later adapters after local artifact logic is verified.

## Safe Run Rule

No live action exists in this package.

If any future adapter adds live capability, it must require:
- explicit scope
- token guard
- readonly before-state
- Telegram approval
- critic PASS
- readonly after-state

## Windows Run

From project root:

```cmd
cd /d D:\ECOM_LISTING_AGENT_MVP
storage\tools\ecom_os_v3\run_local_sandbox_v1.bat
```

## Next Step After PASS

`ADD_IMAGE_GENERATION_ADAPTER_OR_CANVA_TEMPLATE_ADAPTER_V1`
