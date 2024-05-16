document.addEventListener("DOMContentLoaded", function() {
    var ctx = document.getElementById('expenseChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                label: 'Expenses',
                data: amounts,
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            onClick: function(event, elements) {
                if (elements.length > 0) {
                    var datasetIndex = elements[0].datasetIndex;
                    var dataIndex = elements[0].index;
                    var categoryName = myChart.data.labels[dataIndex];
                    // Отправляем запрос на сервер для вычисления общей суммы без выбранной категории
                    fetch(`/calculate_total_expenses_without_category/${categoryName}/`)
                        .then(response => response.json())
                        .then(data => {
                            // Обновляем общую сумму затрат на основе ответа
                            document.getElementById('total-expenses').innerHTML = "Total Expenses (without " + categoryName + "): " + data.total_sum_without_category + "₽";
                        });
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    display: false,
                }
            }
        }
    });
});
