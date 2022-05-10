document.addEventListener("DOMContentLoaded", function() {
    const confirmModal = document.getElementById('confirm-modal')
    const confirmModalForm = document.getElementById('confirm-modal-form')
    confirmModal.addEventListener('show.bs.modal', function(e) {
        confirmModalForm.action = e.relatedTarget.getAttribute('data-confirm-action')
        confirmModalForm.method = e.relatedTarget.getAttribute('data-confirm-method')
        confirmModal.querySelector('.modal-body').innerHTML = e.relatedTarget.getAttribute('data-confirm-text')
    })

    const offerModal = document.getElementById('offer-modal')
    const offerModalForm = document.getElementById('offer-modal-form')
    const offerModalItemName = document.getElementById('offer-modal-item-name')
    offerModal.addEventListener('show.bs.modal', function(e) {
        offerModalForm.querySelector('[name=item]').value = e.relatedTarget.getAttribute('data-item-id')
        offerModalItemName.innerHTML = e.relatedTarget.getAttribute('data-item-name')
    })

    const messageModal = document.getElementById('message-modal')
    if (messageModal) {
        const messageModalForm = document.getElementById('message-modal-form')
        messageModal.addEventListener('show.bs.modal', function(e) {
            let readonly = e.relatedTarget.getAttribute('data-readonly') !== null
            messageModalForm.querySelector('[name=item_id]').value = e.relatedTarget.getAttribute('data-item-id')
            const receiverInput = messageModalForm.querySelector('[name=receiver]')
            const subjectInput = messageModalForm.querySelector('[name=subject]')
            receiverInput.value = e.relatedTarget.getAttribute('data-receiver')
            subjectInput.value = e.relatedTarget.getAttribute('data-subject')
            if (readonly) {
                receiverInput.setAttribute('readonly', 'readonly')
                subjectInput.setAttribute('readonly', 'readonly')
            }
            else {
                receiverInput.removeAttribute('readonly')
                subjectInput.removeAttribute('readonly')
            }
        })
    }
})