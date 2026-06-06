for (const button of document.querySelectorAll("[data-gallery-scroll]")) {
  button.addEventListener("click", () => {
    const gallery = button.closest("#gallery-carousel");
    const strip = gallery?.querySelector(".gallery-strip");
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

const dialog = document.querySelector("#gallery-dialog");
const dialogImage = dialog?.querySelector("img");
const dialogItems = [...document.querySelectorAll("[data-gallery-full]")];
let dialogIndex = -1;

function openDialog(index) {
  if (!dialog || !dialogImage || !dialogItems[index]) {
    return;
  }

  const item = dialogItems[index];
  dialogIndex = index;
  dialogImage.src = item.dataset.galleryFull;
  dialogImage.alt = item.dataset.galleryAlt || "";
  if (item.dataset.galleryWidth && item.dataset.galleryHeight) {
    dialogImage.width = Number(item.dataset.galleryWidth);
    dialogImage.height = Number(item.dataset.galleryHeight);
  } else {
    dialogImage.removeAttribute("width");
    dialogImage.removeAttribute("height");
  }
  if (!dialog.open) {
    dialog.showModal();
  }
}

for (const [index, item] of dialogItems.entries()) {
  item.addEventListener("click", (event) => {
    event.preventDefault();
    openDialog(index);
  });
}

dialog?.addEventListener("click", () => {
  dialog.close();
});

document.addEventListener("keydown", (event) => {
  if (dialog?.open && dialogItems.length) {
    if (event.key === "ArrowLeft") {
      openDialog((dialogIndex - 1 + dialogItems.length) % dialogItems.length);
    } else if (event.key === "ArrowRight") {
      openDialog((dialogIndex + 1) % dialogItems.length);
    } else {
      return;
    }

    event.preventDefault();
  }
});
