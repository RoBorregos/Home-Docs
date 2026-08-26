// Semantic search over the documentation.
//
// The ranking (embeddings + BM25 + reciprocal rank fusion + recency) all runs
// in the Python backend. This file only sends a query and renders the answer.
//
// THE INSTANT-NAVIGATION NOTE: the theme enables navigation.instant, so Material
// swaps the content area over XHR instead of reloading the page. Scripts are not
// re-run, and anything mounted inside the content area is destroyed. Mounting on
// document.body once sidesteps both problems and keeps the panel open across
// navigation. (mermaid-init.js has to subscribe to document$ precisely because
// diagrams live *inside* the content.)

(function () {
  // Change this when the backend is deployed.
  var API_URL = "http://localhost:8001";

  var panel = null;
  var input = null;
  var results = null;

  function el(tag, className, text) {
    var node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  }

  function status(message) {
    results.innerHTML = "";
    results.appendChild(el("div", "rb-ask-status", message));
  }

  function render(hits) {
    results.innerHTML = "";

    if (!hits.length) {
      status("No matches. Try describing what you want to do.");
      return;
    }

    hits.forEach(function (hit) {
      var link = el("a", "rb-ask-hit");
      link.href = hit.url;

      var crumb = el("div", "rb-ask-crumb");
      crumb.appendChild(el("span", null, hit.breadcrumb || hit.source));
      if (hit.year) crumb.appendChild(el("span", "rb-ask-year", hit.year));

      link.appendChild(crumb);
      link.appendChild(el("div", "rb-ask-snippet", hit.snippet));
      results.appendChild(link);
    });
  }

  function search(query) {
    status("Searching...");

    fetch(API_URL + "/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query, top_k: 5 }),
    })
      .then(function (response) {
        if (!response.ok) throw new Error("HTTP " + response.status);
        return response.json();
      })
      .then(function (data) {
        render(data.results);
      })
      .catch(function (error) {
        // Most likely the backend went down after the page loaded.
        status("Search is unavailable. Is the backend running?");
        console.error("[rb-ask]", error);
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
    header.appendChild(el("span", null, "Search the documentation"));
    var closeButton = el("button", "rb-ask-close", "×");
    closeButton.type = "button";
    closeButton.setAttribute("aria-label", "Close");
    header.appendChild(closeButton);

    var form = el("form", "rb-ask-form");
    input = el("input", "rb-ask-input");
    input.type = "text";
    input.placeholder = "e.g. which camera does the robot use?";
    var submit = el("button", "rb-ask-submit", "Search");
    submit.type = "submit";
    form.appendChild(input);
    form.appendChild(submit);

    results = el("div", "rb-ask-results");

    panel.appendChild(header);
    panel.appendChild(form);
    panel.appendChild(results);

    document.body.appendChild(button);
    document.body.appendChild(panel);

    status("Ask a question about the documentation.");

    button.addEventListener("click", function () {
      if (panel.getAttribute("data-open") === "true") close();
      else open();
    });
    closeButton.addEventListener("click", close);

    form.addEventListener("submit", function (event) {
      event.preventDefault();
      var query = input.value.trim();
      if (query) search(query);
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

  // Nothing is injected unless the backend answers. The published site has no
  // backend yet, and a button that fails on every click is worse than no button.
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
