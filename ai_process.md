# AI Process Documentation

## Purpose

<div align='center'>

This document outlines how AI tools were used during the technical phase of the project, including Python and SQL workflows.

</div>

***

## Tools Used

- AI Assistant: **GPT-4.1**
- IDE Integration: **GitHub Copilot**
- Other Tools (if applicable): **GPT-5 mini**

---

## Guiding Principles

- AI was used as a support tool, not a replacement for independent analysis.

- All AI-generated outputs were reviewed, tested, and validated. Use of AI for producing code is outlined with a comment in the code.

- Final decisions were made by the entire team (Thierno, Rolando, Debo).

---

## 1. Data Extraction (SQL)

**Use Cases:**

**Validation Steps:**

(Ro did not use AI for SQL queries.)
> !NOTE
> Speak with team for confirmation on AI usage during this step.

***

## 2. Data Cleaning & Exploration (Python)

<div align='center'>

AI was used for different portions of this step. For most cleaning and exploration, GitHub Copilot, along with software extensions were used to speed up EDA by writing routine code.

</div>

**Use Cases:**
- Pandas transformations
- Handling missing values
- Feature engineering suggestions
- Refactoring code

**Validation Steps:**
- Output inspection
- Shape and datatype verification
- Reproducibility checks

***

## 3. Statistical Testing

<div align='center'>

Similarly to step 2, AI was mostly used her to assist in writing repetitive code.

</div>

**Use Cases:**
- Assist in generating code for tests (e.g., t-test, ANOVA)
- Interpreting p-values and assumptions

**Validation Steps:**
- Assumption checks (normality, variance, independence)
- Re-running tests independently
- Comparing effect sizes

***

## 4. Modeling

**Use Cases:**

**Validation Steps:**

***

## 5. Documentation & Communication

<div align='center'>

For documentation, AI was used primarily to summarize and revise our writing. Spell checks, grammatical errors, and exposition were improved with AI, while ensuring each sentence conveys the our project's goals.

</div>

**Use Cases:**
- Revising spelling and grammar
- Summarizing findings

**Validation Steps:**
- Technical accuracy review
- Consistency with actual results
- Alignment with project objectives

---

## Limitations

- AI outputs may contain inaccuracies.
- AI does not have direct access to private datasets unless explicitly provided.
- All generated code and interpretations require human review.

***
