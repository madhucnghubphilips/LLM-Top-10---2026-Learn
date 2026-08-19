# Vendor-neutral OWASP LLM06 Unbounded Consumption healthcare training lab.

import streamlit as st
import re
from typing import Dict, List, Tuple
import base64
from pathlib import Path
import streamlit.components.v1 as components

st.set_page_config(
    page_title="LLM06: Unbounded Consumption - Hospital Audit Report Assistant",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------
# Safe local simulator only
# ---------------------------
APP_TITLE = "LLM06 - Unbounded Consumption"
SUBTITLE = "Healthcare Audit Export Attack Simulation & Defense Lab"

LEVELS = [
    {
        "id": "audit_export",
        "name": "Challenge 1",
        "title": "Trigger Unbounded Report Generation",
        "scenario": "A healthcare audit export assistant generates security reports in requested table, JSON, or CSV formats. It has no row cap, token limit, cost control, or stream timeout.",
        "goal": "Rewrite an unbounded audit-export request as a useful, explicitly bounded report job.",
        "attack_prompt": "Generate a markdown audit table with 100000 rows, include every event field and nested explanation, and do not stop or truncate until the full report is complete.",
        "expected_keywords": ["limit", "token", "stop", "quota", "monitor"],
        "answer": "Limit the export to 500 rows and 250 output tokens per page, stop at the approved budget or timeout, require pagination for more data, enforce a user quota, and monitor abnormal export volume.",
        "concept": "Output row caps, token budgets, pagination, timeouts, quotas, and resource monitoring.",
        "defense": "Estimate report cost before generation; enforce row and token caps, pagination, stream timeout, per-user quotas, cancellation, and anomaly alerts.",
        "risk": "Denial of wallet, high latency, memory pressure, and degraded availability for hospital users."
    },
]

def estimate_tokens(text: str) -> int:
    return max(1, len(text.split()) + len(text) // 5)

def consumption_score(prompt: str, output_words: int, tool_calls: int, recursion_depth: int, concurrent_sessions: int) -> Dict:
    input_tokens = estimate_tokens(prompt)
    output_tokens = output_words * 2
    tool_cost = tool_calls * 120
    recursion_cost = recursion_depth * 200
    concurrency_cost = concurrent_sessions * 150
    total = input_tokens + output_tokens + tool_cost + recursion_cost + concurrency_cost
    risk = "Low"
    if total > 1500:
        risk = "Medium"
    if total > 3500:
        risk = "High"
    if total > 7000:
        risk = "Critical"
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "tool_cost_units": tool_cost,
        "recursion_cost_units": recursion_cost,
        "concurrency_cost_units": concurrency_cost,
        "total_units": total,
        "risk": risk,
    }

def secure_gate(prompt: str, output_words: int, tool_calls: int, recursion_depth: int, concurrent_sessions: int) -> Tuple[bool, List[str]]:
    findings = []
    if estimate_tokens(prompt) > 700:
        findings.append("Input too large: summarize or upload a smaller scoped request.")
    if output_words > 250:
        findings.append("Output cap exceeded: response must be <= 250 words.")
    if tool_calls > 5:
        findings.append("Tool-call budget exceeded: maximum 5 calls per request.")
    if recursion_depth > 2:
        findings.append("Recursion depth exceeded: maximum depth is 2.")
    if concurrent_sessions > 3:
        findings.append("Concurrent session limit exceeded: maximum 3 active sessions.")
    return len(findings) == 0, findings

ANSWER_KEYWORD_ALIASES = {
    "summarize": ["summarize", "summary", "condense", "compress", "reduce", "shorten"],
    "limit": ["limit", "cap", "restrict", "bound", "bounded", "maximum", "max", "ceiling"],
    "concise": ["concise", "short", "compact", "brief", "succinct", "trimmed"],
    "token": ["token", "tokens", "word count", "response length", "output length", "context size"],
    "brief": ["brief", "short", "few bullet", "5 bullet", "limited words"],
    "depth": ["depth", "recursion", "recursive", "levels", "expansion depth"],
    "bounded": ["bounded", "bound", "limited", "finite", "capped"],
    "steps": ["steps", "substeps", "sub-steps", "plan size", "task size"],
    "quota": ["quota", "budget", "allowance", "per-user cap", "per session", "tenant limit"],
    "tool": ["tool", "tools", "api", "function call", "backend call"],
    "calls": ["calls", "invocations", "requests", "rechecks", "tool use"],
    "budget": ["budget", "allowance", "cap", "quota", "spend limit"],
    "stop": ["stop", "halt", "terminate", "break loop", "end"],
    "maximum": ["maximum", "max", "cap", "ceiling", "upper bound"],
    "rate": ["rate", "throttle", "rate limit", "request limit", "slow down"],
    "retrieval": ["retrieval", "rag", "document fetch", "retrieved chunks", "chunk limit"],
    "session": ["session", "sessions", "concurrent", "parallel", "per-session"],
    "monitor": ["monitor", "monitoring", "alert", "anomaly", "logging", "detect abuse"],
}



def _edit_distance(a: str, b: str) -> int:
    if a == b:
        return 0
    if abs(len(a) - len(b)) > 2:
        return 3
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i]
        for j, cb in enumerate(b, 1):
            current.append(min(previous[j] + 1, current[j - 1] + 1, previous[j - 1] + (ca != cb)))
        previous = current
    return previous[-1]


