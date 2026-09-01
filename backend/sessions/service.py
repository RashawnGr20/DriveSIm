from sqlalchemy import func
from sqlalchemy.orm import Session

from backend.database.models import GazeEvent


def get_pose_breakdown(db: Session, session_id: int) :

    rows = (
        db.query(
            GazeEvent.pose,
            func.count(GazeEvent.id),
            func.avg(GazeEvent.duration),
            func.sum(GazeEvent.duration),
        )
        .filter(GazeEvent.session_id == session_id)
        .group_by(GazeEvent.pose)
        .all()
    )

    return {
        pose: {
            "count": count,
            "avg_duration": avg_duration,
            "total_duration": total_duration,
        }
        for pose, count, avg_duration, total_duration in rows
    }
