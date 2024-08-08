function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Проверка, есть ли этот cookie
        if (cookie.startsWith(name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
      if (!/^http:.*/.test(settings.url) && !/^https:.*/.test(settings.url)) {
        // Устанавливаем CSRF токен перед отправкой запроса
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
      }
    }
});

const form = document.querySelector('.menu')
const label = document.querySelector('.hidden')
const inp = document.querySelector('#code')
let code
let tries = 5
let eol_type


form.addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(form)

    const eol = formData.get('eol')
    const password = formData.get('password')
    const curUrl = document.querySelector('#cur').value
    const mailUrl = document.querySelector('#mail').value
    const sendUrl = document.querySelector('#send').value
    // CHECK DATA ON VALIDATION
    if (eol && password) {
        if (eol.includes('@')) {
            eol_type = 'email'
        } else {
            eol_type = 'login'
        }
    
        if (code) {
            if (tries === 0) {
                tries = 5
                code = undefined
                // REMOVE CODE INPUT
                label.classList.add('hidden')
                inp.classList.add('hidden')
            } else {
                const userCode = formData.get('code')
                if (userCode === code) {
                    $.ajax({
                        type: 'POST',
                        url: mailUrl,
                        data: {success: true, eol: eol, eol_type: eol_type, password: password},
                        success: function() {
                            window.location = sendUrl
                        }
                    })
                }
                tries -= 1
            }
        } else {
            $.ajax({
                type: 'POST',
                // PUT URL HERE
                url: mailUrl,
                data: {eol: eol, eol_type: eol_type, password: password},
                success: function(response) {
                    if (response.cache) {
                        window.location = sendUrl
                    }
                    code = response.code
                    if (label.classList.contains('hidden')) {
                        label.classList.remove('hidden')
                        inp.classList.remove('hidden')
                    }
                },
                error: function() {
                    window.location = curUrl
                }
            })
        }
    }
})