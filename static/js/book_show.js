let bookDetailsModal = new Modal(document.getElementById("book_details_model"))

function viewBookDetails(book_id) {
    $.ajax({
        type: "GET",
        url: "/books/" + book_id,
        success: function(data) {
            $("#book_details_model").html(data);
            bookDetailsModal.show();
        }
    });
}

// Hide book details modal
function hideBookDetailsModal() {
    bookDetailsModal.hide();
  }