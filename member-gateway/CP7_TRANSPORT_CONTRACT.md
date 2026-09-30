# CP7 — AI Transport Integration Contract

**Status:** IMPLEMENTATION / NOT PRODUCTION TRANSPORT

## Decision
CP7 implements a thin AI-facing adapter contract over the existing transport-independent Service Core. It does **not** deploy an MCP/HTTP server or claim OAuth/network authentication. Choosing/deploying a concrete protocol without a verified hosting/auth environment would convert an implementation proof into an unsupported production claim.

The adapter proves the boundaries required before concrete MCP exposure:
- delegated client identity is resolved before discovery/invocation;
- capability discovery exposes only authorized semantic capabilities;
- no Director/Bullpen/Mercer tools;
- only read-only capabilities may cross this initial transport;
- bounded request schema;
- per-client limiter contract;
- unknown capability fails closed;
- GatewayService remains the authority/execution path;
- missing Truth Plane output remains BLOCKED/AWAITING_SCK.

## Deferred to concrete transport/deployment
- OAuth/token issuer and secret storage;
- distributed rate/concurrency limiter;
- TLS/network ingress;
- MCP wire-protocol conformance;
- production hosting and observability.

These are not CP7 PASS claims and remain required before production certification.
