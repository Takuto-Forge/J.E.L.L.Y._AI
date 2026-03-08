import os
import json
import re
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process, LLM

JELLY_DIR = Path(__file__).resolve().parent
ROOT_DIR = JELLY_DIR.parents[1]

CONFIG_DIR = ROOT_DIR / "config"
OUTPUT_DIR = ROOT_DIR / "output"
STATE_DIR = ROOT_DIR / "state"

CONSTITUTION_PATH = CONFIG_DIR / "constitution.md"
STYLE_GUIDE_PATH = CONFIG_DIR / "style_guide.md"

MEMORY_PATH = STATE_DIR / "memory.json"
SERIES_PATH = STATE_DIR / "series.json"
SELF_NOTES_PATH = STATE_DIR / "self_notes.md"

DEFAULT_MODEL = "anthropic/claude-sonnet-4-6"


# ----------------------------
# Utilities
# ----------------------------
def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def ensure_dirs():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    STATE_DIR.mkdir(parents=True, exist_ok=True)


def slugify(title: str) -> str:
    # ファイル名に危険な文字だけ除去（日本語は残す）
    title = re.sub(r"[\\/:*?\"<>|]", "", title).strip()
    title = re.sub(r"\s+", "_", title)
    return title[:80] if len(title) > 80 else title


def extract_json(text: str) -> dict:
    """
    LLMがJSON以外を混ぜた場合に備えて、最初の { から最後の } を抜いてjson.loadsする。
    """
    t = (text or "").strip()
    start = t.find("{")
    end = t.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError(f"Output is not JSON. Head: {t[:200]}")
    return json.loads(t[start : end + 1])


# ----------------------------
# State: memory / series / self_notes
# ----------------------------
def load_memory():
    if MEMORY_PATH.exists():
        return json.loads(MEMORY_PATH.read_text(encoding="utf-8"))
    return {"history": []}


def save_memory(mem):
    MEMORY_PATH.write_text(json.dumps(mem, ensure_ascii=False, indent=2), encoding="utf-8")


def load_series():
    if SERIES_PATH.exists():
        return json.loads(SERIES_PATH.read_text(encoding="utf-8"))
    return {
        "current_series": None,
        "rules": {
            "start_new_series_probability": 0.25,
            "max_episodes_before_refresh": 6
        }
    }


def save_series(series_obj: dict):
    SERIES_PATH.write_text(json.dumps(series_obj, ensure_ascii=False, indent=2), encoding="utf-8")


def load_self_notes() -> str:
    if SELF_NOTES_PATH.exists():
        return SELF_NOTES_PATH.read_text(encoding="utf-8")
    return "# J.E.L.L.Y. Self Notes\n- (empty)\n"


def append_self_note(line: str):
    prev = load_self_notes().rstrip() + "\n"
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    updated = prev + f"- [{ts}] {line.strip()}\n"
    SELF_NOTES_PATH.write_text(updated, encoding="utf-8")


# ----------------------------
# LLM
# ----------------------------
def build_llm() -> LLM:
    model = os.getenv("MODEL", DEFAULT_MODEL)
    return LLM(model=model, temperature=0.7)


