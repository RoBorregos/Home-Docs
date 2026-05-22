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

    Even when the purchase feels urgent, push it through the channel. If it really is urgent, ping the general PM through the team chat so they see it immediately.

## Step-by-step request

### 1. Area PM: quote it

Before pushing anything, prepare a **complete quote**.

- [ ] **What you need**: exact part name, model, specifications.
- [ ] **Why**: which task or milestone this unblocks. If you cannot answer this in one sentence, you are not ready to push the request.
- [ ] **When**: deadline for when you need it (TMR, integration, sponsor demo).
- [ ] **More than one quote** when the item is generic. Multiple options give the general PM something to compare. Ask the finance officer up front whether multiple quotes are required for this specific purchase.
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

## What Home typically buys

Most years, Home does not start a cycle from scratch with a long shopping list. The robot already exists, the basic stack already works, and the focus is iterating. **Big purchases tend to be driven by feedback from the previous international competition**: things that broke, things that were missing, ideas that came up while competing.

Concrete example from the 2026 cycle. After RoboCup the team identified gaps that turned into:

- Speakers for the robot (audio for HRI tasks).
- Custom PCBs for the omnibase electronics.
- A redesign of the omnibase itself.
- A portable battery pack so FRIDA does not stay tethered during demos.

The takeaway: it is hard to predict what hardware you need *before* the international. Once you have that feedback, the next cycle's shopping list almost writes itself.

!!! info "On lead times"
    Lead times vary a lot. Local stock can arrive in days; imports from outside Mexico add weeks for customs; a Tec purchase order for a large item can take more than a month. Get a real lead time from each vendor when you quote; do not assume.

## The two biggest line items: flights and registration

For Home, the largest expenses every cycle are **international travel** (flights) and **competition registration fees**. Both are paid in advance, and both depend on qualifying at TMR.

What this means as a PM:

- **Look for sponsors from day one**, assuming the team will qualify for the international. If you wait until qualification is announced, the runway to find sponsors is too short.
- **Buy flights as early as possible**. The earlier you buy, the cheaper they are.
- **The hard part**: until the team qualifies and until member selection is done, you do not know exactly who is flying. Buying flights before that is risky (cancellation fees, refund rules). Buying after qualification is safer but more expensive.

There is no clean fix for this trade-off. Use whatever sponsor commitment you have to absorb the risk where you can.

## Transparent member selection for the international

Selecting who flies to the international is one of the most sensitive things a PM has to handle. Done badly it fractures the team. The two criteria past PMs have used:

1. **Time dedicated to Home over the cycle.** Members who showed up consistently, did the work, attended the meetings.
2. **Contribution during the competition itself.** Some members are essential because of what they own technically (the person who maintains the gripper, the person who knows the manipulation pipeline best, etc.).

Whatever criteria you end up using, **share them with the team before announcing the selection**. The members who do not make the cut deserve to know what the criteria were and that the process was not arbitrary. This is the single best thing you can do to keep the team intact after the selection happens.

## Reimbursements

For small purchases that a member makes out of pocket:

1. **Before buying**: confirm with the general PM that the reimbursement will be approved. Without that, you risk eating the cost.
2. **At purchase**: ask for an **electronic invoice billed to RoBorregos / Tec**. No invoice, no reimbursement.
3. **After**: submit the invoice through whatever channel your finance uses (usually a Drive sheet; ask).

!!! warning "A paper ticket does not count"
    Tec typically requires an electronic invoice (CFDI) addressed to RoBorregos or Tec for sizeable reimbursements. If the vendor cannot invoice, either let another member buy it, or let finance place the order directly. Confirm the exact requirement with the RoBorregos finance officer.

## Sponsors

Some purchases (especially large ones) can come in as a **donation from a sponsor** instead of cash. That is coordinated by the **team president**, not by you. Your role:

- **Identify** the need and communicate it to the general PM.
- For large or specific items (industrial cameras, arms, etc.), ask the general PM: *"Is there a sponsor that could donate this?"* before quoting from scratch.
- If a sponsor is interested, prepare a **clear technical spec** that the president can forward to the sponsor.

## Tracking and traceability

As a general PM, keep a **spending log** for the whole year. A simple sheet works; what matters is that the columns let you answer the questions below.

| Date | Area | Item | Amount | Status | Reason |
|---|---|---|---|---|---|
| _(fill in for each purchase as it happens)_ | | | | | |

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
