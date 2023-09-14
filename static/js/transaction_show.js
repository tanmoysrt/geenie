let selected_transaction_id = null;
let transaction_return_modal = new Modal(document.getElementById("transaction_return_modal"));
$(document).ready(function () {
  transaction_return_modal.hide();
  $("#members_list_table").DataTable({
    responsive: true,
    searching: false,
    order: [[0, "desc"]],
    columnDefs: [{ width: "20%", targets: 1 }],
  });
});

window.addEventListener(
  "load",
  function () {
    checkQueryParams();
  },
  false,
);

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

// Show transaction details modal
function showTransactionDetailsModal() {
  transaction_return_modal.show();
}

// Hide transaction details modal
function hideTransactionDetailsModal() {
  transaction_return_modal.hide();
}

//   Initiate return book
function initiateReturnBook(transaction_id) {
  $.ajax({
    url: `/transactions/${transaction_id}/return/details`,
    type: "GET",
    success: function (data) {
      $("#transaction_return_modal_normal_days").html(data.charge_details.normal_days);
      $("#transaction_return_modal_normal_per_day_charge").html(data.charge_details.normal_charge / 100);
      $("#transaction_return_modal_normal_total_charge").html(data.charge_details.normal_total_charge / 100);
      $("#transaction_return_modal_late_days").html(data.charge_details.late_days);
      $("#transaction_return_modal_late_per_day_charge").html(data.charge_details.late_charge / 100);
      $("#transaction_return_modal_late_total_charge").html(data.charge_details.late_total_charge / 100);
      $("#transaction_return_total_charge").html(data.total_charges / 100);
      selected_transaction_id = transaction_id;
      showTransactionDetailsModal();
    },
    error: function (data) {
      hideTransactionDetailsModal();
    },
  });
}

// Return book
function returnBook() {
  $.ajax({
    url: `/transactions/${selected_transaction_id}/return`,
    type: "POST",
    success: function (data) {
      hideTransactionDetailsModal();
      Swal.fire({
        title: "Success",
        text: data.message,
        icon: "success",
        confirmButtonText: "Done !",
      }).then((result) => {
        if (result.isConfirmed) {
          window.location.reload();
        }
      });
    },
    error: function (xhr) {
      const error = xhr.responseJSON;
      Swal.fire({
        title: "Error",
        text: error.message || "Unknown error occured.",
        icon: "error",
        confirmButtonText: "Ok",
      });
    },
  });
}
