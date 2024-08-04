const menu = document.querySelector('.user-menu')


window.addEventListener('click', function(event) {
    if (!menu.classList.contains('none') && event.target.closest('.user-menu') === null) {
        menu.classList.add('none')
    }
    
    if (event.target.closest('.btn')) {
        if (menu.classList.contains('none')) {
            menu.classList.remove('none')
        }
    }
})