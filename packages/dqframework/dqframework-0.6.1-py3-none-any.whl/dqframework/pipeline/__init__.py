import enum
import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List

import polars as pl

from dqframework.validators import Validator

columns = [
    "id"
    "check_id"
    "timestamp"
    "check"
    "level"
    "column"
    "rule"
    "value"
    "rows"
    "violations"
    "pass_rate"
    "pass_threshold"
    "status"
]


class Check:
    """
    Check class is responsible for executing the validations and returning the results

    Args:
        level (Check.Level): The level of the check
            if the level is INFO or WARNING, the check will only log the results but won't filter them out from the results
            if the level is ERROR or CRITICAL, the check will filter out the incorrect records from the results
        check_name (str): The name of the check
        pass_threshold (float): The threshold for the check to pass (default is 0.9)
    """

    class Level(enum.Enum):
        INFO = "INFO"
        WARNING = "WARNING"
        ERROR = "ERROR"
        CRITICAL = "CRITICAL"

    def __init__(
        self,
        level: Level,
        check_name: str,
        pass_threshold: float = 0.9,
    ):
        self.level = level
        self.check_name: str = check_name
        self.validations: list[Validator] = []
        self.pass_threshold = pass_threshold
        self.check_id = str(uuid.uuid4())

        self.filter_out = (
            True if self.level in [Check.Level.ERROR, Check.Level.CRITICAL] else False
        )

    def __call__(
        self, df: pl.DataFrame, *args, **kwargs
    ) -> (pl.DataFrame, pl.DataFrame, pl.DataFrame):
        if not self.validations:
            raise ValueError("No validations added to the check")
        correct_acc = df
        incorrect_acc = pl.DataFrame()

        dq_metrics = pl.DataFrame()
        for validation in self.validations:
            val_id = str(uuid.uuid4())
            rule = validation.__class__.__name__
            column = validation.column

            correct, incorrect = validation.execute(correct_acc)
            correct_acc = correct if self.filter_out else df

            # tag the incorrect with the check_id that failed
            incorrect = incorrect.with_columns(
                pl.lit(str(self.check_id)).alias("check_id"),
                pl.lit(str(val_id)).alias("validation_id"),
            )

            incorrect_acc = pl.concat([incorrect_acc, incorrect], how="vertical")

            dq_metrics = pl.concat(
                [
                    dq_metrics,
                    self._calculate_dq(
                        df,
                        incorrect,
                        column,
                        rule,
                        str(validation.get_value()),
                        str(val_id),
                    ),
                ]
            )

        return (
            dq_metrics,
            correct_acc,
            incorrect_acc,
        )

    def _calculate_dq(
        self,
        original_df: pl.DataFrame,
        incorrect_df: pl.DataFrame,
        column: str,
        rule_name: str,
        value_check: str = "",
        validation_id: str = "",
    ) -> pl.DataFrame:
        rows = original_df.height
        violations = incorrect_df.height
        pass_rate = float((rows - violations) / rows) if rows > 0 else 0.0
        return pl.DataFrame(
            {
                "id": [validation_id],
                "check_id": [self.check_id],
                "timestamp": [datetime.now()],
                "check": [self.check_name],
                "level": [self.level.value],
                "column": [column],
                "rule": [rule_name],
                "value": [value_check],
                "rows": [rows],
                "violations": [violations],
                "pass_rate": [pass_rate],
                "pass_threshold": [float(self.pass_threshold)],
                "status": ["PASS" if pass_rate >= self.pass_threshold else "FAIL"],
            }
        )


class Pipeline:
    """
    Pipeline class is responsible for executing the checks and returning the results

    Args:
        checks (List[Check]): The list of checks to be executed in the pipeline
    """

    class Status(enum.Enum):
        NOT_EXECUTED = "NOT_EXECUTED"
        EXECUTED = "EXECUTED"

    def __init__(self, checks: List[Check]):
        self.checks = checks
        self.results = None
        self.status = Pipeline.Status.NOT_EXECUTED

    def execute(self, df: pl.DataFrame):
        """
        Execute the pipeline

        :param df: The DataFrame to be validated
        :return: PipelineResults
        """
        if not self.checks:
            raise ValueError("No checks added to the pipeline")

        aux_df = df
        invalid_records = pl.DataFrame()
        results_df = pl.DataFrame()
        for check in self.checks:
            (results, ok, notok) = check(aux_df)

            invalid_records = pl.concat([invalid_records, notok], how="vertical")
            results_df = pl.concat([results_df, results], how="vertical")
            aux_df = ok

        self.results = results_df
        self.status = Pipeline.Status.EXECUTED

        return PipelineResults(df, aux_df, invalid_records, results_df)

    def results_to_csv(self, path: str):
        """
        Write the results to a CSV file (in path)

        :param path: The path to the CSV file
        :return: None
        """

        if self.status == Pipeline.Status.NOT_EXECUTED:
            raise ValueError("Pipeline not executed")

        self.results.write_csv(path)

    def results_to_xlsx(self, path: str):
        """
        Write the results to an Excel file (in path)

        :param path: The path to the Excel file
        :return: None
        """
        if self.status == Pipeline.Status.NOT_EXECUTED:
            raise ValueError("Pipeline not executed")

        self.results.write_excel(path)

    def results_to_json(self, path: str):
        if self.status == Pipeline.Status.NOT_EXECUTED:
            raise ValueError("Pipeline not executed")

        self.results.write_json(path)


@dataclass
class PipelineResults:
    """
    PipelineResults class is responsible for storing the results of the pipeline execution
    """

    original_records: pl.DataFrame
    valid_records: pl.DataFrame
    invalid_records: pl.DataFrame
    results: pl.DataFrame
