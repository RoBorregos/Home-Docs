---
title: Finances
---

# Finances

Home does not manage its own budget. All money flows through **RoBorregos finance**. As an area PM your job is not to approve purchases. Your job is to **identify the need, get a clean quote, and push the request through the right channel**. As a general PM your job is to **filter and approve** what area PMs push, before sending it up to the president.

## Approval flow

Every hardware purchase (or any team expense) follows this chain:

```mermaid
flowchart LR
    A["1. Area PM<br/>quotes"] -->
    B["2. General PM<br/>approves"] -->
    C["3. RoBorregos<br/>president"] -->
    D["4. RoBorregos<br/>finance officer"]

    style A fill:#e1f5fe
    style B fill:#1e88e5,color:#fff
    style C fill:#0b2545,color:#fff
    style D fill:#fb8c00,color:#fff
```

!!! danger "Do not skip steps"
    If an area PM goes straight to the president or to finance, they **bypass the general PM** and break the control. The general PM needs to see every request so they can:

    - Prioritize across areas when the budget is tight.
    - Defend the case to the president.
    - Keep a spending log.

    Even when the purchase feels urgent, push it through the channel. If it really is urgent, ping the general PM on Slack so they see it immediately.

## Step-by-step request

### 1. Area PM: quote it

Before pushing anything, prepare a **complete quote**.

- [ ] **What you need**: exact part name, model, specifications.
- [ ] **Why**: which task or milestone this unblocks. If you cannot answer this in one sentence, you are not ready to push the request.
- [ ] **When**: deadline for when you need it (TMR? integration? sponsor demo?).
- [ ] **Three quotes from different suppliers** if possible. Tec finance sometimes requires it; ask up front.
- [ ] **Include shipping and taxes** in every quote. The listed price is never what gets paid.
- [ ] **Link to the product page** in each quote, not screenshots.

!!! tip "A weak quote costs two weeks"
    A weak quote comes back with questions at every step (general PM, president, finance, general PM, you again). Each loop is days. A complete quote goes through in one pass.

### 2. General PM: approve or send back

The general PM:

- **Validates** that the justification makes sense and fits the timeline.
- **Compares priorities** against requests from other areas.
- **Decides**: approve and push upward, or send back to the area PM asking for changes.

If approved, the general PM writes a short email or message to the president with the quote attached and a one-line summary.

### 3. Team president: route

The team president does not personally sign off (unless the purchase is small). What they do is:

- **Validate** that the request comes from the general PM (not from a random member).
- **Route to the RoBorregos finance officer** with their sign-off.

### 4. RoBorregos finance officer: execute

Finance processes the purchase per Tec rules:

- Small purchases can be **reimbursements** (someone buys from their own pocket, submits the invoice, gets paid back).
- Larger purchases go through a **Tec purchase order**, which can take a few weeks.

## Purchase types and lead times

| Type | Example | Typical lead time |
|---|---|---|
| **Urgent spare** | Gripper finger broken before TMR | 1 to 2 weeks if there is local stock |
| **Planned component** | Motor for the next arm version | 3 to 6 weeks if it needs to be imported |
| **Consumables** | Screws, cables, basic tools | About 1 week |
| **Large hardware** | New camera, GPU, computer | 4 to 8 weeks (Tec purchase order) |
| **Software / licenses** | Notion, Overleaf subscriptions | Variable; extra approval steps |

!!! warning "Imports take longer"
    Anything bought outside Mexico (Amazon US, Digikey, etc.) goes through customs and adds 2 to 4 weeks. Plan for it.

## Reimbursements

For small purchases that a member makes out of pocket:

1. **Before buying**: confirm with the general PM that the reimbursement will be approved. Without that, you risk eating the cost.
2. **At purchase**: ask for an **electronic invoice billed to RoBorregos / Tec**. No invoice, no reimbursement.
3. **After**: submit the invoice through whatever channel your finance uses (usually a Drive sheet; ask).

!!! warning "A paper ticket does not count"
    Tec does not accept paper receipts for substantial reimbursements. You need a CFDI with the right RFC. If the vendor cannot invoice, let another member buy it, or let finance order it directly.

## Sponsors

Some purchases (especially large ones) can come in as a **donation from a sponsor** instead of cash. That is coordinated by the **team president**, not by you. Your role:

- **Identify** the need and communicate it to the general PM.
- For large or specific items (industrial cameras, arms, etc.), ask the general PM: *"Is there a sponsor that could donate this?"* before quoting from scratch.
- If a sponsor is interested, prepare a **clear technical spec** that the president can forward to the sponsor.

## Tracking and traceability

As a general PM, keep a **spending log** for the whole year:

| Date | Area | Item | Amount | Status | Reason |
|---|---|---|---|---|---|
| 2026-02-15 | Manipulation | Custom gripper finger x 2 | $1,500 | Received | TMR2025 wear replacement |
| 2026-03-01 | Vision | GigE industrial camera | $25,000 | Pending | ZED replacement for reflective scenes |

This is useful for:

- **TDP**: declare hardware investment in the paper.
- **Handoff**: the next PM sees what has been requested and what is still arriving.
- **Defending budget** the following year with data.

## Common mistakes

- Quoting without knowing why. The general PM cannot approve something they cannot defend.
- Forgetting shipping and taxes. The quote looks cheap, arrives expensive, everyone is unhappy.
- Asking for a reimbursement without an invoice. You end up paying.
- Last-minute requests. Asking for a gripper "for TMR" the week before TMR is already too late.
- Not notifying when it arrives. The package shows up, no one knows, it sits in a box for a month. Tell the area when it lands.
