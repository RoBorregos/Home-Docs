# Command Break Down

Go to the dishwasher then find an apple and get it and bring it to the waving person in the office

-> go(dishwasher)
-> find(apple)
----> gaze(n predefined points)
----> detect(apple)
----> approach_point(apple)
-> pick(apple)
-> go(office)
-> find(waving_person)
----> gaze(n predefined points)
----> detect(waving_person)
----> approach_point(waving_person)
-> give(apple)

Locate a waving person in the kitchen and answer a question

-> go(kitchen)
-> find(waving_person)
----> gaze(n predefined points)
----> detect(waving person)
----> approach_point(waving_person)
-> say(ask_question)
-> hear(user)
-> contextual_say(answer)

Meet Axel in the bedroom and answer a quiz
-> go(bedroom)
-> find(Axel)
----> gaze(n predefined points)
----> detect(person)
----> if person[i] == Axel then approach_point(Axel)
----> else: for person in persons: approach_point(person) -> ask if is Axel
----> save_to_context(Axel)
-> say(ask_question)
-> hear(user)
-> contextual_say(answer)

Tell me how many waving persons are in the kitchen
-> go(kitchen)
-> count(waving_person)
----> gaze(n predefined points)
----> detect(waving person)
-> go(task_origin)
-> contextual_say(answer)

Tell me the gesture of the person at the tv stand
-> go(tv_stand)
-> find(person)
----> gaze(n predefined points)
----> detect(person)
-> go(task_origin)
-> contextual_say(gesture)

Say your teams affiliation to the waving person in the bathroom
-> go(bathroom)
-> find(waving_person)
----> gaze(n predefined points)
----> detect(waving person)
----> approach_point(waving_person)
-> contextual_say(affiliation)

Answer the quiz of the person raising their right arm in the living room
-> go(living_room)
-> find(person_raising_right_arm)
----> gaze(n predefined points)
----> detect(person_raising_right_arm)
----> approach_point(person_raising_right_arm)
-> say(ask_quiz)
-> hear(user)
-> contextual_say(answer)

Follow Jane from the desk to the kitchen
-> go(desk)
-> find(Jane)
----> gaze(n predefined points)
----> detect(person)
----> if person[i] == Jane then approach_point(Jane)
----> else: for person in persons: approach_point(person) -> ask if is Jane
----> save_to_context(Jane)

-> say(intent)
-> follow_person_until(Jane, kitchen)

Escort Axel from the trashbin to the pantry

-> go(trashbin)
-> find(Axel)
----> gaze(n predefined points)
----> detect(Axel)
----> if person[i] == Axel then approach_point(Axel)
----> else: for person in persons: approach_point(person) -> ask if is Axel
----> save_to_context(Axel)

-> say(intent)
-> escort_to(pantry)

Take the person pointing to the right from the armchair to the exit
-> go(armchair)
-> find(person_pointing_right)
----> gaze(n predefined points)
----> detect(person_pointing_right)
----> approach_point(person_pointing_right)
-> say(intent)
-> escort_to(exit)

Take the person wearing a yellow t shirt from the side tables to the office
-> go(side_tables)
-> find(person_yellow_tshirt)
----> gaze(n predefined points)
----> detect(person_yellow_tshirt)
----> approach_point(person_yellow_tshirt)
-> say(intent)
-> escort_to(office)

Say hello to the person wearing a gray t shirt in the living room and answer a quiz
-> go(living_room)
-> find(person_gray_tshirt)
----> gaze(n predefined points)
----> detect(person_gray_tshirt)
----> approach_point(person_gray_tshirt)
-> say(hello)
-> say(ask_quiz)
-> hear(user)
-> contextual_say(answer)

Say hello to Morgan in the kitchen and answer a question
-> go(kitchen)
-> find(Morgan)
----> gaze(n predefined points)
----> detect(Morgan)
----> if person[i] == Morgan then approach_point(Morgan)
----> else: for person in persons: approach_point(Morgan) -> ask if is Morgan
----> save_to_context(Morgan)

-> say(hello)
-> say(ask_question)
-> hear(user)
-> contextual_say(answer)

Note: in the second find, the person should be already known i/e found person[i] == Jane
Meet Jane at the entrance then locate them in the kitchen
-> go(entrance)
-> find(Jane)
----> gaze(n predefined points)
----> detect(Jane)
----> if person[i] == Jane then approach_point(Jane)
----> else: for person in persons: approach_point(Jane) -> ask if is Jane
----> save_to_context(Jane)
-> go(kitchen)
-> find(Jane)
----> gaze(n predefined points)
----> detect(Jane)
----> if person[i] == Jane then approach_point(Jane)
----> else: for person in persons: approach_point(Jane) -> ask if is Jane
----> save_to_context(Jane)
-> say(intent finished)

