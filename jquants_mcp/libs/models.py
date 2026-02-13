import re

from pydantic import BaseModel, Field, field_validator


class DateRangeParams(BaseModel):
    """Common parameters for date range queries."""

    code: str | None = Field(None, description="5-digit stock code")
    date: str | None = Field(None, description="Target date (YYYYMMDD or YYYY-MM-DD)")
    from_date: str | None = Field(
        None, description="Start date (YYYYMMDD or YYYY-MM-DD)"
    )
    to_date: str | None = Field(None, description="End date (YYYYMMDD or YYYY-MM-DD)")

    @field_validator("date", "from_date", "to_date")
    @classmethod
    def validate_date_format(cls, v: str | None) -> str | None:
        if not v:
            return ""
        # Remove hyphens if present to standardize on YYYYMMDD for J-Quants
        v_clean = v.replace("-", "")
        if not re.match(r"^\d{8}$", v_clean):
            raise ValueError("Date must be in YYYYMMDD or YYYY-MM-DD format")
        return v_clean


class ListedIssuesParams(BaseModel):
    code: str | None = Field(None, description="5-digit stock code")
    date: str | None = Field(None, description="Reference date")

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: str | None) -> str | None:
        if not v:
            return ""
        v_clean = v.replace("-", "")
        if not re.match(r"^\d{8}$", v_clean):
            raise ValueError("Date must be in YYYYMMDD or YYYY-MM-DD format")
        return v_clean


class FinancialParams(BaseModel):
    code: str | None = Field(None, description="5-digit stock code")
    date: str | None = Field(None, description="Reference date")

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: str | None) -> str | None:
        if not v:
            return ""
        v_clean = v.replace("-", "")
        if not re.match(r"^\d{8}$", v_clean):
            raise ValueError("Date must be in YYYYMMDD or YYYY-MM-DD format")
        return v_clean


class MarginInterestParams(BaseModel):
    code: str | None = Field(None, description="5-digit stock code")
    date: str | None = Field(None, description="Target date (YYYYMMDD)")
    from_date: str | None = Field(None, description="Start date (YYYYMMDD)")
    to_date: str | None = Field(None, description="End date (YYYYMMDD)")

    @field_validator("date", "from_date", "to_date")
    @classmethod
    def validate_date_format(cls, v: str | None) -> str | None:
        if not v:
            return ""
        v_clean = v.replace("-", "")
        if not re.match(r"^\d{8}$", v_clean):
            raise ValueError("Date must be in YYYYMMDD or YYYY-MM-DD format")
        return v_clean


class InvestorTradingParams(BaseModel):
    section: str | None = Field(
        None, description="Market section (e.g., TSEPrime, TSEStandard, TSEGrowth)"
    )
    from_date: str | None = Field(None, description="Start date (YYYYMMDD)")
    to_date: str | None = Field(None, description="End date (YYYYMMDD)")

    @field_validator("from_date", "to_date")
    @classmethod
    def validate_date_format(cls, v: str | None) -> str | None:
        if not v:
            return ""
        v_clean = v.replace("-", "")
        if not re.match(r"^\d{8}$", v_clean):
            raise ValueError("Date must be in YYYYMMDD or YYYY-MM-DD format")
        return v_clean
