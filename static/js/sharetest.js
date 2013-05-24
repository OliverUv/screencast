//function that will disable form's button so that user cannot send multiple requests to our function. It takes boolean value and id of the form.  
$(document).ready(function() {

    var disableSubmit = function(val, id){  
        $(id + ' input[type=submit]').attr('disabled', val);  
    };     
      
    //the fun starts here. On click of 'form-submit' button we run a function  

    $('.form-submit-add').click(function() {  

        //we are storing form object, form id, form's action and form message div id in variables  
        var form = $(this).parents("form:first");  
        var id = '#' + form.attr('id');  
        var action = form.attr('action');  
        var form_message = id + '-message';  
          
        disableSubmit(true, id);  

        $(form_message).removeClass().addClass('loading').html('Adding...').fadeIn();          
        /*
        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: form.serialize(),
            csrfmiddlewaretoken: '{{ csrf_token }}',
            success: function (data) {
                alert('ok');
            }
        });
 */       
   
        $(this).parents("form:first").ajaxSubmit({  
            dataType: "json",  
            "success": function(data) {  
                $(form_message).hide();  

                //change class of message div to 'type' returned by our view and insert 'message' also returned by json serializer  
                $(form_message).removeClass().addClass(data['type']).html(data['message']).fadeIn('slow');  
                disableSubmit(false, id);  

                if(data['type'] == 'success'){  
                    //clear all the form's inputs that are not of submission, button, hidden or reset type  
                    $(':input', id).not(':button, :submit, :reset, :hidden').val('');  
                }                 
            }  
        });  
        return false;  
    });      
        
});
