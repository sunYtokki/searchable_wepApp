$(document).ready(function() {
  $(".form-control").on("input", function() {

    var nameVal = $("#name").val();
    var imgVal = $("#img").val();
    var descVal = $("#description").val();
    var ratingVal = $("#rating").val();
    var review1 = $("#review1").val();
    var user1 = $("#user1").val();

    $("#name-error").addClass("hide");
    $("#img-error").addClass("hide");
    $("#desc-error").addClass("hide");
    $("#rating-error").addClass("hide");
    $("#rating-error").addClass("hide");
    $("#review-error").addClass("hide");

    if (nameVal == "") {
      $("#name-error").text("please input name");
      $("#name-error").addClass("error");
    } else {
      $("#name-error").removeClass("error");
    }

    if (imgVal == "" || !isUrl(imgVal)) {
      $("#img-error").text("please input image URL");
      $("#img-error").addClass("error");
    } else {
      $("#img-error").removeClass("error");
    }

    if (descVal == "") {
      $("#desc-error").text("please input description");
      $("#desc-error").addClass("error");
    } else {
      $("#desc-error").removeClass("error");
    }

    if (ratingVal == "") {
      $("#rating-error").text("please input rating");
      $("#rating-error").addClass("error");
    } else if (isNaN(ratingVal) || ratingVal < 0.1 || ratingVal > 5.0) {
      $("#rating-error").text("please input number between 0~5");
      $("#rating-error").addClass("error");
    } else {
      $("#rating-error").removeClass("error");
    }

    if (review1 == "" || user1 == "") {
      $("#review-error").text("please input username and review");
      $("#review-error").addClass("error");
    } else {
      $("#review-error").removeClass("error");
    }

    if (
      $("#name-error").hasClass("error") ||
      $("#img-error").hasClass("error") ||
      $("#desc-error").hasClass("error") ||
      $("#rating-error").hasClass("error") ||
      $("#rating-error").hasClass("error") ||
      $("#review-error").hasClass("error")
    ) {
      $("#submit").addClass("disabled");
    } else {
      $("#submit").removeClass("disabled");
    }
  });

  $("#submit").click(function() {
    $(".error").removeClass("hide");

    if ($("#submit").hasClass("disabled")) {
      console.log("error");
    } else {
      var new_data = {
        "name": $("#name").val(),
        "image": $("#img").val(),
        "description": $("#description").val(),
        "rating": $("#rating").val(),
        "reviews": [
          {
            "id": 0,
            "is_deleted": false,
            "user": $("#user1").val(),
            "review": $("#review1").val()
          },
        ]
      };

      $.ajax({
        url: "/create_process",
        dataType: "json",
        type: "POST",
        contentType: "application/json; charset=utf-8",
        data: JSON.stringify(new_data),
        success: function(result) {
          new_url = "http://127.0.0.1:5000/view/" + result.id;

          $("#new_entry").attr("href", new_url);
          $("#success_message").text(" is succesfully created!");
          $("#new_entry").text(result.name);

          reset();
          // location.href ='http://127.0.0.1:5000/view/'+ result.id
          console.log(result);
        },
        error: function(request, status, error) {
          $("#search-error").addClass("hide");
          console.log("Error");
          console.log(request);
          console.log(status);
          console.log(error);
        }
      });
    }
  });
});

function isUrl(s) {
  var regexp = /(ftp|http|https):\/\/(\w+:{0,1}\w*@)?(\S+)(:[0-9]+)?(\/|\/([\w#!:.?+=&%@!\-\/]))?/;
  return regexp.test(s);
}

function reset() {
  $("#submit").addClass("disabled");

  $("#name").val("");
  $("#img").val("");
  $("#description").val("");
  $("#rating").val("");
  $("#user1").val("");
  $("#review1").val("");

  $("#name-error").addClass("hide");
  $("#img-error").addClass("hide");
  $("#desc-error").addClass("hide");
  $("#rating-error").addClass("hide");
  $("#rating-error").addClass("hide");
  $("#review-error").addClass("hide");
  $("#search-error").addClass("hide");

  $("#name-error").addClass("error");
  $("#img-error").addClass("error");
  $("#desc-error").addClass("error");
  $("#rating-error").addClass("error");
  $("#rating-error").addClass("error");
  $("#review-error").addClass("error");

  $("#name").focus();
  window.scrollTo(0, 0);
}
