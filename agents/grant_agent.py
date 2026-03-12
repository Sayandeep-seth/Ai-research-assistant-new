from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME

client = Groq(api_key=GROQ_API_KEY)


# --------------------------------------------------
# GRANT PROGRAM SUGGESTION
# --------------------------------------------------

def suggest_grant_program(topic):

    prompt = f"""
You are an academic research funding advisor.

Based on the research topic below, recommend the most suitable grant program.

Available programs:

1. NSF Grant Proposal Format (AI, engineering, computer science)
2. NIH Grant Proposal Format (healthcare, medical AI, bioinformatics)
3. Horizon Europe / EU Grant Format (international collaborative research)
4. SBIR / Startup Innovation Grant Format (AI startups, commercialization)
5. General Academic Grant Proposal Format (university research)

Research Topic:
{topic}

Return the answer in this format:

Recommended Grant Program:
Reason (1-2 sentences):
"""

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# --------------------------------------------------
# GRANT GENERATION
# --------------------------------------------------

def run_grant_agent(methodology, format_type="Default"):

    # --------------------------------------------------
    # DEFAULT FORMAT (original behaviour)
    # --------------------------------------------------

    if format_type == "Default":

        prompt = f"""
Write a professional academic research grant proposal.

Follow a clear academic structure.

Sections:
Title
Abstract (150-200 words)
Problem Statement
Research Gap
Proposed Methodology
Expected Impact
Budget Justification
Timeline

Methodology:
{methodology}
"""

    # --------------------------------------------------
    # NSF GRANT FORMAT
    # --------------------------------------------------

    elif format_type == "NSF Grant Proposal Format":

        prompt = f"""
Write a research grant proposal following the NSF Grant Proposal structure.

Structure:

Cover Page

Project Summary
- Overview
- Intellectual Merit
- Broader Impact

Project Description
- Introduction
- Background & Literature Review
- Research Objectives
- Methodology
- Expected Results

References

Budget & Budget Justification

Biographical Sketch

Facilities & Resources

Methodology:
{methodology}
"""

    # --------------------------------------------------
    # NIH FORMAT
    # --------------------------------------------------

    elif format_type == "NIH Grant Proposal Format":

        prompt = f"""
Write a research grant proposal following the NIH Grant Proposal structure.

Structure:

Cover Letter
Project Summary / Abstract
Specific Aims

Research Strategy
- Significance
- Innovation
- Approach

Preliminary Studies
Research Design & Methods

Budget
Facilities and Equipment
References

Methodology:
{methodology}
"""

    # --------------------------------------------------
    # HORIZON EUROPE FORMAT
    # --------------------------------------------------

    elif format_type == "Horizon Europe / EU Grant Format":

        prompt = f"""
Write a research grant proposal following the Horizon Europe / EU format.

Structure:

Excellence
- Objectives
- Relation to Work Programme
- Methodology

Impact
- Expected Outcomes
- Dissemination Plan

Implementation
- Work Packages
- Timeline
- Risk Management

Budget and Resources
Consortium Information

Methodology:
{methodology}
"""

    # --------------------------------------------------
    # SBIR FORMAT
    # --------------------------------------------------

    elif format_type == "SBIR / Startup Innovation Grant Format":

        prompt = f"""
Write a research grant proposal following the SBIR startup innovation grant format.

Structure:

Executive Summary
Problem Statement
Innovation Description
Technical Approach
Market Opportunity
Commercialization Plan
Team
Budget

Methodology:
{methodology}
"""

    # --------------------------------------------------
    # GENERAL ACADEMIC FORMAT
    # --------------------------------------------------

    elif format_type == "General Academic Grant Proposal Format":

        prompt = f"""
Write a research grant proposal following a standard academic grant proposal format.

Structure:

Title Page
Abstract
Introduction / Problem Statement
Literature Review
Research Gap
Objectives
Methodology
Expected Outcomes
Timeline
Budget
References

Methodology:
{methodology}
"""

    # --------------------------------------------------
    # LLM CALL
    # --------------------------------------------------

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content