import Croppie from 'croppie'

function readFile(input) {
    return new Promise(function(resolve, reject) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();

            reader.onload = function (e) {
                resolve(e.target.result)
            }
            reader.readAsDataURL(input.files[0]);
        }
    })
}
function writeFile(output, croppie) {
    croppie.result({
        type: 'blob'
    }).then(function(img) {
        let file = new File([img], "img.jpg",{type:"image/jpeg", lastModified:new Date().getTime()});
        let container = new DataTransfer();
        container.items.add(file);
        output.files = container.files;
    })
}
let croppie;
function initializeCroppie(cropper, options) {
    if (croppie) {
        croppie.destroy()
    }
    if (!options) {
        options = {
            viewport: {
                width: cropper.getAttribute('data-viewport-width'),
                height: cropper.getAttribute('data-viewport-height'),
                type: cropper.getAttribute('data-viewport-type')
            },
            boundary: {
                width: cropper.getAttribute('data-boundary-width'),
                height: cropper.getAttribute('data-boundary-height')
            },
            showZoomer: false,
            mouseWheelZoom: 'ctrl'
        }
    }
    croppie = new Croppie(document.getElementById('cropper'), options);
}
document.addEventListener("DOMContentLoaded", function() {
    document.querySelector('.dropdown-accordion').addEventListener('click', function(event) {
        event.stopPropagation();
    });

    const cropper = document.getElementById('cropper')
    if (cropper) {
        initializeCroppie(cropper)
    }

    const createItemImage = document.getElementById('create-item-image')
    if (createItemImage && cropper) {
        function initCroppingClasses() {
            let showItems = document.querySelectorAll('.show-on-cropping')
            for (let i=0; i < showItems.length; i++) {
                showItems[i].classList.add('d-none')
            }
            let hideItems = document.querySelectorAll('.hide-on-cropping')
            for (let i=0; i < hideItems.length; i++) {
                hideItems[i].classList.add('d-block')
            }
        }
        function swapCroppingClasses(cl1, cl2) {
            let showItems = document.querySelectorAll('.show-on-cropping')
            for (let i=0; i < showItems.length; i++) {
                showItems[i].classList.replace(cl1, cl2)
            }
            let hideItems = document.querySelectorAll('.hide-on-cropping')
            for (let i=0; i < hideItems.length; i++) {
                hideItems[i].classList.replace(cl2, cl1)
            }
        }
        function showCroppie() {
            swapCroppingClasses('d-none', 'd-block')
        }
        function hideCroppie() {
            swapCroppingClasses('d-block', 'd-none')
        }
        initCroppingClasses()
        let file_url;
        document.getElementById('croppie-select').addEventListener('change', function() {
            if (file_url) {
                const options = {
                    viewport: {
                        width: 420,
                        height: 69,
                        type: 'square'
                    },
                    boundary: {
                        width: '100%',
                        height: 400,
                    },
                    showZoomer: false,
                    mouseWheelZoom: 'ctrl'
                }
                if (this.value == 'id_image') {
                    options['viewport']['width'] = 300
                    options['viewport']['height'] = 300

                    initializeCroppie(cropper, options)
                    croppie.bind({
                        url: file_url
                    })
                }
                else if (this.value == 'id_banner') {
                    options['viewport']['width'] = 300
                    options['viewport']['height'] = 100

                    initializeCroppie(cropper, options)
                    croppie.bind({
                        url: file_url
                    })
                }
                const imagePreview = document.getElementById('image-preview')
                if (this.value == 'id_images') {
                    if (croppie) {
                        croppie.destroy()
                        croppie = undefined
                    }
                    imagePreview.classList.replace('d-none', 'd-block')
                    imagePreview.src = file_url
                }
                else {
                    imagePreview.classList.replace('d-block', 'd-none')
                }
            }
        })
        createItemImage.addEventListener('change', function() {
            readFile(this).then(function(url) {
                file_url = url
                initializeCroppie(cropper)
                croppie.bind({
                    url: url
                })
            })
            showCroppie()
        })
        const imagesContainer = new DataTransfer();
        document.getElementById('add-image-button').addEventListener('click', function() {
            let elName = document.getElementById('croppie-select').value
            let el = document.getElementById(elName)
            if (elName == 'id_images') {
                const reader = new FileReader();

                reader.onload = function (e) {
                    resolve(e.target.result)
                }
                reader.readAsBinaryString(createItemImage.files[0]);
                reader.onload = function(img) {
                    let file = new File([img], "img.jpg",{type:"image/jpeg", lastModified:new Date().getTime()});
                    imagesContainer.items.add(file);
                    el.files = imagesContainer.files;
                }
            }
            else {
                writeFile(el, croppie, true)
            }
            createItemImage.value = ''
            document.getElementById('image-preview').src = ''
            document.getElementById('croppie-select').value = 'id_image'
            hideCroppie()
        })
    }

    const UpdateProfileForm = document.getElementById('update-profile-form')
    if (UpdateProfileForm) {
        let imgUploaded = false;
        cropper.style.display = 'none';
        document.getElementById('id_image').addEventListener('change', function() {
            readFile(this).then(function(url) {
                croppie.bind({
                    url: url
                })
            })
            cropper.style.display = '';
            imgUploaded = true
        })
        document.getElementById('submit-update-form').addEventListener('click', function(e){
            if (imgUploaded) {
                e.preventDefault();

                writeFile(document.getElementById('id_image'), croppie);
                document.getElementById('update-profile-form').submit();
            }
        })
    }
});

