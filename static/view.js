$(document).ready(function() {
  var id = window.location.pathname.split("/")[2];

  $("#add_review").click(function() {
    $("#new_review").removeClass("hide");
    $("#new-user").focus();
  });

  $("#edit-bttn").click(function() {
    $("#dp-mode").addClass("hide");
    $("#edit-mode").removeClass("hide");
    $("#edit_description").val(desc);
    $("#edit_rating").val(rat);
    $("#edit_description").focus();
  });

  $("#cancel_edit").click(function() {
    $("#dp-mode").removeClass("hide");
    $("#edit-mode").addClass("hide");
  });

  $("#cancel_review").click(function() {
    $("#new_review").addClass("hide");
    $("#new-user").val("");
    $("#new-text").val("");
  });

  //add review ajax
  $("#submit").click(function() {
    $.ajax({
      type: "POST",
      url: "/edits",
      dataType: "json",
      data: {
        id: id,
        new_user: $("#new-user").val(),
        new_review: $("#new-text").val()
      },
      success: function() {
        location.reload();
      },
      error: function(request, status, error) {
        $("#review-error").removeClass("hide");
        console.log("Error");
        console.log(request);
        console.log(status);
        console.log(error);
      }
    });
  });

  //edit description ajax
  $("#submit-edit").click(function() {
    $.ajax({
      type: "POST",
      url: "/edits2",
      dataType: "json",
      data: {
        id: id,
        new_description: $("#edit_description").val(),
        new_rating: $("#edit_rating").val()
      },
      success: function() {
        //console.log(result)
        location.reload();
      },
      error: function(request, status, error) {
        $("#review-error").removeClass("hide");
        console.log("Error");
        console.log(request);
        console.log(status);
        console.log(error);
      }
    });
  });

  var deleted_card;
  var backup;
  var jqId;
  
  //delete ajax
  $(document).on("click", ".deleable", function() {
    var delete_id = $(this)
      .closest(".card")
      .attr("id");
    deleted_card = $(this).closest(".card");
    backup = deleted_card.html();
    //console.log(deleted_card.html())
    jqId = "undo" + delete_id;

    $.ajax({
      type: "POST",
      url: "/delete",
      dataType: "json",
      data: {
        venue_id: venue_id,
        delete_id: delete_id,
        is_undo: 0
      },
      success: function() {
        deleted_card.empty();
        deleted_card.append(
          '<button id="' +
            jqId +
            '"' +
            'class="undo btn btn-outline-warning btn-sm my-1"> Undo Delete </button>'
        );
        //undo();
      },
      error: function(request, status, error) {
        console.log("Error");
        console.log(request);
        console.log(status);
        console.log(error);
      }
    });
    
    //function undo() {
      $(document).on("click", ".undo", function() {
        console.log($(this).attr("id"));
        console.log(backup);
        deleted_card.append(backup);
        
        $.ajax({
          type: "POST",
          url: "/delete",
          dataType: "json",
          data: {
            venue_id: venue_id,
            delete_id: delete_id,
            is_undo: 1
          },
          success: function() {
            location.reload();
          },
          error: function(request, status, error) {
            console.log("Error");
            console.log(request);
            console.log(status);
            console.log(error);
          }
        });
      });
    //} //undo
  });
}); //document.ready
