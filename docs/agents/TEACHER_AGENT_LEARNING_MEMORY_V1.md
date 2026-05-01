# TEACHER_AGENT_LEARNING_MEMORY_V1

## Status
DESIGN_CANON_DRAFT_V1

## Purpose
Create a learning layer that turns every success, failure, operator correction, critic block, and marketplace result into reusable project knowledge.

The Teacher Agent does not execute live actions. It improves the rules, prompts, checks, examples, and regression tests used by the other agents.

## Position In ECOM OS V3
The Teacher Agent works with:
- control_agent
- archivist_agent
- runner_agent
- URL_INTAKE_AGENT
- PRODUCT_UNDERSTANDING_AGENT
- EVIDENCE_AGENT
- PHOTO_AGENT
- TITLE_AGENT
- ITEM_SPECIFICS_AGENT
- HTML_DESCRIPTION_AGENT
- MARKETPLACE_CRITIC_AGENT
- TELEGRAM_CONTROL_AGENT
- N8N_ORCHESTRATION_HANDOFF

It must respect the canonical route:
manifest -> rules -> state -> history -> control_agent -> archivist_agent -> runner_agent -> n8n_orchestration -> compact_core_migration

## Inputs
- operator feedback in Russian
- rejected photo packs
- approved photo packs
- critic reports
- blocked URL intake attempts
- successful URL intake attempts
- title options and chosen title
- item specifics corrections
- HTML corrections
- Telegram command logs
- eBay readonly verify results
- live update results after approval
- server cleanup audit results

## Outputs
- new rule suggestion
- corrected checklist
- prompt improvement
- regression test idea
- blocked pattern memory
- successful pattern memory
- next_allowed_action suggestion

## Learning Memory Types

### SUCCESS_PATTERN
Example:
Real product photos + order screenshot + source screenshot allowed the visual agent to correctly identify a 6-piece USB adapter set and create a useful photo pack.

### FAILURE_PATTERN
Example:
Filename-only image selection caused technical PASS but visual FAIL.

### BLOCKED_PATTERN
Example:
Alibaba/AliExpress short links may be inaccessible. Use screenshot fallback without hallucination.

### OPERATOR_PREFERENCE
Example:
For eBay Germany, photo text must be German only. English is reserved for future EU-wide mode.

### MARKETPLACE_RULE
Example:
Photo 1 and photo 2 should be clean, without overlay text. Secondary images may use German feature callouts only when truthful and policy-safe.

### REGRESSION_TEST
Example:
Before marking PHOTO_AGENT PASS, require visible 8-image contact sheet and human review.

## Teacher Agent Workflow

### 01_COLLECT_EVENT
Collect an event from any agent.

### 02_CLASSIFY_EVENT
Classify as:
- SUCCESS_PATTERN
- FAILURE_PATTERN
- BLOCKED_PATTERN
- OPERATOR_PREFERENCE
- MARKETPLACE_RULE
- REGRESSION_TEST
- SAFETY_RULE

### 03_EXTRACT_LESSON
Write one clear lesson:
- what happened
- why it happened
- what must change
- which agent needs the lesson

### 04_UPDATE_CANDIDATE_RULE
Create a candidate rule. Do not silently overwrite canon.

### 05_CRITIC_REVIEW
Marketplace Critic checks if the lesson is safe and not contradictory.

### 06_OPERATOR_CONFIRMATION_FOR_MAJOR_RULES
Major route changes require operator review.

### 07_ARCHIVE_LESSON
Archivist stores lesson and links it to artifacts.

### 08_APPLY_TO_AGENT_PROMPTS_OR_CHECKLISTS
Only after acceptance, update relevant agent docs/checklists.

## Hard Rules
- Teacher Agent cannot publish.
- Teacher Agent cannot delete.
- Teacher Agent cannot change server runtime by itself.
- Teacher Agent cannot replace operator approval.
- Teacher Agent must not learn from a fake PASS.
- Teacher Agent must preserve A -> B -> FINISH -> STOP discipline.

## Current Lessons To Register

### LESSON_001_PHOTO_TECHNICAL_PASS_NOT_ENOUGH
V3/V4/V5 photo routes passed technical checks but failed visually. Future photo PASS requires human-visible gallery and visual critic.

### LESSON_002_FILENAME_SELECTION_FORBIDDEN
Selecting photos by filename or dimensions is not enough. Visual understanding and marketplace suitability are required.

### LESSON_003_URL_INTAKE_NEEDS_FALLBACK
Short supplier URLs may fail. If URL fails, request minimal screenshots or real photos; do not hallucinate.

### LESSON_004_DE_ONLY_FOR_EBAY_GERMANY
For current eBay Germany listing mode, all listing text and infographic text must be German only.

### LESSON_005_MAIN_IMAGES_CLEAN
Photo 1 and Photo 2 should be clean product images with no overlay text. Feature callouts belong to secondary images.

### LESSON_006_VISIBLE_PROOF_REQUIRED
The operator needs to see actual output images and listing previews, not only JSON PASS.

### LESSON_007_SERVER_NOT_SANDBOX
Server is production/runtime only. Experiments happen in GitHub design or local sandbox.

## Output Format

```json
{
  "status": "LESSON_REGISTERED",
  "lesson_id": "LESSON_XXX",
  "type": "SUCCESS_PATTERN_OR_FAILURE_PATTERN",
  "target_agents": [],
  "rule_candidate": "",
  "evidence_artifacts": [],
  "critic_required": true,
  "operator_confirmation_required": false,
  "next_allowed_action": "ARCHIVE_OR_APPLY_LESSON"
}
```

## Next Allowed Action
Create `ECOM_OS_V3_PROJECT_AGENT_MAP_V1.md` to show all agents, status, gaps, and next implementation order.
