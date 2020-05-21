
$(document).ready(function() {
  // $('#search_input').autocomplete({source: names})

  $.ajax({
    url: "/autoComplete",
    dataType: "json",
    success: function(result) {
      $("#search_input").autocomplete({ source: result });
    },
    error: function(request, status, error) {
      console.log("Error");
      console.log(request);
      console.log(status);
      console.log(error);
    }
  });

  $("#search_input").on("input", function() {
    var count = $("#search_input")
      .val()
      .replace(/ /g, "").length;

    if (count > 0 && window.location.pathname.split("/")[1] != "create") {
      $("#search_bttn").removeClass("disabled");
    } else {
      $("#search_bttn").addClass("disabled");
    }
  });

  //search
  $("#search_bttn").on("click", function() {
    search();
  });

  $("#search_input").on("keypress", function(e) {
    if (e.which == 13) {
      search();
      $("ul.ui-autocomplete").hide();
    }
  });
}); //document.ready

function search() {
  var count = $("#search_input")
    .val()
    .replace(/ /g, "").length;

  if (!$("#search_bttn").hasClass("disabled")) {
    $.ajax({
      type: "POST",
      url: "/search_process",
      dataType: "json",
      data: {
        target: $("#search_input")
          .val()
          .trim()
      },
      success: function(result) {
        location.href = "http://127.0.0.1:5000/search";
      },
      error: function(request, status, error) {
        console.log("Error");
        console.log(request);
        console.log(status);
        console.log(error);
      }
    });
    $("#search_input").val("");
  }

  if (count <= 0 && window.location.pathname.split("/")[1] != "create") {
    $("#search_input").val("");
    $("#search-error").removeClass("hide");
    $("#search_bttn").removeClass("disabled");
    $("#search_input").focus();
  }
}
