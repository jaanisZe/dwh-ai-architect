import pytest

from src.services.sql_validator import SQLSecurityError, SQLValidatorService


def test_valid_select_adds_limit():
    sql = "SELECT customer_name FROM dim_customers"
    validated = SQLValidatorService.validate_and_enforce_limits(sql)
    assert "LIMIT 1000" in validated


def test_valid_select_with_keyword_in_string_literal():
    sql = "SELECT * FROM dim_products WHERE product_name = 'DROP TABLE test'"
    validated = SQLValidatorService.validate_and_enforce_limits(sql)
    assert "SELECT" in validated


def test_blocks_drop_statement():
    with pytest.raises(SQLSecurityError):
        SQLValidatorService.validate_and_enforce_limits("DROP TABLE fact_sales")


def test_blocks_stacked_queries():
    with pytest.raises(SQLSecurityError):
        SQLValidatorService.validate_and_enforce_limits("SELECT 1; DELETE FROM fact_sales;")
