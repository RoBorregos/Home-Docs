---
title: Handoff
---

# Handoff

When your cycle ends, the next PM walks in cold. Whatever does not get written down gets lost. This page is the checklist of what to leave behind so the next person can pick up without spending two months rediscovering things you already knew.

There are two sides to a handoff: what you write down once at the end, and the ongoing habits during the year that make the final handoff easier. Both matter.

## End-of-cycle checklist

Before stepping down, leave the following in a place the next PM can find on day one (a shared Drive folder or a private repo works; do not use Slack or your personal notes).

### System state

- [ ] **What works**. Features that are stable and integrated. Per area.
- [ ] **What is broken**. Known bugs, scope of impact, last known reproduction.
- [ ] **What is half done**. Features that started but did not land. For each: the PR or branch, the author, the percentage done, and whether it should be finished or dropped.
- [ ] **Open dependencies**. Cross-area tasks that were blocking something at the end of the cycle.
- [ ] **Hardware status**. What is on the robot, what is in the lab in a drawer, what was lost during travel.

### Priorities for the next cycle

- [ ] **Top three problems** to solve next, in order. Be specific. Not "improve manipulation" but "make pick-cutlery reliable above 80%".
- [ ] **What you would NOT recommend** to start. Things that look tempting but cost more than they yield. Spend a paragraph on each so the next PM avoids the trap.
- [ ] **Risks for the next TMR / RoboCup** that you see today. Even rough ones.

### Key contacts

A simple sheet with name, role, when to contact, how. Examples:

| Name | Role | Reach out for | Channel |
|---|---|---|---|
| Dr. X | Academic advisor | Research questions, paper review, scholarships | Email |
| (sponsor name) | Hardware sponsor | Donations, equipment loans | LinkedIn / email |
| (RoBorregos pres.) | Team president | Escalations, budget, cross-competition issues | Slack |
| (RoBorregos fin.) | Finance officer | Reimbursements, purchases, travel | Email |
| (Active members) | By area | Technical questions per area | Slack channels |

### Accounts, permissions, credentials

This is the part that gets forgotten and hurts the most. The new PM should not be hunting passwords on week three.

- [ ] **GitHub org permissions** (Home-Docs, home2, manipulation repos). Add the new PM with the right role; remove yourself.
- [ ] **Notion access** for the team workspace.
- [ ] **Shared Drive** folders (Tec, RoBorregos, area-specific).
- [ ] **Overleaf** (TDP document, paper drafts).
- [ ] **Sponsor accounts** if applicable (vendor portals, etc.).
- [ ] **Robot lab access**: door, locker, drawer keys, hardware sign-out sheet.
- [ ] **Communication channels**: Slack workspace admin role if you held it, WhatsApp group admin, etc.

!!! warning "Do not share passwords directly"
    Use the team's password manager or rotate the credential and share through a secure channel. Passwords sent on Slack or email stay in those channels forever.

## Habits during the year

The handoff is easier if you do these things continuously, not the night before stepping down:

- **Document decisions when you make them**. If you decide to drop a feature, write down why in the spotlight that week. Months later neither of you will remember.
- **Keep the spending log up to date** (see [Finances](finances.md#tracking-and-traceability)). At the end of the year you have the data for the TDP without scrambling.
- **Maintain the active member roster**. Add joiners; mark people who left and when.
- **Keep the cross-area dependency sheet** (see [Planning](planning.md#1-make-cross-area-dependencies-visible)). The next PM sees what shape the cross-area situation was in.
- **Write the TDP early**. November to January is the right window. If you wait, it eats your March (which is feature-freeze time).

## People management during your cycle

This is part of the role and gets less attention than it deserves. The pattern that worked:

### When a member is not delivering

1. **Talk 1:1 first**. Privately, no public callouts. Ask what is going on; sometimes it is a bad month at school, sometimes the task was unclear, sometimes the member quietly checked out. Listen first, react second.
2. **Agree on a concrete commitment**. Not "do more"; something like "next Friday have task X open as a PR." Concrete enough that both of you know what success looks like.
3. **If the pattern continues for two to three weeks**, escalate to a general PM. Bring data (which tasks, when, what was committed).
4. **Do not let it ride**. If you say nothing, the other members notice. The implicit message is "you can stop delivering and nothing happens", and the rest of the team disengages too.

### When a member leaves

Members do leave. School, work, motivation. When it happens:

- Mark them as inactive in the roster.
- Reassign their open tasks immediately (do not leave them dangling for two weeks).
- Send a short thank-you. They come back later more often than people expect.
- Update the next-PM contact list if they had a specific role (lab access, account ownership, etc.).

## What a good handoff looks like

Two questions to ask yourself before signing off:

1. **If I disappeared today, could the next PM run the next cycle without calling me?**
2. **Is there any one piece of information that lives only in my head?**

If the answer to (2) is yes, write it down before you leave. Even informally. It does not have to be polished.

## Common mistakes

- **Doing the handoff in one document the night before stepping down**. Half of it is wrong by morning. Spread it across the cycle.
- **Leaving accounts in your name "just in case"**. The new PM cannot do their job if half the credentials are still tied to you.
- **Skipping the "what NOT to do" section**. Without it, the next PM walks into the same trap you spent three months getting out of.
- **Not introducing the new PM to key contacts**. A two-line introduction email from you carries way more weight than the new PM cold-emailing.
