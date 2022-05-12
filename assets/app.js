import Croppie from 'croppie'

const croppieOptions = {
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
        type: 'blob',
        size: 'original',
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
        options = croppieOptions
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
        function croppieSelectChange() {
            if (file_url) {
                const imagePreview = document.getElementById('image-preview')
                const croppieSelect = document.getElementById('croppie-select')
                if (croppieSelect.value == 'id_images') {
                    if (croppie) {
                        croppie.destroy()
                        croppie = undefined
                    }
                    if (imagePreview) {
                        imagePreview.classList.replace('d-none', 'd-block')
                        imagePreview.src = file_url
                    }
                }
                else {
                    if (imagePreview) {
                        imagePreview.classList.replace('d-block', 'd-none')
                    }
                    let selectedOption = croppieSelect.selectedOptions[0]
                    croppieOptions['viewport']['width'] = selectedOption.dataset.viewportWidth
                    croppieOptions['viewport']['height'] = selectedOption.dataset.viewportHeight
                    croppieOptions['viewport']['type'] = selectedOption.dataset.viewportType
                    initializeCroppie(cropper, croppieOptions)
                    croppie.bind({
                        url: file_url
                    })
                }
            }
        }
        document.getElementById('croppie-select').addEventListener('change', croppieSelectChange)
        createItemImage.addEventListener('change', function() {
            readFile(this).then(function(url) {
                file_url = url
                initializeCroppie(cropper)
                croppie.bind({
                    url: url
                })
                croppieSelectChange()
            })
            showCroppie()
        })
        const imagesContainer = new DataTransfer();
        document.getElementById('add-image-button').addEventListener('click', function() {
            let elName = document.getElementById('croppie-select').value
            let el = document.getElementById(elName)
            if (elName == 'id_images') {
                const xhr = new XMLHttpRequest()
                const formData = new FormData()
                formData.append('image', createItemImage.files[0])
                xhr.open('POST', document.getElementById('image-upload-url').getAttribute('data-image-upload-url'))
                formData.append('csrfmiddlewaretoken', document.querySelector('input[name=csrfmiddlewaretoken]').value)
                xhr.send(formData)
                readFile(createItemImage).then(function(url) {
                    let previewDiv = document.getElementById('id_images_preview')
                    let img = document.createElement('img')
                    img.src = url
                    img.classList.add('img-fluid')
                    previewDiv.appendChild(img)
                })
            }
            else {
                writeFile(el, croppie, true)
                let previewImg = document.getElementById(elName + '_preview')
                if (previewImg) {
                    croppie.result({type: 'base64', size: 'original'}).then(function(url) {
                        previewImg.src = url
                    })
                }
            }
            createItemImage.value = ''
            document.getElementById('image-preview').src = ''
            document.getElementById('croppie-select').value = 'id_image'
            hideCroppie()
        })
        document.getElementById('remove-image-button').addEventListener('click', function() {
            createItemImage.value = ''
            document.getElementById('image-preview').src = ''
            document.getElementById('croppie-select').value = 'id_image'
            hideCroppie()
        })
    }

    const UpdateProfileForm = document.getElementById('update-profile-form')
    if (UpdateProfileForm) {
        function updateBio() {
            document.getElementById('update-profile-placeholder-bio').innerText = document.getElementById('id_bio').value
        }
        document.getElementById('id_bio').addEventListener('input', updateBio)
        updateBio()
        let imgUploaded = false;
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

