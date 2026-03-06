import textwrap

import streamlit as st


def generate_star_bullets_llm(
    job_role: str, impact: str, challenges: str, num_points: int = 5
) -> list[str]:
    """
    Generate STAR bullets using an LLM (OpenAI as an example).
    It is not always necessary to generate all 5 bullet points; generate as many high-quality, quantifiable STAR bullets as are relevant (up to num_points).
    Each bullet must use a unique metric (no repeats of %/$/time/volume/scale per bullet), and each bullet should be concise—about 10 words in length.
    Falls back to an empty list if the client or API key is not configured.
    """

    if openai is None or not os.getenv("OPENAI_API_KEY"):
        return []

    prompt = f"""
You are an expert resume writer.

Generate exactly {num_points} resume bullet points that follow the STAR (Situation, Task, Action, Result) framework and are highly quantifiable.

Context:
- Job role: {job_role}
- Impact created: {impact}
- Challenges faced: {challenges}

Guidelines:
- Each bullet must start with a strong action verb.
- Each bullet must clearly describe the situation, the task, the actions taken, and the measurable result.
- Each bullet must contain at least one specific metric (%, $, time, volume, or scale).
- Avoid first person ("I", "my") and company‑specific confidential information.

Return ONLY the bullet points as a numbered list (e.g. "1. ...", "2. ..."), one per line.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a world-class resume writing assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.4,
        )
        text = response["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"LLM error while generating bullets: {e}")
        return []

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    bullets: list[str] = []

    for line in lines:
        # Strip leading numbering or dashes
        if line[0].isdigit():
            # Remove patterns like "1. " or "1)" etc.
            parts = line.split(".", 1)
            if len(parts) > 1 and parts[0].isdigit():
                line = parts[1].strip()
            else:
                parts = line.split(")", 1)
                if len(parts) > 1 and parts[0].isdigit():
                    line = parts[1].strip()
        if line.startswith("- "):
            line = line[2:].strip()

        if not line:
            continue

        bullets.append(textwrap.fill(line, width=100))

        if len(bullets) >= num_points:
            break

    return bullets[:num_points]


def main() -> None:
    st.set_page_config(
        page_title="Resume Bullet Generator (STAR)",
        page_icon="📝",
        layout="centered",
    )

    st.title("Resume Bullet Points Generator (STAR)")
    st.write(
        "Enter your role, the impact you created, and the key challenges you faced. "
        "The app will generate **5 STAR-structured, quantifiable bullet points** you can refine for your resume."
    )

    with st.form("resume_bullet_form"):
        job_role = st.text_input("Job role", placeholder="e.g. Senior Software Engineer, Product Manager")
        impact = st.text_area(
            "Impact created",
            placeholder=(
                "Describe the outcomes and metrics if possible.\n"
                "Example: Increased API reliability from 95% to 99.9%, reduced incident response time by 40%, "
                "improved customer NPS by 15 points."
            ),
            height=120,
        )
        challenges = st.text_area(
            "Challenges faced",
            placeholder=(
                "Describe the problem, constraints, or complexity.\n"
                "Example: Legacy monolith with high downtime, cross‑team alignment issues, tight deadlines, "
                "rapidly growing data volume."
            ),
            height=120,
        )

        submitted = st.form_submit_button("Generate bullet points")

    if submitted:
        if not job_role.strip() or not impact.strip() or not challenges.strip():
            st.error("Please fill in all three fields to generate bullet points.")
            return

        bullets = generate_star_bullets_llm(job_role, impact, challenges, num_points=5)

        if not bullets:
            st.warning("Unable to generate bullet points. Please refine your inputs and try again.")
            return

        st.subheader("Suggested resume bullet points")
        st.caption(
            "These follow the STAR pattern (Situation, Task, Action, Result). "
            "Edit them to match your exact metrics, tools, and company context."
        )

        for b in bullets:
            st.markdown(f"- {b}")

        st.divider()
        st.info(
            "Tip: Make sure at least one number appears in each bullet "
            "(%, $, time saved, volume, scale, etc.) so the impact is clearly quantifiable."
        )


if __name__ == "__main__":
    main()


