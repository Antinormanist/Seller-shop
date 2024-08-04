const menu3 = document.querySelector('.delete-menu')


window.addEventListener('click', function(event) {
    if (!menu3.classList.contains('none') && event.target.closest('.delete-menu') === null) {
        menu3.classList.add('none')
    }
    
    if (event.target.closest('.btn-delete')) {
        if (menu3.classList.contains('none')) {
            menu3.classList.remove('none')
        }
    }
})