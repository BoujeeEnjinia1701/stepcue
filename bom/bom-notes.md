# BOM notes

- Prices are for one unit: one instrumented insole and one heel pod (decision D1 in `docs/decisions/0001-trl2-review-decisions.md`).
- Line numbers 1 to 11 match the exploded-view callouts in `media/exploded.png`. Line 12 (hardware and consumables) is partly modeled (the lid screws and tapes). Lines 13 (tail connector) and 14 (spacer foam) were added by the design for construction record STC-DDR-003; they are in the model and the build plan pictures, and the spacer is drawn as part of callout 3 in the exploded view.
- The FSR 402 price and the Adafruit 3898 cell price were checked against the supplier listings on 2026-09-25. All other prices are indicative and are confirmed at order.
- The total, USD 89.94, is checked against the value-engineering target in `project.yaml` (`budget_usd`, USD 200) by `docs/04-calcs/sizing.py` (STC-CAL-001, section 11). The target is a hypothetical control figure, not a spending limit.
- TRL 2 lines removed by the 2026-09-25 decisions: ESP32-C3 module, separate IMU breakout, piezo buzzer and analog multiplexer.
