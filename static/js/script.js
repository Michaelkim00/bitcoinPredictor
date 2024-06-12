$('#predictionForm').submit(function (event) {
    event.preventDefault();
    const formData = new FormData(this);
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
            const resultElement = document.getElementById('predictedPrice');
            resultElement.innerHTML = `Predicted Exchange Rate: ${data.predicted_price} KRW per USD`;

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
    const chart = new Chart(ctx, {
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
                        source: 'auto'  // This will ensure that only the formatted dates are displayed
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