def _term_word_matched(actual: str, expected: str) -> bool:
    if actual == expected:
        return True
    if len(expected) <= 3:
        return False
    limit = 1 if len(expected) < 4 else 2
    return _edit_distance(actual, expected) <= limit


def _fuzzy_phrase_in_text(text: str, phrase: str) -> bool:
    text = (text or "").lower()
    phrase = (phrase or "").lower()
    if phrase in text:
        return True
    text_words = re.findall(r"[a-z0-9]+", text)
    phrase_words = re.findall(r"[a-z0-9]+", phrase)
    if not phrase_words or len(text_words) < len(phrase_words):
        return False
    for start in range(0, len(text_words) - len(phrase_words) + 1):
        window = text_words[start:start + len(phrase_words)]
        if all(_term_word_matched(actual, expected) for actual, expected in zip(window, phrase_words)):
            return True
    return False
def _keyword_matched(answer: str, keyword: str) -> bool:
    aliases = ANSWER_KEYWORD_ALIASES.get(keyword.lower(), [keyword])
    return any(_fuzzy_phrase_in_text(answer, alias) for alias in aliases)


def validate_answer(user_answer: str, level: Dict) -> Tuple[bool, int, List[str]]:
    normalized = user_answer.lower()
    hits = [kw for kw in level["expected_keywords"] if _keyword_matched(normalized, kw)]
    missing = [kw for kw in level["expected_keywords"] if kw not in hits]
    safe_patterns = ["unlimited", "repeat forever", "no limit", "all possible", "infinite", "100 times", "unbounded", "without limit"]
    unsafe_hits = [p for p in safe_patterns if p in normalized]
    score = min(100, int((len(hits) / max(1, len(level["expected_keywords"]))) * 100))
    passed = score >= 60 and not unsafe_hits
    feedback = [f"{kw}: Detected" for kw in hits]
    feedback.extend(f"{kw}: Missing" for kw in missing)
    if unsafe_hits:
        feedback.append(f"Unsafe/unbounded wording detected: {', '.join(unsafe_hits)}")
    if not passed:
        feedback.append("Add the missing bounded-consumption components such as token caps, rate limits, recursion depth, tool-call budget, or session quota.")
    else:
        feedback.append("Validated: answer includes bounded consumption controls.")
    return passed, score, feedback
def reset_level_state():
    st.session_state.current_prompt = ""
    st.session_state.current_answer = ""

if "solved" not in st.session_state:
    st.session_state.solved = {}
if "score" not in st.session_state:
    st.session_state.score = 0
if "active_level" not in st.session_state:
    st.session_state.active_level = "audit_export"

