function validate(){
	var fInput=document.getElementById("profilePic");
	var email=document.getElementById("email");
	var userId=document.getElementById("userId");
	var password=document.getElementById("password");
	var flag=0;
	if(fInput.value.length!=0){
		/* file validation */
		var validExt= /(\.jpg|\.jpeg|\.png|\.gif)$/i;
		if (!validExt.exec(fInput.value)) {
			document.getElementById("filecheck").innerHTML='<font color="red">Only JPEG, JPG, PNG and GIF formats are supported!</font>';
            fInput.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("filecheck").innerHTML='<font color="green">Looks good!</font>';
			flag=1;
            fInput.style.borderColor="green";
		} 
    }
	if(email.value.length!=0){
		/* email validation */
		var res=email.value.split('@');
		var ext = /(\.com|\.in|\.ac.in|\.net)$/i;
		if (res[0].length<2 || res[1].length<4 || !ext.exec(res[1]) || res[1]==undefined || res[0]==undefined){
			document.getElementById("emailcheck").innerHTML='<font color="red">Please enter a valid email!</font>';
			flag=0;
            email.style.borderColor="red";
		}
		else{
			document.getElementById("emailcheck").innerHTML='<font color="green">Looks good!</font>';
			flag=1;
            email.style.borderColor="green";
		} 
    }

	if(userId.value.length!=0){
		/* userId validation */
		var res=userId.value
		if (res.length<5 || res.length>20) {
			document.getElementById("idcheck").innerHTML='<font color="red">Length of User Id should be in between 5-20 characters!</font>';
            userId.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("idcheck").innerHTML='<font color="green">Looks good!</font>';
            userId.style.borderColor="green";
			flag=1;
		} 
    }

	if(password.value.length!=0){
		/* password validation */
		var res=password.value
		if (res.length<6 || res.length>15) {
			document.getElementById("passcheck").innerHTML='<font color="red">length of Password should be in between 6-15 characters!</font>';
            password.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("passcheck").innerHTML='<font color="green">Looks good!</font>';
            password.style.borderColor="green";
			flag=1;
		}
	 
    }

    if(flag==1){
        return true;
    }
    else{
        return false;
    }	
}

function validate_login(){
	var userId=document.getElementById("userId");
	var password=document.getElementById("password");
	var flag=0;

	if(userId.value.length!=0){
		/* userId validation */
		var res=userId.value
		if (res.length<5 || res.length>20) {
			document.getElementById("idcheck").innerHTML='<font color="red">&nbsp;&nbsp;&nbsp;&nbsp;Length of User Id should be in between 5-20 characters!</font>';
            userId.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("idcheck").innerHTML='<font color="green">&nbsp;&nbsp;&nbsp;&nbsp;Looks good!</font>';
			flag=1;
            userId.style.borderColor="green";
		} 
    }

	if(password.value.length!=0){
		/* password validation */
		var res=password.value
		if (res.length<6 || res.length>15) {
			document.getElementById("passcheck").innerHTML='<font color="red">&nbsp;&nbsp;&nbsp;&nbsp;Length of Password should be in between 6-15 characters!</font>';
            password.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("passcheck").innerHTML='<font color="green">&nbsp;&nbsp;&nbsp;&nbsp;Looks good!</font>';
			flag=1; 
            password.style.borderColor="green";
		}
	 
    }

    if(flag==1){
        return true;
    }
    else{
        return false;
    }	
}

function remove_msg(){
	if(document.getElementById("alert alert-success")!=null){
		document.getElementById("alert alert-success").style.display='none';
	}
	if(document.getElementById("alert alert-danger")!=null){
		document.getElementById("alert alert-danger").style.display='none';
	}
}

