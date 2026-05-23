---
title: Recruiting
---

# Recruiting

Home does not run its own open call. New members arrive through **RoBorregos**, the robotics team that represents Tec de Monterrey campus Monterrey. As a PM your job is not to publish a public form. Your job is to **spot the right candidates inside the natural RoBorregos flow and pull them into Home at the right moment**.

## Where members come from

Three intake paths are active in any given year.

### 1. Advanced candidates go straight to Home

Every year RoBorregos runs an internal call that splits applicants into **beginners** and **advanced**. Advanced candidates already have experience (personal projects, other competitions, prior courses) and **usually skip juniors and join Home directly**. This path delivers the highest quality intake: people who already know Linux, programming, and sometimes ROS.

!!! tip "Catch them early"
    In the first general meeting, ask each new member where they come from. If they are advanced candidates, they are pre-qualified. If they are beginners who landed in Home for other reasons, see the next paths below.

### 2. Beginners who outgrew juniors

Some beginner candidates are accepted into RoBorregos but **no longer qualify for junior categories by age**. Those members often land in Home because Home is one of the few RoBorregos competitions with no junior age cap.

These members usually need **more technical onboarding** than advanced candidates. They might have no exposure to Linux, ROS, or Docker. Plan for that from the start (see [Onboarding](onboarding.md)).

### 3. Internal migration from juniors

After **TMR** (April), members who competed in junior competitions and decided not to continue into the international can switch to a different competition. Home is one of the options they can pick.

This path tends to produce the most committed members. They have already spent a year inside RoBorregos and know the culture. But you need to find them actively; they do not show up by themselves.

## The team selection form

When the **global RoBorregos spotlight** is published (the one that covers every competition, not Home's), it includes a **form where interested members declare which competition they want to apply to next year**. That form is what gives the team a roster of who belongs where.

As a PM, your responsibilities around the form are:

- [ ] **Make sure Home appears as an option** on the global team form. Coordinate with the general PMs so this happens.
- [ ] **Review the responses as soon as the form closes**. It tells you:
    - How many members you start the cycle with.
    - Which advanced candidates self-selected into Home.
    - Which members are migrating from juniors.
- [ ] **Talk 1:1 with each advanced candidate** to confirm interest and to start scoping where in Home they would fit best.
- [ ] **For beginners who ended up in Home** by the age path, plan their [extended onboarding](onboarding.md#for-members-without-technical-background) during the first week.

## When each intake path opens

The dates below are taken from the 2025 cycle. They are approximate and can shift year to year. Confirm with the general PMs at the start of your cycle.

```mermaid
gantt
    title Recruiting calendar (approximate, based on the 2025 cycle)
    dateFormat YYYY-MM-DD
    axisFormat %b

    section Candidates (RoBorregos-wide)
    Initial meeting (beginners + advanced kickoff) : milestone, 2025-08-25, 0d
    Candidates event                               : 2025-08-25, 2025-10-31
    Selection of accepted candidates               : 2025-10-31, 2025-11-15

    section Home
    Welcoming meeting                              : milestone, 2025-11-15, 0d
    Per-area onboarding (timing varies by area PM) : 2025-11-15, 2026-01-15

    section Junior migration
    TMR (junior competitions end here)             : milestone, 2025-04-30, 0d
    Migration window opens                         : 2025-04-30, 2025-08-25
```

What each item means:

- **Candidates kickoff (late August).** Single initial meeting at the start of the August semester. Both beginner and advanced candidates attend.
- **Candidates event.** The full RoBorregos onboarding-and-evaluation period for new applicants. In 2025 the last day was Halloween (October 31).
- **Selection.** Roughly two weeks after the event ends, accepted candidates are confirmed.
- **Welcoming meeting (mid November).** First meeting where the accepted candidates meet their team. For Home this is the [Phase 1 onboarding](onboarding.md#phase-1-general-welcome-meeting).
- **Per-area onboarding.** The area PM takes over their assigned members. There is no fixed schedule; it depends on the area.
- **Junior migration window (post TMR).** After TMR finishes (April), junior members who decided not to continue into the international can switch competitions. Home is one of the options.

## Signals to read when assessing a candidate

Home does not have a formal acceptance test. There are no hard requirements like "X hours per week" or "must know ROS". What follows are **signals a PM can use** to spot whether a candidate will fit, based on past experience. None of them are deal-breakers on their own.

| Signal | Why it helps you read the fit |
|---|---|
| Real willingness to commit to the cycle | The cycle is several months long. Home does not work with members who are enthusiastic for two weeks and disengage by November. Look for someone who understands that the competition is a real time investment, without putting a specific hour count on it. |
| Comfort in a Linux terminal | The stack runs on Ubuntu and Docker. Without Linux, the first weeks are slow. Not a blocker if they want to learn. |
| Programming experience in Python or C++ | All project code is in one of those. If they have neither, ask if they are interested in learning. |
| Self-driven learning attitude | Home does not give step-by-step tutorials. If they expect one, the gap shows up by week three. |
| Personal projects, hackathons, side experiments | A strong signal that they will keep going when something does not work the first try. |
| You did not know them personally before | Sometimes useful (less bias), sometimes harder (no track record). Notice the asymmetry. |

These are **heuristics, not gatekeeping criteria**. Use them in a short conversation with the candidate, not as a checklist.

!!! info "Home recruiting needs a real process"
    Today's reality: Home does not have a formal recruiting funnel. We rely on the global RoBorregos call + word of mouth + reading signals like the ones above. **This is one of the areas where future PMs should invest**. A short intake questionnaire (background, motivation, time commitment, prior experience), plus a single structured conversation, would go a long way. The signals above are a starting point for that questionnaire when someone gets to it.

## Common recruiting mistakes

- Accepting every applicant without filtering. Leads to demotivated members by week four.
- Not reaching out to advanced candidates fast enough. Another competition takes them if Home is slow.
- Forgetting the junior-migration window. Members who hit one year in RoBorregos are ripe, but you need to go get them.
- Not coordinating Home's presence on the global form with the general PMs. If your competition is not listed, no one applies.