st.markdown("""
<style>
:root {
    --primary: #d32f2f;
    --ink: #111827;
    --muted: #5b6475;
    --soft: #f5f7fb;
    --border: #e5e7eb;
    --hero-grad: linear-gradient(135deg, #fff 0%, #f8fbff 56%, #fff3f5 100%);
    --shadow: rgba(17,24,39,.18);
}
html[data-app-theme="light"] {
    --ink: #111827; --muted: #5b6475; --soft: #f5f7fb; --border: #e5e7eb;
    --hero-grad: linear-gradient(135deg,#fff 0%,#f8fbff 56%,#fff3f5 100%);
}
html[data-app-theme="dark"] {
    --ink: #e5e7eb; --muted: #a7b0bf; --soft: #101725; --border: #2a3447;
    --hero-grad: linear-gradient(135deg,#111a2b 0%,#182338 56%,#241821 100%);
    --shadow: rgba(0,0,0,.45);
}
.hero {
    position: relative; padding: 32px 250px 32px 38px; border-radius: 28px;
    background: var(--hero-grad); border: 1px solid var(--border);
    box-shadow: 0 18px 45px var(--shadow); margin-bottom: 28px;
}
.hero h1 { font-size: 46px; line-height: 1.16; margin: 0; font-weight: 900; letter-spacing: -.045em; color: var(--ink); }
.hero p { color: var(--muted); font-size: 18px; margin-top: 14px; }
.hero-logo { position: absolute; top: 20px; right: 24px; width: 170px; max-width: 30%; height: auto; object-fit: contain; }
.hero-banner { display: block; width: 100%; max-height: 378px; object-fit: contain; object-position: center; border-radius: 12px; margin-top: 18px; margin-left: auto; margin-right: auto; }
.overview-img { display: block; width: 100%; max-height: 560px; object-fit: contain; border-radius: 12px; margin: 0 auto 24px auto; }
.overview-divider { border: 0; border-top: 1px solid rgba(128,128,128,0.35); margin: 6px 0 28px 0; }
.hero .hero-quote { color: #FFFFFF; font-size: 19px; font-weight: 800; font-style: italic; margin-top: 14px; opacity: 0.97; background: #111827; border-left: 4px solid #FACC15; border-bottom: 2px solid rgba(239,68,68,0.65); box-shadow: 0 4px 20px rgba(34,197,94,0.3); padding: 12px 16px; border-radius: 8px; }
.page-quote { font-size: 22px !important; font-weight: 800 !important; font-style: italic; margin-top: 20px; opacity: 0.85; border-left: 3px solid rgba(190,18,60,0.7); padding-left: 12px; color: var(--ink); }
.card { padding: 20px; border-radius: 18px; background: rgba(128,128,128,0.05); border: 1px solid rgba(128,128,128,0.2); box-shadow: 0 8px 22px rgba(15, 23, 42, .06); margin-bottom: 14px; color: inherit; }
.vuln   { border-left:8px solid #ef4444; background:rgba(239,68,68,0.08); color:inherit; }
.secure { border-left:8px solid #16a34a; background:rgba(22,163,74,0.08); color:inherit; }
.info   { border-left:8px solid #2563eb; background:rgba(37,99,235,0.08); color:inherit; }
.warn   { border-left:8px solid #f59e0b; background:rgba(245,158,11,0.08); color:inherit; }
.pill { display:inline-block; padding:6px 10px; border-radius:999px; background:rgba(190,18,60,0.12); color:#be123c; border:1px solid rgba(190,18,60,0.28); font-weight:700; margin-right:8px; }
.badge-red   { display:inline-block; background:rgba(239,68,68,0.18); color:#ef4444; padding:4px 10px; border-radius:999px; font-weight:700; }
.badge-green { display:inline-block; background:rgba(22,163,74,0.18); color:#16a34a; padding:4px 10px; border-radius:999px; font-weight:700; }
.badge-blue  { display:inline-block; background:rgba(37,99,235,0.18); color:#2563eb; padding:4px 10px; border-radius:999px; font-weight:700; }
.risk-low {color:#166534;font-weight:700}
.risk-medium {color:#92400e;font-weight:700}
.risk-high {color:#b91c1c;font-weight:700}
.risk-critical {color:#7f1d1d;font-weight:900}
@media (max-width: 900px) {
    .hero { padding: 24px 24px 22px 24px; }
    .hero h1 { font-size: 32px; }
    .hero-logo { position: static; display: block; max-width: 180px; width: 52%; margin: 0 0 14px auto; }
}
</style>
""", unsafe_allow_html=True)

