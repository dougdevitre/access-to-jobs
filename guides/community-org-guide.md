# Guide: Deploying Access to Jobs for Community Organizations

A practical guide for nonprofits, libraries, community action agencies, faith-based
organizations, and advocacy groups that want to use Access to Jobs to serve their clients.

---

## Who This Is For

- **Community Action Agencies** providing workforce services alongside housing, energy, and food assistance
- **Libraries** offering job search support and computer access
- **Faith-based organizations** running job clubs or reentry programs
- **Reentry organizations** helping people transition from incarceration to employment
- **Veteran service organizations** assisting with civilian career transitions
- **Youth-serving organizations** (YouthBuild, Job Corps partners, foster care agencies)
- **Immigrant and refugee resettlement agencies** providing employment navigation
- **Domestic violence shelters** helping survivors achieve economic independence

---

## What You Get

Access to Jobs gives your organization an AI-powered workforce navigator that can:

1. **Screen clients for program eligibility** — WIOA, SNAP E&T, vocational rehabilitation, veterans services, and more
2. **Build resumes and cover letters** — ATS-optimized, tailored to specific job postings
3. **Prepare clients for interviews** — role-specific questions with structured answer coaching
4. **Create action plans** — 7-day job search plans calibrated to urgency
5. **Navigate training pathways** — find the shortest path to a credential with funding
6. **Generate staff documentation** — case notes, referral letters, employer outreach scripts

All outputs are trauma-informed, population-aware, and grounded in official WIOA data.

---

## Setup (15 minutes)

### Option A: Claude.ai (Simplest)
1. Download the `.skill` file from the [GitHub releases page](https://github.com/cotrackpro/access-to-jobs/releases)
2. Go to Claude.ai → Settings → Skills
3. Upload the `.skill` file
4. Start chatting — the skill activates automatically when you ask employment questions

### Option B: Shared Computer / Kiosk
1. Set up a Claude.ai account for your organization
2. Install the skill as above
3. Create a bookmark or shortcut with a starter prompt:
   ```
   "I need help finding a job. Where do I start?"
   ```
4. Print the slash commands reference (from `slash-commands/commands.md`) and post next to the computer

### Option C: Staff-Assisted
1. Train 1–2 staff members to use the skill (30-minute orientation)
2. Staff use the skill during client appointments to:
   - Screen for programs (Module 0)
   - Build resumes in real-time (Module 2)
   - Generate case notes after appointments (Module 11)
   - Draft referral letters (Module 12)

---

## Customizing for Your Organization

### Update the Local Area File
The most impactful customization: replace `references/local-area.md` with your service area's data.

**Include:**
- Your nearest American Job Center (address, phone, hours)
- Top 10 local employers hiring now
- Local training providers (community colleges, CTE centers)
- Your organization's specific partner agencies and referral contacts
- Any local job fairs or hiring events calendar

### Add Your Organization's Resources
Add a section to `local-area.md` with your organization's specific services:

```markdown
## [YOUR ORG NAME] — Additional Resources

- [Service 1 — e.g., "Free professional clothing closet"]
- [Service 2 — e.g., "Transportation vouchers for interviews"]
- [Service 3 — e.g., "Childcare during appointments"]
- [Service 4 — e.g., "Computer lab open M-F 9am-5pm"]
- Contact: [phone] | [email] | [address]
```

---

## Population-Specific Deployment Notes

### Reentry Organizations
- The skill already handles justice-involved populations — it will never recommend disclosing conviction history unless the client asks
- It flags Fair Chance employers and DOC vocational credentials
- Train staff to start with: `/eligible` → will route to reentry programs
- Print the glossary (`assets/glossary.md`) — clients won't know acronyms like WOTC or OJT

### Domestic Violence / Survivor Services
- The skill uses trauma-informed, non-judgmental language by default
- For survivors building economic independence, start with Coach Mode (`/coach`)
- Consider adding safety-specific notes to your local-area.md (confidential address programs, safe phone numbers)
- Never require clients to disclose DV status to use the skill

### Youth Programs
- The skill auto-adjusts tone for youth (14–24) — lighter formality, smaller action steps
- For youth without work experience, the resume module leads with education and skills
- Flag: WIOA Youth starts at age 14; TANF subsidized employment available at ≤185% poverty
- Excel Center (adults 21+) includes free childcare — important for young parents

### Immigrant / Refugee Services
- The skill supports plain language for English learners
- AEL ELL services + IET (English + job training simultaneously) are flagged automatically
- Consider creating a simplified slash commands card in the client's primary language
- Note: all AEL students must be referred to Job Centers at orientation

---

## Training Your Staff (30 minutes)

### Session Outline
1. **(5 min)** What Access to Jobs is and isn't
   - It IS: an AI assistant that helps build documents, screen programs, and navigate the workforce system
   - It is NOT: a replacement for case management, a legal advisor, or an eligibility determination tool
2. **(10 min)** Live demo of 3 key workflows
   - `/eligible` — show program screening
   - `/resume` — show resume generation with a sample JD
   - `/casenote` — show case notes generation
3. **(10 min)** Hands-on practice
   - Each staff member runs one prompt from the prompt library (`assets/prompt-library.md`)
4. **(5 min)** Q&A and scheduling follow-up

### Staff Quick Reference Card (print and laminate)

```
ACCESS TO JOBS — QUICK REFERENCE

For clients:
  /coach    → Full assessment + plan
  /eligible → Program screening
  /resume   → Build a resume
  /apply    → Resume + cover letter + email
  /interview → Interview prep

For staff:
  /intake   → New participant triage
  /casenote → Write case notes
  /refer    → Referral letter
  /pitch    → Employer outreach script

Tips:
  • Paste the job description for best results
  • The AI never fabricates experience
  • Always refer to Job Center for official enrollment
  • For sensitive populations, the AI auto-adjusts tone
```

---

## Measuring Impact

Track these metrics to demonstrate value to funders:

| Metric | How to Track |
|---|---|
| Resumes created | Count of Module 2 sessions |
| Applications submitted | Client self-report or application tracker |
| Interviews secured | Client self-report at follow-up |
| Job placements | Client self-report; WIOA Q2 outcome if enrolled |
| Programs identified | Count of Module 0 sessions with program matches |
| Time saved per client | Compare to pre-skill appointment duration |

---

## Frequently Asked Questions

**Q: Does the AI store client data?**
A: No. Claude does not retain conversation data between sessions. Each conversation starts fresh. Do not enter SSNs, full birthdates, or other sensitive PII.

**Q: Can clients use this on their own?**
A: Yes. The job seeker modules are designed for self-service. Staff-assisted use produces better results for complex situations.

**Q: Is this WIOA-compliant?**
A: The skill is grounded in WIOA State Plan data and uses educational framing. It does not make eligibility determinations. All official enrollment must go through the local American Job Center.

**Q: How often is the data updated?**
A: See `assets/data-sources.md` for data vintage. State plan data updates every 2 years. Labor market data should be refreshed annually.

**Q: Can we customize it for our state?**
A: Yes. See `DEPLOYMENT.md` for the full state deployment guide. You replace 4 state-specific files and lightly customize 4 others.
