"""Small sklearn-style example using LoggerMixin and @trace."""

from __future__ import annotations

import logging
from typing import Any

from traceprint import LoggerMixin, TracerHandler, trace, tracer


class BaseEstimator:
    """Empty stand-in for sklearn.base.BaseEstimator."""


class TransformerMixin:
    """Empty stand-in for sklearn.base.TransformerMixin."""


class SampleNameTransformer(LoggerMixin, TransformerMixin, BaseEstimator):
    """A tiny transformer shaped like a scikit-learn estimator."""

    def __init__(self, *, verbose: bool = True) -> None:
        super().__init__(
            verbose=verbose,
            logging_level=logging.INFO,
            logging_passthrough=True,
            lazy_init=True,
        )
        self.seen_count_: int | None = None

    @trace(label="SampleNameTransformer.fit")
    def fit(self, rows: list[dict[str, Any]]) -> SampleNameTransformer:
        self._ensure_logger()
        self.seen_count_ = len(rows)
        self.log.info("fitted on %s rows", self.seen_count_)
        return self

    @trace(label="SampleNameTransformer.transform")
    def transform(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        self._ensure_logger()
        self.log.info("normalizing sample names")
        return [
            {
                **row,
                "sample_name": str(row["sample_name"]).strip().lower(),
            }
            for row in rows
        ]

    def fit_transform(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return self.fit(rows).transform(rows)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s",
        handlers=[TracerHandler()],
        force=True,
    )
    tracer.configure(use_colors=None, print_transitions=False)
    tracer.install()

    try:
        rows = [
            {"sample_id": "S1", "sample_name": " Control "},
            {"sample_id": "S2", "sample_name": " Treatment "},
        ]
        transformed = SampleNameTransformer().fit_transform(rows)
        print(transformed)
    finally:
        tracer.uninstall()


if __name__ == "__main__":
    main()
