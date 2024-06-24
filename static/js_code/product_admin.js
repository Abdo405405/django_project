// product_admin.js
document.addEventListener('DOMContentLoaded', function () {
    var categorySelect = document.getElementById('id_category');
    var subcategorySelect = document.getElementById('id_subcategory');

    categorySelect.addEventListener('change', function () {
        var categoryId = this.value;
        if (!categoryId) {
            subcategorySelect.innerHTML = '';
            return;
        }

        htmx.ajax({
            url: '/load_categories/',  // Update the URL here
            hxTarget: '#id_subcategory',
            hxIndicator: 'dots'
        });
    });
});
