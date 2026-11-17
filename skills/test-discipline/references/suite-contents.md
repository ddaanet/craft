# What belongs in the suite

- **Automate by default.** A manual check does not compound: it is a tax paid
  again on every change. Keep manual only for judgement no assertion can
  express, and re-ask the question on each plan — a check too hard to automate
  last time is often trivial once a fixture exists.
- **Writing the cases is most of the cost.** Once the cases are written,
  automating them is a small markup on that work. Do not propose an agent-driven
  test where an assertion-based shell test works; eyeball only what resists
  assertion — TUI rendering, screenshot diffs, smoke output on real data.
- **Grep the suite before writing a fixture.** The path is often already
  covered. A hand run is for dogfooding the real product end to end, which is a
  different job from testing a script.
- **A skipped test is a dead test.** A test that cannot run on some platform for
  want of a tool (macOS ships no `timeout`) is made portable: replace the
  dependency with something the suite owns, and pin that replacement with a test
  of its own. Never `skip` it and never branch per platform — a skip reports
  green while checking nothing, and a branch is a skip on every machine but one.
- **Dogfood the day it ships.** Run a self-contained slice on the real target
  the same day rather than letting the next plan validate the last one. Fixtures
  encode what was expected to vary; the real environment holds what nobody
  thought to parameterize. A surprise there is a patch to the just-shipped plan.
  Running the pipeline on real data *before* planning is the `plan-contracts`
  skill's.
- **A clean run says nothing about failure reporting.** It is evidence about
  behaviour, never about observability. Enumerate the failure paths and ask who
  learns about each: one silent to everyone gets fixed; one visible to the user
  but not the agent is weaker; one whose signal would be inferred rather than
  observed may stay silent when inferring it produces false alarms.
