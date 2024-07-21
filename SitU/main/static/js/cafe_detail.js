// cafe_detail.js

document.addEventListener('DOMContentLoaded', function () {
    // reserve_button 요소를 선택합니다.
    const reserveButton = document.querySelector('.reserve_button');

    // reserve_button 클릭 이벤트 리스너를 추가합니다.
    reserveButton.addEventListener('click', function () {
        // 데이터 속성에서 cafe_id 값을 가져옵니다.
        const cafeId = this.getAttribute('data-cafe-id');

        // cafe_id 값을 이용하여 URL을 생성합니다.
        const url = '/cafe/' + cafeId + '/seats/';

        // URL로 페이지를 이동합니다.
        window.location.href = url;
    });
});

$(document).ready(function () {
    $('#likeButton').click(function (e) {
        e.preventDefault();
        var cafeId = $(this).data('cafe-id');

        $.ajax({
            url: '/like_cafe/' + cafeId + '/',
            type: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            },
            success: function (response) {
                // 성공 시 처리
            },
            error: function (xhr, errmsg, err) {
                console.log('AJAX error', errmsg, err);
            },
        });
    });
});

// CSRF 토큰을 쿠키에서 가져오는 함수
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + '=') {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
