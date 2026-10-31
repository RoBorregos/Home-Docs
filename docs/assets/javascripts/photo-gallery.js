// Photo gallery slideshow (Overview/Media.md).
//
// Turns every `.photo-gallery` (a plain list of <a><img></a>) into a large
// slideshow with prev/next arrows and a thumbnail strip, like the carousel on
// the landing page. Without JS the gallery stays a thumbnail grid.
(function () {
  function enhance(gallery) {
    if (gallery.dataset.enhanced) return;
    var links = Array.prototype.slice.call(gallery.querySelectorAll("a"));
    if (!links.length) return;
    gallery.dataset.enhanced = "1";

    var stage = document.createElement("div");
    stage.className = "photo-gallery__stage";
    var main = document.createElement("a");
    main.target = "_blank";
    var mainImg = document.createElement("img");
    main.appendChild(mainImg);
    var caption = document.createElement("div");
    caption.className = "photo-gallery__caption";
    stage.appendChild(main);

    var prev = document.createElement("button");
    prev.className = "photo-gallery__prev";
    prev.setAttribute("aria-label", "Previous photo");
    prev.innerHTML = "&#10094;";
    var next = document.createElement("button");
    next.className = "photo-gallery__next";
    next.setAttribute("aria-label", "Next photo");
    next.innerHTML = "&#10095;";
    stage.appendChild(prev);
    stage.appendChild(next);

    var strip = document.createElement("div");
    strip.className = "photo-gallery__thumbs";
    links.forEach(function (a, i) {
      a.addEventListener("click", function (ev) {
        ev.preventDefault();
        show(i);
      });
      strip.appendChild(a);
    });

    gallery.appendChild(stage);
    gallery.appendChild(caption);
    gallery.appendChild(strip);
    gallery.classList.add("photo-gallery--slideshow");

    var current = 0;
    function show(i) {
      current = (i + links.length) % links.length;
      var a = links[current];
      var img = a.querySelector("img");
      main.href = a.href;
      mainImg.src = img.src;
      mainImg.alt = img.alt;
      caption.textContent = img.alt;
      links.forEach(function (l, j) {
        l.classList.toggle("is-active", j === current);
      });
    }
    prev.addEventListener("click", function () { show(current - 1); });
    next.addEventListener("click", function () { show(current + 1); });
    show(0);
  }

  function scan() {
    document.querySelectorAll(".photo-gallery").forEach(enhance);
  }

  if (typeof window.document$ !== "undefined" && typeof window.document$.subscribe === "function") {
    window.document$.subscribe(scan);
  } else if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", scan);
  } else {
    scan();
  }
})();
