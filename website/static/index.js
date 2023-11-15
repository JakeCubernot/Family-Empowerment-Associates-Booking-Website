// Function to handle note deletion
function deleteNote(noteId) {
  fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
      window.location.href = "/";
  });
}
