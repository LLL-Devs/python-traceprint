Usage guide
===========

Installation
------------

Use pip >=26.2.2 or uv >=0.13.4. For older environments, follow the
`certificate recovery steps <https://github.com/LLL-Devs/python-traceprint/blob/main/CONTRIBUTING.md#certificate-security-and-existing-environments>`_
before installing packages.

Install a local checkout with ``python -m pip install .``. For the public
distribution, use ``python -m pip install python-traceprint``. Python imports remain
``traceprint``. To develop or build these docs, run ``uv sync --dev``.

Tracing print output
--------------------

Passing the tracer as ``file`` avoids changing process streams:

.. code-block:: python

   from traceprint import Tracer

   tracer = Tracer(use_colors=False, use_tabulation=True)
   print("starting", file=tracer)
   with tracer.span("load"):
       print("loaded", 42, "records", file=tracer)

The default prefix includes a UTC timestamp, cumulative time since construction,
elapsed time since the last formatted message and the full label path. Elapsed
times use a monotonic performance clock. Metadata is added once per nonblank
output line. Blank lines pass through, partial writes appear immediately and
``flush()`` does not end the current line. Use a newline to begin a fresh prefix.

To intercept ordinary ``print()``, install explicitly and always restore streams:

.. code-block:: python

   tracer.install(stdout=True, stderr=False)
   try:
       print("hello", "world")
   finally:
       tracer.uninstall()

``stderr=True`` routes intercepted stderr to the same tracer sink. There is no
independent stderr formatting path. Avoid overlapping installations by multiple
tracers: restoration uses the streams captured by each installation.

Spans and decorators
--------------------

``span()`` increases depth and adds a label inside its context, then restores
them on exit, including when the body raises. ``push()`` and ``pop()`` provide
manual equivalents when a context manager is inconvenient.

.. code-block:: python

   from traceprint import trace

   @trace(tracer_instance=tracer, label="transform")
   def transform() -> None:
       print("transformed", file=tracer)

   transform()

Without a label, the decorator uses the function name. Without a
``tracer_instance``, it uses the package's global ``tracer``. The decorator wraps
synchronous function calls; it does not track an async coroutine's execution
across awaits or a generator's iteration. Context state belongs to the tracer,
not an individual thread or async task. Keep tracer configuration stable while a
span or decorated call is active.

Configuration
-------------

.. code-block:: python

   tracer.configure(
       use_colors=False,
       use_tabulation=True,
       print_transitions=True,
       filter_levels=range(0, 3),
       output_format="[{label_full}] {original_message}",
   )

``use_colors=None`` checks whether the output stream is a TTY. Explicit ``True``
or ``False`` overrides detection. ``use_tabulation=True`` inserts four spaces per
depth level. With the default metadata color, indentation precedes the message;
with ``metacolor=None``, it precedes the whole formatted line. Colors do not
change indentation placement.

``filter_levels`` accepts allowed depths as a range or iterable, or a predicate
that returns ``True`` for allowed depths. ``None`` allows all depths. Filtering
suppresses output rather than changing nesting. ``disable()`` forwards raw text
and prevents depth changes; ``enable()`` resumes formatting. ``lock()`` prevents
depth changes until ``unlock()``.

The custom format accepts ``timestamp``, ``cumulative``, ``elapsed``, ``label``,
``label_full`` and ``original_message``. Include ``original_message`` to retain
the text. Timestamp syntax follows ``datetime.strftime``. ``label`` is the last
label and ``label_full`` is the slash-separated stack; regular labeled messages
add ``/>``. Timing advances when a message is formatted, including direct
``format()`` calls.

The format is applied to the first nonblank fragment of a line; subsequent
fragments are appended immediately. Prefer prefix-based formats for incremental
output, since a custom suffix would follow that first fragment.

Logging
-------

Use a dedicated logger to avoid changing the application's root logging setup:

.. code-block:: python

   import logging
   from traceprint import TracerHandler

   logger = logging.getLogger("example")
   handler = TracerHandler(tracer_instance=tracer)
   handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
   logger.addHandler(handler)
   logger.setLevel(logging.INFO)
   logger.propagate = False
   try:
       logger.info("loaded %s records", 42)
   finally:
       logger.removeHandler(handler)
       handler.close()

``LoggerMixin`` provides a class-named logger and a ``self.log`` proxy controlled
by ``verbose``. The transformer example shows it with empty scikit-learn-style
base classes. ``logging_passthrough=True`` attaches a handler targeting the
global tracer and disables propagation; this changes the shared class logger's
handlers. Leave it off when the application configures logging itself.

Files
-----

Mirror tracer output to a file, stripping terminal escape sequences:

.. code-block:: python

   from traceprint import TracerFileHandler

   file_handler = TracerFileHandler("trace.log", mode="a")
   tracer.add_file_handler(file_handler)
   try:
       print("saved", file=tracer)
       tracer.flush()
   finally:
       tracer.remove_file_handler(file_handler)
       file_handler.close()

Alternatively, attach ``TracerFileHandler(..., tracer_instance=tracer)`` directly
to a logger. It formats each record for the file. Use one route for a given
record to avoid duplicates. File logging and mirroring strip ANSI escapes.
Closing a handler owns file cleanup; uninstalling a tracer only restores process
streams. Raw output while the tracer is disabled bypasses mirrored file handlers.

Global labels
-------------

``TRACEPRINT_INITIAL_LABELS=job/load`` seeds the global tracer's label stack at
import time. Empty slash-separated components are ignored. It does not install
the tracer. Explicit ``Tracer`` instances do not read this variable.
