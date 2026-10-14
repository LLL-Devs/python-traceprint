API reference
=============

All supported imports below come from ``traceprint``. Signatures and methods
are generated from the installed package. The :doc:`usage` explains common
combinations and cleanup.

Tracer
------

.. autoclass:: traceprint.Tracer
   :members:

Constructor options
~~~~~~~~~~~~~~~~~~~

* ``stream``: text sink; defaults to the current stdout at construction. An
  implicit sink is refreshed on installation. ``error_stream`` is accepted for
  compatibility but does not currently select a separate intercepted stderr sink.
* ``intercept_stdout`` and ``intercept_stderr``: install on construction when
  requested; both default to ``False``. Call ``uninstall()`` for cleanup.
* ``use_colors``: TTY detection when ``None``; otherwise an explicit boolean.
* ``use_tabulation``: four spaces per nesting level; defaults to ``False``.
* ``color_scheme``: ANSI strings selected cyclically by depth. An empty list or
  ``None`` selects the default palette.
* ``metacolor``: metadata color; defaults to dark grey. ``None`` uses the depth
  color for the entire line.
* ``print_transitions``: show entry and exit messages; defaults to ``False``.
* ``filter_levels``: allowed depths or a depth predicate; ``None`` allows all.
* ``start_enabled``: defaults to ``True``; disabled output is forwarded raw.
* ``output_format``: Python format string; defaults to timestamp, cumulative time,
  elapsed time, full label and the original message.
* ``timestamp_format``: UTC ``strftime`` format, default ``%Y-%m-%d %H:%M:%S``.

``configure()`` accepts configuration attributes after construction and raises
``AttributeError`` for unknown names. ``depth`` and ``labels`` describe the shared
current context; use spans or push/pop to manage them. ``write()`` returns the
length of the input even when output is filtered. ``format()`` formats a message
without writing, advances timing and does not change the current line state.

Global tracer
-------------

.. autodata:: traceprint.tracer
   :no-value:

The convenience instance is created at import without stream installation. It
can be seeded by ``TRACEPRINT_INITIAL_LABELS``; see :doc:`usage`.

Function tracing
----------------

.. autofunction:: traceprint.trace

Supports ``@trace`` and ``@trace(label="name", tracer_instance=target)``. The
wrapped function's result and exceptions pass through, and context is restored
in ``finally``. ``force`` is a transition-emission option; emitted writes still
obey depth filtering. This decorator targets synchronous functions.

Logging handlers
----------------

.. autoclass:: traceprint.TracerHandler
   :members: emit

An optional standard logging formatter prepares the record before tracer
formatting. Omitting ``tracer_instance`` selects the global tracer.

.. autoclass:: traceprint.TracerFileHandler
   :members: emit, write, flush, close
   :undoc-members:

The file opens on construction, creating parent directories. Default mode is
append and encoding is UTF-8. Direct ``write()`` expects already formatted text;
``emit()`` adds tracer formatting. The sink strips terminal escapes. Remove the
handler from its logger or tracer and close it when finished.

Logger mixin
------------

.. autoclass:: traceprint.LoggerMixin
   :members: logger, log

``verbose`` controls calls through ``self.log``; accessing ``self.logger`` gives
the underlying standard logger without that proxy gate. ``logging_level`` sets
its level. ``lazy_init`` delays logger creation until access.
``logging_passthrough`` routes through the global tracer and replaces handlers
on the shared class-named logger; defaults to ``False``.

Color constants
---------------

.. autodata:: traceprint.DARK_GREY
   :no-value:

.. autodata:: traceprint.DEFAULT_COLORS
   :no-value:

.. autodata:: traceprint.RESET
   :no-value:

ANSI metadata color, cyclic depth palette and reset sequence, respectively.
