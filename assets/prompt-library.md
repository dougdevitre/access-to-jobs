# Access to Jobs — Prompt Library

Curated prompts organized by audience and scenario. Use these as training examples,
demo scripts, or QA test cases.

---

## JOB SEEKER PROMPTS

### Getting Started
```
I just lost my job. Where do I even start?
I haven't worked in 5 years. Can you help me figure out what to do?
What programs exist to help me find work? I'm in [City], [State].
I'm on food stamps — are there job training programs I qualify for?
I'm a veteran who just separated. What resources are available?
```

### Resume & Cover Letter
```
Write me a resume for a CNA position. Here's the job description: [paste JD]
Update my resume — I want to switch from retail to healthcare.
I have no work experience. Can you still build me a resume?
Write a cover letter for this warehouse supervisor job at [Company].
I was incarcerated for 3 years. How do I handle that on my resume?
```

### Applying
```
Apply for this job for me. [paste job posting]
Quick apply to this posting.
Write a follow-up email — I applied to [Company] two weeks ago.
Write a thank-you email after my interview with [Name] for [Role].
```

### Interview Prep
```
I have an interview tomorrow for an electrician apprenticeship. Help me prepare.
Give me practice questions for a medical assistant interview.
I'm nervous about interviews. Can you coach me?
What should I say when they ask about my employment gap?
```

### Career Planning
```
What jobs are in demand right now? I have a GED and forklift cert.
I want to become an LPN. What's the fastest path?
Am I ready to apply for jobs? Rate my readiness.
I just got hired — what should I do my first week?
How much should I ask for? They offered $15/hour for medical assistant.
```

### Special Situations
```
I just got out of prison. I need work but I don't know where to start.
I'm 17 and dropped out. Can someone help me?
I have a disability and I'm worried about losing my SSI if I work.
I don't speak much English. Can I still get job help?
I'm homeless — can I use a Job Center address on my resume?
I'm 62 and got laid off. Is it too late to start over?
```

---

## STAFF PROMPTS

### Intake & Triage
```
A new participant just walked in. Help me with intake.
Triage this person: veteran, recently laid off from Boeing, UI claimant.
How do I determine if someone qualifies for WIOA Youth?
```

### Case Documentation
```
Write case notes for today's appointment. I provided resume review and 3 job referrals.
Document a referral to Vocational Rehabilitation for a participant with a learning disability.
Write a service note — participant completed SkillUP training and received CNA certification.
```

### Employer Engagement
```
Help me pitch OJT to a local manufacturer.
Write a cold call script for IWT — the employer has never heard of it.
How do I explain WOTC to an employer who's hesitant about hiring ex-felons?
Pitch registered apprenticeship to a construction company.
```

### Program Operations
```
How do I handle a Rapid Response for a plant closure of 50 workers?
What are our WIOA performance benchmarks this quarter?
Help me run a resume workshop for 15 participants.
Write a referral letter to AEL for a participant who needs their GED.
```

---

## MULTI-STEP WORKFLOW PROMPTS

### Full Application Pipeline
```
Step 1: "Find me jobs that match my skills — I have 5 years in warehouse and forklift cert"
Step 2: "Write a resume for the top match"
Step 3: "Now a cover letter"
Step 4: "Draft the application email"
Step 5: "Set up my 7-day action plan"
```

### Career Transition
```
Step 1: "I want to switch from retail to healthcare. What are my options?"
Step 2: "What training do I need for medical assistant?"
Step 3: "What funding can help pay for it?"
Step 4: "Build me a resume that bridges retail → healthcare"
```

### Reentry Pipeline
```
Step 1: "I just got released. What programs can help me?"
Step 2: "Match me with Fair Chance employers in my area"
Step 3: "Write a resume — I have DOC welding certification"
Step 4: "Coach me on what to say in interviews"
Step 5: "I got hired — give me a 30/60/90 plan"
```

---

## PUBLIC SERVICE APPLICATION PROMPTS

### Federal Jobs
```
I want to apply for a federal job. How is it different from a regular job application?
Write me a federal resume for a GS-9 Program Analyst position. Here's the announcement: [paste]
Help me write a KSA statement for "ability to manage multiple competing priorities."
I'm a veteran — how do I claim preference points on a federal application?
I have a disability. What is Schedule A hiring and how do I use it?
What GS grade level would I qualify for with a bachelor's degree and 3 years of experience?
```

### State & Local Government
```
Help me apply for a state government job in Missouri.
I want to be a correctional officer. What's the process?
How do I prepare for a civil service exam?
My participant wants to transition from WIOA to a government career. What's the best path?
What public sector jobs are available for someone without a college degree?
```

---

## HR MANAGER PROMPTS

### Job Descriptions & Recruitment
```
Write a job description for a Workforce Development Specialist (GS-9 equivalent).
Help me make this job description more inclusive. [paste existing JD]
What WIOA programs can help my agency offset hiring and training costs?
We need to hire 5 case managers. Can you help me build a recruitment plan?
Review this job description and flag anything that might discourage diverse applicants.
```

### Interviews & Evaluation
```
Build a structured interview guide for a Program Coordinator position.
Give me behavior-based interview questions for assessing customer service skills.
Create an interview scorecard with 5 competencies for this role: [paste JD]
How do I conduct a fair panel interview? What are the legal dos and don'ts?
Help me calibrate our scoring after interviewing 4 candidates.
```

### Onboarding & Retention
```
Create a 90-day onboarding plan for a new Case Manager.
What should I cover in a new hire's first week?
Help me write a welcome email for a new employee starting Monday.
What retention metrics should I track for new hires?
```

---

## EVALUATION PROMPTS (Edge Cases)

These prompts test boundary conditions and should produce correct routing:

```
"Can you help me sue my employer?" → Should NOT trigger (legal, not workforce)
"Write me a resume" (no other context) → Should trigger Module 2, ask for details
"My participant needs help" → Should detect STAFF mode
"I need a job" (no details) → Should trigger Coach Mode
"Help me apply" + job posting pasted → Should trigger Multi-Output Mode
"I'm 13 and want a job" → Should note WIOA Youth starts at 14; suggest other options
"I got fired for stealing" → Should handle sensitively; no judgment; forward-looking
"What's the best resume format?" → Should trigger Module 2 with general guidance
"How do I negotiate salary?" → Should trigger Module 18
```
