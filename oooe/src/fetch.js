// Custom hook to fetch data from the API
let url = 'http://localhost:5000';
const fetchData = (async function(starting_registers, costs) {
  try {
    const response = await fetch(url+'/start-session', {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            },
            body: JSON.stringify({starting_registers: starting_registers, costs: costs}),
            });
    const data = await response.json();
    console.log(data);
    let session_id = data.session_id;
    let fetchData = async (endpoint, post_params) => {
        try {
            const response = await fetch(url+endpoint, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({...post_params, session_id: session_id}),
                    });
            const data = await response.json();
            // console.log(data);
            return data;
        } catch (error) {
            console.error('Error fetching request:', error);
            return null;
        }
        }
    return fetchData;
  } catch (error) {
    console.error('Error starting session:', error);
    return null;
  }
});

export default fetchData;