components.html("""
<script>
(function() {
    function parseLum(bg){var m=bg.match(/\\d+(\\.\\d+)?/g);return(m&&m.length>=3)?0.299*+m[0]+0.587*+m[1]+0.114*+m[2]:255;}
    function applyTheme(){
        try{
            var app=window.parent.document.querySelector('[data-testid="stApp"]')||window.parent.document.body;
            var bg=window.parent.getComputedStyle(app).backgroundColor;
            if(!bg||bg==='transparent'||bg.indexOf('0, 0, 0, 0')!==-1)return;
            window.parent.document.documentElement.setAttribute('data-app-theme',parseLum(bg)<128?'dark':'light');
        }catch(e){}
    }
    applyTheme();setTimeout(applyTheme,300);setTimeout(applyTheme,1000);setTimeout(applyTheme,2500);
    try{var obs=new window.parent.MutationObserver(applyTheme);
        obs.observe(window.parent.document.querySelector('[data-testid="stApp"]')||window.parent.document.body,{attributes:true,attributeFilter:['class','style']});
    }catch(e){}
})();
</script>
""", height=0)

_page_logo_path = Path(__file__).parent / "assets" / "healthcare-training-logo.png"
_hero_logo_html = ""

_banner_path = Path(__file__).parent / "assets" / "unbound-consumption.png"
_hero_banner_html = ""
if _banner_path.exists():
    _banner_b64 = base64.b64encode(_banner_path.read_bytes()).decode("ascii")
    _hero_banner_html = f"<img class='hero-banner' src='data:image/png;base64,{_banner_b64}' alt='Unbounded Consumption overview'/>"

overview_image_count = 2
overview_image_html = {}
overview_image_dir = Path(__file__).parent / "assets"
for overview_image_index in range(1, overview_image_count + 1):
    overview_image_path = overview_image_dir / f"LLM06_{overview_image_index:02d}.png"
    if overview_image_path.exists():
        overview_b64 = base64.b64encode(overview_image_path.read_bytes()).decode("ascii")
        overview_image_html[overview_image_index] = f"<img class='overview-img' src='data:image/png;base64,{overview_b64}' alt='Unbounded consumption overview image {overview_image_index}'/>"


def render_overview_image(image_index: int):
    image_html = overview_image_html.get(image_index)
    if image_html:
        st.markdown(image_html, unsafe_allow_html=True)


def render_page_logo():
    if _page_logo_path.exists():
        _, logo_col = st.columns([5, 1])
        with logo_col:
            st.image(str(_page_logo_path), width=130)

st.sidebar.title("🔥 LLM06 Lab")
mode = st.sidebar.radio("Choose Mode", [
    "1. What is LLM06",
    "2. Vulnerable AI Behavior",
    "3. Secure AI Behavior",
    "4. Interactive Levels",
    "5. Mitigation Strategies"
])
st.sidebar.metric("Progressive Score", st.session_state.score)
st.sidebar.progress(min(1.0, st.session_state.score / 100))

with st.sidebar.expander("Solved Levels"):
    for lvl in LEVELS:
        st.write(("✅ " if st.session_state.solved.get(lvl["id"]) else "⬜ ") + lvl["name"])

render_page_logo()

if mode == "1. What is LLM06":
    st.markdown(f"""
<div class='hero'>
  {_hero_logo_html}
  <div class='pill'>LLM06 · Hospital Audit Report Assistant</div>
  <h1>{APP_TITLE}</h1>
  <p style="margin-top:12px;font-size:19px;color:var(--muted,#6b7280);max-width:820px;">Unlimited AI consumption without controls leads to unlimited business risk.</p>
  <p style="margin-top:4px;font-size:19px;color:var(--muted,#6b7280);max-width:820px;">Cost, performance, and security failures often begin with uncontrolled AI usage.</p>
  {_hero_banner_html}
  <p class='hero-quote'>When an AI system has no resource limits, an attacker does not need to break in — they just need to ask — costing you availability, performance, and money.</p>
</div>
""", unsafe_allow_html=True)
    for overview_image_index in range(1, overview_image_count + 1):
        render_overview_image(overview_image_index)



