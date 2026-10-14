"""Small main-file example using tracer labels around a loop."""

from __future__ import annotations

import logging

from traceprint import TracerHandler, tracer


def process_item(item: str) -> str:
    logging.info("processing %s", item)
    return item.upper()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(message)s",
        handlers=[TracerHandler()],
        force=True,
    )
    tracer.configure(
        use_colors=None,
        use_tabulation=False,
        print_transitions=False,
        filter_levels=None,
    )
    tracer.install()

    try:
        items = ["alpha", "beta", "gamma"]

        logging.info("starting loop")
        tracer.push("loop")
        try:
            results = []
            for index, item in enumerate(items, start=1):
                tracer.push(f"item_{index}")
                try:
                    print(f"input: {item}")
                    results.append(process_item(item))
                    print(f"output: {results[-1]}")
                finally:
                    tracer.pop()
        finally:
            tracer.pop()

        logging.info("finished loop")
        print(results)
    finally:
        tracer.uninstall()


if __name__ == "__main__":
    main()
