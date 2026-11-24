import streamlit as st

from config.settings import settings
from src.controllers.query_controller import QueryController
from src.domain.models import QueryRequest
from src.repositories.dwh_repository import DWHRepository
from src.services.llm_service import LLMService
from src.services.sql_validator import SQLSecurityError, SQLValidatorService

st.set_page_config(page_title="DWH AI Architect", layout="wide")


@st.cache_resource
def init_controller() -> tuple[QueryController, dict]:
    llm_service = LLMService(
        api_key=settings.gemini_api_key,
        model_name=settings.llm_model,
        semantic_layer_path=settings.semantic_layer_path,
    )
    repo = DWHRepository(
        db_uri=settings.db_uri,
        timeout_seconds=settings.query_timeout_seconds,
    )
    controller = QueryController(
        llm_service=llm_service,
        validator_service=SQLValidatorService(),
        dwh_repository=repo,
    )
    return controller, llm_service.semantic_context


controller, semantic_context = init_controller()

st.title("🛡️ DWH Text-to-SQL with Semantic Layer")
st.caption("Clean Architecture: MariaDB (RBAC) + YAML Semantic Layer + sqlglot AST Guardrails")

with st.sidebar:
    st.header("📐 Semantic Layer")
    st.json(semantic_context, expanded=False)
    st.info(
        f"**Security Policy:**\n"
        f"- DB User: `{settings.db_user}` (`SELECT-only`)\n"
        f"- Max Rows: `{SQLValidatorService.MAX_ROW_LIMIT}`\n"
        f"- Timeout: `{settings.query_timeout_seconds}s`"
    )

question = st.text_input(
    "Ask a business question about sales data:",
    placeholder="e.g., What is the net revenue by country and product category?",
)

if st.button("Run Analysis", type="primary") and question:
    try:
        req = QueryRequest(question=question)
        with st.spinner("Processing query..."):
            result = controller.handle_query(req)

        st.success(f"Executed in {result.execution_time_ms} ms")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("1. Validated SQL (AST Guardrails)")
            st.code(result.generated_sql, language="sql")
        with col2:
            st.subheader("2. MariaDB Result")
            st.dataframe(result.data, use_container_width=True)

    except SQLSecurityError as sec_err:
        st.error(f"🚨 Security Block: {sec_err}")
    except Exception as e:
        st.error(f"System Error: {e}")
