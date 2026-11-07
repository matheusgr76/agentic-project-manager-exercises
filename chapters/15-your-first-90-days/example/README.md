# Runnable Chapter 15 pilot plan

From the repository root, with Python 3.10 or newer:

~~~powershell
python chapters/15-your-first-90-days/example/plan_builder.py --case a
python chapters/15-your-first-90-days/example/plan_builder.py --case b
python chapters/15-your-first-90-days/example/plan_builder.py --case c
python chapters/15-your-first-90-days/example/plan_builder.py --case d
python chapters/15-your-first-90-days/example/plan_builder.py --case e
python -m unittest discover -s chapters/15-your-first-90-days/example/tests -v
~~~

The program reads [fictional pilot charters](fixtures/pilot-cases.json), [phase gates](phase-gates.json), the [required stop conditions](required-stop-conditions.json), and a committed copy of Chapter 14's [fictional recorded value result](fixtures/value-recorded.json). It writes `outputs/<case>/plan.json` and `plan.md`; the output folder is ignored by Git. Read the [policy](90-day-policy.md), [expected results](expected-results.md), and [sample plan](sample-plan.md) before adapting the [reader prompt](pilot-prompt.md).

To use the files produced by Chapter 14 instead of the committed copy, first run Chapter 14's `recorded` scenario. Then add `--from-prior-outputs` to a Chapter 15 command. The plan accepts that result only as a fictional projection with unmeasured delivery improvement.

The generated plan is a draft. It does not authenticate a person, verify access approval, collect baseline tasks, call a model or connector, deploy anything, or authorize expansion. The reader must replace Acme's invented figures with approved evidence from a real pilot.