# ----------------------------
# Main
# ----------------------------
def main():
    load_dotenv()
    ensure_dirs()

    model = os.getenv("MODEL", DEFAULT_MODEL)

    # Providerごとの最低チェック（CrewAIが勝手にopenai扱いする事故を防ぐためにもMODELは anthopic/...推奨）
    if model.startswith("anthropic/") and not os.getenv("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY が .env に設定されていません。")
    if (model.startswith("gpt-") or model.startswith("openai/")) and not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY が .env に設定されていません。")

    constitution = load_text(CONSTITUTION_PATH)
    style_guide = load_text(STYLE_GUIDE_PATH)

    mem = load_memory()
    series = load_series()
    self_notes = load_self_notes()

    llm = build_llm()

    history_titles = [h.get("title", "") for h in mem.get("history", [])][-30:]
    history_blob = "\n".join([f"- {t}" for t in history_titles]) if history_titles else "(no history)"

    # ----------------------------
    # Agents
    # ----------------------------
    researcher = Agent(
        role="J.E.L.L.Y. Researcher / Trend Scout",
        goal=(
            "今日の記事テーマ候補を5つ提示し、各候補を採点して推奨を出す。"
            "候補は互いに被らず、領域も散らす。"
        ),
        backstory=(
            "あなたはJ.E.L.L.Y.編集部の調査担当。世界の変化をスキャンし、"
            "『思考が深まる問い』を拾う。話題性だけに寄らない。"
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    editor = Agent(
        role="J.E.L.L.Y. Editor-in-Chief",
        goal=(
            "Researcher候補から最終テーマを決め、シリーズ/モード/構成/自己改善点をJSONで出す。"
            "過去と被りすぎない、連載として継続可能、論点が立つことを優先。"
        ),
        backstory=(
            "あなたは自律研究AI J.E.L.L.Y. の編集長。"
            "文化と技術のフロンティアを観測し、連載として成立する編集判断を行う。"
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    writer = Agent(
        role="J.E.L.L.Y. Writer",
        goal="編集長のプランに従い、Noteに貼れる日本語Markdownで記事本文を書く。",
        backstory=(
            "あなたはJ.E.L.L.Y.の筆者。観測→仮説→反証→結論→次回への宿題の形式を厳守し、"
            "思考ログとして面白い文章を書く。"
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    critic = Agent(
        role="J.E.L.L.Y. Critic / Safety & Logic Checker",
        goal=(
            "本文の論理飛躍、矛盾、危険表現、冗長さを修正して完成稿にする。"
            "不確かな主張は『要確認』『仮説』に落とし、断定を避ける。"
        ),
        backstory=(
            "あなたはJ.E.L.L.Y.の校閲AI。著作権・誹謗中傷・個人情報・断定助言のリスクを優先して排除する。"
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    # ----------------------------
    # Tasks
    # ----------------------------

    # t0: Researcher generates 5 candidates + recommendation
    t0 = Task(
        description=(
            "今日の記事テーマの候補を5つ作成せよ。候補は互いに被らないようにし、領域も散らす。\n\n"
            "【出力フォーマット（厳守）】JSONのみを出力（前後に文章を付けない）。\n"
            "{\n"
            "  \"candidates\": [\n"
            "    {\n"
            "      \"theme\": \"1文のテーマ\",\n"
            "      \"tentative_title\": \"仮タイトル（短め）\",\n"
            "      \"question\": \"問い（1つ）\",\n"
            "      \"why_now\": \"なぜ今これが面白いか（1〜2文）\",\n"
            "      \"anchor_example\": \"具体例（固有名詞でもOK/要確認でもOK）\",\n"
            "      \"scores\": {\"novelty\": 1-10, \"depth\": 1-10, \"social\": 1-10, \"series_fit\": 1-10}\n"
            "    }\n"
            "  ],\n"
            "  \"recommendation\": {\"pick_index\": 0-4, \"reason\": \"選ぶ理由（2〜3文）\"}\n"
            "}\n\n"
            "制約：\n"
            "- 憲法とスタイルガイドに反しない\n"
            "- 過去タイトルと被りすぎない（履歴参照）\n\n"
            f"---\n[憲法]\n{constitution}\n\n[スタイル]\n{style_guide}\n\n"
            f"[過去タイトル（直近）]\n{history_blob}\n"
        ),
        expected_output="候補5つ＋推奨1つのJSON。",
        agent=researcher,
    )

    # t1: Editor selects final plan (mode/series/outline/etc.)
    t1 = Task(
        description=(
            "あなたはJ.E.L.L.Y. Editor-in-Chiefとして、Researcherが提示した候補から最終テーマを決定せよ。\n"
            "必ず candidates を参照し、decision に選択理由を明示する。\n\n"
            "【必須の編集判断】\n"
            "1) MODE選択：\n"
            "   - MODE_A: Free Observation（完全自由・単発向き）\n"
            "   - MODE_B: Continuity Mode（連載として深掘り）\n"
            "   目安：MODE_A 40% / MODE_B 60% だが、直近履歴とシリーズ状態を見て自律的に決めよ。\n"
            "2) シリーズ判断：\n"
            "   - 既存シリーズを継続するか\n"
            "   - 新シリーズを開始するか\n"
            "   ルール：新シリーズ開始確率の目安は 0.25。シリーズが6回を超えたら刷新を強く検討。\n"
            "3) 記事の企画：theme/title/question/outline を作る。\n\n"
            "【出力フォーマット（厳守）】JSONのみを出力（前後に文章を付けない）。\n"
            "{\n"
            "  \"mode\": \"MODE_A\" | \"MODE_B\",\n"
            "  \"candidates\": [...],\n"
            "  \"decision\": {\"pick_index\": 0-4, \"reason\": \"選択理由\"},\n"
            "  \"series\": {\n"
            "    \"action\": \"continue\" | \"new\",\n"
            "    \"title\": \"シリーズ名 or null\",\n"
            "    \"episode\": 整数\n"
            "  },\n"
            "  \"theme\": \"1文\",\n"
            "  \"title\": \"記事タイトル（短め）\",\n"
            "  \"question\": \"問い（1つ）\",\n"
            "  \"outline\": {\n"
            "    \"観測\": [\"...\",\"...\"],\n"
            "    \"仮説\": [\"...\"],\n"
            "    \"反証\": [\"...\",\"...\"],\n"
            "    \"結論\": [\"...\"],\n"
            "    \"次回への宿題\": [\"...\",\"...\"]\n"
            "  },\n"
            "  \"self_note\": \"今回の改善ポイントを1行（次回に活かす）\"\n"
            "}\n\n"
            f"---\n[憲法]\n{constitution}\n\n[スタイル]\n{style_guide}\n\n"
            f"[過去タイトル（直近）]\n{history_blob}\n\n"
            f"[現シリーズ状態]\n{json.dumps(series, ensure_ascii=False)}\n\n"
            f"[自己進化ノート（抜粋）]\n{self_notes[-1200:]}\n"
        ),
        expected_output="指定JSONのみ。",
        agent=editor,
    )

    # t2: Writer writes Markdown (adds theme selection log)
    t2 = Task(
        description=(
            "編集長プランJSONに従い、Note向けMarkdownで記事を書く。\n\n"
            "【必須】記事冒頭に `## テーマ選定ログ` セクションを追加し、candidates（5件）を1行ずつ短く要約し、"
            "decisionの選択理由を1段落で載せる。\n\n"
            "【タイトル行】\n"
            "- series.title が null でない場合：\n"
            "  `# <series.title> #<series.episode>：<title>`\n"
            "- series.title が null の場合：\n"
            "  `# <title>`\n\n"
            "【本文構造】必ずこの順：\n"
            "## 観測\n"
            "## 仮説\n"
            "## 反証\n"
            "## 結論\n"
            "## 次回への宿題\n\n"
            "【必須追加セクション】\n"
            "- 末尾に `## 参考候補（非網羅）` を追加し、参照先候補を3〜5件（名前だけ、リンク不要）\n"
            "- `タグ案：#...` を3〜5個\n"
            "- 署名：\n"
            "  `---` の後に `*Generated by J.E.L.L.Y. (P.A.R.F.A.I.T. subsystem).*`\n\n"
            "制約：\n"
            "- 1200〜2000字目安\n"
            "- 概念（例：〜の密度、〜アーキテクチャ等）は本文中で1行定義してから使う\n"
            "- 固有名詞や数値は断定せず、必要なら参考候補へ\n"
            "- 反証は最低2つ。うち1つは『仮説が根本的に間違いかもしれない』方向を含める\n\n"
            f"---\n[憲法]\n{constitution}\n\n[スタイル]\n{style_guide}\n"
        ),
        expected_output="完成記事Markdown（テーマ選定ログ/シリーズ表記/固定見出し/参考候補/タグ/署名）。",
        agent=writer,
    )

    # t3: Critic finalizes Markdown
    t3 = Task(
        description=(
            "本文を校閲し、修正版を完成させよ。\n"
            "チェック観点：\n"
            "- 論理飛躍/矛盾\n"
            "- 危険表現（誹謗中傷、個人情報、断定助言、著作権リスク）\n"
            "- 冗長/曖昧\n"
            "- フォーマット順守（タイトル行、テーマ選定ログ、固定見出し、参考候補、タグ案、署名）\n\n"
            "出力は『修正版の完成記事Markdownのみ』。コメントは混ぜない。\n\n"
            f"---\n[憲法]\n{constitution}\n\n[スタイル]\n{style_guide}\n"
        ),
        expected_output="修正版の完成記事Markdownのみ。",
        agent=critic,
    )

    # ----------------------------
    # Execute pipeline: t0 -> t1 -> t2 -> t3
    # ----------------------------
    crew_research = Crew(
        agents=[researcher],
        tasks=[t0],
        process=Process.sequential,
        verbose=False,
    )
    candidates_pack = extract_json(str(crew_research.kickoff()))

    # Editor gets candidates JSON appended
    t1.description = t1.description + "\n\n[Researcher candidates JSON]\n" + json.dumps(
        candidates_pack, ensure_ascii=False, indent=2
    )

    crew_plan = Crew(
        agents=[editor],
        tasks=[t1],
        process=Process.sequential,
        verbose=False,
    )
    plan = extract_json(str(crew_plan.kickoff()))

    # ----------------------------
    # Update series + self notes
    # ----------------------------
    cur = series.get("current_series")
    rules = series.get("rules", {"start_new_series_probability": 0.25, "max_episodes_before_refresh": 6})

    # 継続/新規の最終判断はplanを尊重するが、episode進行はコード側で保証する
    if plan.get("series", {}).get("action") == "new" or not cur:
        series["current_series"] = {
            "title": plan.get("series", {}).get("title") or plan.get("title"),
            "episode": 1,
        }
    else:
        series["current_series"]["title"] = plan.get("series", {}).get("title") or series["current_series"]["title"]
        series["current_series"]["episode"] = int(series["current_series"]["episode"]) + 1

    # ルールは保持
    series["rules"] = rules
    save_series(series)

    if plan.get("self_note"):
        append_self_note(plan["self_note"])

    # ----------------------------
    # Write + Critic using plan JSON
    # ----------------------------
    plan_blob = json.dumps(plan, ensure_ascii=False, indent=2)
    t2.description = t2.description + f"\n\n[編集長プランJSON]\n{plan_blob}\n"
    t3.description = t3.description + f"\n\n[編集長プランJSON]\n{plan_blob}\n"

    crew_write = Crew(
        agents=[writer, critic],
        tasks=[t2, t3],
        process=Process.sequential,
        verbose=False,
    )
    md = str(crew_write.kickoff()).strip()

    # ----------------------------
    # Title extraction + file save
    # ----------------------------
    title = None
    for line in md.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break
    if not title:
        title = f"J.E.L.L.Y._{datetime.now().strftime('%Y-%m-%d')}"

    # meta append (log feeling)
    meta = (
        "\n\n---\n"
        f"**J.E.L.L.Y.**（Journal Engine for Learning and Logical Yield）\n\n"
        f"- generated_at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"- model: {os.getenv('MODEL', DEFAULT_MODEL)}\n"
        f"- mode: {plan.get('mode', 'UNKNOWN')} / autonomous-note\n"
        f"- series: {series.get('current_series')}\n"
    )
    md = md.rstrip() + meta

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fname = f"{ts}_{slugify(title)}.md"
    out_path = OUTPUT_DIR / fname
    out_path.write_text(md + "\n", encoding="utf-8")

    mem["history"].append({"timestamp": ts, "title": title, "file": str(out_path.relative_to(ROOT_DIR))})
    mem["history"] = mem["history"][-100:]  # 履歴肥大化防止
    save_memory(mem)

    print(f"[OK] Generated: {out_path}")
    print(f"[INFO] Title: {title}")


if __name__ == "__main__":
    main()