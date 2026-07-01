import logging

import pandas as pd
from datafusion import SessionContext
from datafusion.object_store import AmazonS3
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.constants import ATTENDANCE_S3_BUCKET, AWS_REGION
from app.exceptions import RepositoryError

logger = logging.getLogger(__name__)


class DataFusionBaseRepository:
    """Shared DataFusion session and S3 wiring for repos."""

    def __init__(self):
        self._ctx = SessionContext()
        self._register_s3()

    def _register_s3(self):
        s3 = AmazonS3(bucket_name=ATTENDANCE_S3_BUCKET, region=AWS_REGION)
        self._ctx.register_object_store("s3", s3, None)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, min=1, max=5),
        retry=retry_if_exception_type(ValueError),
        reraise=True,
    )
    def _query_with_retry(self, sql: str) -> pd.DataFrame:
        return self._ctx.sql(sql).to_pandas()

    def _run_query(self, sql: str) -> pd.DataFrame:
        try:
            return self._query_with_retry(sql)
        except ValueError as e:
            logger.error("query failed after retries: %s", e, exc_info=True)
            raise RepositoryError("failed to execute query", cause=e) from e