function getUsersData(){
	fetch('/users')
	.then(
		(res) => {
			return res.json();
		}
	)
	.then(
		(data)=>{
			console.log(data)
			if(data.users.length > 0){
				let users='<div class="user-data-div"><table><tr><th>User ID</th><th>Profile</th><th>Username</th><th>Email</th><th>Event Name</th><th>Action</th></tr>';
				data.users.map(
					(user)=>{
						users=users.concat("<tr>");
						users=users.concat("<td>"+ user.userID +"</td>");
						users=users.concat('<td><img src="'+ user.profilePic +'" class="profile"></td>');
						users=users.concat("<td>"+ user.username +"</td>");
						users=users.concat("<td>"+ user.email +"</td>");
						users=users.concat("<td>"+ user.eventName +"</td>");
						// users=users.concat('<td><img src = "'+ user.eventPic +'" class = "result_img" ></td>');
						if(user.isActive == 1){
							users=users.concat('<td><input type="submit" class="btn btn-danger" value="Deactivate" onClick="deactivate('+ user.userID +')"></td>');	
						}
						else{
							users=users.concat('<td><input type="submit" class="btn btn-primary" value="Activate" onClick="activate('+ user.userID +')"></td>');
						}
						users=users.concat("</tr>");
					}
				);
				users=users.concat("</table></div>");
				document.getElementById("user_data").innerHTML=users;
				document.getElementById("getUsersDataBtn").style.visibility='hidden';
			}
			else{
				document.getElementById("user_data").innerHTML='<h1><font color="white">No data available.</font></h1>';
			}

		}
	);
}

function activate(id){
	fetch('/activate/'+id)
	.then((res)=>{
		return res.json()
	})
	.then(
		(response)=>{
			if(response.status==200){
				getUsersData();
			}
		}
	);
}
function deactivate(id){
	fetch('/deactivate/'+id)
	.then((res)=>{
		return res.json()
	})
	.then(
		(response)=>{
			if(response.status==200){
				getUsersData();
			}
		}
	);
}

function set_settings_param(){
	let code=document.getElementById("settings_mode").value;
	let data;
	if(code!=99){
		if(code==0){
			data="<center><table>";
			data+='<tr><td><b>New User Name</b></td><td><input type="text" id="uname" name="uname" placeholder="User Name"></td></tr><tr><td><b>(re-Type)New User Name</b></td><td><input type="text" id="reuname" name="reuname" placeholder="Retype User Name"></td></tr><tr><td><input type="submit" value="Change" onClick="changeUname()" class="btn btn-primary"></td><td><input type="reset" value="Cancel" class="btn btn-danger"></td></tr></table><div id"unamecheck"></div></center>';
		}
		else if(code==1){
			data="<center><table>";
			data+='<tr><td><b>New Password</b></td><td><input type="password" name="pass" id="pass" placeholder="Password"></td></tr><tr><td><b>(re-Type)New Password</b></td><td><input type="password" id="repass" name="repass" placeholder="Retype password"></td></tr><tr><td><input type="submit" value="Change" onClick="changePass()" class="btn btn-primary"></td><td><input type="reset" value="Cancel" class="btn btn-danger"></td></tr></table><div id="passcheck"></div></center>';	
		}
		else if(code==2){
			data="<center><table>";
			data+='<tr><td><b>New Email</b></td><td><input type="email" name="email" id="email" placeholder="Email"></td></tr><tr><td><b>(re-Type)New Email</b></td><td><input type="email" id="reemail" name="reemail" placeholder="Retype Email"></td></tr><tr><td><input type="submit" value="Change" onClick="changeEmail()" class="btn btn-primary"></td><td><input type="reset" value="Cancel" class="btn btn-danger"></td></tr></table><div id="emailcheck"></div></center>';
		}
		else if(code==3){
			data="<center>";
			 data+='<form method="post" enctype="multipart/form-data" onSubmit="return validateAndUpload()" action="changeProfilePicture"><table><tr><td><b>New Profile Picture</b></td><td><input type="file" id="profpic" name="profpic" onChange="validateUpload()" name="profpic"></td></tr><tr><td><input type="submit" value="Change" class="btn btn-primary"></td><td><input type="reset" value="Cancel" class="btn btn-danger"></td></tr></table></form><div id="filecheck"></div></center>';
		}
		else{
			data="Invalid selection code!";
		}
	}
	else{
		data="";
	}
	document.getElementById("settings").innerHTML=data;
}

