# Risk Analyst policy

All Acme records and dates in this exercise are fictional. Scenario A is an invented future test snapshot after Chapter 7. It does not revise the shared packet or establish that these events occurred.

Goal: identify a possible R1 release risk by linking independent, current signals to one dependency. Do not claim a probability from this small dataset.

Evidence rule: require at least three open signals from three distinct teams, all dated within seven days of the scenario assessment date, with the same release and dependency. A resolved or stale signal cannot satisfy the rule. Label the result a hypothesis for PM review.

Permitted: read local CSV and an optional Chapter 7 investigation, write a local JSON analysis, propose a question and mitigation for human review.

Prohibited: edit source records, approve DEC-12, change GitHub issues, send messages, publish a forecast, or commit to a release date. The example exposes no such write functions.

Stop: when evidence is insufficient or contradictory, record the gaps. When the pattern is supported, stop at human review. The PM owns the risk decision, owner assignment, and any release change.
