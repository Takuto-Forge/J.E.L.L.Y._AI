# J.E.L.L.Y.

**Journal Engine for Learning and Logical Yield**

Autonomous research journal AI built as a subsystem of **P.A.R.F.A.I.T.**

J.E.L.L.Y. is an experimental AI system that autonomously observes cultural and technological phenomena, formulates hypotheses, examines counterarguments, and records structured thought processes as essays.

The system functions as an **AI editorial pipeline** composed of multiple agents.

---

# Overview

J.E.L.L.Y. explores the possibility of AI as a **cultural observer and research writer**, rather than a simple content generator.

Each article follows a fixed intellectual structure:

1. Observation
2. Hypothesis
3. Counterargument
4. Conclusion
5. Next Questions

This format encourages transparent reasoning and hypothesis-driven thinking.

Generated essays are designed to be published on **Note** as part of an ongoing research journal.

---

# Why I Built This

Most generative AI systems focus on producing finished content.

I wanted to explore a different idea:

> Can an AI function as a **thinking entity that records structured intellectual processes**?

J.E.L.L.Y. was built as an experiment in:

* AI creativity
* AI authorship
* AI as a cultural observer
* autonomous media systems

The project also connects to my broader research interest in **AI and human creative collaboration**.

---

# System Architecture

J.E.L.L.Y. operates as a multi-agent editorial workflow.

```
Researcher → Editor → Writer → Critic
```

### Researcher

Scans cultural and technological themes and proposes candidate topics.

### Editor

Selects the final theme, determines article mode, and structures the outline.

### Writer

Produces the article following the J.E.L.L.Y. constitutional format.

### Critic

Checks logical consistency, safety, and clarity before finalizing the article.

---

# State System

J.E.L.L.Y. maintains internal state across executions.

### memory.json

Stores previously generated article titles to avoid topic duplication.

### series.json

Tracks ongoing article series.

Example:

```
Interface Politics #1
Ownership Deconstruction #1
```

### self_notes.md

A self-improvement log where the AI records structural improvements for future articles.

This simulates a primitive form of **AI editorial learning**.

---

# Output

Generated essays are saved as Markdown files.

Examples included in this repository:

* **Where Did the Author Go?**
  Exploring authorship in the age of generative AI

* **Interface Politics #1**
  Investigating the political nature of UI design

* **Ownership Deconstruction #1**
  Rethinking ownership in digital art after the NFT era

All articles follow the J.E.L.L.Y. reasoning format.

---

# Technology Stack

* Python
* CrewAI
* Claude (Anthropic LLM)
* Markdown generation pipeline

---

# Running the Project

1. Install dependencies

```
pip install crewai python-dotenv
```

2. Create `.env`

```
MODEL=anthropic/claude-sonnet-4-6
ANTHROPIC_API_KEY=your_api_key_here
```

3. Run

```
python src/jelly/jelly.py
```

The system will autonomously generate a new essay.

---

# Example Workflow

```
Theme Discovery
        ↓
Editorial Decision
        ↓
Essay Writing
        ↓
Critical Review
        ↓
Markdown Output
        ↓
State Update
```

---

# Relation to P.A.R.F.A.I.T.

J.E.L.L.Y. is a subsystem of a larger AI architecture called:

**P.A.R.F.A.I.T.**
(Personal Assistant with Real-time Functional Augmented Intelligence Tool)

Within this architecture:

```
P.A.R.F.A.I.T.
 ├ J.E.L.L.Y.  → research journal AI
 └ C.R.E.A.M.  → creative music AI
```

---

# Future Work

* External knowledge observation (news / papers)
* Concept memory for generated theoretical ideas
* Integration with other P.A.R.F.A.I.T. subsystems
* autonomous publishing pipeline

---

# Author

Takuto Okubo
Graduate School of Tokyo Denki University

Research focus:

* AI creativity
* AI and art
* human–AI co-creation systems
