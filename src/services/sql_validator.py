import sqlglot
from sqlglot import exp


class SQLSecurityError(Exception):
    """Raised when a generated SQL query violates security or resource policies."""


class SQLValidatorService:
    MAX_ROW_LIMIT = 1000

    @classmethod
    def validate_and_enforce_limits(cls, sql_query: str) -> str:
        if not sql_query or not sql_query.strip():
            raise SQLSecurityError("Received an empty SQL query.")

        try:
            parsed_statements = sqlglot.parse(sql_query, read="mysql")
        except sqlglot.errors.ParseError as e:
            raise SQLSecurityError(f"Invalid SQL syntax: {e}")

        if len(parsed_statements) != 1 or parsed_statements[0] is None:
            raise SQLSecurityError("Only a single SQL statement is allowed per execution.")

        statement = parsed_statements[0]

        if not isinstance(statement, exp.Select):
            raise SQLSecurityError(
                "Security violation: Only SELECT queries are permitted, "
                f"got {type(statement).__name__}."
            )

        if statement.args.get("limit") is None:
            statement = statement.limit(cls.MAX_ROW_LIMIT)

        return statement.sql(dialect="mysql")
