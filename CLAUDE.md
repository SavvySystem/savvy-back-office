# Savvy back office

This folder is where Savvy's back-end work happens in Claude Code: setting up tools, building screens, fixing skills, and keeping the structure organized. It holds pointers, notes and scripts. It holds no rules, records or client facts of its own.

## Read these live, every time

Savvy's records are in the Airtable base **Savvy — Master Operations**. Read what you need live. Never work from memory or from an earlier chat.

- **The back-end list:** the open Tasks linked to the Builds row "The Reorganization of our systems and processes (Claude project)". Each task's Instructions, "For Claude" field and What's left say what it is, how to do it and where it stopped.
- **The map:** the table Where Things Live. It says where each kind of thing lives. Read only the rows for the Area you're working in.
- **Rules:** HOW·Standards. Read the logging rule (STD-251), the delete rule (STD-232) and the 'Who says yes' rows live before acting on them.
- **Before any Airtable write:** load the `airtable-write-safely` skill.
- **Before building or changing a screen:** read that screen's row in Builds first. A screen's own row wins on how it looks. The look rule (STD-188) covers what the row doesn't say. Carley's Staff Preferences tagged "Working on screens" are background. Build in the Zite test copy only. Nothing is published without Carley's yes. When someone says something about a screen, put their words on that screen's row the same turn, and make a fix card (Playbook template "Fix something on a page") for anything that should change.
- **Skills:** the copy of Savvy's skills repository is next door, at `../savvy-skills-repo`.

## How chats work here

- One task per chat. Start with "pick up [task name]", or paste the task's Copy for Claude text. End with "wrap up", which saves where it stopped on the task.
- Where something stands goes on its task in Airtable the same turn it changes, not only in the chat or in this folder.
- Background chats: two or three at most, each on exactly one task from the back-end list, only for long jobs that don't need a person midway. Each ends with the wrap-up skill on its task.
- Decisions come to Patrick or Carley grouped by area, each with why, the options, Claude's pick and what it changes. Bring only the decisions on the path of the work at hand.
- Hand-over notes for the next chat go in `notes/`. They're for chats, not people. What people need goes on the task.

## Never

- Copy a rule, a standard or a record into this folder. Point to it instead.
- Give a person record IDs or an Airtable link.
- Turn on an automation, publish a screen, delete anything, or send anything a client, vendor or the team will see without the yes the rules name.
