const url_action_bw = 'http://localhost:8000/BecomeWaifu'

async function BWMeimeiHimari(bahasa, access_token) {
    const url = `${url_action_bw}/change-voice`;
    const requestBody = {
        BahasaYangDigunakan: bahasa,
        speakerID: 14
    }
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(requestBody),
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

async function BWKusukabeTsumugi(bahasa, access_token) {
    const url = `${url_action_bw}/change-voice`;
    const requestBody = {
        BahasaYangDigunakan: bahasa,
        speakerID: 8
    }
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(requestBody),
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

async function BWNurseT(bahasa, access_token) {
    const url = `${url_action_bw}/change-voice`;
    const requestBody = {
        BahasaYangDigunakan: bahasa,
        speakerID: 47
    }
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(requestBody),
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

async function BWNo7(bahasa, access_token) {
    const url = `${url_action_bw}/change-voice`;
    const requestBody = {
        BahasaYangDigunakan: bahasa,
        speakerID: 29
    }
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(requestBody),
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

async function BWSayo(bahasa, access_token) {
    const url = `${url_action_bw}/change-voice`;
    const requestBody = {
        BahasaYangDigunakan: bahasa,
        speakerID: 46
    }
    try {
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(requestBody),
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