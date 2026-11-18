
// product image gallery
const mainImage = document.getElementById("mainProductImage");
const thumbnails = document.querySelectorAll(".product-thumbnail");

thumbnails.forEach(thumbnail => {
    thumbnail.addEventListener("click", () => {

        // change the main image
        if (mainImage) {
            mainImage.src = thumbnail.dataset.image;
        }

        // update selected thumbnail
        thumbnails.forEach(item => item.classList.remove("active"));
        thumbnail.classList.add("active");
    });
});


// quantity controls
const quantityInput = document.getElementById("productQuantity");
const decreaseButton = document.getElementById("decreaseQuantity");
const increaseButton = document.getElementById("increaseQuantity");

decreaseButton.addEventListener("click", () => {
    const quantity = Number(quantityInput.value);

    if (quantity > 1) {
        quantityInput.value = quantity - 1;
    }
});

increaseButton.addEventListener("click", () => {
    const quantity = Number(quantityInput.value);

    if (quantity < 99) {
        quantityInput.value = quantity + 1;
    }
});


// cart integration will be added when the cart route is ready
const productForm = document.getElementById("productForm");
const cartMessage = document.getElementById("cartMessage");

productForm.addEventListener("submit", event => {
    event.preventDefault();

    if (!productForm.reportValidity()) {
        return;
    }

    cartMessage.textContent = "Cart integration is not connected yet.";
});
