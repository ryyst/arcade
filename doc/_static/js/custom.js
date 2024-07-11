document.ready(() => {
  // Make sections in the sidebar togglable.
  let hasCurrent = false;
  let menuHeaders = document.querySelectorAll(
    ".wy-menu-vertical .caption[role=heading]",
  );
  menuHeaders.forEach((it) => {
    let connectedMenu = it.nextElementSibling;

    // Enable toggling.
    it.addEventListener(
      "click",
      () => {
        if (connectedMenu.classList.contains("active")) {
          connectedMenu.classList.remove("active");
          it.classList.remove("active");
        } else {
          connectedMenu.classList.add("active");
          it.classList.add("active");
        }

        // Hide other sections.
        menuHeaders.forEach((ot) => {
          if (ot !== it && ot.classList.contains("active")) {
            ot.nextElementSibling.classList.remove("active");
            ot.classList.remove("active");
          }
        });

        registerOnScrollEvent(mediaQuery);
      },
      true,
    );

    // Set the default state, expand our current section.
    if (connectedMenu.classList.contains("current")) {
      connectedMenu.classList.add("active");
      it.classList.add("active");

      hasCurrent = true;
    }
  });

  // Unfold the first (general information) section on the home page.
  if (!hasCurrent && menuHeaders.length > 0) {
    menuHeaders[0].classList.add("active");
    menuHeaders[0].nextElementSibling.classList.add("active");

    registerOnScrollEvent(mediaQuery);
  }
});
