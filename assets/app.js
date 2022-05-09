import Croppie from 'croppie'

// Function for accordion in dropdown.
document.addEventListener("DOMContentLoaded", function() {
    document.querySelector('.dropdown-accordion').addEventListener('click', function(event) {
        event.stopPropagation();
    });

    let UpdateProfileForm = document.getElementById('update-profile-form')
    if (UpdateProfileForm) {
        const crop = new Croppie(document.getElementById('cropper'), {
        enableExif: true,
        viewport: {
            width: 420,
            height: 420,
            type: 'circle'
        },
        boundary: {
            width: 512,
            height: 512
        }
    });
        function readFile(input) {
            if (input.files && input.files[0]) {
                const reader = new FileReader();

                reader.onload = function (e) {
                    crop.bind({
                        url: e.target.result
                    })

                }
                reader.readAsDataURL(input.files[0]);
            }
        }
        document.getElementById('cropper').style.display = 'none';
        let imgUploaded = false;
        document.getElementById('id_image').addEventListener('change', function(){
                readFile(this);
                imgUploaded = true;
                document.getElementById('cropper').style.display = '';
            });
        document.getElementById('submit-update-form').addEventListener('click', function(e){
            if (imgUploaded){
             e.preventDefault();
            crop.result({
                type: 'blob'
            }).then(function(img) {
                let file = new File([img], "img.jpg",{type:"image/jpeg", lastModified:new Date().getTime()});
                let container = new DataTransfer();

                container.items.add(file);
                document.getElementById('id_image').files = container.files;
                document.getElementById('update-profile-form').submit();
            })
            }
        })
    }



});