Tell me how many people in the office are wearing yellow coats
-> go(office)
-> count(person_yellow_coat)
----> gaze(n predefined points)
----> detect(person_yellow_coat)
----> save_to_context(count)

-> go(task_origin)
-> contextual_say(answer)

Tell me how many people in the living room are wearing gray coats
-> go(living_room)
-> count(person_gray_coat)
----> gaze(n predefined points)
----> detect(person_gray_coat)
----> save_to_context(count)
-> go(task_origin)
-> contextual_say(answer)

Tell the gesture of the person at the side tables to the person at the tv stand
-> go(side_tables)
-> find(person)
----> gaze(n predefined points)
----> detect(person)
----> save_to_context(gesture)

-> go(tv_stand)
-> find(person)
----> gaze(n predefined points)
----> detect(person)
-> contextual_say(gesture)

Follow the standing person in the living room
-> go(living_room)
-> find(standing_person)
----> gaze(n predefined points)
----> detect(standing_person)
----> approach_point(standing_person)
-> say(intent)
-> follow_person_until_canceled(standing_person)

Go to the kitchen then locate a snack and get it and deliver it to Adel in the bathroom
-> go(kitchen)
-> find(snack)
----> gaze(n predefined points)
----> detect(snack)
----> approach_point(snack)
-> pick(snack)
-> go(bathroom)
-> find(Adel)
----> gaze(n predefined points)
----> detect(Adel)
----> if person[i] == Adel then approach_point(Adel)
----> else: for person in persons: approach_point(Adel) -> ask if is Adel
----> save_to_context(Adel)
-> say(intent)
-> give(snack)

Take a cleaning supply from the kitchen table and bring it to the standing person in the kitchen
-> go(kitchen_table)
-> find(cleaning_supply)
----> gaze(n predefined points)
----> detect(cleaning_supply)
----> approach_point(cleaning_supply)
-> pick(cleaning_supply)
-> find(standing_person)
----> gaze(n predefined points)
----> detect(standing_person)
----> approach_point(standing_person)
-> say(intent)
-> give(cleaning_supply)

Locate a cleaning supply in the bedroom then take it and bring it to the standing person in the bedroom
-> go(bedroom)
-> find(cleaning_supply)
----> gaze(n predefined points)
----> detect(cleaning_supply)
----> approach_point(cleaning_supply)
-> pick(cleaning_supply)
-> find(standing_person)
----> gaze(n predefined points)
----> detect(standing_person)
----> approach_point(standing_person)
-> say(intent)
-> give(cleaning_supply)

Tell me how many fruits there are on the bed
-> go(bed)
-> count(fruits)
----> gaze(n predefined points)
----> detect(fruits)
----> save_to_context(count)
-> go(task_origin)
-> contextual_say(answer)

TODO: how to detect biggest object?
Tell me what is the biggest object on the kitchen table
-> go(kitchen_table)
-> find(biggest_object)
----> gaze(n predefined points)
----> detect(biggest_object)
----> save_to_context(objects)
-> go(task_origin)
-> contextual_say(biggest_object)

Bring me a soccer ball from the dishwasher
-> go(dishwasher)
-> find(soccer_ball)
----> gaze(n predefined points)
----> detect(soccer_ball)
----> approach_point(soccer_ball)
-> pick(soccer_ball)
-> go(task_origin)
-> give(soccer_ball)

TODO: how to detect lightest object that is a toy?
Tell me what is the lightest toy on the bookshelf
-> go(bookshelf)
-> find(lightest_toy)
----> gaze(n predefined points)
----> detect(toys)
----> save_to_context(toys)

-> go(task_origin)
-> contextual_say(lightest_toy)

## Todo ideas

TODO: how to detect lightest object that is a toy?

- When in the find method, insert all objects matching description to a db.
- In the db, store previously know object properties.
- When determining the lightest object, compare the objects in the db and return the lightest one.
  - Perhaps, implement a contextual_say method that fetches context to answer queries?
  - Let the contextual say choose between the databases

TODO: how to detect biggest object?

- Same idea as previous todo

TODO: how to handle finds with different requirements?

- i.e. find by name, by posture, by object recognizable with model?

TODO: deux ex machina integration

-

TODO: confirmation implementation

- How to add confirmation and fallbacks to the subcommands? add confirmation within the subcommand or before/after the subcommands?
