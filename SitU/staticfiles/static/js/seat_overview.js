document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.seat').forEach(function (seat) {
        var status = seat.getAttribute('data-status');
        updateSeatVisual(seat, status);

        seat.addEventListener('click', function () {
            var selectedSeatId = this.id;
            var currentStatus = this.getAttribute('data-status');
            var newStatus;
            var cafeId = document.getElementById('cafe-id').value;

            if (currentStatus === 'available') {
                newStatus = 'reserved';
            } else if (currentStatus === 'reserved') {
                newStatus = 'occupied';
            } else if (currentStatus === 'occupied') {
                newStatus = 'available';
            } else if (currentStatus === 'requesting') {
                newStatus = 'reserved';
            } else {
                console.error('Unknown current status:', currentStatus);
                return;
            }

            console.log(`Requesting status update for seat ID: ${selectedSeatId} to status: ${newStatus}`);

            fetch(`/cafe/${cafeId}/update_seat_status/${selectedSeatId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: JSON.stringify({ status: newStatus }),
            })
                .then((response) => {
                    if (!response.ok) {
                        return response.text().then((text) => {
                            throw new Error(`HTTP error! status: ${response.status}, message: ${text}`);
                        });
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data && data.success) {
                        updateSeatVisual(seat, newStatus);
                        console.log('Seat status updated successfully:', { selectedSeatId });
                    } else {
                        console.error('Failed to update seat status:', data ? data.error : 'Unknown error');
                    }
                })
                .catch((error) => {
                    console.error('Error updating seat status:', error.message);
                });
        });
    });
});

function updateSeatVisual(seatElement, status) {
    seatElement.setAttribute('data-status', status);

    const chairs = seatElement.querySelectorAll('.chair');
    const table = seatElement.querySelector('.table');

    if (status === 'reserved') {
        chairs.forEach((chair) => {
            chair.style.backgroundColor = '#ff8244';
            chair.style.color = 'white';
            chair.style.border = '2px solid #ff8244';
            chair.classList.add('reserved');
        });
        if (table) {
            table.style.backgroundColor = '#ff8244';
            table.style.color = 'white';
            table.style.border = '2px solid #ff8244';
            table.classList.add('reserved');
        }
    } else if (status === 'occupied') {
        chairs.forEach((chair) => {
            chair.style.backgroundColor = '#4a4a4a';
            chair.style.color = '#ffffff';
            chair.style.border = '2px solid #4a4a4a';
            chair.classList.remove('reserved');
        });
        if (table) {
            table.style.backgroundColor = '#4a4a4a';
            table.style.color = '#ffffff';
            table.style.border = '2px solid #4a4a4a';
            table.classList.remove('reserved');
        }
    } else if (status === 'requesting') {
        chairs.forEach((chair) => {
            chair.style.backgroundColor = '#ffffff';
            chair.style.color = '#4a4a4a';
            chair.style.border = '2px solid #4a4a4a';
            chair.classList.add('requesting');
        });
        if (table) {
            table.style.backgroundColor = '#ffffff';
            table.style.color = '#4a4a4a';
            table.style.border = '2px solid #4a4a4a';
            table.classList.add('requesting');
        }
    } else {
        chairs.forEach((chair) => {
            chair.style.backgroundColor = 'white';
            chair.style.color = '#ff8244';
            chair.style.border = '2px solid #ff8244';
            chair.classList.remove('reserved');
            chair.classList.remove('requesting');
        });
        if (table) {
            table.style.backgroundColor = 'white';
            table.style.color = '#ff8244';
            table.style.border = '2px solid #ff8244';
            table.classList.remove('reserved');
            table.classList.remove('requesting');
        }
    }
}

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

document.addEventListener('DOMContentLoaded', function () {
    var seats = document.querySelectorAll('.seat');
    var popupElement = document.getElementById('popup');

    seats.forEach(function (seat) {
        seat.addEventListener('mouseover', function () {
            var seatId = seat.getAttribute('id');
            var seatStatus = seat.getAttribute('data-status');
            var startTime = seat.getAttribute('data-start-time');
            var useTime = seat.getAttribute('data-use-time');

            document.getElementById('seat-info').textContent = seatId + '번 자리 좌석 이용 현황';
            document.getElementById('seat-status').textContent = '좌석 상태: ' + getSeatStatusText(seatStatus);
            document.getElementById('seat-start-time').textContent = '입장 시각: ' + startTime;
            document.getElementById('seat-use-time').textContent = '사용 시간: ' + useTime;

            popupElement.classList.add('active');
        });
    });

    function getSeatStatusText(status) {
        switch (status) {
            case 'available':
                return '사용 가능';
            case 'reserved':
                return '예약됨';
            case 'occupied':
                return '사용 중';
            case 'requesting':
                return '예약 요청 중';
            default:
                return '알 수 없음';
        }
    }
});

function closePopup() {
    document.getElementById('popup').classList.remove('active');
}

// 팝업 닫기 버튼 설정
var popupCloseButton = document.getElementById('popup-close');
popupCloseButton.addEventListener('click', closePopup);

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

document.addEventListener('DOMContentLoaded', function () {
    const confirmButtons = document.querySelectorAll('.button_success');
    const cancelButtons = document.querySelectorAll('.button_cancel');

    confirmButtons.forEach((button) => {
        button.addEventListener('click', function (event) {
            if (!confirm('예약 요청을 승인하시겠습니까?')) {
                event.preventDefault();
            }
        });
    });

    cancelButtons.forEach((button) => {
        button.addEventListener('click', function (event) {
            if (!confirm('예약 요청을 취소하시겠습니까?')) {
                event.preventDefault();
            }
        });
    });
});
