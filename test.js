const user = require('./fetch_user_set')
const autentikasi = require('./fetch_auth')
const actionAIU = require('./fetch_action')
const email = 'godim.ngadinegaran@gmail.com';
const password = '230205';
const access_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxZGQwMDkwZS0xZDdmLTQ0NTQtYmEyMi0xNzlmYWQzNTJkNzciLCJsZXZlbCI6InVzZXIiLCJleHAiOjE2OTkxOTM4Njl9.nRwd5FSVS8s1DK3nSmb3i8QXa0f9EToX_l-QNzWd0l8'

actionAIU.deleteObrolan(access_token)
    .then(data => {
        if (data) {
            console.log('Response:', data);
        }
    })
    .catch(error => {
        console.error(error);
    });


user.getUserData(access_token)
    .then(data => {
        if (data) {
            console.log('Response:', data);
        }
    })
    .catch(error => {
        console.error(error);
    });

autentikasi.loginFetch(email,password)
    .then(output=>{
        if (output){
            console.log(output);
        }
    })
    .catch(error => {
        console.error(error);
    });
