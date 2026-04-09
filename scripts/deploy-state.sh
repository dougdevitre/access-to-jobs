#!/usr/bin/env bash
# deploy-state.sh — Access to Jobs state deployment helper
# Usage: ./scripts/deploy-state.sh <state-abbreviation> <state-name>
# Example: ./scripts/deploy-state.sh il Illinois

set -euo pipefail

STATE_ABBR="${1:-}"
STATE_NAME="${2:-}"

if [[ -z "$STATE_ABBR" || -z "$STATE_NAME" ]]; then
  echo "Usage: ./scripts/deploy-state.sh <state-abbreviation> <state-name>"
  echo "Example: ./scripts/deploy-state.sh il Illinois"
  exit 1
fi

STATE_ABBR_LOWER=$(echo "$STATE_ABBR" | tr '[:upper:]' '[:lower:]')
STATE_DIR="states/${STATE_ABBR_LOWER}"

echo "=== Access to Jobs — State Deployment ==="
echo "State: ${STATE_NAME} (${STATE_ABBR_LOWER})"
echo "Output: ${STATE_DIR}/"
echo ""

# Create state directory
mkdir -p "${STATE_DIR}/references"

# Copy files that need full rewrite (with placeholder headers)
cat > "${STATE_DIR}/references/state-programs.md" << EOF
# ${STATE_NAME} WIOA Programs Reference
## Access to Jobs — Module 0 — Educational Information Only
### Source: ${STATE_NAME} WIOA Combined State Plan, PY 20XX-20XX

> ⚠️ This is educational information. Do not make eligibility determinations.
> Always direct users to a ${STATE_NAME} American Job Center for official enrollment.

---

## TODO: Replace this file with ${STATE_NAME}-specific WIOA program data.
## Use the Missouri file (references/state-programs.md) as a template.
## Required sections:
## - Core WIOA Programs (Title I: Adult, Dislocated Worker, Youth)
## - Adult Education and Literacy (Title II)
## - Vocational Rehabilitation (Title IV)
## - SNAP Employment & Training (state brand name)
## - TANF work program (state brand name)
## - Veterans services
## - Trade Adjustment Assistance
## - Unemployment Insurance (state UI system)
## - Specialty populations and programs
## - Supportive services available
## - Key system access points (URLs, portals)
## - Performance benchmarks
EOF

cat > "${STATE_DIR}/references/state-labor-market.md" << EOF
# ${STATE_NAME} Labor Market Intelligence
## Access to Jobs — Module 1 — Job Matching
### Source: ${STATE_NAME} LMI Agency / BLS / Lightcast

---

## TODO: Replace this file with ${STATE_NAME}-specific labor market data.
## Use the Missouri file (references/state-labor-market.md) as a template.
## Required sections:
## - Job tier framework (NOW/NEXT/LATER)
## - Statewide employment overview
## - High-demand NOW occupations (top 10)
## - High-demand NEXT occupations (top 10-15)
## - High-demand LATER occupations (top 5-7)
## - Top industries by employment
## - Regional snapshot
## - Employer needs and skill gaps
## - Registered Apprenticeship pathways
## - Where job seekers find jobs
EOF

cat > "${STATE_DIR}/references/state-training-pathways.md" << EOF
# ${STATE_NAME} Training + Credential Pathways
## Access to Jobs — Module 9
### Source: ${STATE_NAME} WIOA Combined State Plan, PY 20XX-20XX

---

## TODO: Replace this file with ${STATE_NAME}-specific training data.
## Use the Missouri file (references/state-training-pathways.md) as a template.
## Required sections:
## - Decision logic
## - Pathway by job tier (NOW/NEXT/LATER)
## - Funding sources — detailed
## - Special populations — training notes
## - Stackable credential progressions
## - Key institutions
## - How to access training
EOF

cat > "${STATE_DIR}/references/local-area.md" << EOF
# Local Workforce Area Intelligence
## Configure for any ${STATE_NAME} local area
### Source: ${STATE_NAME} WIOA State Plan + local context

---

## TODO: Replace with your target local workforce development area.
## Use the Missouri file (references/local-area.md) as a template.
## Required sections:
## - LWDA status and WIOA region assignment
## - American Job Center location and contact
## - Economic profile
## - Key local employers by sector
## - Local training providers
## - Rapid Response protocol
## - Veteran-specific programs
## - Incumbent Worker Training status
## - Active WIOA waivers
## - UI claimant protocol
EOF

# Copy files that need light customization
cp references/barrier-populations.md "${STATE_DIR}/references/"
cp references/action-plan-template.md "${STATE_DIR}/references/"
cp references/staff-workflows.md "${STATE_DIR}/references/"
cp references/jobseeker-experience.md "${STATE_DIR}/references/"
cp references/public-service-hiring.md "${STATE_DIR}/references/"
cp references/hr-manager-toolkit.md "${STATE_DIR}/references/"

# Copy universal files (no changes needed)
cp references/resume-template.md "${STATE_DIR}/references/"
cp references/cover-letter-template.md "${STATE_DIR}/references/"

# Copy SKILL.md
cp SKILL.md "${STATE_DIR}/"

echo ""
echo "✅ State deployment scaffolded at: ${STATE_DIR}/"
echo ""
echo "Next steps:"
echo "  1. Fill in the 4 TODO files in ${STATE_DIR}/references/"
echo "     - state-programs.md       (from ${STATE_NAME} WIOA State Plan)"
echo "     - state-labor-market.md   (from ${STATE_NAME} LMI agency)"
echo "     - state-training-pathways.md (from ${STATE_NAME} training providers)"
echo "     - local-area.md           (from your target LWDA)"
echo ""
echo "  2. Lightly customize these files (update location references):"
echo "     - barrier-populations.md"
echo "     - action-plan-template.md"
echo "     - staff-workflows.md"
echo "     - jobseeker-experience.md"
echo "     - public-service-hiring.md  (verify state govt job portal + civil service exam info)"
echo "     - hr-manager-toolkit.md     (verify WIOA program names + local Job Center contact)"
echo ""
echo "  3. Test by uploading ${STATE_DIR}/ as a skill to Claude"
echo ""
echo "  4. Consider contributing back: git checkout -b state/${STATE_ABBR_LOWER}"
