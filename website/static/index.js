// Function to handle note deletion
function deleteNote(noteId) {
  fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
      window.location.href = "/";
  });
}
// Couldn't get show 15 min interval instead of 00-59 to work. Yet. 
// function setFifteenMinuteIntervals() {
//     document.querySelectorAll("input[type='time']").forEach(function(timeInput) {
//         timeInput.addEventListener('change', function() {
//             var time = this.value.split(':');
//             var hours = parseInt(time[0]);
//             var minutes = parseInt(time[1]);

//             minutes = 15 * Math.round(minutes / 15);
//             if (minutes === 60) {
//                 hours++;
//                 minutes = 0;
//             }

//             this.value = hours.toString().padStart(2, '0') + ':' + minutes.toString().padStart(2, '0');
//         });
//     });
// }

// window.onload = setFifteenMinuteIntervals;
