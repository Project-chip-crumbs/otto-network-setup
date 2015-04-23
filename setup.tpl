<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">
  <title>Otto WifiSetup</title>
</head>

<body>
  <div class="container">
    <h1>Otto Wifi Setup</h1>

    <p>
      Otto is currently in setup mode.
      Please select the name of the Wifi network you would like to use
      and enter the password.
    </p>

    <form role="form" id="form">
    
    <div class="form-group"> 
    <label for="network">Network:</label>
    <select id="network"class="form-control">
%if len(wifis):
%for w in wifis:
          <option value="{{w}}">{{w}}</option>
%end
%else:
          <option value="scanning...">scanning...</option>
%end
    </select>
    </div>

    <div class="form-group">
    <label for="password">Password:</label>
    <input type="password" id="password" class="form-control" placeholder="enter password"/>
    </div>

    <button type="submit" id="connect" class="btn btn-default">Connect</button>

    <p id="result">
    </p>

      <!-- DBG: Timer executed <span id="counter">0</span> times...
      <span id="wifis">scanning for networks...</span> -->

  </div>

  <script src="jquery-1.11.2.min.js"></script>
  <script src="bootstrap/js/bootstrap.min.js"></script>
  <script language="javascript" type="text/javascript">
  jQuery(function() {

    $("#form").submit( function(event) {
      $('#result').html("connecting...");
      var json_data={ network: $('#network').val(), password: $('#password').val() };
      $.ajax({
        type: 'POST',
        url: '/api/v1/setup',
        data: JSON.stringify(json_data),
        contentType: "application/json; charset=utf-8",
        success: function(data) {
          $('#result').html(data);
        }
      });
      event.preventDefault();
      event.unbind();
      });

  });
  var count = 0;

  update_fun=function() {
    //DBG: $('#counter').html(++count);

    $.ajax({
      dataType: 'json',
      url: '/wifis',
      success: function(json) {
      console.log('got data:'+json);
        var selected = $("#network").val();
        $.each( json, function(i,w) {
          if(i==0) $("#network").html("");
          $("<option>").attr("value",w).text(w).appendTo("#network");
          if(w==selected) {
            $("#network").val(w);
          }
        });
      },
    });
    
    setTimeout(update_fun, 3000);
  };

  setTimeout(update_fun, 1000);
</script>
</head>

</body>
</html>
