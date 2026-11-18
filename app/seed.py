"""Insert sample data:  uv run python -m app.seed"""

from sqlmodel import Session

from app.db import engine, init_db
from app.models import Survey


def main() -> None:
    init_db()
    with Session(engine) as session:
        session.add(
            Survey(
                title="Q4 Engagement Pulse",
                description="A quick check-in on how the team is feeling.",
            )
        )
        # TODO: seed questions / responses once those tables exist
        session.commit()
    print("Seeded.")


if __name__ == "__main__":
    main()
