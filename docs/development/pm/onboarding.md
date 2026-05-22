---
title: Onboarding
---

# Onboarding

Onboarding in Home has **two phases**: a general meeting run by the general PMs (all new members together, every area presenting), and a deep onboarding inside each area (area PM with their new members). The two are distinct responsibilities and both are necessary.

!!! warning "Home expects self-driven learning"
    Unlike juniors, Home does not give step-by-step tutorials for every tool. State this explicitly during the general meeting. If a member is not willing to learn on their own, they do not fit in Home. Better to find that out in week one than in week four.

## Phase 1. General welcome meeting

**Owner:** general PMs.
**When:** first Home meeting after applications close.
**Attendees:** all new members, every area PM, both general PMs.

### Typical agenda (about 90 min)

1. **Welcome and Home vision** (15 min).
    - What @Home means inside RoBorregos and RoboCup.
    - What the robot is (FRIDA) and what it does.
    - Macro calendar for the year: TMR (April / May), RoboCup (June / July), demos.

2. **Each area presents** (about 8 min each, six areas = 48 min).
    - The area PM explains:
        - What the area does (what technical problem it solves).
        - Sub-areas they work on and who is active there.
        - What they look for in new members.
        - Tutorial and tooling recommendations to start studying (videos, codelabs, books).

3. **Area assignment** (15 min).
    - New members pick an area. Many include a second and third choice in case the first one is full.
    - General PMs validate and break ties.

4. **Closing and next steps** (10 min).
    - Remind everyone that per-area onboarding starts the following week.
    - Restate the expectation of self-driven learning.
    - Show where the documentation lives (this site, Home-Docs).

!!! tip "Half the value is the tutorial recommendations"
    The new member does not know what to study first. If your area uses ROS 2, recommend it explicitly: *"start with the official ROS 2 Humble tutorials, then come back to us."* Without that, they will stare at code for two weeks and learn nothing.

## Phase 2. Per-area onboarding (area PM)

After the general meeting, **the area PM takes over** the new members assigned to that area. The goal for this phase is that in **three to four weeks** the member can pick up real tasks.

### Recommended plan

=== "Week 1. Setup and orientation"

    1. **Share the area docs**. Point them to this site's pages for your area. For Manipulation: `Development → Manipulation → Setup & Build`.
    2. **Technical setup**:
        - Clone the project repo (with `--recursive`).
        - Install Docker.
        - Run `./run.sh <area>` for the first time (this can take 30+ minutes on slower hardware).
        - Confirm they can bring up the basic stack for the area.
    3. **Code walkthrough**, group or 1:1.
    4. **Buddy assignment**. A veteran member of the area is their first point of contact. This reduces friction more than anything else.

=== "Week 2. First small task"

    1. Give them a **scoped task** that touches the main flow of the area but with no risk of breaking anything critical. Examples:
        - **Manipulation**: add a new named pose to `xarm_configurations.py` and try it from `keyboard_input`.
        - **Vision**: wire an existing detector to the pipeline with a new parameter.
        - **Navigation**: build a new map or tune planner parameters.
    2. **Code review** their PR. That first review teaches team conventions.

=== "Weeks 3 and 4. Cross-area task (optional)"

    1. If the member is on track, give them something that requires coordinating with another area (for example vision plus manipulation).
    2. Bring them to their first **cross-area discussion** so they see how API boundaries get negotiated.
    3. By the end of week four they should be ready to pull tasks from the backlog without close supervision.

### For members without technical background { #for-members-without-technical-background }

Some members land in Home because they no longer qualify for juniors by age (see [Recruiting](recruiting.md#2-beginners-who-outgrew-juniors)). These members usually need an extra two or three weeks before touching the area stack:

| If they don't know... | Recommend first |
|---|---|
| Linux / terminal | [The Missing Semester (MIT)](https://missing.csail.mit.edu/), first four lessons. |
| Python | [Python official tutorial](https://docs.python.org/3/tutorial/) plus a tiny personal project. |
| Git | [Pro Git book](https://git-scm.com/book/en/v2), first three chapters. |
| Docker | [Docker getting started](https://docs.docker.com/get-started/), sections 1 to 4. |
| ROS 2 | [ROS 2 Humble tutorials](https://docs.ros.org/en/humble/Tutorials.html): `Beginner: CLI tools` and `Beginner: Client libraries`. |

Be honest with them: "You will spend two weeks on tools before touching our code. It is normal and expected."

## What to publish and where

| Resource | Where it lives | Owner |
|---|---|---|
| This documentation | [home-docs](https://github.com/RoBorregos/Home-Docs) | All PMs |
| Project repo | [home2](https://github.com/RoBorregos/home2) | The whole team |
| Active member roster by area | Form / sheet in the RoBorregos Drive | General PM |
| Per-area Slack / WhatsApp channel | (varies by area) | Area PM |

## Common mistakes

- Skipping the general meeting. New members arrive at an area without global context. They do not understand how Home fits inside RoBorregos or RoboCup.
- Running the general meeting but skipping per-area onboarding. The member floats. They do not even know what to clone.
- Assuming everyone already knows Docker and ROS 2. If the person comes from juniors or from outside RoBorregos, they probably do not.
- Not assigning a buddy. The PM cannot be the only point of contact. A veteran absorbs 80% of the technical questions.
- Expecting results by day 14. A new member is realistically productive around week four in the best case. Plan for that.
