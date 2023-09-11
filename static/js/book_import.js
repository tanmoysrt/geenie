let page = 0;
let alreadyFetchingBooks = false;
let searchUsed = false;
let searchBasedOn = "";
let searchQuery = "";
let noMoreBooksFound = false;
let bookDetailsModal = new Modal(document.getElementById("book_details_model"));

// Scroll to top on page load
window.addEventListener("beforeunload", function () {
  $(window).scrollTop(0);
});

// Hide spinner on page load
window.addEventListener(
  "load",
  function () {
    checkQueryParams();
    fetchBooks();
  },
  false,
);

// Listen if user scroll to bottom of page
window.addEventListener("scroll", onScroll);
window.addEventListener("touchmove", onScroll);

function onScroll() {
  if ($(window).scrollTop() + $(window).outerHeight() >= $(document).outerHeight() - 20) {
    fetchBooks();
  }
}

// Fetch books
function fetchBooks() {
  if (noMoreBooksFound) {
    return;
  }
  if (alreadyFetchingBooks) {
    return;
  }
  alreadyFetchingBooks = true;
  $("#loading-books-spinner").show();

  document.documentElement.scrollTop = document.documentElement.scrollHeight - document.documentElement.clientHeight;

  // send ajax request
  $.ajax({
    url: buildQueryUrl(page + 1),
    type: "GET",
    withCredentials: true,
    success: function (data, textStatus, xhr) {
      if (xhr.status == 204) {
        $("#loading-books-spinner").hide();
        noMoreBooksFound = true;
        $("#no-more-books").show();
        return;
      }
      $("#books-list").append(data);
      page++;
    },
    complete: function () {
      alreadyFetchingBooks = false;
      $("#loading-books-spinner").hide();
    },
  });
}

// Build query url for books
function buildQueryUrl(page_no) {
  let url = "/books/import?page=" + page_no;
  if (searchUsed) {
    url += "&type=" + searchBasedOn + "&query=" + searchQuery;
  }
  return url;
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

// Show book details modal
function showBookDetailsModal(title, isbn, authors, publisher, pages, img_url) {
  $("#book_details_model_title").text(title);
  $("#book_details_model_isbn").text("ISBN: " + isbn);
  $("#book_details_model_authors").text(authors);
  $("#book_details_model_publisher").text(publisher);
  $("#book_details_model_pages").text(pages + " pages");
  $("#book_details_model_img").attr("src", img_url);
  bookDetailsModal.show();
}

// Hide book details modal
function hideBookDetailsModal() {
  bookDetailsModal.hide();
}

// Import book
function importBook(title, isbn, authors, publisher, pages, img_url) {
  // Ask for no of copies
  const copies = prompt("How many copies do you want to import?", 1);
  if (copies == null) {
    return;
  }
  setProcessingStateImportBtn(isbn, true);
  // Send ajax request
  $.ajax({
    url: "/books/import",
    type: "POST",
    data: {
      title: title,
      isbn_code: isbn,
      authors: authors,
      publisher: publisher,
      pages: pages,
      img_url: img_url,
      copies: copies,
    },
    withCredentials: true,
    success: function (data, textStatus, xhr) {
      if (xhr.status == 200) {
        Swal.fire({
          icon: "success",
          title: data.message,
        });
      } else {
        Swal.fire({
          icon: "error",
          title: "Oops...",
          text: data.message || "Something went wrong!",
        });
      }
    },
    error: function (xhr, textStatus, errorThrown) {
      Swal.fire({
        icon: "error",
        title: "Oops...",
        text: xhr.responseJSON.message || "Something went wrong!",
      });
    },
    complete: function () {
        setProcessingStateImportBtn(isbn, false);
    }
  });
}

// Set processing state for button
function setProcessingStateImportBtn(isbn, loading) {
    if (loading) {
        $("#import_btn_" + isbn).attr("disabled", true);
        $("#import_btn_" + isbn+" i").show();
    } else {
        $("#import_btn_" + isbn).attr("disabled", false);
        $("#import_btn_" + isbn+" i").hide();
    }
}