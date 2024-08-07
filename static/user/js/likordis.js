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

const sendLikeUrl = document.querySelector('#sendlikeurl').value
const sendDislikeUrl = document.querySelector('#senddislikeurl').value

window.addEventListener('click', function(event) {
    // if (event.target.closest('.commentary')) {
    //     const comment = event.target.closest('.commentary')
    // }
    if (event.target.closest('.like')) {

        const comment = event.target.closest('.commentary')
        const commentId = comment.querySelector('.comment-id').value
        const likes = comment.querySelector('.people-like')
        $.ajax({
            type: 'POST',
            url: sendLikeUrl,
            data: {comment_id: commentId},
            success: function(response) {
                if (response.status === 200) {
                    likes.innerText = parseInt(likes.innerText) + 1 + ' people like this commentary'
                }
            }
        })
    } else if (event.target.closest('.dislike')) {
        const comment = event.target.closest('.commentary')
        const commentId = comment.querySelector('.comment-id').value
        const dislikes = comment.querySelector('.people-dislike')
        $.ajax({
            type: 'POST',
            url: sendDislikeUrl,
            data: {comment_id: commentId},
            success: function(response) {
                if (response.status === 200) {
                    dislikes.innerText = parseInt(dislikes.innerText) + 1 + ' people don\'t like this commentary'
                }
            }
        })
    }
})