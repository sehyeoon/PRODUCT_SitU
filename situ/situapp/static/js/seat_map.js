document.addEventListener('DOMContentLoaded', function () {
    var popup = document.getElementById('popup');
    var seatInfo = document.getElementById('seat-info');
    var reserveSeatButton = document.getElementById('reserveSeatButton');
    var closeButton = document.getElementById('popup-close');
    var selectedSeatId = '';

    document.querySelectorAll('.seat', '.box').forEach(function (seat) {
        seat.addEventListener('click', function () {
            var seatId = this.id;
            var seatNo = this.querySelector('.seat.table').textContent;
            var plug = this.dataset.plug === 'True';
            var backseat = this.dataset.backseat === 'True';

            var status = this.getAttribute('data-status');
            if (status !== 'available') {
                alert('현재 이 좌석은 다른 고객님이 이용 중인 좌석입니다. 다른 좌석을 선택해 주세요!');
                return; // 상태가 'available'이 아니면 함수 종료
            }
            console.log('Clicked seat ID:', seatId);

            if (seatId && seatId !== '') {
                selectedSeatId = seatId;

                seatInfo.innerHTML = `
                <div>${seatNo}번 자리 선택 완료</div>
                <div class="seat-features-container">
                  <span class="seat-feature ${plug ? 'available' : 'unavailable'}">플러그${plug ? 'O' : 'X'}</span> 
                  <span class="seat-feature ${backseat ? 'available' : 'unavailable'}">등받이${
                    backseat ? 'O' : 'X'
                }</span>
                </div>
              `;

                document.getElementById('popup-seat-id').value = seatId;
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

function showFloor(floor) {
    console.log('Showing floor: ', floor);
    document.getElementById('floor1').style.display = 'none';
    document.getElementById('floor2').style.display = 'none';
    document.getElementById('floor1Button').classList.remove('active');
    document.getElementById('floor2Button').classList.remove('active');

    document.getElementById(floor).style.display = 'block';

    if (floor === 'floor1') {
        document.getElementById('floor1Button').classList.add('active');
        document.getElementById('floor2Button').classList.remove('active');
    } else if (floor === 'floor2') {
        document.getElementById('floor2Button').classList.add('active');
        document.getElementById('floor1Button').classList.remove('active');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('floor2Button').addEventListener('click', function () {
        showFloor('floor2');
    });
});

//스터디룸 클릭시 알림창
document.querySelectorAll('#floor2.box, .studyroom').forEach(function (element) {
    element.addEventListener('click', function () {
        alert('스터디룸 예약 기능은 준비 중입니다!');
    });
});
