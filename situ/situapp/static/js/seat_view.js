document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.seat').forEach(function (seat) {
        seat.addEventListener('click', function () {
            var seatId = this.id;
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
                return; // 알 수 없는 상태일 경우 함수 종료
            }

            console.log(`Requesting status update for seat ID: ${seatId} to status: ${newStatus}`);

            fetch(`/update_seat_status/${seatId}/`, {
                // URL 수정
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
                        console.log('Seat status updated successfully:', { seatId });
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
    seatElement.setAttribute('data-status', status); // 상태 속성 업데이트

    // 모든 chair와 table 요소 선택
    const chairs = seatElement.querySelectorAll('.seat.chair');
    const table = seatElement.querySelector('.seat.table');

    // 상태에 따른 클래스 설정
    const statusClass = status === 'reserve' ? 'reserved' : '';

    if (status === 'reserve') {
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
            chair.style.backgroundColor = '#333333';
            chair.classList.remove('reserved');
        });
        if (table) {
            table.style.backgroundColor = '#333333';
            table.classList.remove('reserved');
        }
    } else {
        // 'available' 상태
        chairs.forEach((chair) => {
            chair.style.backgroundColor = ''; // 기본 색상으로 리셋
            chair.classList.remove('reserved');
        });
        if (table) {
            table.style.backgroundColor = ''; // 기본 색상으로 리셋
            table.classList.remove('reserved');
        }
    }
}
// getCookie 함수는 그대로 유지

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

// 좌석 상태 업데이트 후 로컬 스토리지에 저장
function saveSeatStatus(seatId, status) {
    localStorage.setItem(`seat_${seatId}`, status);
}

// 업데이트 후 상태 저장
saveSeatStatus(seatId, newStatus);
