PYTHON ?= python3
ROOT_DIR := TrevorOS_v41

validate:
	$(PYTHON) $(ROOT_DIR)/tools/validate_schema.py $(ROOT_DIR)/examples/sample.json

tree:
	find $(ROOT_DIR) -maxdepth 4 -print

edgecoach-example:
	@echo "Work:" >  $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "- Draft AI PD agenda." >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "Personal:" >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "- Walk after work." >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "Emotional State:" >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "- Tired but optimistic." >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "Tasks:" >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "- Finalize governance slide." >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "Decisions:" >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "- Prioritize teacher workflows first." >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "Concerns:" >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "- Cognitive overload for staff." >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "Wins:" >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "- Framework draft approved." >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "Questions for Later:" >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "- How to measure long-term impact?" >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "Next Actions:" >> $(ROOT_DIR)/examples/edgecoach_example.txt
	@echo "- Schedule site leader check-in." >> $(ROOT_DIR)/examples/edgecoach_example.txt

	$(PYTHON) $(ROOT_DIR)/tools/edgecoach_to_record.py \
		--edgecoach-file $(ROOT_DIR)/examples/edgecoach_example.txt \
		--record-type reflection \
		--title "Example Edge Coach Reflection" \
		--status draft \
		--owner trevor \
		--output $(ROOT_DIR)/examples/edgecoach_record.json

	$(PYTHON) $(ROOT_DIR)/tools/validate_schema.py $(ROOT_DIR)/examples/edgecoach_record.json

dailylog-to-record:
	$(PYTHON) $(ROOT_DIR)/tools/daily_log_to_record.py \
		--input $(ROOT_DIR)/examples/daily_log_example.md \
		--output $(ROOT_DIR)/examples/daily_log_record.json
	$(PYTHON) $(ROOT_DIR)/tools/validate_schema.py $(ROOT_DIR)/examples/daily_log_record.json
