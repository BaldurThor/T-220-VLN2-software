document.addEventListener("DOMContentLoaded", function() {
    const confirmModal = document.getElementById('confirm-modal')
    const confirmModalForm = document.getElementById('confirm-modal-form')
    confirmModal.addEventListener('show.bs.modal', function(e) {
        confirmModalForm.action = e.relatedTarget.getAttribute('data-confirm-action')
        confirmModalForm.method = e.relatedTarget.getAttribute('data-confirm-method')
        confirmModal.querySelector('.modal-body').innerHTML = e.relatedTarget.getAttribute('data-confirm-text')
    })
})