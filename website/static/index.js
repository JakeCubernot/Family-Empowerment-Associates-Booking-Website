// Take noteId passed to this function and send POST request to delete-note, then refreshes page. 
function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),  //Converts to string so views.delete_note() can read it
    }).then((_res) => {
      window.location.href = "/";
    });
  }
