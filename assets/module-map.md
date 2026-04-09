# Access to Jobs — Module Map

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           TRI-USER DETECTION                                    │
│  Job seeker signals → SEEKER    Staff signals → STAFF    HR signals → HR MGR    │
└─────────────┬──────────────────────┬──────────────────────┬─────────────────────┘
              │                      │                      │
   ┌──────────▼───────────┐ ┌───────▼──────────┐ ┌────────▼──────────┐
   │  JOB SEEKER MODULES  │ │  STAFF MODULES   │ │  HR MGR / PUBLIC  │
   │  0–9 · 14–18         │ │  10 · 11 · 12    │ │  SERVICE MODULES  │
   │  + Special Modes     │ │  13 · 19         │ │  20 · 21          │
   └──────────────────────┘ └──────────────────┘ └───────────────────┘
```

---

## Module Dependency Graph

```
                    ┌──────────────┐
                    │  USER INPUT  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │  TASK ROUTER │
                    └──────┬───────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
   ┌────▼─────┐     ┌─────▼──────┐    ┌─────▼──────┐
   │ CORE     │     │ ADVANCED   │    │ STAFF      │
   │ 0–9     │     │ 14–19      │    │ 10–13      │
   └────┬─────┘     └─────┬──────┘    └─────┬──────┘
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────────────────────────────────────────┐
   │           REFERENCE FILE LAYER              │
   │                                             │
   │  state-programs.md ──────── Module 0        │
   │  state-labor-market.md ──── Module 1        │
   │  resume-template.md ─────── Module 2        │
   │  cover-letter-template.md ─ Module 3        │
   │  action-plan-template.md ── Module 8        │
   │  state-training-pathways.md Module 9        │
   │  staff-workflows.md ─────── Modules 10–13   │
   │  jobseeker-experience.md ── Modules 14–19   │
   │  public-service-hiring.md ─ Module 20       │
   │  hr-manager-toolkit.md ──── Module 21       │
   │  barrier-populations.md ─── ALL modules     │
   │  local-area.md ──────────── ALL modules     │
   └─────────────────────────────────────────────┘
```

---

## Module Quick Reference

### Core Job Seeker (Modules 0–9)

| # | Module | Input | Output | Ref File |
|---|---|---|---|---|
| 0 | Eligibility Screener | situation, education | Program routing + next steps | `state-programs.md` |
| 1 | Job Matcher | skills[], location, experience | Top 5 roles (NOW/NEXT/LATER) | `state-labor-market.md` |
| 2 | Resume Builder | name, skills[], experience, JD | ATS-optimized resume | `resume-template.md` |
| 3 | Cover Letter | name, target job, JD, experience | 3–4 paragraph letter | `cover-letter-template.md` |
| 4 | Application Email | target job, tone | Submit email (<150 words) | — |
| 5 | Follow-Up Email | target job, date applied | Follow-up (<100 words) | — |
| 6 | Thank You Email | interviewer name(s), topics | Thank you (<150 words) | — |
| 7 | Interview Prep | target job title | 5 Qs + STAR answers + tips | — |
| 8 | Action Plan | target job, urgency | 7-day plan + log | `action-plan-template.md` |
| 9 | Training Pathways | skills, target role | Shortest path + funding | `state-training-pathways.md` |

### Advanced Job Seeker (Modules 14–19)

| # | Module | Input | Output | Ref File |
|---|---|---|---|---|
| 14 | Readiness Assessment | target job, situation | 7-dimension scorecard | `jobseeker-experience.md` |
| 15 | Job Retention | job title, industry | 30/60/90-day plan | `jobseeker-experience.md` |
| 16 | LinkedIn Builder | experience, target role | Full profile content | `jobseeker-experience.md` |
| 17 | Job Fair Prep | event, target employers | Before/during/after kit | `jobseeker-experience.md` |
| 18 | Salary Guidance | role, location, offer | Market data + negotiation | `jobseeker-experience.md` |
| 19 | Workshop Guide | workshop type | Facilitation script | `jobseeker-experience.md` |

### Staff Modules (Modules 10–13)

| # | Module | Input | Output | Ref File |
|---|---|---|---|---|
| 10 | Intake & Triage | walk-in participant | Assessment + routing | `staff-workflows.md` |
| 11 | Case Notes | service provided, actions | MoJobs-compatible note | `staff-workflows.md` |
| 12 | Referral Letter | participant, agency, reason | Formal referral letter | `staff-workflows.md` |
| 13 | Employer Outreach | program to pitch | Cold call / pitch script | `staff-workflows.md` |

### Public Service & HR Manager (Modules 20–21)

| # | Module | Input | Output | Ref File |
|---|---|---|---|---|
| 20 | Public Service Applications | target agency/level, role, veteran status | Gov resume, KSA, checklist | `public-service-hiring.md` |
| 21 | HR Manager Toolkit | position to fill, grade, qualifications | Job description, interview guide, scorecard | `hr-manager-toolkit.md` |

### Special Modes

| Mode | Trigger | Output |
|---|---|---|
| Multi-Output | "apply for this job" | Resume + Cover Letter + Email |
| Quick | "quick apply" | 3-bullet summary + cover note + email |
| Coach | "where do I start?" | Readiness + gaps + today's action + 7-day plan |

---

## Population Routing Matrix

| Population | Module 0 | Module 1 | Module 2 | Module 7 | Module 8 | Module 9 | Module 20 | Module 21 |
|---|---|---|---|---|---|---|---|---|
| Justice-involved | Reentry programs | Fair Chance employers | No conviction disclosure | Forward-looking answers | Federal Bonding flag | DOC vocational creds | Fair Chance Act; avoid positions with conduct bars | WOTC incentive for employer |
| Veterans | Priority of service | Military skill translation | MOS → civilian titles | Leadership examples | DVOP referral | GI Bill stacking | 5/10-pt preference; VEOA/VRA authorities | Show-Me Heroes; OJT subsidy |
| Youth 14–24 | Youth programs | NOW-tier focus | Entry-level format | Behavioral focus | Smaller daily actions | Subsidized employment | Pathways Program; state internships | TANF subsidized placement |
| Disability | MVR/RSB referral | Customized employment | Accommodations note | ADA awareness | Benefits counseling | VR training funding | Schedule A hiring; SPPC contact | ADA accommodation in hiring |
| SNAP/TANF | SkillUP/MWA | Any demand role | Standard | Standard | DSS LISTSERV | SkillUP training | Stable gov benefits ease transition | WOTC-eligible candidates |
| No diploma | AEL/Excel Center | NOW-tier only | Education → Skills lead | Transferable skills | GED as Day 1 action | IET model | Limited below GS-2; credential first | Entry-level trades/maintenance |
| English learner | AEL ELL | Plain language roles | Simplified format | Practice answers | Plain language steps | IET concurrent | Bilingual positions in demand | Language premium pay |
| Homeless | Wraparound services | Flexible schedule roles | Job Center address OK | Realistic prep | Job Center access | Short-term certs | Standard gov application process | Standard |
| Older (55+) | SCSEP | Experience-valued roles | Modernized format | Age-redirect coaching | LinkedIn update | Upskill certs | No mandatory retirement; strong benefits | Experience highly valued |
