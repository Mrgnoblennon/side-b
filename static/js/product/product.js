// SIDE B. product page interactions
document.addEventListener("DOMContentLoaded", () => {
    const mainImage = document.getElementById("mainProductImage");
    const thumbnails = document.querySelectorAll(".product-thumbnail");

    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener("click", () => {
            if (mainImage) mainImage.src = thumbnail.dataset.image;
            thumbnails.forEach(item => item.classList.remove("active"));
            thumbnail.classList.add("active");
        });
    });

    const form = document.getElementById("productForm");
    const quantityInput = document.getElementById("productQuantity");
    const decreaseButton = document.getElementById("decreaseQuantity");
    const increaseButton = document.getElementById("increaseQuantity");
    const variantSelect = document.getElementById("productVariant");
    const stockMessage = document.getElementById("stockMessage");
    const cartMessage = document.getElementById("cartMessage");
    const addButton = form?.querySelector(".product-add-cart");

    if (!form || !quantityInput || !decreaseButton || !increaseButton) return;

    // Each variant has its own stock. If no variants exist, use product stock.
    const productStock = Number(quantityInput.max) || 0;

    function availableStock() {
        if (!variantSelect) return productStock;
        if (!variantSelect.value) return 0;
        const option = variantSelect.options[variantSelect.selectedIndex];
        return Math.max(0, Number(option.dataset.stock) || 0);
    }

    function updateStock() {
        const stock = availableStock();
        const waitingForVariant = variantSelect && !variantSelect.value;
        quantityInput.max = String(stock);
        quantityInput.value = String(Math.min(Math.max(1, Number(quantityInput.value) || 1), Math.max(1, stock)));
        increaseButton.disabled = stock === 0 || Number(quantityInput.value) >= stock;
        decreaseButton.disabled = stock === 0 || Number(quantityInput.value) <= 1;
        if (addButton) addButton.disabled = stock === 0;
        if (stockMessage) {
            stockMessage.textContent = waitingForVariant
                ? "Choose an option to check availability."
                : stock === 0 ? "Out of stock." : stock + " available";
        }
    }

    decreaseButton.addEventListener("click", () => {
        quantityInput.value = String(Math.max(1, Number(quantityInput.value) - 1));
        updateStock();
    });

    increaseButton.addEventListener("click", () => {
        quantityInput.value = String(Math.min(availableStock(), Number(quantityInput.value) + 1));
        updateStock();
    });

    if (variantSelect) variantSelect.addEventListener("change", () => {
        quantityInput.value = "1";
        if (cartMessage) cartMessage.textContent = "";
        updateStock();
    });

    // Allow the form to POST to Flask; browser validates required variant.

    updateStock();
});
