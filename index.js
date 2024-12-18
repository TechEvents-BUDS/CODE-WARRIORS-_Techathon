// const form = document.getElementById('weatherForm');
//         const temperatureResult = document.getElementById('temperatureResult');

//         form.addEventListener('submit', async (e) => {
//             e.preventDefault();
//             const location = document.getElementById('location').value;

//             try {
//                 const response = await fetch('http://localhost:5000/get-temperature', {
//                     method: 'POST',
//                     headers: { 'Content-Type': 'application/json' },
//                     body: JSON.stringify({ location })
//                 });

//                 const data = await response.json();
//                 if (data.success) {
//                     temperatureResult.innerText = `Temperature: ${data.temperature} °C`;
//                 } else {
//                     temperatureResult.innerText = 'Failed to fetch temperature.';
//                 }
//             } catch (error) {
//                 console.error("Error:", error);
//                 temperatureResult.innerText = 'Error fetching data. Check console.';
//             }
//         });

      
//         // Fetch data from the Node.js server
//         fetch('/api/temperature') // Relative path works since server serves this
//             .then(response => response.json())
//             .then(data => {
//                 document.getElementById('location').innerText = data.location;
//                 document.getElementById('temperature').innerText = data.temperature;
//             })
//             .catch(err => console.error('Error:', err));


// NEW??

      async function getGeminiResponse() {
            const prompt = document.getElementById('prompt').value;

            try {
                const response = await fetch('http://localhost:5000/api/gemini', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ prompt })
                });

                const data = await response.json();
                document.getElementById('response').innerText = data.response || 'No response';
            } catch (error) {
                console.error('Error:', error);
                document.getElementById('response').innerText = 'Error fetching response.';
            }
        }
