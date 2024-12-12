# Stickler for the Rules

## Description

The task consist in having 4 of at least 5 persons inside the arena stop breaking house rules. At least 3 different rules are being broken, each one with a maximum of 2 times.

- No shoes inside the house: take guests to leave their shoes at the entrance.
- Forbidden room: Take offenders to other party guests.
- No littering: Make the closest person pick the trash from the ground and throw it in the bin.
- Compulsory hydration: Take guests to the kitchen/bar for a drink.

The robot must verify the rules are followed after imposed and can assume a person won't break two rules.

`Main Goal`: Identify party guests breaking the house rules, politely clarify to the guest what to do
and confirm that the guest is following the rule.

`Optional Goals`: Politely clarify to the guest what rule is being broken.

## Needs from other areas

- Vision: Trash detection on the ground.
- Vision: Person detection in forbidden room.
- Vision: Shoe detection.
- Vision: Cup detection.
- Vision: Person Re-ID.
- Navigation: Identify the forbidden room.
- Navigation: Idle by moving through the arena.
- HRI: Communicating with rule breakers.

## Score sheet

| Action | Score |
| ---- | ---- |
| **Regular Rewards** | |
| Identify a guest breaking a house rule (indicating the rule by voice). | 4×100 |
| Making eye-contact, politely clarify to the guest what action he should take. | 4×100 |
| Confirm that the guest is following the rule. | 4×200 |
| **Bonus Rewards** | |
| Making eye-contact, politely clarify to the guest what rule is being broken. | 4×100 |
| **Regular Penalties** | |
| Talking to a guest about a rule they are not breaking | 4×–100 |
| **Deus Ex Machina Penalties** | |
| A human directs the robot towards a guest who is breaking a rule | 4×–50 |
| A human tells the robot which rule is being broken | 4×–100 |
| **Special Penalties & Bonuses** | |
| Not attending (see sec. 3.9.1) | –500 |
| Using alternative start signal (see sec. 3.7.8) | –100 |
| Outstanding performance (see sec. 3.9.3) | 200 |
| **Total Score (excluding special penalties & standard bonuses)** | 2000 |