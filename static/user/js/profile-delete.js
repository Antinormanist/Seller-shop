function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Получаем CSRF-токен и устанавливаем общий обработчик для всех AJAX-запросов
const csrftoken = getCookie('csrftoken');

$(document).ready(function() {
    // Устанавливаем CSRF-токен в заголовок каждого AJAX-запроса
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^http:.*/.test(settings.url) && !/^https:.*/.test(settings.url)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});

const menu5 = document.querySelector('.sure-menu')
const label = document.querySelector('.label-s')
const inp = document.querySelector('.input-s')
const codeUrl = document.querySelector('#emailurl').value
const curUrl = document.querySelector('#cururl').value
const signUrl = document.querySelector('#signurl').value
let code


window.addEventListener('click', function(event) {
    if (!menu5.classList.contains('none') && event.target.closest('.sure-menu') === null) {
        menu5.classList.add('none')
        if (!label.classList.contains('none')) {
            label.classList.add('none')
            inp.classList.add('none')
        }
    }
    
    if (event.target.closest('.del-btn')) {
        if (menu5.classList.contains('none')) {
            menu5.classList.remove('none')
        }
    }
})

window.addEventListener('click', function(event) {
    if (event.target.closest('.sure-btn')) {
        if (code) {
            if (code === inp.value) {
                $.ajax({
                    type: 'POST',
                    url: codeUrl,
                    data: {success: true},
                    success: function() {
                        window.location = signUrl
                    }
                })
            } else {
                window.location = curUrl
            }
        } else {
            $.ajax({
                type: 'POST',
                url: codeUrl,
                data: {need_code: true},
                success: function(response) {
                    code = response.code
                    label.classList.remove('none')
                    inp.classList.remove('none')
                }
            })
        }
    }
})