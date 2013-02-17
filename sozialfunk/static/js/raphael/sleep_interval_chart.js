
var bars = [];

function componentToHex(c) {
var hex = c.toString(16);
return hex.length == 1 ? "0" + hex : hex;
}

function rgbToHex(r, g, b) {
  return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}

var canvas;
var weekdays_str = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
var months_str = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
var paper;

mix_color = {'r':255,'g':255,'b':255};

function style_font(x)
{
  return x.attr({'font-family':'Century Gothic','font-size':12})
}

Raphael.fn.sleep_interval_chart = function ()
{
  var paper = this;
  var chart = this.set();
  var n_days = sleep_interval_data[sleep_interval_data.length-1][0]
  var plot_width = canvas.offsetWidth;
  var plot_height = canvas.offsetHeight;
  var margin_y_top = 10;
  var margin_y_bottom = 60;
  var margin_x = 60;
  var axis_width = canvas.offsetWidth-2*margin_x;
  var axis_height = canvas.offsetHeight-margin_y_top-margin_y_bottom;
  var bar_width = axis_width/n_days*0.5;
  var ref_date = Date.parse(sleep_duration_metadata['ref_date']);
  var last_date = new Date(ref_date.getTime());
  last_date.add(n_days).days();

  var textstr = "23/04/2012\nlorem ipsum\nSleep quality: Good";
  var text = style_font(paper.text(0,0,textstr)).attr({'text-anchor':'start'}).toFront();
  var textrect = paper.rect(text.getBBox().x-20,text.getBBox().y-20,text.getBBox().width+40,text.getBBox().height+40).attr({'fill':'#fff'});
  var textgroup = paper.set();
  text.toFront();
  textgroup.push(text);
  textgroup.push(textrect);
  textgroup.attr({opacity:0});
        
  function process_data(i)
  {
    var start_day = sleep_interval_data[i][0];
    var start_hour = sleep_interval_data[i][1];
    var start_minute = sleep_interval_data[i][2];
    var stop_day = sleep_interval_data[i+1][0];
    var stop_hour = sleep_interval_data[i+1][1];
    var stop_minute = sleep_interval_data[i+1][2];
    var j = i/2;
    
    var start_column = start_day;
    
    if (start_hour < 12)
    {
      start_column-=1;
    }
    
    var stop_column = stop_day;
    
    if (stop_hour < 12)
    {
      stop_column-=1;
    }
        
    var current_year = ref_date.getFullYear();
    var curent_month = ref_date.getMonth();
    var current_day = ref_date.getDay();

    var bar_min = sleep_duration_metadata['min_duration'];
    var bar_max = sleep_duration_metadata['max_duration'];
    var bar_value = sleep_duration_data[j];

    
    var date = new Date(ref_date.getTime());
    date.add(start_column).days();

    var grad_value = 1;
    
    var r,g,b;
    r = 0;
    if (grad_value < 0.5)
    {
      b = 255;
      g = grad_value/0.5*255;
    }
    else
    {
      g = 255-155*(grad_value-0.5)/0.5;
      b = 255*(1-(grad_value-0.5)/0.5);
    }
    r = 0;
    g = 255;
    b = 0;
    
    var colorstr = rgbToHex(Math.floor((r+mix_color.r)/2),Math.floor((g+mix_color.g)/2),Math.floor((b+mix_color.b)/2));
    
    var current_column = start_column;

    while (current_column <= stop_column)
    {
      var bar_height,start_position,stop_position;
      if (current_column == start_column){
        start_position = ((start_hour+12)%24+start_minute/60.0)/24.0;
      }
      else{
        start_position = 0;
      }
      if (current_column < stop_column)
      {
        stop_position = 1;
      }
      else
      {
        stop_position = ((stop_hour+12)%24+stop_minute/60.0)/24.0;
      }
      bar_height = (stop_position-start_position)*axis_height;
      var x_pos = margin_x+(current_column/n_days)*axis_width;
      var y_pos = margin_y_top+start_position*axis_height;
      var grad_value = (bar_value-bar_min)/(bar_max-bar_min);
      
      var bar = paper.rect(x_pos, y_pos, bar_width,bar_height).toBack();
      bar.attr({'fill':colorstr,'stroke':'none'})

      bar.mouseover(function () {
          textgroup.attr({text:date.getDate()+" "+months_str[date.getMonth()]+" "+date.getFullYear()+"\nSlept:\t"+Math.floor(sleep_duration_data[j])+"h "+Math.floor(sleep_duration_data[j]*60%60)+"m\nInterruptions:\t 0\nSleep quality:\tGood\n"});
          textgroup.transform("t"+bar.getBBox().x+" -100");
          textgroup.stop().animate({opacity: 1,transform:"T"+(bar.getBBox().x2+30)+" "+100}, 300);
       }).mouseout(function () {
           textgroup.stop().animate({opacity: 0,transform:"T"+Math.floor(text.getBBox().x)+" -100"}, 300);
       });
      chart.push(bar);
      chart.push(text);
      current_column++;
    }
  }

  for(var i = 0;i < sleep_interval_data.length;i+=2)
  {
    process_data(i);
  }

  for(var i = 0;i<= 24; i+=4)
  {
    y_pos = margin_y_top+axis_height*i/24;
    pathstr = "M "+margin_x+" "+y_pos+"L"+(margin_x+axis_width)+" "+y_pos;
    path = paper.path(pathstr).toBack();
    path.attr({'stroke':'#aaa','stroke-dasharray':'--','stroke-width':0.5});

    hour = (12 +i)%24;
    if (hour == 0)
    {
      path.attr({'stroke-width':2});
    }
    var text = style_font(paper.text(margin_x-5,y_pos,hour).attr({'text-anchor':'end','font-size':18}));
  }

  var current_year = 0;
  var current_month = -1;

  for (var i=2; i<n_days;i+=5)
  {
    var date = new Date(ref_date.getTime());
    date.add(i).days();
    next_date = new Date(date.getTime());
    next_date.add(1).day();
    
    var x_pos = margin_x+((i+0.25)/n_days)*axis_width;

    pathstr = "M "+x_pos+" "+margin_y_top+"L"+x_pos+" "+(plot_height-margin_y_bottom);
    path = paper.path(pathstr).toBack();
    path.attr({'stroke':'#aaa','stroke-dasharray':'--','stroke-width':0.5});

    var text = style_font(paper.text(x_pos,plot_height-margin_y_bottom+16,weekdays_str[date.getDay()]+"/"+weekdays_str[next_date.getDay()]).attr({'text-anchor':'start','font-size':18}))     
    var text = style_font(paper.text(x_pos,plot_height-margin_y_bottom+32,date.getDate()+"/"+next_date.getDate()).attr({'text-anchor':'start','font-size':18}))
    if (date.getFullYear() != current_year || date.getMonth() != current_month)
    {
      var str = "";
      if (current_month != date.getMonth())
      {
        str+=months_str[date.getMonth()]
      }
      if (current_year != date.getFullYear())
      {
        str+=" "+date.getFullYear()
      }
      current_year = date.getFullYear();
      current_month = date.getMonth();
      var text = style_font(paper.text(margin_x+((i+0.25)/n_days)*axis_width,plot_height-margin_y_bottom+48,str).attr({'text-anchor':'start','font-size':18})).toBack();
    }
  }

}
