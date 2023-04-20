$(document).ready(function () {
  $("#add-site-submit-form").click(function (e) {
    e.preventDefault();
    var url = $("#url").val();
    if (!isValidUrl(url)) {
      var toast = $(".toast");
      toast.find(".toast-body").text("Invalid URL");
      toast.toast("show");
    } else {
      $.ajax({
        type: "GET",
        url: "/check-url",
        data: { url: url },
        success: function (response) {
          if (response.status === "success") {
            $("#add-site-form").submit();
            // Show the toast
            var toast = $(".toast");
            toast.find(".toast-body").text("Saved Successfully");
            toast.toast("show");
          } else {
            // Show the toast
            var toast = $(".toast");
            toast.find(".toast-body").text(response.message);
            toast.toast("show");
          }
        },
        error: function () {
          // Show the toast
          var toast = $(".toast");
          toast.find(".toast-body").text("Error checking URL");
          toast.toast("show");
        },
      });
    }
  });
});

// Open a new tap when the 'Go To' button is clicked
$(document).ready(function () {
  $("button[data-url]").click(function () {
    var url = $(this).data("url");
    window.open(url, "_blank");
  });
});

// Open in same tap when the 'View' button is clicked
$(document).ready(function () {
  $("#view-site-data").click(function () {
    var name = $(this).data("name");
    var my_site = window.location.href + 'view/'
    window.open(my_site + name, '_self');
  });
});

$(document).ready(function () {
  $("#is_login_required").change(function () {
    const loginFields = document.getElementById("login_fields");
    if (this.checked) {
      loginFields.style.display = "block";
    } else {
      loginFields.style.display = "none";
    }
  });
});

// get the checkbox element and login-fields div element
// var isLoginRequiredCheckbox = document.getElementById("is_login_required");
// var loginFields = document.getElementById("login-fields");
// console.log(isLoginRequiredCheckbox, loginFields);
// // add event listener to checkbox element to show/hide login fields
// isLoginRequiredCheckbox.addEventListener("change", function() {
//   if (this.checked) {
//     loginFields.style.display = "block";
//   } else {
//     loginFields.style.display = "none";
//   }
// });




function isValidUrl(url) {
  try {
    new URL(url);
    return true;
  } catch (error) {
    return false;
  }
}
