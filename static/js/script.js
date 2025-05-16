// static/contacts/js/script.js
document.addEventListener('DOMContentLoaded', function () {
    const formsetContainer = document.getElementById('formset-container');
    const totalForms = document.getElementById('id_form-TOTAL_FORMS');
    const emptyFormTemplate = document.getElementById('empty-form-template').innerHTML;

    // Add Phone button
    document.querySelector('.add-formset').addEventListener('click', function () {
        const formCount = parseInt(totalForms.value);
        const newFormHtml = emptyFormTemplate.replaceAll('__prefix__', formCount);
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = newFormHtml;
        const newForm = tempDiv.firstElementChild;

        formsetContainer.appendChild(newForm);
        totalForms.value = formCount + 1;
    });

    // Remove Phone button
    document.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-formset')) {
            const row = e.target.closest('.formset-row');
            const deleteInput = row.querySelector('input[type="checkbox"][name$="-DELETE"]');
            if (deleteInput) {
                deleteInput.checked = true;
                row.style.display = 'none';
            } else {
                row.remove();
                totalForms.value = formsetContainer.querySelectorAll('.formset-row').length;
            }
        }
    });
});
