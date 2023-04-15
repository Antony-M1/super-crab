$(document).ready(function () {
  $("#add-site-submit-form").click(function (e) {
    e.preventDefault();
    var url = $("#url").val();
    $.ajax({
      type: "GET",
      url: "/check-url",
      data: { url: url },
      success: function (response) {
        if (response.status === "success") {
          $("#add-site-form").submit();
        } else {
          alert(response.message);
        }
      },
      error: function () {
        alert("Error checking URL");
      },
    });
  });
});
