document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.seat').forEach(function (seat) {
        var status = seat.getAttribute('data-status');
        updateSeatVisual(seat, status);

        seat.addEventListener('click', function () {
            var selectedSeatId = this.id;
            var currentStatus = this.getAttribute('data-status');
            var newStatus;

            if (currentStatus === 'available') {
                newStatus = 'reserved';
            } else if (currentStatus === 'reserved') {
                newStatus = 'occupied';
            } else if (currentStatus === 'occupied') {
                newStatus = 'available';
            } else {
                console.error('Unknown current status:', currentStatus);
                return;
            }

            console.log(`Requesting status update for seat ID: ${selectedSeatId} to status: ${newStatus}`);

            fetch(`/update_seat_status/${selectedSeatId}/`, {
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

    const chairs = seatElement.querySelectorAll('.seat.chair');
    const table = seatElement.querySelector('.seat.table');

    if (status === 'reserved') {
        chairs.forEach((chair) => {
            chair.style.backgroundColor = '#ff8244';
            chair.classList.add('reserved');
        });
        if (table) {
            table.style.backgroundColor = '#ff8244';
            table.classList.add('reserved');
        }
    } else if (status === 'occupied') {
        chairs.forEach((chair) => {
            chair.style.backgroundColor = '#4A4949';
            chair.classList.remove('reserved');
        });
        if (table) {
            table.style.backgroundColor = '#333333';
            table.classList.remove('reserved');
        }
    } else {
        chairs.forEach((chair) => {
            chair.style.backgroundColor = '';
            chair.classList.remove('reserved');
        });
        if (table) {
            table.style.backgroundColor = '';
            table.classList.remove('reserved');
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
    // 모든 좌석 요소 가져오기
    var seats = document.querySelectorAll('.seat');

    seats.forEach(function (seat) {
        seat.addEventListener('mouseover', function () {
            // 좌석 ID 가져오기
            var seatId = seat.getAttribute('id');
            // 좌석 상태 가져오기
            var seatStatus = seat.getAttribute('data-status');
            // 입장 시각 가져오기 (예시로 start_time이라는 속성을 가정)
            var startTime = seat.getAttribute('data-start-time');

            // 팝업 내용을 채우기
            var seatInfoElement = document.getElementById('seat-info');
            seatInfoElement.textContent = seatId + '번 자리 좌석 이용 현황';

            var popupContentElement = document.getElementById('popup-content');
            var popupStatus = popupContentElement.querySelector('p');

            if (seatStatus === 'available') {
                popupStatus.textContent = '좌석 상태: 사용 가능';
            } else if (seatStatus === 'reserved') {
                popupStatus.textContent = '좌석 상태: 예약됨';
            } else if (seatStatus === 'occupied') {
                popupStatus.textContent = '좌석 상태: 사용 중';
            }

            var popupStartTime = popupContentElement.querySelector('p:nth-child(2)');
            if (startTime) {
                popupStartTime.textContent = '입장 시각: ' + startTime;
            } else {
                popupStartTime.textContent = '';
            }

            // 팝업 열기
            var popupElement = document.getElementById('popup');
            popupElement.classList.add('active');
        });

        seat.addEventListener('mouseout', function () {
            // 팝업 닫기
            var popupElement = document.getElementById('popup');
            popupElement.classList.remove('active');
        });
    });

    // 팝업 닫기 버튼 설정
    var popupCloseButton = document.getElementById('popup-close');
    popupCloseButton.addEventListener('click', function () {
        var popupElement = document.getElementById('popup');
        popupElement.classList.remove('active');
    });
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
document.addEventListener('DOMContentLoaded', function () {
    const confirmButtons = document.querySelectorAll('.btn-success');

    confirmButtons.forEach((button) => {
        button.addEventListener('click', function (event) {
            if (!confirm('Do you really want to confirm this reservation?')) {
                event.preventDefault();
            }
        });
    });
});
