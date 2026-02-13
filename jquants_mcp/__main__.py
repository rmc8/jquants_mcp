import sys

# Handle --help argument manually before any strict initialization
if "--help" in sys.argv or "-h" in sys.argv:
    print("jquants-mcp: MCP server for J-Quants API")
    print("\nThis is a Model Context Protocol (MCP) server.")
    print("It is intended to be used with an MCP client (e.g., Claude Desktop).")
    print("\nConfiguration:")
    print("  - Environemnt Variable: JQUANTS_API_KEY (Required)")
    # We can't list tools easily without initializing mcp, but we can list documented ones or try to init mcp safely?
    # For now, just static help is better than hanging.
    print("\nTools:")
    print("  - get_listed_issues")
    print("  - get_daily_quotes")
    print("  - get_financial_summary")
    print("  - get_earnings_calendar")
    print("  (and more...)")
    sys.exit(0)

import logging
from typing import Any

from mcp.server.fastmcp import FastMCP

from jquants_mcp.libs.client import get_client
from jquants_mcp.libs.models import (DateRangeParams, FinancialParams,
                                     InvestorTradingParams, ListedIssuesParams,
                                     MarginInterestParams)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("jquants-mcp")

# Initialize FastMCP server
mcp = FastMCP("jquants-mcp")

# Initialize JQuants API Client
cli = get_client()


@mcp.tool()
async def get_listed_issues(code: str | None = None, date: str | None = None) -> Any:
    """
    Get listed issue information (equities master).

    Args:
        code: 5-digit stock code (e.g., 86040).
        date: Reference date (YYYYMMDD or YYYY-MM-DD).
    """
    try:
        # Validate inputs
        params = ListedIssuesParams(code=code, date=date)

        df = cli.get_eq_master(code=params.code or "", date_yyyymmdd=params.date or "")
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error fetching listed issues: {e}")
        return f"Error: {e}"


