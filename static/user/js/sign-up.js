// const form = document.querySelector('.menu')
// const label = document.querySelector('.hidden')
// const inp = document.querySelector('#hidden')
// const codeUrl = document.querySelector('#sign-url').value
// const curUrl = document.querySelector('#sign').value
// const csrfToken = $('meta[name="csrf-token"]').attr('content');

// let code
// let tries = 5

// form.addEventListener('submit', function(event) {
//     event.preventDefault()
//     const formData = new FormData(form)
//     const email = formData.get('email')
//     const username = formData.get('username')
//     const password1 = formData.get('password1')
//     const password2 = formData.get('password2')

//     // VALIDATION
//     if (password1 != password2) {
//         window.location = curUrl
//     }

//     // OTHER BORING THINGS
//     if (code) {
//         if (tries === 0) {
//             tries = 5
//             code = undefined
//             label.classList.add('hidden')
//             inp.classList.add('hidden')
//         } else {
//             const userCode = formData.get('code')
//             if (userCode === code) {
//                 $.ajax({
//                     type: 'POST',
//                     url: codeUrl,
//                     data: {success: true, email: email, username: username, password1: password1, password2: password2, csrfmiddlewaretoken: csrfToken},
//                     headers: {
//                         'X-CSRFToken': csrfToken
//                     }
//                 })
//             }
//             tries -= 1
//         }
//     } else {
//         $.ajax({
//             type: 'POST',
//             url: codeUrl,
//             data: {email: email, username: username, password1: password1, password2: password2, csrfmiddlewaretoken: csrfToken},
//             headers: {
//                 'X-CSRFToken': csrfToken
//             },
//             success: function(response) {
//                 code = response.code
//                 if (label.classList.contains('hidden')) {
//                     label.classList.remove('hidden')
//                     inp.classList.remove('hidden')
//                 }
//             },
//             error: function() {
//                 console.log(111)
//                 // window.location = curUrl
//             }
//         })
//     }
// })
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Проверка, есть ли этот cookie
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Установка CSRF токена в заголовках AJAX-запроса
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^http:.*/.test(settings.url) && !/^https:.*/.test(settings.url)) {
            // Сохраняем заголовок X-CSRFToken
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('.menu');
    const label = document.querySelector('.hidden');
    const inp = document.querySelector('#hidden');
    const codeUrl = document.querySelector('#sign-url').value;
    const curUrl = document.querySelector('#sign').value;
    const mailUrl = document.querySelector('#mailurl').value
    const sendUrl = document.querySelector('#sendurl').value
    // const csrfToken = $('meta[name="csrf-token"]').attr('content');

    let code;
    let tries = 5;

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);
        const email = formData.get('email');
        const username = formData.get('username');
        const password1 = formData.get('password1');
        const password2 = formData.get('password2');

        // VALIDATION
        if (password1 !== password2) {
            window.location = curUrl;
            return;
        }

        // OTHER BORING THINGS
        if (code) {
            if (tries === 0) {
                tries = 5;
                code = undefined;
                label.classList.add('hidden');
                inp.classList.add('hidden');
            } else {
                const userCode = formData.get('code');
                if (userCode === code) {
                    // formData.append('success', 1)
                    $.ajax({
                        type: 'POST',
                        url: mailUrl,
                        data: formData,
                        processData: false,
                        contentType: false,
                        beforeSend: function(xhr) {
                            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                        },
                        success: function(response) {
                            // обработка успешного ответа
                            window.location = sendUrl
                        },
                        error: function(xhr) {
                            console.error(xhr.responseText);
                        }
                    });
                }
                tries -= 1;
            }
        } else {
            $.ajax({
                type: 'POST',
                url: codeUrl,
                data: formData,
                processData: false, // Обязательно отключите обработку данных
                contentType: false, // Обязательно отключите заголовок Content-Type
                success: function(response) {
                    code = response.code;
                    if (label.classList.contains('hidden')) {
                        label.classList.remove('hidden');
                        inp.classList.remove('hidden');
                    }
                },
                error: function(xhr) {
                    console.error(xhr.responseText);  // Логируем ошибку
                }
            });
        }
    });
});