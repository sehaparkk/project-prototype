document.addEventListener('DOMContentLoaded', function() {
    //remove form
    document.querySelectorAll('.remove-form').forEach(function(btn){
        btn.addEventListener('click', function() {
            var formDiv = btn.closest('.form');
            formDiv.remove();
            var formset = document.closest('.formset');
            var totalForms = formset.querySelector('input[name$="-TOTAL_FORMS"]');
            var count = formset.querySelectorAll('.form').length;
            totalForms.value = count;
        });
    });
    document.querySelectorAll('.add-form').forEach(function(btn){
        btn.addEventListener('click', function() {
            var formset = btn.closest('.formset');
            var totalForms = formset.querySelector('input[name$="-TOTAL_FORMS"]');
            var count = parseInt(totalForms.value);
            var emptyForm = formset.querySelector('.empty-form').innerHTML;
            var newFormHtml = emptyForm.replace(/__prefix__/g, count);
            var newFormDiv = document.createElement('div');
            newFormDiv.classList.add('form');
            newFormDiv.innerHTML = newFormHtml;
            formset.insertBefore(newFormDiv, btn);
            totalForms.value = count + 1;
        });
    });
});