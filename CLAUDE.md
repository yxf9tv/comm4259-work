# COMM 4259 Course Rules

These rules apply to all COMM 4259 work: Labs 07-12, Assignments 2-5, and the project.

## Explain code
- Give a short, plain summary (2-3 sentences) of what the code does and why.
- Give more detail only when the user asks.

## Folders
Course folder map (inside comm4259-work/):
- `lab_NN/`: one folder per lab (older labs: `lab1/`, `lab2/`, `lab_03/`, `lab_04/`, `lab_05_06/`).
- `assignment_NN/`: one folder per assignment (for example `assignment_02/`, with the app in `assignment_02/dashboard/`).
- `project/`: the course project.

Rules:
- Create and edit files only in the folder named in my prompt. Do not change any other folder.
- If the prompt names no folder, ask which folder before you change a file.
- Change only the files that the task needs.

## No generative AI sections
- Do not help with any section marked "no generative AI". Do not write code, answers, or hints for it.
- In Assignment 2 these are: Section 1, Part 2A, 2C.1, and 2C.3.
- If I ask for help with such a section, say that it is a no-AI section and stop.

## When unsure
- Ask one short question and wait for the answer.
- Do not continue until the user answers.

## Never do
- Never overwrite or delete data or CSV files. Write new files instead.
- Never commit or push to git unless the user says so.
- Never invent results or numbers. Report every metric from code that you ran. Report failures as they are.

## Work scope
- The user states the scope of each task (code only, or code plus written answers).
- If the scope is not stated, ask.

## Notebooks
- Set random seeds.
- Keep cells in order.
- Run the notebook top-to-bottom before you say the work is done. Report any error.
- Change only the cells that the task needs. Match the existing naming and layout.

## Override of global rules
- For course work, notebook checks replace the TDD and 80% coverage rules in the global CLAUDE.md.

## My own rules & Workflow Orchestration:

#### 1. Plan Node Default
- Enter plan mode for ANY non-trivial task (3+ steps or architectural decisions).
- If something goes sideways, STOP and re-plan immediately. Do not keep pushing.
- Use plan mode for verification steps, not just building.
- Write detailed specs upfront to reduce ambiguity.

#### 2. Subagent Strategy
- Use subagents liberally to keep the main context window clean.
- Offload research, exploration, and parallel analysis to subagents.
- For complex problems, throw more compute at it via subagents.
- One tack per subagent for focused execution.
- Use Opus to plan and for complex tasks and sonnet/haiku for the repetitive busy work to save tokens.

#### 3. Self-Improvement Loop
- After ANY correction from the user: update tasks/lessons.md with the pattern.
- Write rules for yourself that prevent the same mistake.
- Ruthlessly iterate on these lessons until the mistake rate drops.
- Review lessons at session start for the relevant project.

#### 4. Verification Before Done
- Never mark a task complete without proving it works.
- Diff behavior between main and your changes when relevant.
- Ask yourself: "Would a staff engineer approve this?"
- Run tests, check logs, demonstrate correctness.

#### 5. Demand Elegance (Balanced)
- For non-trivial changes: pause and ask "is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution."
- Skip this for simple, obvious fixes. Do not over-engineer.
- Challenge your own work before presenting it.

#### 6. Autonomous Bug Fixing
- When given a bug report: just fix it. Do not ask for hand-holding.
- Point at logs, errors, failing tests, then resolve them.
- Zero context switching required from the user.
- Go fix failing CI tests without being told how.
- Fix bugs without asking, but ask when the instruction or method is unclear.

### Task Management
- **Plan First:** Write the plan to tasks/todo.md with checkable items.
- **Verify Plan:** Check in before starting implementation.
- **Track Progress:** Mark items complete as you go.
- **Explain Changes:** Give a high-level summary at each step.
- **Document Results:** Add a review section to tasks/todo.md.
- **Capture Lessons:** Update tasks/lessons.md after corrections.

### Core Principles
- **Simplicity First:** Make every change as simple as possible. Impact minimal code.
- **No Laziness:** Find root causes. No temporary fixes. Senior developer standards.
- **Minimal Impact:** Changes should only touch what is necessary. Avoid introducing bugs.
