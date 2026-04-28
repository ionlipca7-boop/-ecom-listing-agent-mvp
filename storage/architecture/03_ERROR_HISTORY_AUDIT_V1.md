# ERROR HISTORY AUDIT V1

## Confirmed recurring issues

1. Pointer / state confusion
- Not always reading CURRENT_POINTER before action
- Caused wrong step execution

2. Local vs Server mismatch
- Commands executed in wrong environment
- Result: missing files, wrong runtime path

3. Publish audit mismatch
- GitHub JSON shows http_status 200
- eBay real active listings did not change
- Conclusion: audit != real visibility

4. 504 / retry confusion
- Edge errors interpreted as system failure
- Later success not properly verified against real eBay state

5. Large output / chat overflow
- findstr outputs too large to process
- Broke workflow

6. Token / execution mismatch (historical)
- Token fixed, but execution path mismatch still possible

## Root cause summary
- No strict module boundaries
- No single brain enforcement in practice
- Mixing read-only and live actions
- Lack of verification layer after publish

## Required fixes (not applied yet)
- enforce brain-only orchestration
- add verification layer after publish
- separate modules logically
- enforce environment clarity
