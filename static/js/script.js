let chart;  // Declare chart variable to hold the chart instance

$('#predictionForm').submit(function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const resultElement = document.getElementById('predictedPrice');
    resultElement.innerHTML = `<div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div>`;
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            // Sort the actual data by timestamps
            const actualData = data.timestamps.map((timestamp, index) => {
                return { timestamp: new Date(timestamp), price: data.actual_prices[index] };
            }).sort((a, b) => a.timestamp - b.timestamp);

            // Sort the future predicted data by timestamps
            const futureData = data.timestamps_line.map((timestamp, index) => {
                return { timestamp: new Date(timestamp), price: data.predicted_prices_line[index] };
            }).sort((a, b) => a.timestamp - b.timestamp);

            // Extract sorted timestamps and prices
            const actualTimestamps = actualData.map(item => item.timestamp.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }));
            const actualPrices = actualData.map(item => item.price);
            const futureTimestamps = futureData.map(item => item.timestamp.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }));
            const futurePredictedPrices = futureData.map(item => item.price);

            // Update prediction result on the page
            resultElement.innerHTML = `Predicted Price: ${data.predicted_price.toFixed(2)} KRW per USD`;

            // Update chart with sorted data
            updateChart(actualTimestamps, actualPrices, futureTimestamps, futurePredictedPrices);
        })
        .catch(error => {
            console.error('Error:', error);
            const resultElement = document.getElementById('predictionResult');
            resultElement.innerHTML = `<div class="alert alert-danger">An error occurred. Please try again later.</div>`;
        });
});

// Function to update the chart with new data
function updateChart(labels, actualPrices, futureLabels, futurePredictedPrices) {
    const ctx = document.getElementById('predictionChart').getContext('2d');

    if (chart) {
        // Update existing chart
        chart.data.labels = labels.concat(futureLabels);
        chart.data.datasets[0].data = actualPrices;
        chart.data.datasets[1].data = new Array(labels.length).fill(null).concat(futurePredictedPrices);
        chart.update();
    } else {
        // Create new chart if it doesn't exist
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels.concat(futureLabels),
                datasets: [{
                    label: 'Actual Exchange Rate',
                    data: actualPrices,
                    borderColor: 'green',
                    fill: false
                }, {
                    label: 'Predicted Exchange Rate',
                    data: new Array(labels.length).fill(null).concat(futurePredictedPrices),
                    borderColor: 'blue',
                    fill: false
                }]
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: 'USD to KRW Exchange Rate Prediction'
                },
                scales: {
                    xAxes: [{
                        type: 'time',
                        time: {
                            unit: 'day',
                            displayFormats: {
                                day: 'MMM DD YYYY'
                            }
                        },
                        scaleLabel: {
                            display: true,
                            labelString: 'Date'
                        },
                        ticks: {
                            source: 'auto'  // Ensure that only the formatted dates are displayed
                        }
                    }],
                    yAxes: [{
                        scaleLabel: {
                            display: true,
                            labelString: 'Exchange Rate (KRW per USD)'
                        }
                    }]
                }
            }
        });
    }
}
