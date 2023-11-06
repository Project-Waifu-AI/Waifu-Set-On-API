const user = require('./fetch_user_set')
const autentikasi = require('./fetch_auth')
const actionAIU = require('./fetch_action_ai_u')
const email = 'dimas.ngadinegaran@gmail.com';
const obrolan = 'hai siapa namamu';
const password = '230205';
const access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI5YTU3ZGM3OS1mZTZjLTQzN2EtYjcyYy1kNTI5MjQ4ZTExZmIiLCJsZXZlbCI6InVzZXIiLCJleHAiOjE2OTkyNjI5Mjl9.LLmg7hQ_tHJZgpRw00D2S4Ri04rcRRv4_kZwPg8yKy4';
/*
actionAIU.pesanSayo(obrolan, access_token)
    .then(data=>{
        if(data){
            const response = data[0].response
            const pesan = data[0].pesan
            const audio_streaming = data[1].streaming_audio
            console.log(audio_streaming)
        }
    })
*/

/*
actionAIU.deleteObrolan(access_token)
    .then(data => {
        if (data) {
            console.log('Response:', data);
        }
    })
    .catch(error => {
        console.error(error);
    });
*/

user.getUserData(access_token)
    .then(data => {
        if (data) {
            let userid = data.user_id
            console.log( userid);
        }
    })
    .catch(error => {
        console.error(error);
    });

/*
autentikasi.loginFetch(email,password)
    .then(output=>{
        if (output){
            console.log(output);
        }
    })
    .catch(error => {
        console.error(error);
    });
*/
/*
const pesan_sayo = actionAIU.pesanSayo(pesan, access_token)

const output = pesan_sayo.then(data=>{
    const response = data[0].response
    const translate = data[0].translate
    const streaming_audio = data[1].streaming_audio
    return response
})
*/
