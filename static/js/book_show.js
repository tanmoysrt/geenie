let searchUsed = false;
let searchBasedOn = "";
let searchQuery = "";
let bookDetailsModal = new Modal(document.getElementById("book_details_model"));
let bookIssueModal = new Modal(document.getElementById("book_issue_model"));
let selectedBookId = "";

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

// Issue book
function openIssueBookModal(book_id, available_copies) {
  selectedBookId = book_id;
  $("#book_issue_model_member_name").val("");
  $("#book_issue_model_available_copies_count").text(available_copies);
  $("#book_issue_model_member_id").hide();
  $("#book_issue_model_member_id").val("");
  $("#book_issue_model_issue_btn").hide();
  bookIssueModal.show();
}

// Hide book issue modal
function hideBookIssueModal() {
  bookIssueModal.hide();
}


// Search member
function searchMember() {
  const member_name = $("#book_issue_model_member_name").val();
  $.ajax({
    type: "GET",
    url: "/members?format=json&type=name&query=" + member_name,
    success: function (data) {
      let html_data = '<option value="" selected disabled>Select member</option>';
      for (let i = 0; i < data.length; i++) {
        html_data += '<option value="' + data[i].id.toString() + '">' + data[i].name + ' [ID ' + data[i].id.toString() + ']</option>';
      }
      // Set the member list
      $("#book_issue_model_member_id").html(html_data);
      if (data.length > 0) {
        $("#book_issue_model_member_id").show();
      } else {
        $("#book_issue_model_member_id").hide();
      }
      // hide the issue button
      $("#book_issue_model_issue_btn").hide();
    },
    error: function (data) {
      alert("Member not found");
    },
  });
}

// Select member for issue
function selectMemberForIssue() {
  let member_id = $("#book_issue_model_member_id").val();
  if(member_id) {
    $("#book_issue_model_issue_btn").show();
  } else {
    $("#book_issue_model_issue_btn").hide();
  }
}

// Issue book
function issueBook() {
  const member_id = $("#book_issue_model_member_id").val();
  const count = parseInt($("#book_issue_model_count").val()) || 1;
  // set the loading icon and disable the button
  $("#book_issue_model_issue_btn i").show();
  $("#book_issue_model_issue_btn").attr("disabled", true);
  $.ajax({
    type: "POST",
    url: "/books/issue",
    data: {
      member_id: member_id,
      book_id: selectedBookId,
      count: count,
    },
    success: function (data, status, xhr) {
      console.log(data);
      if (xhr.status == 200) {
        Swal.fire({
          title: "Done !",
          text: data.message,
          icon: "success",          
        })
        hideBookIssueModal();
      } else {
        Swal.fire({
          title: "Error !",
          text: data.message,
          icon: "error",          
        })
      }      
    },
    error: function (xhr) {
      let data = xhr.responseJSON;
      Swal.fire({
        title: "Error !",
        text: data.message,
        icon: "error",          
      })
    },
    complete: function () {
      $("#book_issue_model_issue_btn i").hide();
      $("#book_issue_model_issue_btn").attr("disabled", false);
    }
  });
}