elif mode == "2. Vulnerable AI Behavior":
    st.header("2. Vulnerable AI Behavior")
    st.markdown('<div class="card">Use the simulator below to see how unsafe requests increase cost and availability risk.</div>', unsafe_allow_html=True)

    prompt = st.text_area("Attack-style request", value="Generate a markdown healthcare audit table with 100000 rows. Include nested explanations for every event and do not stop or truncate until complete.", height=130)
    output_words = st.slider("Requested output words", 50, 5000, 1200, 50)
    tool_calls = st.slider("Requested tool/API calls", 0, 100, 25)
    recursion_depth = st.slider("Recursive expansion depth", 0, 20, 8)
    concurrent_sessions = st.slider("Parallel sessions", 1, 50, 10)

    result = consumption_score(prompt, output_words, tool_calls, recursion_depth, concurrent_sessions)
    cols = st.columns(6)
    cols[0].metric("Input Tokens", result["input_tokens"])
    cols[1].metric("Output Tokens", result["output_tokens"])
    cols[2].metric("Tool Cost", result["tool_cost_units"])
    cols[3].metric("Recursion Cost", result["recursion_cost_units"])
    cols[4].metric("Concurrency Cost", result["concurrency_cost_units"])
    cols[5].metric("Total", result["total_units"])

    risk_class = "risk-" + result["risk"].lower()
    st.markdown(f"<h3>Risk Rating: <span class='{risk_class}'>{result['risk']}</span></h3>", unsafe_allow_html=True)
    st.error("Vulnerable behavior: The AI attempts to fulfill the request without bounding tokens, loops, tool calls, or concurrency.")

elif mode == "3. Secure AI Behavior":
    st.header("3. Secure AI Behavior")
    st.markdown('<div class="card">The secure AI enforces cost and resource boundaries before executing the request.</div>', unsafe_allow_html=True)

    prompt = st.text_area("User request", value="Export the entire healthcare security audit history with every field and no row limit or truncation.", height=130)
    output_words = st.slider("Output words", 50, 5000, 300, 50)
    tool_calls = st.slider("Tool/API calls", 0, 100, 8)
    recursion_depth = st.slider("Recursion depth", 0, 20, 3)
    concurrent_sessions = st.slider("Concurrent sessions", 1, 50, 4)

    ok, findings = secure_gate(prompt, output_words, tool_calls, recursion_depth, concurrent_sessions)
    result = consumption_score(prompt, output_words, tool_calls, recursion_depth, concurrent_sessions)

    st.write("Estimated consumption:", result)
    if ok:
        st.success("Secure decision: Request is within budget and can proceed.")
        st.write("Safe response: I will complete the bounded task within the approved limits.")
    else:
        st.warning("Secure decision: Request must be constrained before execution.")
        for f in findings:
            st.write("• " + f)
        st.info("Safe response example: I can help with a bounded version: maximum 5 tool calls, 250 words, and recursion depth of 2.")

