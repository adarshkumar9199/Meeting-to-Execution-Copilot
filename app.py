import re
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Meeting to Execution Copilot", page_icon="📝", layout="wide")
st.title("📝 Meeting to Execution Copilot")
st.caption("Turn meeting notes into reviewable summaries, decisions, blockers and action items.")

DEFAULT = """Decision: Launch the revised product page after QA approval.
Action: Priya to prepare the event tracking plan by 2026-12-05.
Action: Engineering team to share API readiness update by Friday.
Blocker: Analytics access is pending from the data team.
We agreed to review the checkout prototype in the next product sync."""
text = st.text_area("Paste meeting transcript or notes", value=DEFAULT, height=220)

ACTION_RE = re.compile(r"(?i)\b(action|todo|task)\s*:\s*(.+)")
DECISION_RE = re.compile(r"(?i)\b(decision|decided|agreed)\s*:\s*(.+)")
BLOCKER_RE = re.compile(r"(?i)\b(blocker|blocked|risk)\s*:\s*(.+)")
OWNER_RE = re.compile(r"(?i)^(.+?)\s+to\s+(.+)$")
DATE_RE = re.compile(r"\b(20\d{2}-\d{2}-\d{2})\b")

def parse_notes(raw):
    actions, decisions, blockers, summary = [], [], [], []
    for line in [x.strip(" -•\t") for x in raw.splitlines() if x.strip()]:
        m = ACTION_RE.search(line)
        if m:
            task = m.group(2).strip()
            owner, description = "", task
            om = OWNER_RE.match(task)
            if om:
                owner, description = om.group(1).strip(), om.group(2).strip()
            dm = DATE_RE.search(task)
            actions.append({"Task": description, "Owner": owner, "Due date": dm.group(1) if dm else "", "Status": "Open"})
            continue
        m = DECISION_RE.search(line)
        if m:
            decisions.append(m.group(2).strip()); continue
        m = BLOCKER_RE.search(line)
        if m:
            blockers.append(m.group(2).strip()); continue
        summary.append(line)
    return actions, decisions, blockers, summary

if st.button("Extract meeting outputs", type="primary"):
    st.session_state["outputs"] = parse_notes(text)

if "outputs" in st.session_state:
    actions, decisions, blockers, summary = st.session_state["outputs"]
    c1, c2, c3 = st.columns(3)
    c1.metric("Action items", len(actions)); c2.metric("Decisions", len(decisions)); c3.metric("Blockers", len(blockers))
    st.subheader("Summary"); st.write(" ".join(summary) if summary else "No general discussion lines detected.")
    st.subheader("Decisions")
    for item in decisions: st.markdown(f"- {item}")
    if not decisions: st.info("No explicitly labelled decisions found.")
    st.subheader("Blockers")
    for item in blockers: st.markdown(f"- {item}")
    if not blockers: st.info("No explicitly labelled blockers found.")
    st.subheader("Action items — review and edit before sharing")
    if actions:
        edited = st.data_editor(pd.DataFrame(actions), num_rows="dynamic", use_container_width=True)
        st.download_button("Download action items CSV", edited.to_csv(index=False).encode("utf-8"), "meeting_action_items.csv", "text/csv")
    else:
        st.info("No explicitly labelled action items found. Prefix tasks with 'Action:' to help the extractor.")
    st.warning("Heuristic MVP: verify names, owners, dates, decisions and blockers against the original meeting before acting.")
else:
    st.info("Paste notes and select Extract meeting outputs to see structured results.")
