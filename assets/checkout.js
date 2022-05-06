document.addEventListener("DOMContentLoaded", function() {
    let createContactContainer = document.getElementById('create-contact-container')
    if (createContactContainer) {
        const fragment = document.createDocumentFragment()
        const contactChanged = () => {
            if (document.getElementById('id_contact').value === '') {
                document.getElementById('create-contact-container-placeholder').appendChild(createContactContainer)
            }
            else {
                fragment.appendChild(createContactContainer)
            }
        }
            document.getElementById('id_contact').addEventListener("change", contactChanged)
            contactChanged()
    }
    let checkoutRating = document.getElementById('checkout-rating')
    if (checkoutRating) {
        const changeHunger = function(rating) {
            document.getElementById('id_rating').value = rating
            const hungerContainers = checkoutRating.querySelectorAll('.hunger-container')
            const hungerImages = checkoutRating.querySelectorAll('img.hunger-rating')
            for (let i=0; i < hungerImages.length; i++) {
                hungerImages[i].style.display = 'none'
            }
            for (let i=0; i < hungerContainers.length; i++) {
                let ri = hungerContainers.length - 1 - i
                if (ri < rating / 2 - 1 || ri < rating / 2 && rating % 2 === 0) {
                    hungerContainers[i].querySelector('img.hunger-full').style.display = 'block'
                }
                else if (ri < rating / 2 && rating % 2 > 0) {
                    hungerContainers[i].querySelector('img.hunger-half').style.display = 'block'
                }
                else {
                    hungerContainers[i].querySelector('img.hunger-empty').style.display = 'block'
                }
            }
        }
        let overlays = checkoutRating.getElementsByClassName('hunger-overlay')
        for (let i=0;i<overlays.length;i++) {
            overlays[i].addEventListener('mouseenter', function(event) {
                let rating = event.target.dataset.number * 2
                if (event.target.classList.contains('hunger-overlay-left')) {
                    rating += 2
                }
                else {
                    rating += 1
                }
                changeHunger(rating)
            })
        }
        changeHunger(5)
    }
});