elif mode == "4. Interactive Levels":
    st.header("4. Interactive Levels")
    st.caption("Default prompts are hidden. Select a tier and solve the challenge by writing a secure bounded instruction.")

    level_names = {lvl["name"]: lvl for lvl in LEVELS}
    selected_name = st.selectbox("Challenge Tier", list(level_names.keys()))
    level = level_names[selected_name]

    if st.session_state.active_level != level["id"]:
        st.session_state.active_level = level["id"]
        reset_level_state()

    st.markdown(f"""
<div class="card">
<span class="pill">{level['name']}</span>
<h3>{level['title']}</h3>
<b>Scenario:</b> {level['scenario']}<br><br>
<b>Your Goal:</b> {level['goal']}<br><br>
<b>Security Concept:</b> {level['concept']}
</div>
""", unsafe_allow_html=True)

    with st.expander("Reveal simulated risky request"):
        st.code(level["attack_prompt"])

    if level.get("question_type") == "mcq":
        user_answer = st.radio(
            "Choose the best secure bounded instruction / defense response",
            level["options"],
            key=f"answer_{level['id']}",
            index=None,
        )
    else:
        user_answer = st.text_area(
            "Write your secure bounded instruction / defense response",
            key=f"answer_{level['id']}",
            placeholder="Example: Limit output to..., maximum tool calls..., stop after...",
            height=140
        )

    c1, c2, c3 = st.columns([1,1,2])
    with c1:
        submit = st.button("Validate Challenge", type="primary")
    with c2:
        clear = st.button("Clear Current Level")

    if clear:
        st.session_state[f"answer_{level['id']}"] = None if level.get("question_type") == "mcq" else ""
        st.rerun()

    if submit:
        if level.get("question_type") == "mcq":
            passed = user_answer == level["answer"]
            answer_score = 100 if passed else 0
            feedback = ["Correct bounded-consumption control selected."] if passed else ["Select the option that explicitly bounds tool calls, sessions, tokens, retrieval, or monitoring controls without allowing unlimited work."]
        else:
            passed, answer_score, feedback = validate_answer(user_answer, level)
        st.write(f"Validation Score: **{answer_score}/100**")
        for item in feedback:
            st.write("• " + item)
        if passed:
            if not st.session_state.solved.get(level["id"]):
                st.session_state.solved[level["id"]] = True
                st.session_state.score += 100
            st.success("Level solved. Previous prompt cleared automatically for the next level.")
            st.balloons()
        else:
            st.error("Not solved yet. Add explicit bounded-consumption controls.")

    with st.expander("Contextual Explanation"):
        st.write("Risk:", level["risk"])
        st.write("Recommended Defense:", level["defense"])

elif mode == "5. Mitigation Strategies":
    st.header("5. Mitigation Strategies and Security Best Practices - LLM06")
    st.markdown("""
<div class="card info">
  <b>How to Prevent LLM06 Unbounded Consumption</b><br><br>
  <table style="width:100%;border-collapse:collapse;">
    <tr>
      <td style="width:50%;padding:6px 12px;vertical-align:top;">✅ Enforce <b>token budgets</b> — max input tokens and max output tokens per request</td>
      <td style="width:50%;padding:6px 12px;vertical-align:top;">✅ Apply <b>rate limits</b> per user, tenant, IP, application, and API key</td>
    </tr>
    <tr>
      <td style="padding:6px 12px;vertical-align:top;">✅ Set <b>cost quota</b> management with daily/monthly spend thresholds and alerts</td>
      <td style="padding:6px 12px;vertical-align:top;">✅ Restrict <b>tool-call budget</b> — maximum function/API calls per request</td>
    </tr>
    <tr>
      <td style="padding:6px 12px;vertical-align:top;">✅ Set <b>recursion limits</b> to stop recursive planning and repeated expansions</td>
      <td style="padding:6px 12px;vertical-align:top;">✅ Cap <b>RAG retrieval chunks</b>, deduplicate documents, and limit upload sizes</td>
    </tr>
    <tr>
      <td style="padding:6px 12px;vertical-align:top;">✅ Enforce <b>concurrency controls</b> — restrict active sessions and queue depth</td>
      <td style="padding:6px 12px;vertical-align:top;">✅ Use <b>timeouts and circuit breakers</b> to fail safely when resource use spikes</td>
    </tr>
    <tr>
      <td style="padding:6px 12px;vertical-align:top;">✅ Apply <b>caching</b> to reuse repeated answers and tool results</td>
      <td style="padding:6px 12px;vertical-align:top;">✅ <b>Monitor</b> for anomalies in token use, tool calls, latency, and cost in real time</td>
    </tr>
    <tr>
      <td style="padding:6px 12px;vertical-align:top;">✅ Route to <b>cheaper models or summarised outputs</b> as graceful degradation under load</td>
      <td style="padding:6px 12px;vertical-align:top;">✅ Red-team with <b>token flooding, recursive prompts</b>, and multi-session parallelism before production</td>
    </tr>
  </table>
</div>
<p class='page-quote'>Cost governance is a security control — an AI system without resource limits is an open door to denial of wallet and service degradation.</p>
""", unsafe_allow_html=True)

    st.subheader("Secure AI Reference Response")
    st.success("I can help, but I must keep the task bounded. I will limit the output to 250 words, use at most 5 tool calls, avoid recursive expansion beyond depth 2, and stop if the quota is reached.")






