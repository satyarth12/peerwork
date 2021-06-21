$(function () {

  /* Functions */

  var loadForm = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-work").modal("show");
      },
      success: function (data) {
        $("#modal-work .modal-content").html(data.html_form);
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
          $("#work-table").html(data.html_work_list);
          $("#modal-work").modal("hide");
        }
        else {
          $("#modal-work .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create Work
  $(".js-create-work").click(loadForm);
  $("#modal-work").on("submit", ".js-work-create-form", saveForm);

  // Update work
  $("#work-table").on("click", ".js-update-work", loadForm);
  $("#modal-work").on("submit", ".js-work-update-form", saveForm);

$("#work-table").on("click", ".js-delete-work", loadForm);
$("#modal-work").on("submit", ".js-work-delete-form", saveForm);

});