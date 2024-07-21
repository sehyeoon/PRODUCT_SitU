document.addEventListener('DOMContentLoaded', function () {
    var reservationsData = JSON.parse(document.getElementById('reservations-data').textContent);

    var labels = [];
    var data = [];

    reservationsData.forEach(function (reservation) {
        labels.push(reservation.day);
        data.push(reservation.count);
    });

    var ctx = document.getElementById('reservationsChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Number of Reservations',
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1,
                },
            ],
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true,
                },
            },
        },
    });
});