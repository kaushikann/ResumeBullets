import textwrap

import streamlit as st


def generate_star_bullets(job_role: str, impact: str, challenges: str, num_points: int = 5) -> list[str]:
    job_role = job_role.strip()
    impact = impact.strip()
    challenges = challenges.strip()

    if not job_role or not impact or not challenges:
        return []

    base_context = (
        f"As a {job_role}, you faced challenges such as {challenges}. "
        f"Through your actions, you created impact like {impact}."
    )

    # Re-usable STAR fragments that we can mix slightly to get 5 bullets
    templates = [
        (
            "Led efforts as {role} to address {challenges}, "
            "owning the end‑to‑end task of designing and executing solutions, "
            "which resulted in {impact}."
        ),
        (
            "Partnered with cross‑functional stakeholders in the {role} role to tackle {challenges}, "
            "defining clear goals and action plans that delivered {impact}."
        ),
        (
            "Analyzed the situation around {challenges} as {role}, "
            "prioritized the highest‑value tasks, and implemented targeted improvements, "
            "achieving measurable results such as {impact}."
        ),
        (
            "Proactively identified {challenges} while working as {role}, "
            "framed the task with success metrics, executed on a focused action plan, "
            "and drove outcomes including {impact}."
        ),
        (
            "Owned critical initiatives as {role} in the context of {challenges}, "
            "taking decisive actions and continuously iterating, "
            "ultimately delivering quantifiable results like {impact}."
        ),
    ]

    bullets: list[str] = []

    for i in range(num_points):
        template = templates[i % len(templates)]
        bullet = template.format(role=job_role, challenges=challenges, impact=impact)
        bullets.append(bullet)

    # Add a short preface reminding the user to customize metrics
    bullets = [
        textwrap.fill(
            b.replace("like ", "such as ").replace("including ", "such as "),
            width=100,
        )
        for b in bullets
    ]

    return bullets


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

        bullets = generate_star_bullets(job_role, impact, challenges, num_points=5)

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

