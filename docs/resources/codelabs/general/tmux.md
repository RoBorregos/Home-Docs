# Using Tmux

## Introduction

Tmux is a terminal multiplexer that allows you to run multiple terminal sessions within a single window. This is particularly useful for managing long-running processes or when you want to keep your terminal sessions organized. It is specially handy when working with remote servers or devices, because the processes will continue running even if you disconnect from the session.

When running several docker containers, we often use tmux to keep track of the different processes in the Orin AGX.

In addition, tmux sessions can also be created programmatically, which is useful for running multiple processes in the background, or when orchestrating the launch of multiple nodes in ROS2. For examples, see the [scripting folder](https://github.com/RoBorregos/home2/tree/main/scripting).

## Activities

For a reference of the available commands, check the last section of this codelab.

1. Create a session called `onboarding` and leave it in the background.

<details>
<summary>Answer</summary>

```bash
# Create the session
tmux new -s onboarding

# Once in the session, press ctrl + b d to leave it running in the background. First press ctrl + b, then release both keys and press d.
tmux ls # you should see the session listed
```
</details>

2. Kill all the tmux sessions (be sure to have at least one session available).

(ps: the command isn't in this codelabs's reference)

<details>
<summary>Answer</summary>
```bash
# Create the session
# Then run:
tmux kill-server
```
</details>

3. Open 2 terminals and connect to the same tmux session.


<details>
<summary>Observation</summary>
Both terminals should show the same output, being updated at the same time. In addition, you can interact with the session from both terminals.
</details>

## Command reference

```bash
# Create a terminal
tmux new -s [name]

# List terminals
tmux ls

# Attach to a terminal
tmux attach -t [name]

# Kill a specific session
tmux kill-session -t [name]

# Exit terminal, leave it running in the background:
ctrl + b, d

# Enter scroll mode
ctrl + b + [

# Save all text from a Tmux session to a file (while inside the session)
tmux capture-pane -S - -E - -p > ~/tmux_full_history.txt

# Save all text from a Tmux session to a file (while outside the session)
tmux capture-pane -t [session-name] -S - -E - -p > output.txt
```
