{% load static %}
{% include 'messages.html' %}
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet"  href="{% static 'css/login.css' %}"> 
<title>Spacewood Login</title>

</head>
<body>

<div class="container" id="container">

	
	
	<div class="form-container sign-in-container">
		<form action="login" method="post">
			{% csrf_token %}
			<h1>Sign in</h1>
			
			<input type="username" placeholder="Username" name="username" required="required"/>
			<input type="password" placeholder="Password" name="password" required="required"/>
			<a href="reset_password/">Forgot your password?</a>
			<div>
				
			</div>
		</br>
		<center><p><b>New user? <a href="reg">Register Here</a>.</b></p></center>
			<button>Sign In</button>
		</form>
	</div>
	<div class="overlay-container">
		<div class="overlay">
			<div class="overlay-panel overlay-left">
				<h1>Welcome Back!</h1>
				<p>To start with Spacewood please login with your personal info</p>
				<button class="ghost" id="signIn">Sign In</button>
			</div>
			<div class="overlay-panel overlay-right">
				<h1>Welcome Back!</h1>
				<p>To start with Spacewood please login with your personal info</p>
				
			</div>
		</div>
	</div>
</div>

<script type="text/javascript">
	const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');

signUpButton.addEventListener('click', () => {
	container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
	container.classList.remove("right-panel-active");
});
</script>

<script type="text/javascript">
function showPassword() {
	  var x = document.getElementById("password");
	  if (x.type === "password") {
	    x.type = "text";
	  } else {
	    x.type = "password";
	  }
	}
</script>
<script>
	setTimeout(function() {
		if ($('#msg').length > 0){
			$('$msg'). remove();
		}
		
	}, 2000);
</script>

</body>
</html>
