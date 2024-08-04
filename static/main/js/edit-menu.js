const menu4 = document.querySelector('.edit')


window.addEventListener('click', function(event) {
    if (!menu4.classList.contains('none') && event.target.closest('.edit') === null) {
        menu4.classList.add('none')
    }
    
    if (event.target.closest('.btn-edit')) {
        if (menu4.classList.contains('none')) {
            menu4.classList.remove('none')
        }
    }
})