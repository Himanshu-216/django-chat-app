from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.django import DjangoInstrumentor

# Set up tracer provider
trace.set_tracer_provider(TracerProvider())
tracer = trace.get_tracer_provider()

# Configure OTLP exporter
otlp_exporter = OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces")  # Update if needed
span_processor = BatchSpanProcessor(otlp_exporter)
tracer.add_span_processor(span_processor)

# Instrument Django
DjangoInstrumentor().instrument()
