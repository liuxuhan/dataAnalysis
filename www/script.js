function predictPrice(){
    console.log("okay")
    km = $("input#inputKm")[0].value
    age = $("input#inputYear")[0].value
    model = $("select#inputModel")[0].value
    seller = $("select#inputSell")[0].value
    trans = $("select#inputTrans")[0].value
    owner = $("select#inputOwner")[0].value
    fuel = $("select#inputFuel")[0].value
    city = $("select#inputCity")[0].value
    body = $("select#inputBody")[0].value
    color = $("select#inputColor")[0].value

   param =  {
    "KmNumeric":km,
    

    }


// send ajax request
    var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
    }
  };
  xhttp.open("GET", "http://127.0.0.1:5002/test", true);
  xhttp.send();
}