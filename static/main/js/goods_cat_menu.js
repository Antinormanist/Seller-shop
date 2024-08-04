const menu2 = document.querySelector('.category-menu')


window.addEventListener('click', function(event) {
    if (!menu2.classList.contains('none') && event.target.closest('.category-menu') === null) {
        menu2.classList.add('none')
    }
    
    if (event.target.closest('.cat-menu')) {
        if (menu2.classList.contains('none')) {
            menu2.classList.remove('none')
        }
    }
})