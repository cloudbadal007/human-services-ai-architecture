.PHONY: install test test-unit test-integration test-compliance test-scenarios demo compliance-report lint clean

install:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=src/human_services --cov-report=term-missing

test-unit:
	pytest tests/unit/ -v

test-integration:
	pytest tests/integration/ -v

test-compliance:
	pytest tests/integration/test_eu_ai_act_*.py -v

test-scenarios:
	python -m tests.scenarios.contextually_insane_agent
	python -m tests.scenarios.single_mother_scenario
	python -m tests.scenarios.compliance_audit_simulation

demo:
	python scripts/demo.py

compliance-report:
	python scripts/compliance_audit.py

lint:
	ruff check src/ tests/

clean:
	rm -rf __pycache__ .pytest_cache .mypy_cache dist build *.egg-info .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
