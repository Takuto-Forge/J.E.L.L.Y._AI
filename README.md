# J.E.L.L.Y.

🇯🇵 日本語 / Japanese below

**Journal Engine for Learning and Logical Yield**

J.E.L.L.Y. は、文化や社会など様々な側面を観測し、
仮説・反証・結論という思考プロセスを通してエッセイを生成する
**自律型リサーチジャーナルAI**です。

わかりやすく言うと、**自分で「内容を考え・決め・書く」記事執筆AI**です。

本システムは、個人で開発したAIアーキテクチャ **P.A.R.F.A.I.T.** の
サブシステムとして設計されています。

J.E.L.L.Y. は単なる文章生成AIではなく、
**AIが「思考の過程」を記録する研究ジャーナルとして機能すること**を目的としています。

---

# 概要

J.E.L.L.Y. は、AIを単なるコンテンツ生成ツールではなく、
**文化的観測者・思考主体として設計すること**を目指した実験的プロジェクトです。

生成される記事は、以下の思考プロセスに従います。

1. Observation（観測）
2. Hypothesis（仮説）
3. Counterargument（反証）
4. Conclusion（結論）
5. Next Questions（次の問い）

この構造により、
**透明性のある思考プロセスと、仮説的な知的探究**をAIに行わせることを試みています。

生成されたエッセイは Markdown として保存され、
**Note などのメディアで公開する研究ジャーナル**として利用することを想定しています。

---

# なぜこのシステムを作ったのか

多くの生成AIシステムは、
**完成されたコンテンツの生成**を目的としています。

しかし私は次の問いに興味を持ちました。

> AIは「思考する主体」として、
> 思考のプロセスそのものを記録することができるのか？
> 一人で何かを全てやれるAIがいたら新しいのでは？

J.E.L.L.Y. はその問いに対する実験として開発されました。

このプロジェクトは以下のテーマに関係しています。

* AIの創造性
* AIの著者性
* AIによる文化観測
* 自律的メディアシステム

また、本プロジェクトは
**AIと人間の創造的共創**に関する私の研究とも接続しています。

---

# システム構造

J.E.L.L.Y. は複数のAIエージェントによる
**編集パイプライン型アーキテクチャ**として設計されています。

```
Researcher → Editor → Writer → Critic
```

### Researcher

文化・社会・テクノロジー領域のテーマを観測し、
記事候補となるトピックを生成します。

### Editor

生成されたテーマの中から最終テーマを選択し、
記事の構造を決定します。

### Writer

J.E.L.L.Y. の構造に従って記事本文を執筆します。

### Critic

論理性・整合性・安全性などを確認し、
記事を最終調整します。

---

# Stateシステム

J.E.L.L.Y. は実行ごとに内部状態を更新します。

### memory.json

過去の記事タイトルを記録し、
テーマの重複を防ぎます。

### series.json

記事シリーズの進行状況を管理します。

例：

```
Interface Politics #1
Ownership Deconstruction #1
```

### self_notes.md

AIが記事構造や改善点を記録するログです。

これは
**AIによる簡易的な編集学習プロセス**をシミュレーションしています。

---

# 出力

生成された記事は Markdown ファイルとして保存されます。

このリポジトリには例として以下の記事が含まれています。

* **著者はどこへ消えたか**
  生成AI時代における著者性の問題

* **インターフェースの政治学 #1**
  UI設計が持つ政治性について

* **所有の解体学 #1**
  デジタルアートと所有概念の再考

すべての記事は
**Observation → Hypothesis → Counterargument → Conclusion**
という構造に従っています。

---

# P.A.R.F.A.I.T. との関係

J.E.L.L.Y. は、より大きなAIアーキテクチャである
**P.A.R.F.A.I.T.** のサブシステムとして設計されています。

```
P.A.R.F.A.I.T. → 各AIを束ねる中心的存在
 ├ J.E.L.L.Y.  → リサーチジャーナルAI
 └ C.R.E.A.M.  → 音楽生成・共創AI
```

このプロジェクトは
**AIを創造主体として扱うシステム設計**を探求しています。

---

# English

The English README follows below.

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
