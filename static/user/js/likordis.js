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