function changeUname(){
	let nuname=document.getElementById("uname");
	let renuname=document.getElementById("reuname");
	if(nuname.value==renuname.value){
		if (nuname.length<5 || renuname.length>20) {
			document.getElementById("unamecheck").innerHTML='<font color="red">length of User name should be in between 5-20 characters!</font>';
			nuname.style.borderColor="red";
			renuname.style.borderColor="red";
		}
		else{
			let formdata = new FormData();		
			formdata.append("mode", "0");
			formdata.append("value", nuname.value);

			let requestOptions = {
  				method: 'POST',
  				body: formdata,
  				redirect: 'follow'
			};	

		fetch("/changeCredentials", requestOptions)
		.then(response => response.json())
		.then((result) => {
			if(result.status==200){
				  window.location.href='http://127.0.0.1:5000/';
			}
			else{
				alert("Server error! Try again later.");
			}
		})
  		.catch(error => console.log('error', error));
		
		
		}
		
	}
	else{
		document.getElementById("unamecheck").innerHTML='<font color="red">User Name and retyped User Name not matching!</font>';
		nuname.style.borderColor="red";
		renuname.style.borderColor="red";

	}

}

function changePass(){
	var npass=document.getElementById("pass");
	var renpass=document.getElementById("repass");
	if(renpass.value==npass.value){
		if (npass.length<6 || npass.length>15) {
			document.getElementById("passcheck").innerHTML='<font color="red">length of Password should be in between 6-15 characters!</font>';
			npass.style.borderColor="red";
			renpass.style.borderColor="red";
		}
		else{
			let formdata = new FormData();		
			formdata.append("mode", "1");
			formdata.append("value", npass.value);

			let requestOptions = {
  				method: 'POST',
  				body: formdata,
  				redirect: 'follow'
			};	

		fetch("/changeCredentials", requestOptions)
		.then(response => response.json())
		.then((result) => {
			if(result.status==200){
				  window.location.href='http://127.0.0.1:5000/';
			}
			else{
				alert("Server error! Try again later.");
			}
		})
  		.catch(error => console.log('error', error));
		
		}
	}
	else{
		document.getElementById("passcheck").innerHTML='<font color="red">Password and retyped password not matching!</font>';
		npass.style.borderColor="red";
		renpass.style.borderColor="red";

	}

}


function changeEmail(){
	var nemail=document.getElementById("email");
	var reemail=document.getElementById("reemail");
	if(reemail.value==nemail.value){
		let formdata = new FormData();		
			formdata.append("mode", "2");
			formdata.append("value", nemail.value);

			let requestOptions = {
  				method: 'POST',
  				body: formdata,
  				redirect: 'follow'
			};	

		fetch("/changeCredentials", requestOptions)
  		.then(response => response.json())
  		.then((result) => {
			  if(result.status==200){
					window.location.href='http://127.0.0.1:5000/';
			  }
			  else{
				  alert("Server error! Try again later.");
			  }
		  })
  		.catch(error => console.log('error', error));
		
		
		}
	else{
		document.getElementById("emailcheck").innerHTML='<font color="red">Email and retyped email not matching!</font>';
		npass.style.borderColor="red";
		renpass.style.borderColor="red";

	}

}

function validateUpload(){
	var fInput = document.getElementById("profpic")
	var flag = 0
	if(fInput.value.length!=0){
		/* file validation */
		var validExt= /(\.jpg|\.jpeg|\.png|\.gif)$/i;
		if (!validExt.exec(fInput.value)) {
			document.getElementById("filecheck").innerHTML='<font color="red">Only JPEG, JPG, PNG and GIF formats are supported!</font>';
			fInput.style.borderColor="red";
			flag=0;
		}
		else{
			document.getElementById("filecheck").innerHTML='<font color="green">Looks good!</font>';
			flag=1;
			fInput.style.borderColor="green";
		} 
	}
	if(flag==0){
		return false;
	}
	else{
		return true;
	}

}

