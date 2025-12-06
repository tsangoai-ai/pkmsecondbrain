TrevorOS v4.1 Folder Purpose Cheat Sheet
Location: vault root

00Admin
Purpose: Control tower and system docs.
Use: Store templates, reports, changelogs, and system notes.

00Admin/Templates
Purpose: Reusable note and log layouts.
Use: Daily log template, Edge Coach block, project brief templates, meeting note templates.

00Admin/Reports
Purpose: Periodic summaries.
Use: Monthly reviews, PD summaries, AI pilot snapshots, board report drafts.

00Admin/Changelogs
Purpose: System history.
Use: Record vault changes, workflow changes, and shortcut versions.

01Logs
Purpose: All raw capture that has a timestamp.
Use: Anything that feels like a log, not yet curated.

01Logs/Raw
Purpose: Ingest from Shortcuts and external tools.
Use: Direct output from TrevorOS Pro, clipboard captures, imported plain text.

01Logs/Processed
Purpose: Clean JSON records that pass schema validation.
Use: Output from daily_log_to_record and edgecoach_to_record, plus any future converters.

01Logs/InboxArchive
Purpose: Old raw inputs you no longer want in the active queue.
Use: Move processed files here instead of deleting.

01Logs/Daily
Purpose: Human written daily notes.
Use: One markdown file per day using the daily_log_template.

02Reflections
Purpose: Structured thinking and review.
Use: Anything where you step back and think.

02Reflections/Daily
Purpose: End of day reflections.
Use: Daily Edge Coach notes, quick debriefs.

02Reflections/Weekly
Purpose: Weekly reviews.
Use: What worked, what did not, priorities for next week.

02Reflections/Monthly
Purpose: Monthly and longer horizon reviews.
Use: Goal tracking, big-picture adjustments.

03Actions
Purpose: Work that needs to move.
Use: Tasks, decisions, roadmaps.

03Actions/Tasks
Purpose: Larger than a single Todoist line, smaller than a project.
Use: Multi step actions that matter enough to track in the vault.

03Actions/Decisions
Purpose: Decision log.
Use: Date, decision, options considered, rationale, next check date.

03Actions/Roadmaps
Purpose: Sequenced plans.
Use: PD cycles, AI framework rollout, multi month projects.

04Projects
Purpose: Anything with a clear outcome and end date.
Use: Store one hub note per project, plus links to related logs and reflections.

04Projects/EdTechPD
Purpose: District PD work.
Use: PD day plans, slide outlines, session backlogs, debriefs.

04Projects/Personal
Purpose: Personal projects.
Use: Health, house, side products, travel.

05Knowledge
Purpose: Reference library.
Use: Things you want to reuse, not logs of what happened.

05Knowledge/People
Purpose: Lightweight CRM.
Use: Key contacts, who they are, what you are working on with them.

05Knowledge/Systems
Purpose: Systems and workflows.
Use: TrevorOS specs, automation diagrams, AI pipeline notes.

05Knowledge/Policies
Purpose: Rules and guardrails.
Use: District policies, AI governance notes, union references.

05Knowledge/Tools
Purpose: Tool how to notes.
Use: Gemini, NotebookLM, Formative, Shortcuts, Make, Obsidian plugins.

05Knowledge/FAQ
Purpose: Question driven reference.
Use: “How do I…?” answers for your future self and for staff.

05Knowledge/Recipes
Purpose: Cooking and repeatable setups.
Use: Food, prep flows, plus any “recipe style” tech setups.

05Knowledge/Recipes/Inbox
Purpose: Quick drops from web or screenshots.
Use: Paste rough notes here before turning into cards.

05Knowledge/Recipes/Cards
Purpose: Clean recipe cards.
Use: One per dish or setup.

05Knowledge/Media
Purpose: Content you want to remember.
Use: YouTube, shorts, reels, talks.

05Knowledge/Media/YouTube
Purpose: YouTube items.
Use: One note per video or playlist with summary and links.

05Knowledge/Media/ReelsShorts
Purpose: Short form clips.
Use: Captured via Shortcut, summarized later.

inbox
Purpose: General catch all.
Use: Anything that does not have a clear home yet.

attachments
Purpose: Files that support notes.
Use: PDFs, images, exports tied to notes.

index.json
Purpose: Machine readable index.
Use: Future automation. No direct edits.

TrevorOS_v41
Purpose: Engine room for the schema and tools.
Use: Hold JSON schema, ontology, templates, and CLI conversion tools.

TrevorOS_v41/templates
Purpose: Authoritative template sources.
Use: Capture JSON, daily log, Edge Coach block.

TrevorOS_v41/tools
Purpose: CLI utilities.
Use: validate_schema, edgecoach_to_record, daily_log_to_record.

TrevorOS_v41/examples
Purpose: Working demonstrations.
Use: Example markdown, example JSON records for testing.