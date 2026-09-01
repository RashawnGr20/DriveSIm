import os
from datetime import datetime

from fastapi import HTTPException
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from sqlalchemy.orm import Session

from backend.database.models import CoachingReport
from backend.database.models import Session as SessionModel
from backend.sessions.service import get_pose_breakdown

from .schemas import CoachingReportSchema

DEFAULT_MODEL = "claude-haiku-4-5"

SYSTEM_PROMPT = """You are a driving instructor reviewing a student's performance in a \
driver's-test simulator scenario. The student was scored on whether they performed the \
correct mirror/blind-spot observation checks at the right times.

Given the scenario definition and the student's observed results, write a coaching report \
that is encouraging but honest. Focus on what the student did well, what they need to work \
on, and give a short note for each individual required check."""

HUMAN_PROMPT = """Scenario: {scenario} ({scenario_type})
Required checks, in order if applicable: {expected_sequence}
Overall score: {score} / 100

Per-step results: {step_results}

Observed pose durations/frequency during the session: {pose_breakdown}
Total gaze events recorded: {total_events}
Average glance duration: {avg_duration} seconds"""


def _build_chain() :
    model_name = os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL)
    api_key = os.getenv("ANTHROPIC_API_KEY")

    llm = ChatAnthropic(model=model_name, api_key=api_key, temperature=0.3)
    structured_llm = llm.with_structured_output(CoachingReportSchema)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", HUMAN_PROMPT),
    ])

    return prompt | structured_llm


def build_session_aggregates(db: Session, session: SessionModel) :

    pose_breakdown = get_pose_breakdown(db, session.id)

    total_events = sum(stat["count"] for stat in pose_breakdown.values())

    durations = [stat["total_duration"] or 0 for stat in pose_breakdown.values()]
    counts = [stat["count"] for stat in pose_breakdown.values()]
    avg_duration = (sum(durations) / sum(counts)) if sum(counts) else None

    return {
        "scenario": session.scenario,
        "scenario_type": session.scenario_type,
        "expected_sequence": session.expected_sequence,
        "score": session.score,
        "step_results": session.step_results,
        "pose_breakdown": pose_breakdown,
        "total_events": total_events,
        "avg_duration": avg_duration,
    }


def generate_coaching_report(aggregates: dict) -> CoachingReportSchema :

    chain = _build_chain()

    try :
        return chain.invoke(aggregates)
    except Exception as exc :
        message = str(exc)
        if "rate_limit" in message.lower() or "overloaded" in message.lower() :
            raise HTTPException(status_code=503, detail="Coaching report generation is temporarily unavailable") from exc
        raise HTTPException(status_code=502, detail="Coaching report generation failed") from exc


def get_or_create_coaching_report(db: Session, session: SessionModel) :

    if session.coaching_report is not None :
        return session.coaching_report, True

    if session.completed_at is None :
        raise HTTPException(status_code=409, detail="Session has not been completed yet")

    aggregates = build_session_aggregates(db, session)
    report_data = generate_coaching_report(aggregates)

    report = CoachingReport(
        session_id=session.id,
        summary=report_data.summary,
        strengths=report_data.strengths,
        areas_to_improve=report_data.areas_to_improve,
        per_check_notes=[note.model_dump() for note in report_data.per_check_notes],
        overall_score=session.score,
        model=os.getenv("ANTHROPIC_MODEL", DEFAULT_MODEL),
        raw_response=report_data.model_dump(),
        created_at=datetime.utcnow(),
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report, False
