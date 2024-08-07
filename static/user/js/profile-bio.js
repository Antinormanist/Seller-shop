const menu6 = document.querySelector('.bio-menu')
const inp1 = document.querySelector('.bio-menu-inp1')
const inp2 = document.querySelector('.bio-menu-inp2')
const btn = document.querySelector('.bio-inside-btn')


window.addEventListener('click', function(event) {
    if (!menu6.classList.contains('none') && event.target.closest('.bio-menu') === null) {
        menu6.classList.add('none')
        if (!label.classList.contains('none')) {
            label.classList.add('none')
            inp.classList.add('none')
        }
    }
    
    if (event.target.closest('.bio-btn')) {
        if (menu6.classList.contains('none')) {
            menu6.classList.remove('none')
        }
    }
})

// btn.addEventListener('click', function() {
//     const name = inp1.value
//     const description = inp2.value
//     if (name && description) {
//         $.ajax({
//             type: 'POST',
//             url: 'URL',
//             data: {name: name, description: description},
//         })
//     } else {
//         window.location = 'URL'
//     }
// })