@mcp.tool()
async def get_daily_quotes(
    code: str | None = None,
    date: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> Any:
    """
    Get stock daily quotes (OHLC).

    Args:
        code: 5-digit stock code.
        date: Target date (YYYYMMDD).
        from_date: Start date for range (YYYYMMDD).
        to_date: End date for range (YYYYMMDD).
    """
    try:
        # Validate inputs
        params = DateRangeParams(
            code=code, date=date, from_date=from_date, to_date=to_date
        )

        df = cli.get_eq_bars_daily(
            code=params.code or "",
            date_yyyymmdd=params.date or "",
            from_yyyymmdd=params.from_date or "",
            to_yyyymmdd=params.to_date or "",
        )
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error fetching daily quotes: {e}")
        return f"Error: {e}"


@mcp.tool()
async def get_financial_summary(
    code: str | None = None, date: str | None = None
) -> Any:
    """
    Get financial summary (quarterly financial results).

    Args:
        code: 5-digit stock code.
        date: Target date.
    """
    try:
        params = FinancialParams(code=code, date=date)

        try:
            df = cli.get_fin_summary(
                code=params.code or "", date_yyyymmdd=params.date or ""
            )
        except TypeError:
            # Fallback just in case
            df = cli.get_fin_summary(code=params.code or "", date=params.date or "")

        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error fetching financial summary: {e}")
        return f"Error: {e}"


@mcp.tool()
async def get_earnings_calendar() -> Any:
    """
    Get earnings calendar (upcoming earnings announcements).
    """
    try:
        df = cli.get_eq_earnings_cal()
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error fetching earnings calendar: {e}")
        return f"Error: {e}"


@mcp.tool()
async def get_indices_daily(
    code: str | None = None,
    date: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> Any:
    """
    Get indices daily quotes (TOPIX, Nikkei 225, etc.).

    Args:
        code: Index code (e.g., '0000' for TOPIX, '0001' for Nikkei 225).
        date: Target date.
        from_date: Start date.
        to_date: End date.
    """
    try:
        params = DateRangeParams(
            code=code, date=date, from_date=from_date, to_date=to_date
        )

        df = cli.get_idx_bars_daily(
            code=params.code or "",
            date_yyyymmdd=params.date or "",
            from_yyyymmdd=params.from_date or "",
            to_yyyymmdd=params.to_date or "",
        )
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error fetching indices daily: {e}")
        return f"Error: {e}"


@mcp.tool()
async def get_market_segment_breakdown(
    date: str | None = None, from_date: str | None = None, to_date: str | None = None
) -> Any:
    """
    Get market segment breakdown (trading breakdown).

    Args:
        date: Target date.
        from_date: Start date.
        to_date: End date.
    """
    try:
        params = DateRangeParams(date=date, from_date=from_date, to_date=to_date)

        df = cli.get_mkt_breakdown(
            date_yyyymmdd=params.date or "",
            from_yyyymmdd=params.from_date or "",
            to_yyyymmdd=params.to_date or "",
        )
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error fetching market breakdown: {e}")
        return f"Error: {e}"


@mcp.tool()
async def get_financial_dividends(
    code: str | None = None,
    date: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> Any:
    """
    Get dividend information.

    Args:
        code: 5-digit stock code.
        date: Reference date (YYYYMMDD).
        from_date: Start date (YYYYMMDD).
        to_date: End date (YYYYMMDD).
    """
    try:
        params = DateRangeParams(
            code=code, date=date, from_date=from_date, to_date=to_date
        )

        df = cli.get_fin_dividend(
            code=params.code or "",
            date_yyyymmdd=params.date or "",
            from_yyyymmdd=params.from_date or "",
            to_yyyymmdd=params.to_date or "",
        )
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error fetching dividends: {e}")
        return f"Error: {e}"


@mcp.tool()
async def get_financial_statements_detail(
    code: str | None = None, date: str | None = None
) -> Any:
    """
    Get detailed financial statements (BS/PL/CF).

    Args:
        code: 5-digit stock code.
        date: Reference date (YYYYMMDD).
    """
    try:
        params = FinancialParams(code=code, date=date)

        df = cli.get_fin_details(
            code=params.code or "", date_yyyymmdd=params.date or ""
        )
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error fetching financial details: {e}")
        return f"Error: {e}"


@mcp.tool()
async def get_short_sale_ratio(
    code: str | None = None,
    date: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> Any:
    """
    Get short sale ratio (market sentiment).

    Args:
        code: 5-digit stock code.
        date: Disclosed date (YYYYMMDD).
        from_date: Start date (YYYYMMDD).
        to_date: End date (YYYYMMDD).
    """
    try:
        params = DateRangeParams(
            code=code, date=date, from_date=from_date, to_date=to_date
        )

        df = cli.get_mkt_short_sale_report(
            code=params.code or "",
            disclosed_date=params.date or "",
            disclosed_date_from=params.from_date or "",
            disclosed_date_to=params.to_date or "",
        )
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error fetching short sale report: {e}")
        return f"Error: {e}"


@mcp.tool()
async def get_market_margin_interest(
    code: str | None = None,
    date: str | None = None,
    from_date: str | None = None,
    to_date: str | None = None,
) -> Any:
    """
    Get margin interest balance (weekend balance).
    Useful for analyzing supply/demand and potential squeeze (anomaly).

    Args:
        code: 5-digit stock code.
        date: Target date (YYYYMMDD).
        from_date: Start date (YYYYMMDD).
        to_date: End date (YYYYMMDD).
    """
    try:
        params = MarginInterestParams(
            code=code, date=date, from_date=from_date, to_date=to_date
        )

        # Signature: (code: str = '', from_yyyymmdd: str = '', to_yyyymmdd: str = '', date_yyyymmdd: str = '')
        df = cli.get_mkt_margin_interest(
            code=params.code or "",
            date_yyyymmdd=params.date or "",
            from_yyyymmdd=params.from_date or "",
            to_yyyymmdd=params.to_date or "",
        )
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error fetching margin interest: {e}")
        return f"Error: {e}"


@mcp.tool()
async def get_investor_trading_trends(
    section: str | None = None, from_date: str | None = None, to_date: str | None = None
) -> Any:
    """
    Get trading by investor type (Foreigners, Individuals, etc.).
    Useful for analyzing market trends and investor sentiment (anomaly).

    Args:
        section: Market section (e.g., TSEPrime, TSEStandard, TSEGrowth).
        from_date: Start date (YYYYMMDD).
        to_date: End date (YYYYMMDD).
    """
    try:
        params = InvestorTradingParams(
            section=section, from_date=from_date, to_date=to_date
        )

        # Signature: (section: str = '', from_yyyymmdd: str = '', to_yyyymmdd: str = '')
        # Note: 'section' parameter in get_eq_investor_types
        df = cli.get_eq_investor_types(
            section=params.section or "",
            from_yyyymmdd=params.from_date or "",
            to_yyyymmdd=params.to_date or "",
        )
        return df.to_dict(orient="records")
    except Exception as e:
        logger.error(f"Error fetching investor trading trends: {e}")
        return f"Error: {e}"


def main():
    """Entry point for the jquants-mcp command."""
    logger.info("Starting jquants-mcp server...")
    mcp.run()


if __name__ == "__main__":
    main()
