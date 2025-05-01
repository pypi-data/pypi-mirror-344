# Saga Orchestrator SDK

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A gRPC-based implementation of the Saga pattern for distributed transactions.

## Features

- Transaction orchestration
- Automatic compensation
- gRPC interface
- Pluggable storage backends

## Installation

```bash
pip install grpc_orchestrator
```

## Quick Start

```python
from saga_orchestrator import SagaClient

client = SagaClient(orchestrator_host="localhost")

response = client.start_saga(
    saga_id="order_123",
    steps=[{
        "service": "payment:50051",
        "method": "ChargeCard",
        "compensation": "RefundPayment"
    }]
)
```