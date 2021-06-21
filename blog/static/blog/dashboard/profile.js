$(function () {

  $(".js-create-profile").click(function () {
    $.ajax({
      url: '/profile/new/',
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-profile").modal("show");
      },
      success: function (data) {
        $("#modal-profile .modal-content").html(data.html_form);
      }
    });
  });

});