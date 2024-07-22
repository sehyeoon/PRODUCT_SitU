var reserveSeatButton = document.getElementById('reserveSeatButton');
if (reserveSeatButton) {
    reserveSeatButton.addEventListener('click', function (event) {
        event.preventDefault(); // 기본 동작 방지

        // seat_id 가져오기
        var seatId = document.querySelector('input[name="seat_id"]').value;

        // 예약 상태 업데이트 요청 보내기
        fetch(`/update_seat_status/${seatId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            },
            body: JSON.stringify({ status: 'reserved' }),
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.success) {
                    // 예약 상태 업데이트 성공
                    updateSeatStatus(seatId, 'reserved');
                    console.log('Reservation completed successfully:', { seatId });
                    window.location.href = '/reservation_complete';
                } else {
                    console.error('Failed to update seat status');
                }
            })
            .catch((error) => {
                console.error('Error updating seat status:', error);
            });
    });
}

// 예약 상태 업데이트 함수
function updateSeatStatus(seatId, status) {
    var seatElement = document.getElementById(seatId);
    if (seatElement) {
        if (status === 'available') {
            seatElement.classList.add('reserved');
        } else {
            seatElement.classList.remove('reserved');
        }
    } else {
        console.error(`Element with ID '${seatId}' not found.`);
    }
}
