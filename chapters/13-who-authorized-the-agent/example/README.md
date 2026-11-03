# Runnable Chapter 13 authority gate

From the repository root, with Python 3.10 or newer:

~~~powershell
python chapters/13-who-authorized-the-agent/example/authority_gate.py --case a
python chapters/13-who-authorized-the-agent/example/authority_gate.py --case b
python chapters/13-who-authorized-the-agent/example/authority_gate.py --case c
python chapters/13-who-authorized-the-agent/example/authority_gate.py --case d
python chapters/13-who-authorized-the-agent/example/authority_gate.py --case e
python chapters/13-who-authorized-the-agent/example/authority_gate.py --case f
python -m unittest discover -s chapters/13-who-authorized-the-agent/example/tests -v
~~~

The program reads the committed Chapter 12 [reviewable health record](fixtures/health-a.json), [fictional requests](fixtures/requests.json), [fictional actor context](fixtures/actor-context.json), [fictional approvals](fixtures/approvals.json), and [policy](policy.json). It writes `outputs/<case>/decision.json` and `outputs/audit.jsonl`. The ignored output files contain source IDs, not raw `source_text`.

For a direct handoff, run Chapter 12 case A first, then add `--from-prior-outputs` to a Chapter 13 command. Both `READY_FOR_PM_REVIEW` and a safe `ALREADY_PROCESSED` replay are accepted as reviewable inputs. A blocked, mismatched, or already published run cannot authorize an external-effect action.

The [authority matrix](authority-matrix.md) explains the scopes; [expected results](expected-results.md) gives the case sequence. Use the [governance prompt](governance-prompt.md) and [checklist](governance-checklist.md) to write a human review note and identify what a real pilot would still require.

No command authenticates a real person, accesses a secret, calls an external service, or executes an authorized action. `SIMULATED_AUTHORIZED` is a policy-test result only.
