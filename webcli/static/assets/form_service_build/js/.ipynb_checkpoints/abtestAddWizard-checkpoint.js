/*!

 =========================================================
 * Paper Bootstrap Wizard - v1.0.2
 =========================================================
 
 * Product Page: https://www.creative-tim.com/product/paper-bootstrap-wizard
 * Copyright 2017 Creative Tim (http://www.creative-tim.com)
 * Licensed under MIT (https://github.com/creativetimofficial/paper-bootstrap-wizard/blob/master/LICENSE.md)
 
 =========================================================
 
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 */

// Paper Bootstrap Wizard Functions

searchVisible = 0;
transparent = true;

        $(document).ready(function(){

            /*  Activate the tooltips      */
            $('[rel="tooltip"]').tooltip();

            // Code for the Validator
            var $validator = $('.wizard-card form').validate({
        		  rules: {
        		    firstname: {
        		      required: true,
        		      minlength: 3
        		    },
        		    lastname: {
        		      required: true,
        		      minlength: 3
        		    },
        		    email: {
        		      required: true
        		    }
                },
        	});

            // Wizard Initialization
          	$('.wizard-card').bootstrapWizard({
                'tabClass': 'nav nav-pills',
                'nextSelector': '.btn-next',
                'previousSelector': '.btn-previous',

                onNext: function(tab, navigation, index) {
                	var $valid = $('.wizard-card form').valid();
                	if(!$valid) {
                		$validator.focusInvalid();
                		return false;
                	}
                },

                onInit : function(tab, navigation, index){

                  //check number of tabs and fill the entire row
                  var $total = navigation.find('li').length;
                  $width = 100/$total;

                  navigation.find('li').css('width',$width + '%');

                },

                onTabClick : function(tab, navigation, index){

                    var $valid = $('.wizard-card form').valid();

                    if(!$valid){
                        return false;
                    } else{
                        return true;
                    }

                },

                onTabShow: function(tab, navigation, index) {
                    var $total = navigation.find('li').length;
                    var $current = index+1;

                    var $wizard = navigation.closest('.wizard-card');

                    // If it's the last tab then hide the last button and show the finish instead
                    if($current >= $total) {
                        $($wizard).find('.btn-next').hide();
                        $($wizard).find('.btn-finish').show();
                    } else {
                        $($wizard).find('.btn-next').show();
                        $($wizard).find('.btn-finish').hide();
                    }

                    //update progress
                    var move_distance = 100 / $total;
                    move_distance = move_distance * (index) + move_distance / 2;

                    $wizard.find($('.progress-bar')).css({width: move_distance + '%'});
                    //e.relatedTarget // previous tab

                    $wizard.find($('.wizard-card .nav-pills li.active a .icon-circle')).addClass('checked');

                }
	        });


                // Prepare the preview for profile picture
                $("#wizard-picture").change(function(){
                    readURL(this);
                });

                $('[data-toggle="wizard-radio"]').click(function(){
                    wizard = $(this).closest('.wizard-card');
                    wizard.find('[data-toggle="wizard-radio"]').removeClass('active');
                    $(this).addClass('active');
                    $(wizard).find('[type="radio"]').removeAttr('checked');
                    $(this).find('[type="radio"]').attr('checked','true');
                });

                $('[data-toggle="wizard-checkbox"]').click(function(){
                    if( $(this).hasClass('active')){
                        $(this).removeClass('active');
                         console.log('tttt',$(this).find('[type="checkbox"]'));
                        $(this).find('[type="checkbox"]').removeAttr('checked');
                        console.log('haha',$(this).find('[name="pub"]'));
                        if ($(this).find('[name="pub"]').length>0){
                            $('#form_opertype').removeAttr('value');
                        }
                        if ($(this).find('[name="reg"]').length>0){
                            $('#form_opertype2').removeAttr('value');
                            //$(".releaseFlux").addClass("layui-hide");
                            //$('#form_opertype').attr('checked','false');
                            //$(this).find('[type="checkbox"]').attr('disabled',"disabled");
                        }
                        
                        if ($(this).find('[name="mail"]').length>0){
                            $('#form_emailmsg').removeAttr('value');
                        }
                        
                        //$(this).find('[type="checkbox"]').removeAttr('value');
                        //$(this).find('[type="checkbox"]').find($('#form_opertype')).val("Hello Kitty");
                        //console.log($(this).find('[type="checkbox"]').find($('#form_opertype')).val("Hello Kitty"),'ddadsdsds');
                        console.log($('#form_opertype').val(),'newval');
                        console.log($('#form_opertype2').val(),'newval');
                        console.log($('#form_emailmsg').val(),'newval');
                        
                    } else {
                        $(this).addClass('active');
                        $(this).find('[type="checkbox"]').attr('checked','true');
                        if ($(this).find('[name="pub"]').length>0){
                            $('#form_opertype').attr('value','发布');
                            $(".releaseFlux").addClass("layui-hide");
                        }
                        if ($(this).find('[name="reg"]').length>0){
                            $('#form_opertype2').attr('value','注册');
                            $(".releaseFlux").removeClass("layui-hide");
                            
                        }
                        
                        if ($(this).find('[name="mail"]').length>0){
                            $('#form_emailmsg').attr('value','是');
                        }
                        
                        
                        
                        
                        console.log($('#form_opertype').val(),'oldval');
                        console.log($('#form_opertype2').val(),'oldval');
                        console.log($('#form_emailmsg').val(),'oldval');
                    }
                });

                $('.set-full-height').css('height', 'auto');

            });



         //Function to show image before upload

        function readURL(input) {
            if (input.files && input.files[0]) {
                var reader = new FileReader();

                reader.onload = function (e) {
                    $('#wizardPicturePreview').attr('src', e.target.result).fadeIn('slow');
                }
                reader.readAsDataURL(input.files[0]);
            }
        }

//实现单选
$(function () {
		    $('#recommendtype div:first-child div').addClass('active');
		    $('#recommendtype div div').click(function () {
		        $(this).addClass('active');
		        $(this).parent().siblings().find('div').removeClass('active');
                
		    });
		});