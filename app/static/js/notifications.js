// Import the functions you need from the SDKs you need
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-analytics.js";
import { getMessaging, getToken, onMessage } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-messaging.js";

// importScripts("https://www.gstatic.com/firebasejs/9.18.0/firebase-app.js");
// importScripts("https://www.gstatic.com/firebasejs/9.18.0/firebase-analytics.js");
// importScripts("https://www.gstatic.com/firebasejs/9.18.0/firebase-messaging.js");


// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyCTDkVIxcP3uXCIcaF2Mw8FXme9VKliYfg",
    authDomain: "foodrus-32dac.firebaseapp.com",
    projectId: "foodrus-32dac",
    storageBucket: "foodrus-32dac.appspot.com",
    messagingSenderId: "943790030033",
    appId: "1:943790030033:web:b294a28a21753ce2f259f0",
    measurementId: "G-3YGL19WHVY"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);




// Initialize Firebase Cloud Messaging and get a reference to the service
const messaging = getMessaging(app);
getToken(messaging, {vapidKey: "BFOzrZseOAA92DvYoLs91pMGtRTG3oW8C0pM4bHUea8RceH1uwAgsHHC0yUyeUFL80xRmatCAM67jgiQjaq-yWI"}).then((currentToken) => {
    if (currentToken) {
        if(isTokenSentToServer(currentToken) == false){
            fetch('api/fcmtoken', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ "fcm": currentToken })
            })
            .then(response => response.text())
            .then(response => console.log(JSON.stringify(response)))
            setTokenSentToServer(currentToken);
            console.log(currentToken)
        }
        else{
            console.log(currentToken)
            console.log("token already saved")
        }
    } else {
        Notification.requestPermission().then((permission) => {
            if (permission === 'granted') {
                console.log('Notification permission granted.');
            }
        });
        
        // ...
    }
    }).catch((err) => {
    console.log('An error occurred while retrieving token. ', err);
    // ...
    });

    
onMessage(messaging, (payload) => {
    console.log('Message received. ', payload);
    new Notification(payload.notification.title, payload.notification);
    
});


function isTokenSentToServer(currentToken) {
    return window.localStorage.getItem('sentFirebaseMessagingToken') == currentToken;
}

function setTokenSentToServer(currentToken) {
    window.localStorage.setItem(
        'sentFirebaseMessagingToken',
        currentToken ? currentToken : ''
    );
}

