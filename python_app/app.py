import os
from flask import Flask, request, jsonify
import requests

# 1. Importações do OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# NOVO: Importações para o OTLP Exporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter # Opcional: para ver traces no console

# 2. Instrumentações
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor


# 3. Configuração do TracerProvider e Exporter
# Para o Jaeger, é uma boa prática definir o service.name no Resource
resource = Resource.create({
    "service.name": "my-python-flask-app", # Mantenha ou adicione esta linha
})

# Configure o TracerProvider
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)


# === REMOVA OU COMENTE A LINHA jaeger_exporter ANTIGA ===
# from opentelemetry.exporter.jaeger.thrift import JaegerExporter
# jaeger_exporter = JaegerExporter(
#    agent_host_name=os.getenv("JAEGER_AGENT_HOST", "jaeger"),
#    agent_port=int(os.getenv("JAEGER_AGENT_PORT", 6831)),
# )

# NOVO: Configurar o OTLP Exporter
otlp_exporter = OTLPSpanExporter(
    endpoint=os.getenv("JAEGER_OTLP_ENDPOINT", "http://jaeger:4317"), # Jaeger Collector OTLP gRPC endpoint
    # Se você quiser OTLP/HTTP: endpoint="http://jaeger:4318/v1/traces"
)


# Adicione o exporter ao TracerProvider
provider.add_span_processor(
    BatchSpanProcessor(otlp_exporter)
)

# Opcional: para ver os spans no log do console também
# provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))


# Instrumentar a aplicação Flask e a biblioteca requests
app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

# Obtenha o tracer (já corrigido em passos anteriores)
tracer = trace.get_tracer(__name__)

# Seu código de rota Flask
@app.route('/')
def home():
    with tracer.start_as_current_span("process_home_request") as span:
        message = "Hello from Python Flask App!"
        # Exemplo de chamada HTTP externa
        try:
            response = requests.get("https://www.google.com", timeout=5)
            span.set_attribute("http.status_code.google", response.status_code)
            message += f" Google Status: {response.status_code}"
        except requests.exceptions.RequestException as e:
            span.set_attribute("error", True)
            span.set_attribute("error.message", str(e))
            message += f" Error calling Google: {e}"
        return jsonify(message=message)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
