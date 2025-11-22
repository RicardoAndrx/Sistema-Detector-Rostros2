#!/usr/bin/env bash
# Script funcional simple (requiere servidor corriendo en otra terminal)
set -e
mkdir -p evidence
curl -v -X GET http://127.0.0.1:8000/ > evidence/functional_home.txt 2>&1 || true
curl -v -X GET http://127.0.0.1:8000/validation_status/ > evidence/functional_status.txt 2>&1 || true
# Flujo POST de validación (fallará si no hay session form_data, esperado manejar error)
curl -v -X POST http://127.0.0.1:8000/process_validation/ -H 'Content-Type: application/json' -d '{}' > evidence/functional_process.txt 2>&1 || true
