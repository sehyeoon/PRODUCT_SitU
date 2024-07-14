document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.seat').forEach(function (seat) {
        seat.addEventListener('click', function () {
            var seatId = this.id; //
            if (seatId) {
                window.location.href = `/reserve/${seatId}/`;
            } else {
                console.error('Seat ID not found');
            }
        });
    });
});
