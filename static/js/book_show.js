let searchUsed = false;
let searchBasedOn = "";
let searchQuery = "";
let bookDetailsModal = new Modal(document.getElementById("book_details_model"));

window.addEventListener(
  "load",
  function () {
    checkQueryParams();
  },
  false,
);

function viewBookDetails(book_id) {
  $.ajax({
    type: "GET",
    url: "/books/" + book_id,
    success: function (data) {
      $("#book_details_model").html(data);
      bookDetailsModal.show();
    },
  });
}

// Hide book details modal
function hideBookDetailsModal() {
  bookDetailsModal.hide();
}

// From query params find info about search and fill the values
function checkQueryParams() {
  const urlParams = new URLSearchParams(window.location.search);
  const query = urlParams.get("query");
  const type = urlParams.get("type");
  if (query && type) {
    searchUsed = true;
    searchBasedOn = type;
    searchQuery = query;
    $("#search-query").val(query);
    $("#search-type").val(type);
  } else {
    searchUsed = false;
  }
}
