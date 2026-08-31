// Semantic search over the documentation, with a generated answer.
//
// Two requests on purpose: /search paints sources in ~100ms, /ask fills the
// answer in 4-35s later. Mounted on document.body so navigation.instant, which
// swaps only the content area, cannot destroy the panel.

(function () {
  // Change this when the backend is deployed.
  var API_URL = "http://localhost:8001";

  var panel = null;
  var input = null;
  var answerBox = null;
  var results = null;

  // Guards against a slow response overwriting a newer question.
  var requestToken = 0;
  var elapsedTimer = null;

  var REASONS = {
    not_configured: "Answers are not enabled on this backend. The matching documents are below.",
    quota_exceeded: "The daily API limit has been reached. The matching documents are below.",
    provider_error: "The model is busy right now.",
    timeout: "The model took too long to respond.",
    truncated: "The answer was cut off before it finished.",
    no_results: "Nothing in the documentation matches that question.",
  };

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

  // Handles [1], [1][2] and [1, 2] — all three appear in real answers.
  function linkCitations(html, hits) {
    return html.replace(/\[\s*\d+(?:\s*,\s*\d+)*\s*\]/g, function (match) {
      var numbers = match.slice(1, -1).split(",");
      var links = numbers.map(function (raw) {
        var n = parseInt(raw.trim(), 10);
        var hit = hits[n - 1];
        // Out of range means an invented citation: render it as plain text.
        if (!hit) return String(n);
        return '<a class="rb-ask-cite" href="' + escapeHtml(hit.url) +
               '" title="' + escapeHtml(hit.source) + '">' + n + "</a>";
      });
      return "[" + links.join(", ") + "]";
    });
  }

  function status(container, message) {
    container.innerHTML = "";
    container.appendChild(el("div", "rb-ask-status", message));
  }

  function startElapsed() {
    var started = Date.now();
    stopElapsed();
    // A rising counter reads as progress; a static spinner reads as a hang.
    elapsedTimer = setInterval(function () {
      var seconds = Math.round((Date.now() - started) / 1000);
      status(answerBox, "Thinking... " + seconds + "s");
    }, 1000);
    status(answerBox, "Thinking... 0s");
  }

  function stopElapsed() {
    if (elapsedTimer) clearInterval(elapsedTimer);
    elapsedTimer = null;
  }

  function renderSources(hits) {
    results.innerHTML = "";
    if (!hits.length) return;

    results.appendChild(el("div", "rb-ask-sources-title", "Sources"));

    hits.forEach(function (hit, index) {
      var link = el("a", "rb-ask-hit");
      link.href = hit.url;

      var crumb = el("div", "rb-ask-crumb");
      crumb.appendChild(el("span", "rb-ask-num", String(index + 1)));
      crumb.appendChild(el("span", null, hit.breadcrumb || hit.source));
      if (hit.year) crumb.appendChild(el("span", "rb-ask-year", hit.year));

      link.appendChild(crumb);
      link.appendChild(el("div", "rb-ask-snippet", hit.snippet));
      results.appendChild(link);
    });
  }

  function renderAnswer(data) {
    answerBox.innerHTML = "";

    if (data.answer) {
      var body = el("div", "rb-ask-answer");
      body.innerHTML = linkCitations(renderMarkdown(data.answer), data.results);
      answerBox.appendChild(body);
      return;
    }

    var note = el("div", "rb-ask-status", REASONS[data.reason] || "No answer available.");
    answerBox.appendChild(note);

    // These clear on retry, so offer it instead of making the user retype.
    if (data.reason === "provider_error" || data.reason === "timeout") {
      var retry = el("button", "rb-ask-retry", "Try again");
      retry.type = "button";
      retry.addEventListener("click", function () {
        ask(data.query);
      });
      answerBox.appendChild(retry);
    }
  }

  function ask(query) {
    var token = ++requestToken;
    input.value = query;

    status(results, "Searching...");
    startElapsed();

    // Sources are ready in milliseconds and useful on their own.
    fetch(API_URL + "/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query, top_k: 5 }),
    })
      .then(function (response) {
        return response.ok ? response.json() : Promise.reject(response.status);
      })
      .then(function (data) {
        if (token !== requestToken) return;
        renderSources(data.results);
        if (!data.results.length) {
          stopElapsed();
          status(answerBox, REASONS.no_results);
        }
      })
      .catch(function (error) {
        if (token !== requestToken) return;
        stopElapsed();
        status(results, "Search is unavailable. Is the backend running?");
        answerBox.innerHTML = "";
        console.error("[rb-ask] search", error);
      });

    // The answer arrives later and drops into the slot above the sources.
    fetch(API_URL + "/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query, top_k: 5 }),
    })
      .then(function (response) {
        return response.ok ? response.json() : Promise.reject(response.status);
      })
      .then(function (data) {
        if (token !== requestToken) return;
        stopElapsed();
        renderAnswer(data);
      })
      .catch(function (error) {
        if (token !== requestToken) return;
        stopElapsed();
        status(answerBox, "The answering service is unavailable.");
        console.error("[rb-ask] ask", error);
      });
  }

  function open() {
    panel.setAttribute("data-open", "true");
    input.focus();
  }

  function close() {
    panel.setAttribute("data-open", "false");
  }

  function build() {
    var button = el("button", "rb-ask-button", "Ask the docs");
    button.type = "button";

    panel = el("div", "rb-ask-panel");
    panel.setAttribute("data-open", "false");

    var header = el("div", "rb-ask-header");
    header.appendChild(el("span", null, "Ask the documentation"));
    var closeButton = el("button", "rb-ask-close", "×");
    closeButton.type = "button";
    closeButton.setAttribute("aria-label", "Close");
    header.appendChild(closeButton);

    var form = el("form", "rb-ask-form");
    input = el("input", "rb-ask-input");
    input.type = "text";
    input.placeholder = "e.g. how do I install GPD?";
    var submit = el("button", "rb-ask-submit", "Ask");
    submit.type = "submit";
    form.appendChild(input);
    form.appendChild(submit);

    var body = el("div", "rb-ask-body");
    answerBox = el("div", "rb-ask-answer-slot");
    results = el("div", "rb-ask-results");
    body.appendChild(answerBox);
    body.appendChild(results);

    panel.appendChild(header);
    panel.appendChild(form);
    panel.appendChild(body);

    document.body.appendChild(button);
    document.body.appendChild(panel);

    status(answerBox, "Ask a question about the documentation.");

    button.addEventListener("click", function () {
      if (panel.getAttribute("data-open") === "true") close();
      else open();
    });
    closeButton.addEventListener("click", close);

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var query = input.value.trim();
      if (query) ask(query);
    });

    document.addEventListener("keydown", function (event) {
      if (event.key === "Escape") close();
    });

    document.addEventListener("click", function (event) {
      if (panel.getAttribute("data-open") !== "true") return;
      if (panel.contains(event.target) || button.contains(event.target)) return;
      close();
    });
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
