/**
 * Created by maxim on 30.11.13.
 */

function setupAjaxDjango(){
    // using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
}

jQuery(document).ready(function() {
    setupAjaxDjango();
    $('.rating-btn').click(function(){
        var model = $(this).parents(".toRate");
        var on = model.data("model");
        var id = model.data("id");
        var type = $(this).data("type");
        $.ajax({
                type: "post",
                url: "rating",
                data:
                {
                    id: id,
                    on: on,
                    type: type
                }
            })
            .done(function(msg)
                {
                    if (msg["error"] != null)
                    {
                        toastr.error(msg["error"]);
                        return;
                    }
                    toastr.success(msg["msg"]);
                    model.find(".rating-value").text(msg["rating"]);
                })

            .fail(function(msg){
               toastr.error("Произошла ошибка, попробуйте ещё раз.");
            });
        return false;
    });


    $('.correct-btn').click(function(){
        var model = $(this).parents(".toCorrect");
        var id = model.data("id");
        $.ajax({
                type: "post",
                url: "correct",
                data:
                {
                    id: id
                }
            })
            .done(function(msg)
                {
                    if (msg["error"] != null)
                    {
                        alert(msg["error"]);
                        return;
                    }
                    toastr.success(msg["msg"]);
                    if (msg["type"] == 1)
                    {
                        model.addClass("alert-success");
                        model.find(".correct-btn").text("Неправильный ответ");

                    }
                    if (msg["type"] == 0)
                    {
                        model.removeClass("alert-success");
                        model.find(".correct-btn").text("Правильный ответ");

                    }

                })

            .fail(function(msg){
                 toastr.error("Произошла ошибка, попробуйте ещё раз.");
            });
        return false;
    });


 $("#formRegistration").validate({
      rules: {
       username: {
        required: true,
        minlength: 2,
        maxLength:30
       },
       password: {
        required: true,
        maxlength:128
       },
       email: {
        required: true,
        maxlength:75
       }
      },
      messages: {
       username: {
        required: "Введите имя пользователя",
        minlength: "Имя пользователя не менее 2-х символов",
        maxlength:"Имя пользователя не более 30-ти символов"
       },
       password: {
        required: "Введите пароль",
        maxlength: "Пароль не более 128-ми символов"
       },
       email: {
        required: "Введите электронную почту",
        maxlength: "Электронная почта не более 75-ти символов"
       }
      }
    });



    $("#changeForm").validate({
      rules: {
       username: {
        required: true,
        minlength: 2,
        maxLength:30
       },
       email: {
        required: true,
        maxlength:75
       },
       first_name: {
           maxlength:30
       },
       last_name: {
           maxlength:30
       }
      },
      messages: {
       username: {
        required: "Введите имя пользователя",
        minlength: "Имя пользователя не менее 2-х символов",
        maxlength:"Имя пользователя не более 30-ти символов"
       },
       email: {
        required: "Введите электронную почту",
        maxlength: "Электронная почта не более 75-ти символов"
       },
       first_name: {
           maxlength:"Максимальная длина имени 30 символов"
       },
       last_name: {
           maxlength:"Максимальная длина фамилии 30 символов"
       }
      }
    });

     $("#questForm").validate({
      rules: {
       title: {
        required: true,
        minlength: 10,
        maxLength:100
       },
       body: {
        required: true,
        minlength: 10,
        maxlength:1000
       },
       tags: {
        maxWords: 4

       }
      },
      messages: {
       title: {
        required: "Введите заголовок вопроса",
        minlength: "Заголовок не менее 10 символов",
        maxlength:"Заголовок не более 100 символов"
       },
       body: {
        required: "Введите вопрос",
        minlength: "Вопрос не менее 10 символов",
        maxlength: "Вопрос не более 1000 символов"
       },
      tags: {
        maxWords: "Вы можете ввести не более 3 тегов"
       }
      }
    });

    $("#answerForm").validate({
      rules: {
       body: {
        required: true,
        minlength: 10,
        maxlength:1000
       }
      },
      messages: {
       body: {
        required: "Введите ответ",
        minlength: "Ответ не менее 10 символов",
        maxlength: "Ответ не более 1000 символов"
       }
      }
    });

    $("#formComment").validate({
      rules: {
       body: {
        required: true,
        minlength: 5,
        maxlength:200
       }
      },
      messages: {
       body: {
        required: "Введите комментарий",
        minlength: "Комментарий не менее 5 символов",
        maxlength: "Комментарий не более 200 символов"
       }
      }
    });
});

jQuery(document).ready(function() {
	google.load('visualization', '1.0', {'packages':['corechart']});
    var arr = [];
    arr.push(['Время', 'Значение']);
    var dataInfo = new google.visualization.DataTable();

    setInterval(function drawing() {
	    var data = new google.visualization.DataTable();
	    data.addColumn('string', 'name');
	    data.addColumn('number', 'amount');

	    // Задаем части диаграммы и их значения:
	    data.addRows([
		['Вопросы',  Math.random() * (100)],
		['Ответы', Math.random() * (100)],
		['Комментарии', Math.random() * (100)],
		['Пользователи', Math.random() * (100)]
	    ]);
	    // Задаем заголовок, ширину и высоту диаграммы:
	    var options = {
		'title':'Соотношение случайное',
		'width':800,
		'height':800
	    };
        var options2 = {
		'title':'График с накоплением',
		'width':800,
		'height':800
	    };
        var time = new Date();
        arr.push([time, Math.random()*(100)]);
        if(arr.length > 15)
        {
            arr.splice(1,1);
        }
        var fill = new google.visualization.arrayToDataTable(arr);

	    var chart = new google.visualization.LineChart(document.getElementById('dynamic_div'));
	    chart.draw(data, options);

        var chart2 = new google.visualization.LineChart(document.getElementById('dynamic_div3'));
	    chart2.draw(fill, options2);


        $.ajax({
                type: "get",
                url: "dynamic_graph"
            })
            .done(function(response_data)
            {
                 var data = new google.visualization.DataTable();
                    data.addColumn('string', 'Что');
                    data.addColumn('number', 'Количество');
                    data.addRows([
                        ['Вопросы' , response_data['quest']],
                        ['Ответы', response_data['ans']],
                        ['Комментарии к ответам', response_data['commentA']],
                        ['Комментарии к вопросам', response_data['commentQ']]
                    ]);
                var options = {
                'title':'Соотношение',
                'width':800,
                'height':800
                };
                var chart = new google.visualization.ColumnChart(document.getElementById('dynamic_div2'));


                if( data !== dataInfo )
                {
                    dataInfo = data;
                    chart.draw(data, options);
                }
                })
            .fail(function(response_data){
               toastr.error("Произошла ошибка, попробуйте ещё раз.");
            });
        }  , 1000);
 });