function set_task_param(){
	let code=document.getElementById("task_mode").value;
	let data;
	if(code!=99){
		if(code==1){
			data="<center>";
			data+='<form method="post" enctype="multipart/form-data" onSubmit="return validateAndUploadAdd()" action="addInterest"><table><tr><td><b>Enter comma seperated (,) one word adjectives that descrives who you are : </b></td><td><input type="text" id="interest_words" onChange="validateAndUploadAdd()" name="interest_words"></td></tr><tr><td><input type="submit" value="Add" class="btn btn-primary"></td><td><input type="reset" value="Cancel" class="btn btn-danger"></td></tr></table></form><div id="interest_words_check"></div></center>';	
		}
		else if(code==2){
			data="";
			data+='<div class="d-flex align-items-center">';
  			data+='<strong>Fetching data...</strong>'
  			data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
			data+='</div>'
			view_interests();
		}
		else if(code==3){
			data="<center>";
			data+='<form method="post" enctype="multipart/form-data" onSubmit="return validateAndUploadDelete()" action="deleteInterest"><table><tr><td><b>Enter comma seperated (,) one word adjectives that you want to remove from your profile : </b></td><td><input type="text" id="interest_words" onChange="validateAndUploadDelete()" name="interest_words"></td></tr><tr><td><input type="submit" value="Delete" class="btn btn-primary"></td><td><input type="reset" value="Cancel" class="btn btn-danger"></td></tr></table></form><div id="interest_words_check"></div></center>';
		}
		else if(code==4){
			data="";
			data+='<div class="d-flex align-items-center">';
  			data+='<strong>Fetching data...</strong>'
  			data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
			data+='</div>'
			view_recommended_events();
		}
		else if(code==5){
			data="<center>";
			data+='<form method="post" enctype="multipart/form-data", action = "addEvent"><table><tr><td><b>Event Name</b></td><td><input type="text" id="event_name" name="event_name"></td></tr><tr><td><b>Event Description</b></td><td><input type="text" id="event_description" name="event_description"></td></tr><tr><td><b>Event Date</b></td><td><input type="datetime-local" id="event_date" name="event_date"></td></tr><tr><td><b>Event Location</b></td><td><input type="text" id="event_address" name="event_address"></td></tr><tr><td><b>Event Tags (comma seperated (,) one word adjectives that describes event)</b></td><td><input type="text" id="event_tag" name="event_tag"></td></tr><tr><td><b>New Profile Picture</b></td><td><input type="file" id="eventpic" name="eventpic" name="eventpic"></td></tr><tr><td><input type="submit" value="Create" class="btn btn-primary"></td><td><input type="reset" value="Cancel" class="btn btn-danger"></td></tr></table></form><div id="event_check"></div></center>';
		}
		else if(code==6){
			data="";
			data+='<div class="d-flex align-items-center">';
  			data+='<strong>Fetching data...</strong>'
  			data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
			data+='</div>'
			view_events();
		}
		else{
			data="Invalid selection code!";
		}
	}
	else{
		data="";
	}
	document.getElementById("task").innerHTML=data;
}


function view_interests(){
	fetch('/viewInterest')
	.then((res)=>{
		return res.json()
	})
	.then(
		(response)=>{
			// console.log(response)
			if(response.status==200){
				let data="";
				data+="<b>Interests fetched successfully!</b><br>";
				data+='<table class="user-data-div">';
				data+='<tr><th>Index</th><th>Word</th></tr>';
				
				for(i = 0; i< response.words.length; i = i+1){
					data+='<tr>';
					data+='<td>'+ response.indexes[i] +'</td>';
					data+='<td>'+ response.words[i] +'</td>';
					data+='</tr>';
				}
				data+="</table>";
				document.getElementById("task").innerHTML=data;
			}
		}
	);
}

