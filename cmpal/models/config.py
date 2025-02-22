from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field


class CapitalizationStyle(StrEnum):
    """Whether the subject line should start with a capital letter."""

    CAPITALIZED = "capitalized"  # "Add feature"
    LOWERCASE = "lowercase"  # "add feature"


class PunctuationStyle(StrEnum):
    """Whether the subject line should end with punctuation."""

    WITH_PERIOD = "with_period"  # "Add feature."
    WITHOUT_PERIOD = "without_period"  # "Add feature"


class ScopeFormat(StrEnum):
    """How the scope should be formatted."""

    PARENTHESES = "parentheses"  # "feat(scope): message"
    BRACKETS = "brackets"  # "feat[scope]: message"
    NONE = "none"  # "feat: message" (no scope)


class BreakingChangeIndicator(StrEnum):
    """How breaking changes should be indicated."""

    EXCLAMATION_MARK = "exclamation_mark"  # "feat!: message"
    FOOTER_ONLY = "footer_only"  # "feat: message" + "BREAKING CHANGE: ..."


class FooterFormat(StrEnum):
    """How footers should be formatted."""

    KEY_VALUE_COLON = "key_value_colon"  # "KEY: VALUE"
    KEY_VALUE_EQUALS = "key_value_equals"  # "KEY=VALUE"


class CommitStyleConfigs(BaseModel):
    """Stylistic preferences for conventional commits."""

    capitalization: CapitalizationStyle = Field(
        default=CapitalizationStyle.LOWERCASE,
        description="Whether the subject line should start with a capital letter.",
    )
    punctuation: PunctuationStyle = Field(
        default=PunctuationStyle.WITHOUT_PERIOD,
        description="Whether the subject line should end with a period.",
    )
    scope_format: ScopeFormat = Field(
        default=ScopeFormat.PARENTHESES,
        description="How the scope should be formatted (e.g., parentheses, brackets, or none).",
    )
    breaking_change_indicator: BreakingChangeIndicator = Field(
        default=BreakingChangeIndicator.EXCLAMATION_MARK,
        description="How breaking changes should be indicated (e.g., '!' in header or only in footer).",
    )
    footer_format: FooterFormat = Field(
        default=FooterFormat.KEY_VALUE_COLON,
        description="How footers should be formatted (e.g., 'KEY: VALUE' or 'KEY=VALUE').",
    )
    max_subject_length: Optional[int] = Field(
        default=72,
        description="Maximum length of the subject line. Defaults to 72 characters.",
        ge=50,
        le=100,  # Enforce reasonable limits
    )

    class Config:
        use_enum_values = True

    def pretty_print(self) -> str:
        return self.model_dump_json(indent=2)
