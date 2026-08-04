import enum
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, ENUM
from schema.base import Base


class PipelineStage(enum.Enum):
    added = "added"
    II = "II"
    PS = "PS"
    CI = "CI"
    PF = "PF"
    PO = "PO"
    SW = "SW"
    fail = "fail"
    split = "split"


class Pipeline(Base):
    __tablename__ = "pipeline"

    opportunity_id = Column(Integer, ForeignKey("opportunity.id"), primary_key=True)
    talent_id = Column(UUID(as_uuid=True), ForeignKey("talent.id"), primary_key=True)

    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    stage = Column(
        ENUM(PipelineStage, name="pipeline_stage", create_type=False),
        nullable=False,
        default=PipelineStage.added,
    )

    stage_entered_at = Column(DateTime)


class PipelineStageHistory(Base):
    __tablename__ = "pipeline_stage_history"

    id = Column(Integer, primary_key=True)

    opportunity_id = Column(Integer, ForeignKey("opportunity.id"), nullable=False)
    talent_id = Column(UUID(as_uuid=True), ForeignKey("talent.id"), nullable=False)

    changed_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    to_stage = Column(
        ENUM(PipelineStage, name="pipeline_stage", create_type=False),
        nullable=False,
    )

    created_at = Column(DateTime)