function get_recommedations_feed(){
	fetch('/viewRecommendedEvents')
	.then((res)=>{
		return res.json()
	})
	.then(
		(response)=>{
			console.log(response)
			if(response.status==200){
				let data="";
				data+='<center><div class="card-grid">'
				for(i = 0; i< response.event_name.length; i = i+1){
					data+='<div class = "event_recommendation_card">'
					data+='<img src = "'+ response.event_pic[i] +'" alt="Avatar" style="width: 100%;">'
					data+='<div class="container">'
					data+='<h4><b>'+ response.event_name[i] +'</b></h4>'
					data+='<p>'+ response.event_description[i] +'</p>'
					data+='<p>'+ response.event_date[i] +'</p>'
					data+='<p>'+ response.event_address[i] +'</p>'
					data+='<p>'+ response.event_tags[i] +'</p>'
					data+='</div>'
					data+='</div>'
				}
				data+="</div></center>"
				document.getElementById("recommendation_feed").innerHTML=data;
			}
		}
	);
}

function view_recommended_events(){
	fetch('/viewRecommendedEvents')
	.then((res)=>{
		return res.json()
	})
	.then(
		(response)=>{
			// console.log(response)
			if(response.status==200){
				let data="";
				data+='<center><div class="card-grid">'
				for(i = 0; i< response.event_name.length; i = i+1){
					data+='<div class = "event_recommendation_card">'
					data+='<img src = "'+ response.event_pic[i] +'" alt="Avatar" style="width: 100%;">'
					data+='<div class="container">'
					data+='<h4><b>'+ response.event_name[i] +'</b></h4>'
					data+='<p>'+ response.event_description[i] +'</p>'
					data+='<p>'+ response.event_date[i] +'</p>'
					data+='<p>'+ response.event_address[i] +'</p>'
					data+='<p>'+ response.event_tags[i] +'</p>'
					data+='</div>'
					data+='</div>'
				}
				data+="</div></center>"
				document.getElementById("task").innerHTML=data;
			}
		}
	);
}

function view_events(){
	fetch('/viewEvents')
	.then((res)=>{
		return res.json()
	})
	.then(
		(response)=>{
			// console.log(response)
			if(response.status==200){
				let data="";

				data+='<center><div class="card-grid">'
				for(i = 0; i< response.event_name.length; i = i+1){
					data+='<div class = "event_recommendation_card">'
					data+='<img src = "'+ response.event_pic[i] +'" alt="Avatar" style="width: 100%;">'
					data+='<div class="container">'
					data+='<h4><b>'+ response.event_name[i] +'</b></h4>'
					data+='<p>'+ response.event_description[i] +'</p>'
					data+='<p>'+ response.event_date[i] +'</p>'
					data+='<p>'+ response.event_address[i] +'</p>'
					data+='<p>'+ response.event_tags[i] +'</p>'
					data+='<p><input type="submit" class="btn btn-danger" value="Delete" onClick="delete_event(\''+ response.event_id[i] +'\')"></p>';
					data+='</div>'
					data+='</div>'
				}
				data+="</div></center>"
				document.getElementById("task").innerHTML=data;
			}
		}
	);
}

function delete_event(id){
	fetch('/delete_event/'+id)
	.then((res)=>{
		return res.json()
	})
	.then(
		(response)=>{
			if(response.status==200){
				view_events();
			}
		}
	);
}


