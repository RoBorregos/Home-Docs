// Semantic search over the documentation, with a generated answer.
//
// Two requests on purpose: /search paints sources in ~100ms, /ask fills the
// answer in 4-35s later. Mounted on document.body so navigation.instant, which
// swaps only the content area, cannot destroy the panel.
//
// Questions stack as turns.

(function () {
  // Same origin in production, so no CORS. Locally the API is a second server.
  var LOCAL = location.hostname === "localhost" || location.hostname === "127.0.0.1";
  var API_URL = LOCAL ? "http://localhost:8001/api" : "/api";
  var TOP_K = 5;

  // Taken from the golden set, so they are known to answer well.
  var EXAMPLES = [
    "which camera does the robot use?",
    "how do I install and configure GPD?",
    "what mobile base is the robot built on?",
  ];

  // navigation.instant only intercepts links present at load, so clicking a
  // source reloads the page. The thread is restored from here instead.
  var STORE_KEY = "rb-ask-session";
  var STORE_LIMIT = 10;

  var button = null;
  var panel = null;
  var input = null;
  var thread = null;
  var empty = null;

  var REASONS = {
    not_configured: "Answers are not enabled on this backend. The matching documents are below.",
    quota_exceeded: "The daily API limit has been reached. The matching documents are below.",
    rate_limited: "Too many questions in a short time. The matching documents are below.",
    daily_cap: "The daily answer limit has been reached. The matching documents are below.",
    provider_error: "The model is busy right now.",
    timeout: "The model took too long to respond.",
    truncated: "The answer was cut off before it finished.",
    no_results: "Nothing in the documentation matches that question.",
  };

  var ICON =
    '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3c-4.97 0-9 3.58-9 8 0 2.27 1.07 4.3 2.79 5.75L5 21l4.2-2.1c.9.22 1.84.34 2.8.34 4.97 0 9-3.58 9-8s-4.03-8-9-8z"/></svg>';

  // --- session -------------------------------------------------------------

  // sessionStorage throws in some privacy modes; the widget works without it.
  function readSession() {
    try {
      return JSON.parse(sessionStorage.getItem(STORE_KEY)) || { open: false, turns: [] };
    } catch (error) {
      return { open: false, turns: [] };
    }
  }

  function writeSession(session) {
    try {
      sessionStorage.setItem(STORE_KEY, JSON.stringify(session));
    } catch (error) {
      /* Out of quota or blocked: the thread simply will not survive a reload. */
    }
  }

  function rememberOpen(open) {
    var session = readSession();
    session.open = open;
    writeSession(session);
  }

  // Snippets are no longer rendered, so they are dropped before storing.
  function rememberTurn(data) {
    var session = readSession();
    session.turns.push({
      query: data.query,
      answer: data.answer,
      reason: data.reason,
      results: (data.results || []).map(function (hit) {
        return {
          url: hit.url,
          breadcrumb: hit.breadcrumb,
          source: hit.source,
          year: hit.year,
        };
      }),
    });
    session.turns = session.turns.slice(-STORE_LIMIT);
    writeSession(session);
  }

  function forgetTurns() {
    var session = readSession();
    session.turns = [];
    writeSession(session);
  }

  // --- helpers -------------------------------------------------------------

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  function escapeHtml(text) {
    var div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  // Escape first, then convert: the answer is untrusted model output.
  function renderMarkdown(text) {
    var html = escapeHtml(text);

    html = html.replace(/```[a-z]*\n([\s\S]*?)```/g, function (_, code) {
      return "<pre class=\"rb-ask-code\"><code>" + code.replace(/\n$/, "") + "</code></pre>";
    });
    html = html.replace(/`([^`\n]+)`/g, "<code>$1</code>");
    html = html.replace(/\*\*([^*\n]+)\*\*/g, "<strong>$1</strong>");
    html = html.replace(/\n{2,}/g, "</p><p>").replace(/\n/g, "<br>");

    return "<p>" + html + "</p>";
  }

  // Handles [1], [1][2] and [1, 2] - all three appear in real answers.
  function linkCitations(html, hits) {
    return html.replace(/\[\s*\d+(?:\s*,\s*\d+)*\s*\]/g, function (match) {
      var numbers = match.slice(1, -1).split(",");
      var links = numbers.map(function (raw) {
        var n = parseInt(raw.trim(), 10);
        var hit = hits[n - 1];
        // Out of range means an invented citation: render it as plain text.
        if (!hit) return String(n);
        // Built as a node: serialising it escapes quotes that string concatenation would not.
        var link = el("a", "rb-ask-cite", String(n));
        link.setAttribute("href", hit.url);
        link.setAttribute("title", hit.source);
        return link.outerHTML;
      });
      return "[" + links.join(", ") + "]";
    });
  }

  function status(container, message) {
    container.innerHTML = "";
    container.appendChild(el("div", "rb-ask-status", message));
  }

  // --- turns ---------------------------------------------------------------

  // A turn owns its nodes, so a slow response can only write into its own.
  function createTurn(query) {
    var turn = {
      node: el("div", "rb-ask-turn"),
      answer: el("div", "rb-ask-answer-slot"),
      sources: el("div", "rb-ask-sources"),
      answered: false,
      timer: null,
    };

    turn.answer.setAttribute("aria-live", "polite");
    turn.node.appendChild(el("div", "rb-ask-question", query));
    turn.node.appendChild(turn.answer);
    turn.node.appendChild(turn.sources);

    empty.hidden = true;
    thread.appendChild(turn.node);
    // Scrolling the thread directly: scrollIntoView would also move the page.
    thread.scrollTop = thread.scrollHeight;
    return turn;
  }

  function startElapsed(turn) {
    var started = Date.now();
    stopElapsed(turn);
    // A rising counter reads as progress; a static spinner reads as a hang.
    turn.timer = setInterval(function () {
      var seconds = Math.round((Date.now() - started) / 1000);
      status(turn.answer, "Thinking... " + seconds + "s");
    }, 1000);
    status(turn.answer, "Thinking... 0s");
  }

  function stopElapsed(turn) {
    if (turn.timer) clearInterval(turn.timer);
    turn.timer = null;
  }

  // Document plus deepest section.
  function sourceTitle(hit) {
    var file = hit.source.split("/").pop().replace(/\.md$/, "");
    var path = (hit.breadcrumb || "").split(" > ");
    var section = path[path.length - 1];
    return { file: file, section: section === file ? "" : section };
  }

  function renderSources(container, hits) {
    container.innerHTML = "";
    if (!hits.length) return;

    container.appendChild(el("div", "rb-ask-sources-title", "Sources"));

    hits.forEach(function (hit, index) {
      var link = el("a", "rb-ask-hit");
      link.href = hit.url;

      // The full path stays reachable on hover, now that the row is one line.
      link.setAttribute("title", (hit.breadcrumb || hit.source) + "\n" + hit.source);

      var title = sourceTitle(hit);
      var crumb = el("div", "rb-ask-crumb");
      crumb.appendChild(el("span", "rb-ask-num", String(index + 1)));
      crumb.appendChild(el("span", "rb-ask-doc", title.file));
      if (title.section) {
        crumb.appendChild(el("span", "rb-ask-sep", "\u203a"));
        crumb.appendChild(el("span", "rb-ask-section", title.section));
      }
      if (hit.year) crumb.appendChild(el("span", "rb-ask-year", hit.year));

      link.appendChild(crumb);
      container.appendChild(link);
    });
  }

  function renderAnswer(turn, data) {
    turn.answer.innerHTML = "";

    if (data.answer) {
      var body = el("div", "rb-ask-answer");
      body.innerHTML = linkCitations(renderMarkdown(data.answer), data.results);
      turn.answer.appendChild(body);
      return;
    }

    turn.answer.appendChild(
      el("div", "rb-ask-status", REASONS[data.reason] || "No answer available.")
    );

    // These clear on retry, so offer it instead of making the user retype.
    if (data.reason === "provider_error" || data.reason === "timeout") {
      var retry = el("button", "rb-ask-retry", "Try again");
      retry.type = "button";
      retry.addEventListener("click", function () {
        run(turn, data.query);
      });
      turn.answer.appendChild(retry);
    }
  }

  // --- asking --------------------------------------------------------------

  function run(turn, query) {
    turn.answered = false;
    startElapsed(turn);
    status(turn.sources, "Searching...");

    // Sources are ready in milliseconds and useful on their own.
    fetch(API_URL + "/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query, top_k: TOP_K }),
    })
      .then(function (response) {
        return response.ok ? response.json() : Promise.reject(response.status);
      })
      .then(function (data) {
        if (turn.answered) return;
        renderSources(turn.sources, data.results);
        if (!data.results.length) {
          stopElapsed(turn);
          status(turn.answer, REASONS.no_results);
        }
      })
      .catch(function (error) {
        if (turn.answered) return;
        stopElapsed(turn);
        status(turn.sources, "Search is unavailable. Is the backend running?");
        turn.answer.innerHTML = "";
        console.error("[rb-ask] search", error);
      });

    // The answer arrives later and drops into the slot above the sources.
    fetch(API_URL + "/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query, top_k: TOP_K }),
    })
      .then(function (response) {
        return response.ok ? response.json() : Promise.reject(response.status);
      })
      .then(function (data) {
        turn.answered = true;
        stopElapsed(turn);
        // Citations index into these results, so they replace the provisional list.
        renderSources(turn.sources, data.results);
        renderAnswer(turn, data);
        rememberTurn(data);
      })
      .catch(function (error) {
        turn.answered = true;
        stopElapsed(turn);
        status(turn.answer, "The answering service is unavailable.");
        console.error("[rb-ask] ask", error);
      });
  }

  function ask(query) {
    input.value = "";
    run(createTurn(query), query);
  }

  function clearThread() {
    thread.querySelectorAll(".rb-ask-turn").forEach(function (node) {
      node.remove();
    });
    empty.hidden = false;
    forgetTurns();
    input.focus();
  }

  // Replays stored turns without asking again: no request, no quota.
  function restoreThread(turns) {
    turns.forEach(function (data) {
      var turn = createTurn(data.query);
      turn.answered = true;
      renderSources(turn.sources, data.results);
      renderAnswer(turn, data);
    });
  }

  // --- panel ---------------------------------------------------------------

  function isOpen() {
    return panel.getAttribute("data-open") === "true";
  }

  function open(focusInput) {
    panel.setAttribute("data-open", "true");
    button.setAttribute("aria-expanded", "true");
    button.setAttribute("data-hidden", "true");
    rememberOpen(true);
    // Not on restore: the reader clicked a source to read the page, not to type.
    if (focusInput) input.focus();
  }

  // Focus returns to the button only when the user closed deliberately.
  function close(restoreFocus) {
    panel.setAttribute("data-open", "false");
    button.setAttribute("aria-expanded", "false");
    button.setAttribute("data-hidden", "false");
    rememberOpen(false);
    if (restoreFocus) button.focus();
  }

  function buildEmptyState() {
    empty = el("div", "rb-ask-empty");
    empty.appendChild(
      el("p", null, "Ask a question about the RoBorregos @Home documentation.")
    );

    var list = el("div", "rb-ask-examples");
    EXAMPLES.forEach(function (question) {
      var example = el("button", "rb-ask-example", question);
      example.type = "button";
      example.addEventListener("click", function () {
        ask(question);
      });
      list.appendChild(example);
    });

    empty.appendChild(list);
    return empty;
  }

  function buildHeader() {
    var header = el("div", "rb-ask-header");

    var title = el("div", "rb-ask-title", "Ask the documentation");
    title.id = "rb-ask-title";
    header.appendChild(title);

    var clear = el("button", "rb-ask-clear", "Clear");
    clear.type = "button";
    clear.addEventListener("click", clearThread);
    header.appendChild(clear);

    var closeButton = el("button", "rb-ask-close", "×");
    closeButton.type = "button";
    closeButton.setAttribute("aria-label", "Close");
    closeButton.addEventListener("click", function () {
      close(true);
    });
    header.appendChild(closeButton);

    return header;
  }

  function build() {
    button = el("button", "rb-ask-button");
    button.type = "button";
    button.innerHTML = ICON;
    button.appendChild(el("span", null, "Ask the docs"));
    button.setAttribute("aria-expanded", "false");

    panel = el("div", "rb-ask-panel");
    panel.setAttribute("data-open", "false");
    panel.setAttribute("role", "dialog");
    panel.setAttribute("aria-labelledby", "rb-ask-title");

    thread = el("div", "rb-ask-thread");
    thread.appendChild(buildEmptyState());

    var form = el("form", "rb-ask-form");
    input = el("input", "rb-ask-input");
    input.type = "text";
    input.placeholder = "Ask a question...";
    input.setAttribute("aria-label", "Your question");
    var submit = el("button", "rb-ask-submit", "Ask");
    submit.type = "submit";
    form.appendChild(input);
    form.appendChild(submit);

    panel.appendChild(buildHeader());
    panel.appendChild(thread);
    panel.appendChild(form);

    document.body.appendChild(button);
    document.body.appendChild(panel);

    button.addEventListener("click", function () {
      if (isOpen()) close(false);
      else open(true);
    });

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var query = input.value.trim();
      if (query) ask(query);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape" && isOpen()) close(true);
    });

    document.addEventListener("click", function (event) {
      if (!isOpen()) return;
      if (panel.contains(event.target) || button.contains(event.target)) return;
      close(false);
    });

    var session = readSession();
    if (session.turns.length) restoreThread(session.turns);
    if (session.open) open(false);
  }

  // No backend, no button: better invisible than broken on every click.
  function init() {
    if (document.querySelector(".rb-ask-button")) return;

    fetch(API_URL + "/health")
      .then(function (response) {
        if (response.ok) build();
      })
      .catch(function () {
        /* No backend: stay invisible. */
      });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
