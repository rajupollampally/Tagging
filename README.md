# Story Tagging System Documentation

## Overview

This document describes a story tagging system for Digital.ai Agility. The goal is to improve ownership and decision-making for story release timing by clearly indicating when a story is completed and when it should be released.

## Problem Statement

It is often unclear whether a completed story should be released in the next available release or held for a later release. For example, a story completed in August might be suitable for August release after testing, or it might need to wait for October.

## Proposed Solution

Introduce a tagging system that attaches two timeline tags to each story:

- **Completion Month**: when the story is expected to be completed.
- **Target Release Month**: when the story is intended to be released.

## Tag Format

Use the following standardized format:

- `CM-[MONTH]` — Completion Month
- `TRM-[MONTH]` — Target Release Month

### Example

A story completed in August with an October release target would use:

- `CM-AUG`
- `TRM-OCT`

## Implementation Process

1. **Tag Creation**
   - When a story is created, the responsible team member assigns both `CM-[MONTH]` and `TRM-[MONTH]` tags.

2. **Tag Review**
   - A supervisor reviews the assigned tags to ensure they accurately reflect the expected completion and release timeline.

3. **Tag Updates**
   - If the story timeline changes during development, update the tags accordingly.

4. **Release Planning**
   - Use the `TRM-[MONTH]` tag to identify which stories are intended for each release cycle.

5. **Reporting**
   - Generate reports from Digital.ai Agility using these tags to track story flow and release readiness.

## Roles and Responsibilities

- **Team Members**: assign initial timeline tags at story creation.
- **Supervisors**: review and approve tags prior to delivery manager submission.
- **Delivery Manager**: use the tags to plan releases and manage story inclusion.

## Benefits

- Clear ownership and accountability for story timing.
- Improved visibility into release planning.
- Easier decisions about whether stories belong in the current or future release.
- Better tracking of development progress against planned releases.

## Next Steps

- Implement the tagging system in Digital.ai Agility.
- Train team members on the new tagging process.
- Establish a regular review cadence to verify correct tag usage.
- Gather feedback after 1–2 release cycles and refine the process as needed.

## Sample Backend Implementation

This repository now includes a minimal FastAPI backend to support story tagging and release planning:

- `DevOps-Automation-Platform/app/config.py` — configuration settings.
- `DevOps-Automation-Platform/app/security.py` — JWT and RBAC utilities.
- `DevOps-Automation-Platform/app/database/session.py` — SQLAlchemy session and initialization.
- `DevOps-Automation-Platform/app/models/story.py` — story model for timeline tagging.
- `DevOps-Automation-Platform/app/main.py` — FastAPI application with story CRUD endpoints.
- `DevOps-Automation-Platform/requirements.txt` — Python dependencies.

### Running the service

1. Copy `.env.example` to `.env` and update connection settings.
2. Install dependencies:
   ```bash
   pip install -r DevOps-Automation-Platform/requirements.txt
   ```
3. Start the service:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Story Tagging API

- `POST /stories` — create a story with `CM-[MONTH]` and `TRM-[MONTH]`.
- `GET /stories` — list all stories.
- `GET /stories/{story_id}` — retrieve a story.
- `PUT /stories/{story_id}` — update a story.
- `DELETE /stories/{story_id}` — delete a story (admin only).

## Docker Support

Build and run with Docker:

```bash
docker build -t tagging-api .
docker run --env-file .env -p 8000:8000 tagging-api
```

Or use Docker Compose:

```bash
docker compose up --build
```

The service will be available at `http://localhost:8000`.
