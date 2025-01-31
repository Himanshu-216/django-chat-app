# from django.shortcuts import render
# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from prometheus_client import start_http_server
# from opentelemetry import metrics
# from opentelemetry.exporter.prometheus import PrometheusMetricReader
# from opentelemetry.sdk.metrics import MeterProvider
# from opentelemetry.sdk.resources import SERVICE_NAME, Resource
# from opentelemetry.sdk.trace.export import (
#     BatchSpanProcessor,
#     ConsoleSpanExporter,
# )

# resource = Resource(attributes={
#     SERVICE_NAME: "otel-service"
# })

# start_http_server(port=9464, addr="localhost")

# # reader = PrometheusMetricReader()
# # provider = MeterProvider(resource=resource, metric_readers=[reader])
# # metrics.set_meter_provider(provider)

# provider = TracerProvider()
# processor = BatchSpanProcessor(ConsoleSpanExporter())
# provider.add_span_processor(processor)

# # Sets the global default tracer provider
# trace.set_tracer_provider(provider)

# # Creates a tracer from the global tracer provider
# tracer = trace.get_tracer("my.tracer.name")

# # @login_required
# def home_view(request):
#     with tracer.start_as_current_span("span-name") as span:
#             print('span started')
#     return render(request, 'home.html')


from django.shortcuts import render
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from prometheus_client import start_http_server
from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import Resource, SERVICE_NAME
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.prometheus import PrometheusMetricReader

# Define OpenTelemetry resource
resource = Resource(attributes={SERVICE_NAME: "otel-service"})

# Start Prometheus HTTP server
start_http_server(port=9464, addr="0.0.0.0")  # Allow access from outside localhost
print('started')

# Configure Prometheus metrics reader
prometheus_reader = PrometheusMetricReader()
meter_provider = MeterProvider(resource=resource, metric_readers=[prometheus_reader])
metrics.set_meter_provider(meter_provider)

# Configure OpenTelemetry tracing
tracer_provider = TracerProvider(resource=resource)
span_processor = BatchSpanProcessor(ConsoleSpanExporter())  # Export spans to console
tracer_provider.add_span_processor(span_processor)
trace.set_tracer_provider(tracer_provider)

# Create a tracer
tracer = trace.get_tracer("my.tracer.name")

# Django view
def home_view(request):
    with tracer.start_as_current_span("span-name") as span:
        span.add_event("Home view accessed")  # Add metadata to span
    return render(request, 'home.html')
