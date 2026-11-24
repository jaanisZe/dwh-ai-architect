import logging
import time

from src.domain.models import QueryRequest, QueryResult
from src.repositories.dwh_repository import DWHRepository
from src.services.llm_service import LLMService
from src.services.sql_validator import SQLValidatorService

logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": %(message)s}',
)
logger = logging.getLogger(__name__)


class QueryController:
    def __init__(
        self,
        llm_service: LLMService,
        validator_service: SQLValidatorService,
        dwh_repository: DWHRepository,
    ):
        self._llm = llm_service
        self._validator = validator_service
        self._repo = dwh_repository

    def handle_query(self, request: QueryRequest) -> QueryResult:
        start_time = time.perf_counter()
        logger.info(f'"Audit: Received question: {request.question}"')

        raw_sql = self._llm.generate_sql(request.question)
        safe_sql = self._validator.validate_and_enforce_limits(raw_sql)
        df = self._repo.execute_read_query(safe_sql)

        elapsed_ms = round((time.perf_counter() - start_time) * 1000, 2)
        logger.info(f'"Audit: Query succeeded in {elapsed_ms}ms | SQL: {safe_sql}"')

        return QueryResult(
            question=request.question,
            generated_sql=safe_sql,
            execution_time_ms=elapsed_ms,
            data=df,
        )
