// window.navigator.geolocation.getCurrentPosition(console.log);  For GPS data - not currently needed

window.addEventListener('deviceorientation', (event) => {
  // document.getElementById("updateMe").innerHTML += `[${event.timeStamp}] ${event.alpha} ${event.beta} ${event.gamma}<br/>`;
  document.getElementById("updateMe").innerHTML += `[${event.timeStamp.toFixed(0)}] `;
})
