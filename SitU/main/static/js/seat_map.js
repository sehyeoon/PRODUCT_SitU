document.addEventListener('DOMContentLoaded', function () {
    var popup = document.getElementById('popup');
    var popupContent = document.getElementById('popup-content');
    var seatInfo = document.getElementById('seat-info');
    var reserveSeatButton = document.getElementById('reserveSeatButton');
    var closeButton = document.getElementById('popup-close');
    var selectedSeatId = this.id;

    document.querySelectorAll('.seat').forEach(function (seat) {
        seat.addEventListener('click', function () {
            var seatId = this.id;
            var seatNo = this.querySelector('.seat.table').textContent;
            console.log('Clicked seat ID:', seatId);

            if (seatId && seatId !== '') {
                selectedSeatId = seatId;
                seatInfo.textContent = seatNo + '번 자리 선택완료';
                popup.style.display = 'block';
            } else {
                console.error('Seat ID is empty or not set');
            }
        });
    });

    // 예약 버튼 클릭 시 예약 URL로 이동
    reserveSeatButton.addEventListener('click', function (event) {
        event.preventDefault(); // 폼 제출 방지
        if (selectedSeatId) {
            // 예약 폼의 action 속성을 설정하여 동적으로 URL을 생성
            var reservationForm = document.getElementById('reservationForm');
            var cafeNameElement = document.getElementById('cafeName');
            var cafeId = cafeNameElement.getAttribute('data-id');
            var url = `/reservation/create/${cafeId}/${selectedSeatId}/`; // 예약 URL 생성
            reservationForm.action = url; // action 속성 설정
            document.getElementById('popup-seat-id').value = selectedSeatId; // seat_id 설정
            reservationForm.submit(); // 폼 제출
        } else {
            console.error('No seat selected');
        }
    });

    // 팝업 닫기 기능
    if (closeButton) {
        closeButton.addEventListener('click', function () {
            popup.style.display = 'none';
            selectedSeatId = null;
        });
    }
});
