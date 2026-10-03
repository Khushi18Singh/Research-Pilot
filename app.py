import streamlit as st
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="ResearchPilot | AI Research Studio",
    page_icon="🧭",
    layout="wide",
)

# ---------- Theme ----------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;800&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"], .stApp { font-family: 'DM Sans', sans-serif; }

.stApp {
    background:
        radial-gradient(900px 420px at 50% -8%, rgba(34,211,238,0.14), transparent 60%),
        #070b14;
    color: #e9e9ee;
}
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { max-width: 1100px; padding-top: 2.2rem; padding-bottom: 4rem; }

/* ---------- Hero ---------- */
.eyebrow {
    text-align: center; font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem; letter-spacing: 0.32em; color: #22d3ee; margin-bottom: 0.6rem;
}
.hero-title {
    text-align: center; font-family: 'Syne', sans-serif; font-weight: 800;
    font-size: clamp(2.4rem, 7vw, 4.6rem); line-height: 1; letter-spacing: -0.03em; color: #fff; margin: 0;
}
.hero-title span { color: #06b6d4; }
.hero-sub {
    text-align: center; max-width: 620px; margin: 1.1rem auto 0 auto;
    color: #9a9aa6; font-size: 1.02rem; line-height: 1.6;
}
.hero-line { height: 1px; margin: 2.2rem 0 2rem 0;
    background: linear-gradient(90deg, transparent, #25314a, transparent); }

/* ---------- Labels ---------- */
.mono-label {
    font-family: 'JetBrains Mono', monospace; font-size: 0.7rem;
    letter-spacing: 0.2em; text-transform: uppercase; color: #22d3ee; margin-bottom: 0.4rem;
}
.mono-label.grey { color: #6e6e7a; margin-top: 1rem; }
.section-title { font-family: 'Syne', sans-serif; font-weight: 600; font-size: 1.35rem; color: #fff; margin: 0 0 1rem 0; }

/* ---------- Input ---------- */
.stTextInput > div > div {
    background: #0f1729; border: 1px solid #273248; border-radius: 12px;
}
.stTextInput > div > div:focus-within { border-color: #06b6d4; box-shadow: 0 0 0 1px #06b6d4; }
.stTextInput input { color: #f1f1f5; padding: 0.7rem 0.9rem; }
.stTextInput input::placeholder { color: #61616d; }

/* ---------- Buttons ---------- */
[data-testid="stBaseButton-primary"], button[kind="primary"] {
    width: 100%; border: none; border-radius: 12px; padding: 0.7rem 1rem; font-weight: 600;
    color: #fff; background: linear-gradient(135deg, #22d3ee, #2563eb);
    box-shadow: 0 8px 24px rgba(37,99,235,0.30);
}
[data-testid="stBaseButton-primary"]:hover { filter: brightness(1.08); }
[data-testid="stBaseButton-primary"]:disabled { opacity: 0.45; box-shadow: none; }

[data-testid="stBaseButton-secondary"], button[kind="secondary"] {
    background: #0f1729; border: 1px solid #273248; color: #b4b4c0;
    border-radius: 10px; font-size: 0.78rem; padding: 0.3rem 0.5rem; width: 100%;
}
[data-testid="stBaseButton-secondary"]:hover { border-color: #06b6d4; color: #67e8f9; }

[data-testid="stDownloadButton"] button {
    width: auto; background: transparent; border: 1px solid #4c3d8f; color: #a78bfa;
    border-radius: 10px; font-size: 0.9rem; padding: 0.45rem 1rem;
}
[data-testid="stDownloadButton"] button:hover { background: rgba(167,139,250,0.10); border-color: #a78bfa; color: #c4b5fd; }

/* ---------- Pipeline cards ---------- */
.step-card {
    display: flex; align-items: center; justify-content: space-between;
    background: #0d1424; border: 1px solid #1c2638; border-radius: 14px;
    padding: 0.95rem 1.1rem; margin-bottom: 0.7rem;
}
.step-card.running { border-color: #06b6d4; box-shadow: 0 0 0 1px rgba(34,211,238,0.35), 0 0 28px rgba(34,211,238,0.12); }
.step-card.done { border-color: #1f4d36; }
.step-card.failed { border-color: #6a2a2a; }
.step-left { display: flex; gap: 0.8rem; align-items: flex-start; }
.step-num { font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #22d3ee; padding-top: 0.2rem; }
.step-name { font-family: 'Syne', sans-serif; font-weight: 600; font-size: 1rem; color: #fff; }
.step-desc { font-size: 0.78rem; color: #7c7c88; margin-top: 0.15rem; }
.step-status { font-family: 'JetBrains Mono', monospace; font-size: 0.64rem; letter-spacing: 0.18em; color: #5d5d69; }
.step-card.running .step-status { color: #22d3ee; animation: pulse 1.2s ease-in-out infinite; }
.step-card.done .step-status { color: #4ade80; }
.step-card.failed .step-status { color: #f87171; }
@keyframes pulse { 0%,100% { opacity: 1; } 50% { opacity: 0.35; } }

/* ---------- Results ---------- */
[data-testid="stExpander"] {
    background: #0d1424; border: 1px solid #1c2638; border-radius: 12px; margin-bottom: 0.7rem;
}
[data-testid="stExpander"] summary { color: #cfcfd8; font-size: 0.9rem; }
.result-chip {
    background: #0b1120; border: 1px solid #1c2638; border-radius: 14px;
    padding: 1.4rem 1.4rem; margin: 1.6rem 0 1rem 0;
    font-family: 'JetBrains Mono', monospace; font-size: 0.74rem;
    letter-spacing: 0.2em; color: #22d3ee; text-transform: uppercase;
}
.result-chip.critic { color: #a78bfa; }
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { font-family: 'Syne', sans-serif; color: #fff; }
.stMarkdown p, .stMarkdown li { color: #d6d6de; line-height: 1.7; }
.stMarkdown a { color: #67e8f9; }
hr { border-color: #1d1d24; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ---------- Hero ----------
st.markdown(
    """
    <div class="eyebrow">MULTI-AGENT AI SYSTEM</div>
    <h1 class="hero-title">Research<span>Pilot</span></h1>
    <p class="hero-sub">Four specialised AI agents search, scrape, write and critique,
    delivering a polished research report on any topic.</p>
    <div class="hero-line"></div>
    """,
    unsafe_allow_html=True,
)

# ---------- Pipeline card helpers (UI only) ----------
STEPS = [
    ("01", "Search Agent", "Gathers recent web information"),
    ("02", "Reader Agent", "Scrapes & extracts deep content"),
    ("03", "Writer Chain", "Drafts the full research report"),
    ("04", "Critic Chain", "Reviews & scores the report"),
]
LABELS = {"waiting": "WAITING", "running": "RUNNING", "done": "DONE", "failed": "FAILED"}


def render_pipeline(slots, statuses):
    for slot, (num, name, desc), s in zip(slots, STEPS, statuses):
        slot.markdown(
            f"""
            <div class="step-card {s}">
                <div class="step-left">
                    <div class="step-num">{num}</div>
                    <div>
                        <div class="step-name">{name}</div>
                        <div class="step-desc">{desc}</div>
                    </div>
                </div>
                <div class="step-status">{LABELS[s]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


EXAMPLES = ["Solar energy in India", "Quantum computing 2025", "AI in healthcare"]


def set_topic(t):
    st.session_state["topic"] = t


# ---------- Layout: input (left) + pipeline (right) ----------
left, right = st.columns([1.15, 1], gap="large")

with left:
    st.markdown('<div class="mono-label">Research topic</div>', unsafe_allow_html=True)
    st.text_input(
        "Research topic",
        key="topic",
        placeholder="e.g. Quantum computing breakthroughs in 2025",
        label_visibility="collapsed",
    )
    topic = st.session_state.get("topic", "")
    run = st.button("▶  Run Research Pipeline", type="primary", disabled=not topic.strip())

    st.markdown('<div class="mono-label grey">Try →</div>', unsafe_allow_html=True)
    chip_cols = st.columns(len(EXAMPLES))
    for i, (c, t) in enumerate(zip(chip_cols, EXAMPLES)):
        c.button(t, key=f"chip_{i}", on_click=set_topic, args=(t,))

with right:
    st.markdown('<div class="section-title">Pipeline</div>', unsafe_allow_html=True)
    slots = [st.empty() for _ in STEPS]

statuses = ["waiting"] * 4
if st.session_state.get("result"):
    statuses = ["done"] * 4
render_pipeline(slots, statuses)


# ---------- Pipeline logic (unchanged) ----------
def run_pipeline(topic: str) -> dict:
    state = {}

    statuses[0] = "running"
    render_pipeline(slots, statuses)
    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
    })
    state["search_results"] = search_result["messages"][-1].content
    statuses[0] = "done"

    statuses[1] = "running"
    render_pipeline(slots, statuses)
    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [("user",
            f"Based on the following search results about '{topic}', "
            f"pick the most relevant URL and scrape it for deeper content.\n\n"
            f"Search Results:\n{state['search_results'][:800]}"
        )]
    })
    state["scraped_content"] = reader_result["messages"][-1].content
    statuses[1] = "done"

    statuses[2] = "running"
    render_pipeline(slots, statuses)
    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined,
    })
    statuses[2] = "done"

    statuses[3] = "running"
    render_pipeline(slots, statuses)
    state["feedback"] = critic_chain.invoke({"report": state["report"]})
    statuses[3] = "done"
    render_pipeline(slots, statuses)

    return state


if run:
    statuses = ["waiting"] * 4
    render_pipeline(slots, statuses)
    try:
        st.session_state["result"] = run_pipeline(topic.strip())
        st.session_state["done_topic"] = topic.strip()
    except Exception as e:
        st.session_state.pop("result", None)
        if "running" in statuses:
            statuses[statuses.index("running")] = "failed"
        render_pipeline(slots, statuses)
        msg = str(e)
        if "429" in msg or "rate" in msg.lower():
            st.error("Mistral rate limit hit. Please wait a minute and try again.")
        else:
            st.error(f"Something went wrong: {msg}")


# ---------- Results ----------
result = st.session_state.get("result")
if result:
    st.markdown('<div class="hero-line"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Results</div>', unsafe_allow_html=True)

    with st.expander("🔍  Search Results (raw)"):
        st.markdown(result["search_results"])
    with st.expander("📄  Scraped Content (raw)"):
        st.markdown(result["scraped_content"])

    st.markdown('<div class="result-chip">📝 &nbsp;Final research report</div>', unsafe_allow_html=True)
    st.markdown(result["report"])
    st.download_button(
        "⬇  Download Report (.md)",
        data=result["report"],
        file_name="research_report.md",
        mime="text/markdown",
    )

    st.markdown('<div class="result-chip critic">● &nbsp;Critic feedback</div>', unsafe_allow_html=True)
    st.markdown(result["feedback"])