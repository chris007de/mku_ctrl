function getAllParameters() {
  getData("converter_state");
  getData("pll_lock");
  getData("converter_mode");
  getData("forward_power");
  getData("reverse_power");
  getData("lo_frequency");
  getData("temperature");
  getData("software_version");

  getData("statusmessage");
};

function getData(parameter) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      var x = document.getElementById(parameter);
      if (this.readyState == 4 && this.status == 200) {
        var obj = JSON.parse(this.responseText);
        x.innerHTML = obj.data["response_text"];
      }
    };
    xhttp.open("GET", "get/" + parameter, true);
    xhttp.send();
  }

  function setData(name, value) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 /*&& this.status == 200*/) {
        showSnackbar(this.responseText);
      }
    };
    xhttp.open("GET", "set/" + name + "/" + value, true);
    xhttp.send();
  }

  function showSnackbar(snackbarText) {
    /* Get the snackbar DIV */
    var x = document.getElementById("snackbar");
    
    x.innerHTML = snackbarText;
    
    /* Add the "show" class to DIV */
    x.className = "show";
    
    /* After 3 seconds, remove the show class from DIV */
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
    }