function validateAndUploadAddEvent(){
	var event_name = document.getElementById("event_name")
	var event_description = document.getElementById("event_description")
	var event_date = document.getElementById("event_date")
	var event_address = document.getElementById("event_address")
	var fInput = document.getElementById("event_tag")
	var eventpic = document.getElementById("eventpic")
	var strings = fInput.value.split(',').map(s => s.trim());
	console.log(event_name.value + event_description.value + event_address.value + event_date.value + strings);
	var flag = 1

	if(eventpic.value.length!=0){
		/* file validation */
		var validExt= /(\.jpg|\.jpeg|\.png|\.gif)$/i;
		if (!validExt.exec(eventpic.value)) {
			document.getElementById("event_check").innerHTML='<font color="red">Only JPEG, JPG, PNG and GIF formats are supported!</font>';
			eventpic.style.borderColor="red";
			flag=0;
		}
	}
	else{
		document.getElementById("event_check").innerHTML='<font color="red">Only JPEG, JPG, PNG and GIF formats are supported!</font>';
		eventpic.style.borderColor="red";
		flag = 0
	}

	if(strings.length!=0){
		/* file validation */
		for(let i=0; i<strings.length; i = i + 1){
			if(strings[i].includes(' ')){
				// console.log("Issue");
				document.getElementById("event_check").innerHTML='<font color="red">Only one word adjectives are supported!</font>';
				fInput.style.borderColor="red";
				flag=0;	
			}
			if(strings[i].length == 0){
				flag = 0
			}
		} 
	}
	else{
		document.getElementById("event_check").innerHTML='<font color="red">No tags found!</font>';
		fInput.style.borderColor="red";
		flag = 0
	}

	if (event_name.value.length == 0){
		document.getElementById("event_check").innerHTML='<font color="red">Event name cannot be empty!</font>';
		event_name.style.borderColor="red";
		flag = 0
	}
	if (event_description.value.length == 0){
		document.getElementById("event_check").innerHTML='<font color="red">Event description cannot be empty!</font>';
		event_description.style.borderColor="red";
		flag = 0
	}
	if (event_date.value.length == 0){
		document.getElementById("event_check").innerHTML='<font color="red">Event date cannot be empty!</font>';
		event_date.style.borderColor="red";
		flag = 0
	}
	if (event_address.value.length == 0){
		document.getElementById("event_check").innerHTML='<font color="red">Event address cannot be empty!</font>';
		event_address.style.borderColor="red";
		flag = 0
	} 


	// console.log(flag);
	if(flag==0){
		return false;
	}
	else{
		// console.log("Check Pass!");
		document.getElementById("event_check").innerHTML='<font color="green">Looks good!</font>';
		fInput.style.borderColor="green";
		event_name.style.borderColor="green";
		event_description.style.borderColor="green";
		event_date.style.borderColor="green";
		event_address.style.borderColor="green";
		eventpic.style.borderColor="green";
		
		let formData=new FormData();
		formData.append('context_words',strings);
		formData.append('event_name',event_name.value);
		formData.append('event_description',event_description.value);
		formData.append('event_date',event_date.value);
		formData.append('event_address',event_address.value);
		formData.append('event_pic',eventpic.files[0]);
	// 	let requestOptions = {
	// 		method: 'POST',
	// 		body: JSON.stringify(
	// 			{
	// 				"context_words" : strings,
	// 				"event_name" : event_name.value,
	// 				"event_description" : event_description.value,
	// 				"event_date" : event_date.value,
	// 				"event_address" : event_address.value,
	// 				"eventpic" : eventpic.files[0]
	// 			}
	// 		),
	// 		redirect: 'follow',
	// 		headers: {
	// 			'Content-Type': 'application/json'
	// 		}
	//   };	
		let data="";
		data+='<div class="d-flex align-items-center">';
		data+='<strong>Adding Event...</strong>'
		data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
		data+='</div>'
		document.getElementById("task").innerHTML=data;
	fetch("/addEvent", {
		"method" : "POST",
		"body" : formData,
		redirect: 'follow',
		headers: {
			'Content-Type': 'multipart/form-data'
		}
	})
	.then(response => {
		data='';
		data+='<div class="d-flex align-items-center">';
		data+='<strong>Event Added Sucessfully!</strong>'
		data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
		data+='</div>'
		document.getElementById("task").innerHTML=data;
	})
	}
}

