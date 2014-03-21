var AlsAdmin;
if(!AlsAdmin) AlsAdmin={};

(function($) {
    AlsAdmin.uncheckAllScheduleInputs=function(){
        $('.schedule input[type=checkbox]').removeAttr('checked');
    };

    AlsAdmin.collectValue=function(){
        var result = '', result_minute='', hour = 0, day = 0, minute = 0;

        for(day=0; day<7; day++){
            for(hour=0; hour<24; hour++){
                result_minute = '';
                for(minute=0; minute<4; minute++){
                    result_minute += $('#id-'+day+'_'+hour+'_'+minute).attr('checked')?'1':'0';
                }
                result += parseInt(result_minute, 2).toString(16);
            }
        }
        console.log(result);

        return result
    };

    AlsAdmin.setNewValue = function(){
        $('input[name=schedule]').val(AlsAdmin.collectValue());
    };

    $(document).ready(function(){
        $('.schedule input[type=checkbox]').change(function(){
            AlsAdmin.setNewValue();
        });

        $('a.schedule_header_time').click(function(){
            var self = $(this),
                data_time = $(this).attr('data-time'),
                data_part = parseInt($(this).attr('data-part')),
                inputs = $('input[data-time='+data_time+(data_part*2)+'], input[data-time='+data_time+(data_part*2+1)+']');
            if(self.attr('clicked')){
                inputs.removeAttr('checked');
                self.attr('title','Отметить столбец');
                self.removeAttr('clicked');
            }else{
                inputs.attr('checked','checked');
                self.attr('title','Снять отметки со столбца');
                self.attr('clicked',true);
            }
            AlsAdmin.setNewValue();
        });
        $('a.schedule_header_day').click(function(){
            var self = $(this), inputs = $('input[data-day='+$(this).attr('data-day')+']');
            if(self.attr('clicked')){
                inputs.removeAttr('checked');
                self.attr('title','Отметить ряд');
                self.removeAttr('clicked');
            }else{
                inputs.attr('checked','checked');
                self.attr('title','Снять отметки с ряда');
                self.attr('clicked',true);
            }
            AlsAdmin.setNewValue();
        });

        $('a.schedule_check_all').click(function(){
            $('.schedule input[type=checkbox]').attr('checked', 'checked');
            AlsAdmin.setNewValue();
        });
        $('a.schedule_uncheck_all').click(function(){
            AlsAdmin.uncheckAllScheduleInputs();
            AlsAdmin.setNewValue();
        });
        $('a.schedule_check_standart').click(function(){
            AlsAdmin.uncheckAllScheduleInputs();
            var day=0, hour=0, minute=0;
            for(day=2; day<7; day++){
                for(hour=9; hour<13; hour++){
                    for(minute=0; minute<4; minute++){
                        $('#id-'+day+'_'+hour+'_'+minute).attr('checked','checked');
                    }
                }

                for(hour=14; hour<18; hour++){
                    if(!(day==6 && hour>16)){
                        for(minute=0; minute<4; minute++){
                            $('#id-'+day+'_'+hour+'_'+minute).attr('checked','checked');
                        }
                    }
                }
            }
            AlsAdmin.setNewValue();
        });
        $('a.schedule_check_reverse').click(function(){
            $('.schedule input[type=checkbox]').each(function(el){
                var self=$(this);
                if(self.attr('checked')){
                    self.removeAttr('checked');
                }else{
                    self.attr('checked', 'checked');
                }
            });
            AlsAdmin.setNewValue();
        });
    });
})(django.jQuery);
