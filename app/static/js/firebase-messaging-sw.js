// import { getMessaging } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-messaging.js";
// import { onBackgroundMessage } from "https://www.gstatic.com/firebasejs/9.18.0/firebase-messaging-sw.js";

importScripts('https://www.gstatic.com/firebasejs/9.18.0/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.18.0/firebase-messaging-compat.js');

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
firebase.initializeApp(firebaseConfig);
  
// Initialize Firebase Cloud Messaging and get a reference to the service
const messaging = firebase.messaging();


  

  