# LinkedIn Post — SIGNAL May 2026 (evergreen framing)

No human was in the loop when Claude Code executed a file operation outside its intended scope.

Anthropic published a postmortem on it, and it's still the clearest case study I've seen for anyone running AI agents with write access to a codebase.

The agent had broad filesystem access for a refactoring task. It hallucinated a path, confused src/ with config/, and the tooling executed the change without a second check. The task had been marked "routine."

The hallucination wasn't the root cause, it was the trigger. The root cause was the missing sandbox: no validation layer, no capability model, no automatic rollback. Anthropic's tooling trusted the model's output at face value.

The fix had three parts: time-bound permissions per session, sandboxed writes requiring human approval outside the working directory, and automatic rollback if tests fail after an agent session.

Treat any AI agent with write access as a junior developer with root. Define a capability model before you give it the keys: what it can read, what it can write, what needs a human to sign off.

This came out of SIGNAL, our monthly filter for what actually matters in distributed systems, alongside Oracle's proposal to kill JVMCI (the API that lets GraalVM plug into the JVM) and Amazon and Red Hat pushing back. Full issue: [link]

Running agents with filesystem access in your own stack. What does your capability model look like?
