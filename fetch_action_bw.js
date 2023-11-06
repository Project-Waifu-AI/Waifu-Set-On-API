const url_action_bw = 'http://localhost:8000/BecomeWaifu'

async function BWMeimeiHimari(pesan, access_token) {
    const url = `${url_action_bw}/pesan-meimei-himari?pesan=${pesan}`;
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'access-token': access_token
            }
        });

        if (response.status === 200) {
            const data = await response.json();

            return data;
        } else {
            throw new Error('Request failed with status ' + response.status);
        }
    } catch (error) {
        throw new Error('Error: ' + error);
    }
}