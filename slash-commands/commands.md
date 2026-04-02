# Access to Jobs — Slash Commands

Quick-trigger commands for common workflows. Users can type these to jump
directly to a module without conversational routing.

## Command Routing Map

```mermaid
flowchart TD
    CMD["/command"]:::cmd --> TYPE{"Command Type"}:::router

    TYPE -->|"Job Seeker"| JS
    TYPE -->|"Staff"| ST
    TYPE -->|"Utility"| UT

    subgraph JS["Job Seeker Commands"]
        direction LR
        JS1["/eligible → M0"]:::m0
        JS2["/match → M1"]:::core
        JS3["/resume → M2"]:::core
        JS4["/cover → M3"]:::core
        JS5["/apply → Multi"]:::special
        JS6["/quick → Quick"]:::special
        JS7["/followup → M5"]:::core
        JS8["/thankyou → M6"]:::core
        JS9["/interview → M7"]:::core
        JS10["/plan → M8"]:::core
        JS11["/train → M9"]:::core
        JS12["/ready → M14"]:::adv
        JS13["/hired → M15"]:::adv
        JS14["/linkedin → M16"]:::adv
        JS15["/fair → M17"]:::adv
        JS16["/salary → M18"]:::adv
        JS17["/coach → Coach"]:::special
    end

    subgraph ST["Staff Commands"]
        direction LR
        ST1["/intake → M10"]:::staff
        ST2["/casenote → M11"]:::staff
        ST3["/refer → M12"]:::staff
        ST4["/pitch → M13"]:::staff
        ST5["/workshop → M19"]:::staff
    end

    subgraph UT["Utility Commands"]
        direction LR
        UT1["/glossary"]:::util
        UT2["/programs"]:::util
        UT3["/local"]:::util
        UT4["/track"]:::util
        UT5["/help"]:::util
    end

    classDef cmd fill:#e8f4f8,stroke:#2196F3,color:#000
    classDef router fill:#fff3e0,stroke:#FF9800,color:#000
    classDef m0 fill:#dcedc8,stroke:#689F38,color:#000
    classDef core fill:#e8f5e9,stroke:#4CAF50,color:#000
    classDef adv fill:#bbdefb,stroke:#2196F3,color:#000
    classDef special fill:#fff9c4,stroke:#FFC107,color:#000
    classDef staff fill:#fce4ec,stroke:#E91E63,color:#000
    classDef util fill:#f5f5f5,stroke:#9E9E9E,color:#000
```

---

## Job Seeker Commands

| Command | Action | Module |
|---|---|---|
| `/eligible` | Check program eligibility | Module 0 |
| `/match` | Find best-fit jobs | Module 1 |
| `/resume` | Build or update resume | Module 2 |
| `/cover` | Write a cover letter | Module 3 |
| `/apply` | Full application package (resume + cover + email) | Multi-Output |
| `/quick` | Quick apply (summary + cover note + email) | Quick Mode |
| `/followup` | Write a follow-up email | Module 5 |
| `/thankyou` | Write a thank-you email | Module 6 |
| `/interview` | Interview prep with STAR answers | Module 7 |
| `/plan` | 7-day action plan | Module 8 |
| `/train` | Training and credential pathways | Module 9 |
| `/ready` | Employment readiness assessment | Module 14 |
| `/hired` | 30/60/90-day retention plan | Module 15 |
| `/linkedin` | Build LinkedIn profile | Module 16 |
| `/fair` | Job fair prep kit | Module 17 |
| `/salary` | Salary negotiation guidance | Module 18 |
| `/coach` | Full coaching session (readiness + gaps + plan) | Coach Mode |

---

## Staff Commands

| Command | Action | Module |
|---|---|---|
| `/intake` | Intake and triage script | Module 10 |
| `/casenote` | Generate case notes | Module 11 |
| `/refer` | Draft a referral letter | Module 12 |
| `/pitch` | Employer outreach script | Module 13 |
| `/workshop` | Workshop facilitation guide | Module 19 |

---

## Utility Commands

| Command | Action |
|---|---|
| `/glossary` | Show WIOA acronym definitions |
| `/programs` | List all available programs for user's situation |
| `/local` | Show local workforce area info |
| `/track` | Start or update application tracker |
| `/help` | Show this command list |

---

## Usage Examples

```
User: /resume
Bot: I'll help you build an ATS-optimized resume. What's the job title
     you're targeting? (Paste the job description if you have it.)

User: /apply [pastes job posting]
Bot: I'll create your full application package. Let me generate:
     1. Tailored resume
     2. Cover letter
     3. Application email
     ---
     [Resume output]
     ---
     [Cover letter output]
     ---
     [Application email output]

User: /intake
Bot: [Staff mode detected] Starting intake triage.
     Step 1 — Situation assessment:
     "Welcome. To connect you with the right services today..."

User: /coach
Bot: Let's assess where you stand. I'll score your readiness across
     7 dimensions, identify your top 3 gaps, and give you a specific
     action to take today plus a 7-day plan.
     What job title are you targeting?
```

---

## Notes

- Commands are case-insensitive (`/Resume` = `/resume` = `/RESUME`)
- Commands can include context: `/resume for CNA at SSM Health`
- If a command needs more info, the skill will ask progressively
- Staff commands auto-switch to staff mode
- All commands respect population-specific adjustments
