  # GPSR Merger — Multi-Command Interleaved Execution

  Source dir: task_manager/task_manager/gpsr/
  Entry point: gpsr_task_manager.py (state PLAN_AND_EXECUTE_BATCH)
  Goal: the RoboCup@Home 2026 GPSR +200 pt interleaving bonus — execute several spoken commands as one optimized, gripper-safe plan instead of one-at-a-time.

  ---
  Overview

  The merger takes a batch of parsed commands (one BAML CommandListLLM per utterance) and fuses them into a single InterleavedPlan. That plan reorders work across
  commands to minimize robot travel, while never breaking a command's internal order or the one-item-at-a-time gripper rule. The plan is compiled into a py_trees 
  behaviour tree with a built-in sequential fallback: if the clever interleaved plan fails anywhere, the robot falls back to running each command in plain order — and
  resumes rather than restarts, skipping work it already finished.

  ---
  Architecture

  N spoken commands  (BAML CommandListLLM each)
          │
          ▼
     merge()  ───────────────────────────────────┐  merger.py
       1. decompose each cmd → go_to-led segments │
       2. Held-Karp DP over segments              │
          (precedence + gripper + distance)       │
       3. flatten + collapse redundant go_tos     │
          │                                        │
          ▼                                        │
     InterleavedPlan(actions, fallback)  ──────────┘
          │
          ▼
     build_tree()  ──────────────────────────────┐  bt_builder.py
       Selector "gpsr_root"                       │
         ├─ Timeout(global) ▸ Sequence(interleaved)
         │     └─ Retry(2) ▸ Timeout ▸ ActionLeaf │
         └─ Sequence(sequential_fallback)         │
               └─ SequentialFallbackLeaf(cmd_k)   │
          │                                        │
          ▼                                        │
     tick loop in gpsr_task_manager  ─────────────┘

  ---
  How It Works

  1. Batching (gpsr_task_manager.py)

  Commands are collected into self.batched_commands as the user speaks them. When the batch reaches batch_size (default 3) or hits MAX_COMMANDS, the FSM enters
  PLAN_AND_EXECUTE_BATCH, which plans and runs the whole batch at once. Controlled by ROS params: interleave_enabled, batch_size, test_mode, test_commands.

  2. Merging (merger.py → merge())

  1. Decompose — each command is split into go_to-led segments (a navigation target plus the actions performed there). Each segment is tagged as acquires (picks),
  releases (gives/places), or neutral.
  2. Held-Karp DP — an exact shortest-path DP over the segments. State is (S = bitmask of scheduled segments, last = last segment). A segment is eligible to be added
  only if:
    - prefix order — its command's earlier segments are already scheduled (intra-command order preserved), and
    - gripper safety — if another command is currently mid-block holding an object, only neutral segments may interleave (enforces drop before pick, one item at a
  time).
    - Cost = Euclidean travel between segment locations (via locator), plus a tiny epsilon tiebreaker that prefers per-command order on ties.
  3. Flatten + collapse — the optimal segment order is expanded back into a flat PlanAction list, and back-to-back go_tos to the same place are dropped.

  Locations resolve to (x, y) through _resolve_xy (HRI query_location + nav areas_backup), and the DP is seeded with the robot's real current pose (_current_robot_xy
  via TF map→base_link) rather than the map origin.

  ▎ Safety caps: Held-Karp is O(2^M·M²), so above _M_CAP = 16 segments the merger drops to a plain per-command sequential order. Unknown locations get a sentinel cost
  ▎ LARGE_M = 1000, so the DP only visits them when prefix order forces it.

  3. Execution + Fallback (bt_builder.py, leaf_behaviours.py)

  The plan becomes a Selector:
  - Interleaved branch — each action wrapped in Retry(2) ▸ Timeout ▸ ActionLeaf, inside a global Timeout. Any action exhausting its retries (or the global budget
  firing) fails the whole Sequence and trips the Selector to the fallback.
  - Sequential fallback branch — one SequentialFallbackLeaf per source command, each running that command's actions in original order, logging (not gating on)
  per-action failures so every command still gets its shot. An optional OneShotCallbackLeaf announces the switch on the display.

  Resume, don't restart: every action that succeeds in the interleaved branch is recorded in self._completed. The fallback's is_completed predicate skips any non-go_to
  action already done, and skips a go_to whose entire segment of follow-up work is already complete — so the robot never re-picks an object or drives somewhere with
  nothing left to do. (This is what commit 026f0632 added.)

  on_action_complete forwards every result to hri.add_command_history, so the HRI command history reflects partial progress regardless of which branch ran.

  ---
  Module Reference

  task_manager.gpsr.merger

  ┌──────────────────────────────────┬───────────────────────────────────────────────────────────────────────────┐
  │              Symbol              │                                  Purpose                                  │
  ├──────────────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
  │ merge(commands, locator, origin) │ Top-level entry: N commands → one InterleavedPlan                         │
  ├──────────────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
  │ InterleavedPlan                  │ .actions (interleaved) + .fallback (per-command lists)                    │
  ├──────────────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
  │ PlanAction                       │ One action + provenance (source_cmd, source_idx, location, gripper flags) │
  ├──────────────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
  │ _decompose()                     │ Split a command into go_to-led _Segments                                  │
  ├──────────────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
  │ _optimal_schedule()              │ Held-Karp DP over segments                                                │
  ├──────────────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
  │ _sequential_schedule()           │ Per-command fallback ordering (always feasible)                           │
  ├──────────────────────────────────┼───────────────────────────────────────────────────────────────────────────┤
  │ _collapse_redundant_go_tos()     │ Drop a go_to when already at that location                                │
  └──────────────────────────────────┴───────────────────────────────────────────────────────────────────────────┘

  task_manager.gpsr.bt_builder

  ┌───────────────────────────────────────┬────────────────────────────────────────────────┐
  │               Function                │                    Purpose                     │
  ├───────────────────────────────────────┼────────────────────────────────────────────────┤
  │ build_tree(plan, subtask_handlers, …) │ Build the Selector(interleaved, fallback) tree │
  ├───────────────────────────────────────┼────────────────────────────────────────────────┤
  │ render_tree_ascii(root)               │ Unicode tree dump for logs                     │
  └───────────────────────────────────────┴────────────────────────────────────────────────┘

  task_manager.gpsr.leaf_behaviours

  ┌────────────────────────┬──────────────────────────────────────────────────────────────┐
  │         Class          │                           Purpose                            │
  ├────────────────────────┼──────────────────────────────────────────────────────────────┤
  │ ActionLeaf             │ Runs one PlanAction synchronously, returns SUCCESS/FAILURE   │
  ├────────────────────────┼──────────────────────────────────────────────────────────────┤
  │ SequentialFallbackLeaf │ Runs one command's actions in order; honors resume-skip mask │
  ├────────────────────────┼──────────────────────────────────────────────────────────────┤
  │ OneShotCallbackLeaf    │ Fires a callback once when fallback begins                   │
  └────────────────────────┴──────────────────────────────────────────────────────────────┘

  Dispatch model: each leaf calls the method named after the action's .action field (e.g. "go_to" → go_to(command)) on the first handler in subtask_handlers that
  defines it — same model as search_command.

  task_manager.gpsr.timeouts

  ┌────────────────────┬───────┬───────────────────────────────────────┐
  │      Constant      │ Value │              Applies to               │
  ├────────────────────┼───────┼───────────────────────────────────────┤
  │ NAVIGATE_TIMEOUT_S │ 45    │ go_to, follow, guide                  │
  ├────────────────────┼───────┼───────────────────────────────────────┤
  │ PICK_TIMEOUT_S     │ 30    │ pick / place / give                   │
  ├────────────────────┼───────┼───────────────────────────────────────┤
  │ FIND_TIMEOUT_S     │ 60    │ find / count / question / visual info │
  ├────────────────────┼───────┼───────────────────────────────────────┤
  │ SAY_TIMEOUT_S      │ 10    │ say_with_context                      │
  ├────────────────────┼───────┼───────────────────────────────────────┤
  │ DEFAULT_TIMEOUT_S  │ 30    │ anything else                         │
  ├────────────────────┼───────┼───────────────────────────────────────┤
  │ GLOBAL_BUDGET_S    │ 300   │ whole interleaved sequence            │
  └────────────────────┴───────┴───────────────────────────────────────┘

  timeout_for(action) returns the per-action budget.

  ---
  Key Configuration Parameters

  ┌────────────────────┬────────┬──────────────────────────────────────────────────┐
  │     Parameter      │ Value  │                   Description                    │
  ├────────────────────┼────────┼──────────────────────────────────────────────────┤
  │ interleave_enabled │ True   │ Use batch interleaving vs. one-command-at-a-time │
  ├───────────────────────────┼──────────────────────┼──────────────────────────────────────────────────┤
  │ batch_size                │ 3                    │ Commands collected before planning a batch       │
  ├───────────────────────────┼──────────────────────┼──────────────────────────────────────────────────┤
  │ MAX_COMMANDS              │ 3                    │ Total commands the run will accept               │
  ├───────────────────────────┼──────────────────────┼──────────────────────────────────────────────────┤
  │ _M_CAP                    │ 16                   │ Segment count above which DP → sequential        │
  ├───────────────────────────┼──────────────────────┼──────────────────────────────────────────────────┤
  │ LARGE_M                   │ 1000.0               │ Sentinel cost for unresolved locations           │
  ├───────────────────────────┼──────────────────────┼──────────────────────────────────────────────────┤
  │ _TIEBREAK_EPSILON         │ 1e-6                 │ Tiebreak toward per-command order                │
  ├───────────────────────────┼──────────────────────┼──────────────────────────────────────────────────┤
  │ retry_count               │ 2                    │ Per-action retries in interleaved branch         │
  ├───────────────────────────┼──────────────────────┼──────────────────────────────────────────────────┤
  │ test_mode / test_commands │ False / 3 NL strings │ Run hardcoded commands without mic               │
  └───────────────────────────┴──────────────────────┴──────────────────────────────────────────────────┘

  ---
  Notes

  - The merger is framework-free: it reaches into BAML objects via getattr, so unit tests pass plain stand-ins (no ROS/BAML needed). See
  task_manager/scripts/test/_merger_helpers.py and test_hri_manager.py.
  - The merger provably preserves every command — the "lost first command" symptom is upstream LLM decomposition, not merging.
  - The single-item / drop-before-pick invariant means at most one command can hold the gripper at any moment; the DP enforces this rather than discovering it.

  # Hotwords + Initial Prompt → Whisper Flow
  
  Lets a caller bias STT transcription per-request: hotwords (boost specific words, e.g. a person's name) and initial_prompt (prime the model with expected context).

  The chain (caller → model)

  ┌─────┬──────────────────────────────────────────┬────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
  │  #  │                   File                   │                                                  What it does                                                  │
  ├─────┼──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 1   │ subtask_managers/hri_tasks.py            │ hear() / ask_and_confirm() take hotwords, initial_prompt args → forwarded to hear_streaming(), which packs     │
  │     │                                          │ them into SpeechStream.Goal(). Falls back to self.initial_prompt if none given.                                │
  ├─────┼──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 2   │ frida_interfaces/.../SpeechStream.action │ Goal carries string hotwords, string initial_prompt.                                                           │
  ├─────┼──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 3   │ speech/scripts/hear_streaming.py         │ execute_callback reads the goal — hotwords default to the DEFAULT_HOTWORDS param ("Frida RoBorregos"),         │
  │     │                                          │ initial_prompt to "". record_subscribed streams them over gRPC, initial_prompt only on the first chunk.        │
  ├─────┼──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 4   │ proto_interfaces/speech.proto            │ AudioRequest { bytes audio_data; string hotwords; string initial_prompt; }.                                    │
  ├─────┼──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 5   │ stt/faster-whisper-streaming.py          │ Reads first_chunk.hotwords / first_chunk.initial_prompt, passes both into ServeClientFasterWhisper.            │
  ├─────┼──────────────────────────────────────────┼────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
  │ 6   │ stt/faster_whisper_backend.py            │ transcribe_audio() passes hotwords + initial_prompt straight to transcriber.transcribe(...).                   │
  └─────┴──────────────────────────────────────────┴────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

  Example use

  gpsr_tasks.py (Find Person) passes the expected name as a hotword so Whisper transcribes it more reliably:

  self.subtask_manager.hri.ask_and_confirm(
      question="Can you please tell me your name?",
      query="name",
      use_keyword=False,
      hotwords=command.name,   # ← boosts the target name in STT
  )

  Notes

  - Empty hotwords ⇒ server uses DEFAULT_HOTWORDS; empty initial_prompt ⇒ disabled.
  - last_hotwords is tracked so a transcription equal to the hotwords is treated as "nothing heard" (silence/too-short guard).
  - initial_prompt is sent once (first chunk) to avoid re-priming every audio frame.

  # extract_data Node Fix

  File: hri/packages/nlp/scripts/extract_data.py (+ config/extract_data.yaml, assets/schemas.py)

  The DataExtractor node pulls structured fields (name, etc.) out of free-text via an LLM. The fix makes it fail soft instead of crashing the service, and swaps the
  model.

  Changes

  ┌─────────────────────┬─────────────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────────────────┐
  │        What         │                             Before                              │                                After                                │
  ├─────────────────────┼─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
  │ Model               │ deepseek-r1:7b                                                  │ qwen3                                                               │
  ├─────────────────────┼─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
  │ LLM call            │ unguarded — any API error propagated                            │ wrapped in try/except → logs error, returns ""                      │
  ├─────────────────────┼─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
  │ Parse failure       │ raise rclpy.exceptions.ServiceException(e) (killed the call)    │ returns ""                                                          │
  ├─────────────────────┼─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
  │ Empty result        │ return result.data (could be None)                              │ return result.data if result.data else ""                           │
  ├─────────────────────┼─────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────────────────┤
  │ Schema (schemas.py) │ Shelf.classification_tag: str; separate CategorizeShelvesResult │ classification_tag: list[str] = []; dropped CategorizeShelvesResult │
  └─────────────────────┴─────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────────────────┘

  Why it matters

  extract_data sits in the hot path of every ask / ask_and_confirm. Previously a single bad LLM response or schema-parse error raised a ServiceException that bubbled
  up and broke the calling task. Now every failure mode (network, malformed JSON, empty content) collapses to a benign empty string "", which callers already treat as
  "nothing extracted" — so the task keeps running and can retry.