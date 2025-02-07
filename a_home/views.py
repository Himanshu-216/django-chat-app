from django.shortcuts import render
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor, ConsoleSpanExporter
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

# Define OpenTelemetry resource
resource = Resource(attributes={ResourceAttributes.SERVICE_NAME: "otel-service"})

# Configure OpenTelemetry tracing
tracer_provider = TracerProvider(resource=resource)
# span_processor = BatchSpanProcessor(ConsoleSpanExporter())
span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector:4318/v1/traces"))
tracer_provider.add_span_processor(span_processor)
trace.set_tracer_provider(tracer_provider)

# Create a tracer
tracer = trace.get_tracer("my.tracer.name")

# Configure OpenTelemetry metrics
# otlp_metric_exporter = OTLPMetricExporter(endpoint="http://otel-collector:4318")
# metric_reader = PeriodicExportingMetricReader(otlp_metric_exporter)
# meter_provider = MeterProvider(resource=resource, metric_readers=[metric_reader])
# metrics.set_meter_provider(meter_provider)

print("OpenTelemetry tracing and metrics configured successfully.")

def home_view(request):
    with tracer.start_as_current_span("parent-span") as parent_span:
        print(parent_span)
        parent_span.add_event("Home view accessed")

        # Creating a proper child span
        with tracer.start_as_current_span("child-span") as child_span:
            child_span.add_event("Inside child span")                                                   

    return render(request, 'home.html')

