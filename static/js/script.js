
// open the enlarged image
function openGallery(imageSrc) {
    const modal = document.getElementById("gallery-modal");
    const modalImage = document.getElementById("gallery-modal-image");
    modalImage.src = imageSrc;
    modal.style.display = "flex";
}
// close the enlarged image
function closeGallery() {
    const modal = document.getElementById("gallery-modal");
    modal.style.display = "none";
}

// scroll merchandise left or right
function scrollMerch(direction) {

  // find the merchandise carousel
  const carousel = document.getElementById("merch-carousel");

  // find the first product card
  const card = carousel.querySelector(".merch-card");

  // stop if no products exist
  if (!card) {
      return;
  }

  // get the width of one card and the space between cards
  const cardWidth = card.getBoundingClientRect().width;
  const gap = parseFloat(getComputedStyle(carousel).gap) || 0;

  // move one product at a time
  carousel.scrollBy({
      left: direction * (cardWidth + gap),
      behavior: "smooth"
  });
}