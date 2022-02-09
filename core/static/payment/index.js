//'use strict';

var stripe = Stripe(STRIPE_PUBLISHABLE_KEY);

var elem = document.getElementById("submit");
clientsecret = elem.getAttribute("data-secret");

// Set up Stripe.js and Elements to use in checkout form
var elements = stripe.elements();
var style = {
	base: {
		color: "#000",
		lineHeight: "2.4",
		fontSize: "16px",
	},
};

var card = elements.create("card", { style: style });
card.mount("#card-element");

card.on("change", function (event) {
	var displayError = document.getElementById("card-errors");
	if (event.error) {
		displayError.textContent = event.error.message;
		$("#card-errors").addClass("alert alert-info");
	} else {
		displayError.textContent = "";
		$("#card-errors").removeClass("alert alert-info");
	}
});

//<<<<<<< Updated upstream
var form = document.getElementById("payment-form");

form.addEventListener("submit", function (ev) {
	ev.preventDefault();

	// submitFormData(form);

	var custName = document.getElementById("custName").value;
	var custAdd = document.getElementById("custAdd").value;
	var custAdd2 = document.getElementById("custAdd2").value;
	var postCode = document.getElementById("postCode").value;
	var phone = document.getElementById("phone").value;
	var state = document.getElementById("state").value;

	console.log({
		custName: custName,
		custAdd: custAdd,
		custAdd2: custAdd2,
		postCode: postCode,
	});

	var data = new FormData();

	data.append("order_key", clientsecret);
	data.append("csrfmiddlewaretoken", CSRF_TOKEN);
	data.append("custName", custName);
	data.append("custAdd", custAdd);
	data.append("custAdd2", custAdd2);
	data.append("postCode", postCode);
	data.append("phoneNumber", phone);
	data.append("state", state);
	data.append("action", "post");

	console.log([...data]);

	$.ajax({
		method: "post",
		processData: false,
		contentType: false,
		cache: false,
		data: data,
		enctype: "multipart/form-data",
		url: "https://GoldenBearDelivery.pythonanywhere.com/orders/add/",
		success: function (json) {
			console.log(json.success);
			stripe
				.confirmCardPayment(clientsecret, {
					payment_method: {
						card: card,
						billing_details: {
							address: {
								line1: custAdd,
								line2: custAdd2,
							},
							name: custName,
						},
					},
				})
				.then(function (result) {
					if (result.error) {
						console.log("payment error");
						console.log(result.error.message);
					} else {
						if (result.paymentIntent.status === "succeeded") {
							console.log("payment processed");

							// updating the billing status
							$.ajax({
								method: "post",
								data: {
									action: "post",
									order_key: clientsecret,
									csrfmiddlewaretoken: CSRF_TOKEN,
								},
								url: "https://GoldenBearDelivery.pythonanywhere.com/orders/payment_confirmation/",
								success: function (json) {
									console.log(json.success);
								},
							});

							// There's a risk of the customer closing the window before callback
							// execution. Set up a webhook or plugin to listen for the
							// payment_intent.succeeded event that handles any business critical
							// post-payment actions.
							window.location.replace(
								"https://GoldenBearDelivery.pythonanywhere.com/payment/orderplaced/"
							);
						}
					}
				});
		},
		error: function (xhr, errmsg, err) {},
	});
//=======
var form = document.getElementById('payment-form');

form.addEventListener('submit', function(ev) {
    ev.preventDefault();

var custName = document.getElementById("custName").value;
var custAdd = document.getElementById("custAdd").value;
var custAdd2 = document.getElementById("custAdd2").value;
var postCode = document.getElementById("postCode").value;


$.ajax({
  type: "POST",
  url: 'https://GoldenBearDelivery.pythonanywhere.com/orders/add/',
  data: {
    order_key: clientsecret,
    csrfmiddlewaretoken: CSRF_TOKEN,
    action: "post",
  },
  success: function (json) {
    console.log(json.success)


    stripe.confirmCardPayment(clientsecret, {
      payment_method: {
        card: card,
        billing_details: {
          address:{
              line1:custAdd,
              line2:custAdd2
        },
        name: custName
      },
    }
    }).then(function(result) {
      if (result.error) {
        console.log('payment error')
        console.log(result.error.message);
      } else {
        if (result.paymentIntent.status === 'succeeded') {
          console.log('payment processed')
        // There's a risk of the customer closing the window before callback
        // execution. Set up a webhook or plugin to listen for the
        // payment_intent.succeeded event that handles any business critical
        // post-payment actions.
          window.location.replace("https://GoldenBearDelivery.pythonanywhere.com/payment/orderplaced/");
      }
    }
  });

     },
    error: function (xhr, errmsg, err) {},
  });



//>>>>>>> Stashed changes
});
});
