const modal = document.getElementById("collection-modal");
const modalCard = modal.querySelector("article");
const modalContent = document.getElementById("collection-modal-content");
const modalClose = document.getElementById("collection-modal-close");

document.querySelectorAll("[data-modal-template]").forEach(btn => {
  btn.addEventListener("click", () => {
    const template = document.getElementById(btn.dataset.modalTemplate);
    modalContent.replaceChildren(template.content.cloneNode(true));
    modalCard.className = `card raised ${btn.dataset.color}`;
    modal.showModal();
  });
});

modalClose.addEventListener("click", () => modal.close());

modal.addEventListener("click", ev => { if (ev.target === modal) modal.close(); });