function validateAndUploadAdd(){
	var fInput = document.getElementById("interest_words")
	var strings = fInput.value.split(',').map(s => s.trim());
	// console.log(strings);
	var flag = 1
	if(strings.length!=0){
		/* file validation */
		for(let i=0; i<strings.length; i = i + 1){
			if(strings[i].includes(' ')){
				// console.log("Issue");
				document.getElementById("interest_words_check").innerHTML='<font color="red">Only one word adjectives are supported!</font>';
				fInput.style.borderColor="red";
				flag=0;	
			}
		} 
	}
	// console.log(flag);
	if(flag==0){
		return false;
	}
	else{
		// console.log("Check Pass!");
		document.getElementById("interest_words_check").innerHTML='<font color="green">Looks good!</font>';
		fInput.style.borderColor="green";
		
		
		let formData=new FormData();
		// formData.append('interest_words',strings);
		let requestOptions = {
			method: 'POST',
			body: JSON.stringify(strings),
			redirect: 'follow',
			headers: {
				'Content-Type': 'application/json'
			}
	  };	
		let data="";
		data+='<div class="d-flex align-items-center">';
		data+='<strong>Adding Interests...</strong>'
		data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
		data+='</div>'
		document.getElementById("task").innerHTML=data;
	fetch("/addInterest", requestOptions)
	.then(response => {
		data='';
		data+='<div class="d-flex align-items-center">';
		data+='<strong>Interests Added Sucessfully!</strong>'
		data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
		data+='</div>'
		document.getElementById("task").innerHTML=data;
	})
	// .then((result) => {
	// 	console.log(result);
	// 	if(result.status==200){
	// 		data='';
	// 		data+='<div class="d-flex align-items-center">';
	// 		data+='<strong>Interests Added Sucessfully!</strong>'
	// 		data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
	// 		data+='</div>'
	// 		document.getElementById("task").innerHTML=data;
	// 	}
	// 	else{
	// 		alert("Server error! Try again later.");
	// 	}
	// })
	// .catch(error => console.log('error', error));

	}

}

function validateAndUploadDelete(){
	var fInput = document.getElementById("interest_words");
	var strings = fInput.value.split(',').map(s => s.trim());
	console.log(strings);
	var flag = 1;
	if(strings.length!=0){
		/* file validation */
		for(let i=0; i<strings.length; i = i + 1){
			if(strings[i].includes(' ')){
				console.log("Issue");
				document.getElementById("interest_words_check").innerHTML='<font color="red">Only one word adjectives are supported!</font>';
				fInput.style.borderColor="red";
				flag=0;	
			}
		} 
	}
	console.log(flag);
	if(flag==0){
		return false;
	}
	else{
		console.log("Check Pass!");
		document.getElementById("interest_words_check").innerHTML='<font color="green">Looks good!</font>';
		fInput.style.borderColor="green";
		
		
		let formData=new FormData();
		// formData.append('interest_words',strings);
		let requestOptions = {
			method: 'POST',
			body: JSON.stringify(strings),
			redirect: 'follow',
			headers: {
				'Content-Type': 'application/json'
			}
	  };	
		let data="";
		data+='<div class="d-flex align-items-center">';
		data+='<strong>Deleting Interests...</strong>'
		data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
		data+='</div>'
		document.getElementById("task").innerHTML=data;
	fetch("/deleteInterest", requestOptions)
	.then(response => {
		data='';
		data+='<div class="d-flex align-items-center">';
		data+='<strong>Interests Deleted Sucessfully!</strong>'
		data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
		data+='</div>'
		document.getElementById("task").innerHTML=data;
	})
	// .then((result) => {
	// 	if(result.status==200){
			// data='';
			// data+='<div class="d-flex align-items-center">';
			// data+='<strong>Interests Deleted Sucessfully!</strong>'
			// data+='<div class="spinner-border ms-auto" role="status" aria-hidden="true"></div>'
			// data+='</div>'
			// document.getElementById("task").innerHTML=data;
	// 	}
	// 	else{
	// 		alert("Server error! Try again later.");
	// 	}
	// })
	// .catch(error => console.log('error', error));

	}

}