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
