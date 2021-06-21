$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-education").modal("show");
      },
      success: function (data) {
        $("#modal-education .modal-content").html(data.html_form);
      }
    });
  };

  var saveForm = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          $("#book-table tbody").html(data.html_book_list);
          $("#modal-education").modal("hide");
        }
        else {
          $("#modal-education .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-create-education").click(loadForm);
  $("#modal-education").on("submit", ".js-education-create-form", saveForm);

  // Update book
  $("#resume-table").on("click", ".js-update-education", loadForm);
  $("#modal-education").on("submit", ".js-education-update-form", saveForm);

$("#book-table").on("click", ".js-delete-education", loadForm);
$("#modal-education").on("submit", ".js-education-delete-form", saveForm);

});