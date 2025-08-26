
from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class EventsOfInstruction(BaseModel):
    gain_attention: str
    inform_learners_of_objectives: str
    stimulate_recall: str
    present_stimulus: str
    provide_learning_guidance: str
    elicit_performance: str
    provide_feedback: str
    assess_performance: str
    enhance_retention_transfer: str

class Outcome(BaseModel):
    statement: str
    bloom: str
    kpi_link: str

class Module(BaseModel):
    title: str
    events_of_instruction: EventsOfInstruction
    activities: List[Dict]
    assessment: List[Dict]

class Program(BaseModel):
    goals: List[str]
    outcomes: List[Outcome]
    modules: List[Module]
    delivery: str
    duration_hours: int

class Artifact(BaseModel):
    meta: Dict
    program: Program
    operations: Dict
    compliance: Dict
    accessibility: Dict
    feedback: List[Dict]
    scores: Dict
