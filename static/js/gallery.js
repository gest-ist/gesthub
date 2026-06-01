for (const button of document.querySelectorAll("[data-gallery-scroll]")) {
  button.addEventListener("click", () => {
    const gallery = button.closest("#gallery-carousel");
    const strip = gallery?.querySelector("[data-gallery-strip]");
    const direction = Number(button.dataset.galleryScroll);

    if (!strip || !direction) {
      return;
    }

    const item = strip.querySelector(".gallery-item");
    const gap = Number.parseFloat(getComputedStyle(strip).columnGap) || 0;
    const distance = item ? item.getBoundingClientRect().width + gap : strip.clientWidth * 0.8;

    strip.scrollBy({
      left: direction * distance,
      behavior: "smooth",
    });
  });
}

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape" || !document.querySelector(".gallery-lightbox:target")) {
    return;
  }

  location.hash = "gallery";
});
