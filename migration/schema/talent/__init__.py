from .talent import Talent, TalentStatus, ExpectedSalaryStatus, CandidateSex, EducationLevel
from .talent_note import TalentNote
from .talent_industry import TalentIndustry
from .talent_function import TalentFunction
from .talent_education import TalentEducation, EducationStatus, EducationLevel as EducationLevelEdu
from .talent_source import TalentSource, TalentSourceType

__all__ = [
    # Tables
    "Talent",
    "TalentNote",
    "TalentIndustry",
    "TalentFunction",
    "TalentEducation",
    "TalentSource",

    # Enums (只 export 可能會在外部用到的)
    "TalentStatus",
    "ExpectedSalaryStatus",
    "CandidateSex",
    "EducationLevel",          # Talent 用到的
    "EducationStatus",         # TalentEducation 用到的
    "EducationLevelEdu",       # TalentEducation 用到的 (避免和 Talent 的衝突)
    "TalentSourceType",
]
