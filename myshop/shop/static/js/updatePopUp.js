function openPopup(productId) {
    document.getElementById(`popup-${productId}`).showModal();
}

function closePopup(productId) {
    document.getElementById(`popup-${productId}`).close();
}