$(document).ready(function(){
				$("#reg").on('submit',function(event){
					$.ajax({
							data:{
								name:$('#inputName').val(),
								namel:$('#inputNamel').val(),
								pwd:$('#inputPassword').val(),
								email:$('#inputEmail').val()
							},
							type: "POST",
							url: "/reg"
						}).done(function(data){
						if(data.status=="done"){
        					window.location.replace("/email_sent_confirm.html");
							}else if(data.status=="err"){
							alert(data.discription);
							}
						});
						event.preventDefault();
				});
			});