/**
 * Created by Administrator on 2017/6/19.
 */
requirejs.config({
    paths: {
        'jquery': 'lib/jquery-1.7.1.min'
    }
});

require(['jquery','/js/util/validate.js'],function ($,validate) {
    $("input[type='text'],input[type='password']").focus(function () {
        $(this).parent().addClass('active');
        if($(this).parents(".ir-input-wrapper").next(".help-block").length>0){
            $(this).parents(".ir-input-wrapper").next(".help-block").remove();
        }
        if($(this).parents(".ir-input-inline").next(".help-block").length>0){
            $(this).parents(".ir-input-inline").next(".help-block").remove();
        }
    }).blur(function () {
        $(this).parent().removeClass('active');
    })

    $("#loginBtn").click(function () {
        var $isValid = validate($(".ir-login-form"),{
            username:{
                parent: ".ir-input-wrapper",
                validators:{
                    notEmpty:{
                        message:"请输入用户名"
                    }
                }
            },
            password:{
                parent: ".ir-input-wrapper",
                validators:{
                    notEmpty:{
                        message:"请输入登录密码"
                    }
                }
            },
            // 校验验证码
            validateCode:{
                parent: ".ir-input-inline",
                validators:{
                    notEmpty:{
                        message:"请输入验证码"
                    }
                }
            }
        })
        return $isValid;
    })
})