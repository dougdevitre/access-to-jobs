# Contributing to Access to Jobs

Thank you for your interest in contributing to the Access to Jobs workforce navigator. This project is part of the **Access To** open-source civic tech initiative by CoTrackPro.

---

## Ways to Contribute

### 1. Deploy to a New State
The highest-impact contribution is creating a state-specific implementation. See [DEPLOYMENT.md](DEPLOYMENT.md) for the full guide. You'll need:
- Your state's WIOA Combined State Plan (available from your state workforce agency)
- Labor market data from your state's LMI agency
- Training provider and funding program information
- Local workforce development area details

### 2. Improve Existing Modules
- Fix inaccuracies in Missouri reference data
- Add new output templates or coaching frameworks
- Improve population-specific guidance
- Enhance staff workflow scripts

### 3. Add Evaluation Test Cases
We use a JSON-based evaluation format. Add test cases to `evals/trigger-eval.json`:
```json
{
  "prompt": "I just got laid off from the auto plant. What should I do?",
  "expected_module": "MODULE 0",
  "expected_populations": ["dislocated_worker"],
  "notes": "Should route to eligibility screener and flag Rapid Response / TAA"
}
```

### 4. Translations and Accessibility
- Spanish language versions of job seeker modules
- Plain-language rewrites for low-literacy audiences
- Screen-reader-friendly output formatting

### 5. Bug Reports and Documentation
- Open an issue on GitHub with a clear description
- Include the module number and the user input that triggered the issue
- Suggest a fix if you have one

---

## Contribution Guidelines

### Content Standards
- **No fabricated data.** All statistics, program names, and eligibility criteria must come from official sources (WIOA state plans, BLS, state LMI agencies).
- **Educational framing.** Never make eligibility determinations. Always direct to official enrollment channels.
- **Trauma-informed language.** Calm, professional, empathetic. No judgment. No hype.
- **Child-centered where applicable.** Youth modules should use age-appropriate tone and framing.
- **No discriminatory language.** Never include protected-class references in output templates.

### File Naming
- State-specific files: `state-*.md` (e.g., `state-programs.md`)
- Local area files: `local-area.md`
- Universal files: descriptive name (e.g., `resume-template.md`)

### Pull Request Process
1. Fork the repository
2. Create a feature branch (`feature/illinois-deployment` or `fix/module-7-star-format`)
3. Make your changes
4. Test by uploading the skill to Claude and running sample prompts
5. Submit a PR with a clear description of what changed and why

### Source Citation
When adding or updating data, include the source in a comment or header:
```markdown
### Source: Illinois WIOA Combined State Plan, PY 2024-2027
### Source: BLS Occupational Employment and Wage Statistics, May 2025
```

---

## Code of Conduct

This project serves vulnerable populations including justice-involved individuals, veterans in crisis, youth aging out of foster care, and people experiencing homelessness. Contributors are expected to:

- Treat all populations with dignity and respect
- Avoid language that stigmatizes or stereotypes
- Prioritize accuracy over comprehensiveness
- Test outputs with real-world scenarios before submitting
- Disclose any conflicts of interest (e.g., affiliation with a training provider)

---

## Questions?

- **Email:** dougdevitre@gmail.com
- **GitHub Issues:** [cotrackpro/access-to-jobs/issues](https://github.com/cotrackpro/access-to-jobs/issues)
- **LinkedIn:** [linkedin.com/in/dougdevitre](https://linkedin.com/in/dougdevitre)
