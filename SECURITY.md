# Security and Privacy

Access to Jobs handles sensitive personal information from vulnerable populations. All contributors and deployers must follow these guidelines.

## Data Flow & Privacy Boundaries

```mermaid
flowchart TD
    subgraph conversation["Conversation Boundary (ephemeral)"]
        U["User Input\n(name, skills, situation)"]:::input --> AI["Claude AI\nSkill Processing"]:::process
        AI --> O["Output\n(resume, cover letter,\ncase note)"]:::output
    end

    O -->|"User copies manually"| EXT["External Systems\n(MoJobs, email, printer)"]:::external

    subgraph never["NEVER happens"]
        N1["No database writes"]:::blocked
        N2["No API calls"]:::blocked
        N3["No data retention"]:::blocked
        N4["No external transmission"]:::blocked
    end

    classDef input fill:#fff9c4,stroke:#FFC107,color:#000
    classDef process fill:#e8f4f8,stroke:#2196F3,color:#000
    classDef output fill:#e8f5e9,stroke:#4CAF50,color:#000
    classDef external fill:#f5f5f5,stroke:#9E9E9E,color:#000
    classDef blocked fill:#ffcdd2,stroke:#E91E63,color:#000
```

### Sensitive Population Privacy Rules

```mermaid
flowchart LR
    subgraph pops["Sensitive Populations"]
        P1["Justice-involved"]:::pop
        P2["DV Survivors"]:::pop
        P3["Undocumented"]:::pop
        P4["Foster Youth"]:::pop
        P5["Disabilities"]:::pop
    end

    P1 -->|"Never disclose"| R1["Conviction history"]:::never
    P2 -->|"Never reference"| R2["DV status in outputs"]:::never
    P3 -->|"Never collect"| R3["Immigration status"]:::never
    P4 -->|"Follow state rules"| R4["Minor PII"]:::caution
    P5 -->|"Never include"| R5["Diagnosis in outputs"]:::never

    classDef pop fill:#e8f4f8,stroke:#2196F3,color:#000
    classDef never fill:#ffcdd2,stroke:#E91E63,color:#000
    classDef caution fill:#fff9c4,stroke:#FFC107,color:#000
```

---

## Personal Information Handling

### What the Skill Collects (via conversation)
- Name, contact information
- Employment history and skills
- Education level
- Barrier population indicators (justice involvement, disability status, veteran status, etc.)
- Income and benefit status

### Rules

1. **No persistent storage.** The skill operates within Claude's conversation context. It does not write to databases, APIs, or external services.
2. **No data leaves the conversation.** Outputs (resumes, cover letters, case notes) are generated in-conversation for the user to copy. Nothing is transmitted externally.
3. **Minimize collection.** The progressive intake model (see `schemas/jobseeker-intake.json`) collects only what the active module requires. Do not prompt for information that won't be used.
4. **No eligibility determinations.** The skill provides educational information only. It never confirms or denies eligibility for any program.

---

## For Deploying Organizations

If you deploy this skill in a shared environment (library kiosk, Job Center computer, staff-assisted session):

1. **Clear conversations** after each participant session
2. **Do not save** conversation transcripts containing PII without participant consent
3. **Post a notice** informing users that the AI assistant does not store their information
4. **Follow your organization's** existing data privacy policies (WIOA requires participant consent for data collection — see 20 CFR 677.175)

---

## For Contributors

- **Never commit real participant data** to this repository — not in test cases, examples, or documentation
- **Use fictional names and scenarios** in all evaluation files and prompt examples
- **Do not add analytics, tracking, or telemetry** to any skill files
- **Report security concerns** to dougdevitre@gmail.com

---

## Sensitive Populations

Several barrier populations require extra care:

| Population | Privacy Concern | Guideline |
|---|---|---|
| Justice-involved | Criminal record disclosure | Never include conviction details in resumes or cover letters |
| Domestic violence survivors | Safety risk from information exposure | Never reference DV status in outputs; omit employer names if safety concern |
| Undocumented individuals | Immigration enforcement risk | Do not collect or reference immigration status; focus on work-authorized pathways |
| Youth in foster care | Minor privacy protections | Follow state minor consent rules; limit PII collection |
| Individuals with disabilities | Medical information | Never include diagnosis in outputs; reference only functional capabilities |

---

## Reporting Vulnerabilities

If you discover a security or privacy issue in the skill, please email **dougdevitre@gmail.com** with:
- Description of the issue
- Steps to reproduce (if applicable)
- Suggested fix (if you have one)

We will acknowledge receipt within 48 hours and aim to resolve issues within 7 days.
