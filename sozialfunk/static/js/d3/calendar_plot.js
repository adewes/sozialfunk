d3.calendar_plot = function f(element_id,dates,values,interval_data)
{
    /*This function plots a calendar chart, color-coding the individual dates given in "dates" according to a numerical value stored
     *in "values".
     *
     *
     *
     *
     *
     *
     *
     *
     */

    var start_date = dates[0];
    var end_date = dates[dates.length-1];
    
    var date_format = "%Y-%m-%d";
    
    var dates_str = [];
    
    for(i=0;i<dates.length;i++)
    {
        dates_str.push(d3.time.format(date_format)(dates[i]));
    }
    
    var margin_left  = 40;
    var margin_right = 40;

    var margin_top  = 20;
    var margin_bottom = 0;
    
    var start_weekday = (start_date.getDay()-1)%7;
        
    var days_since_ref = function(date){return Math.floor((date-start_date)/24/60/60/1000);};
    var cell_x = function(date){return Math.floor((days_since_ref(date)+start_weekday)/7)};
    var cell_y = function(date){return (days_since_ref(date)+start_weekday)%7};

    var max_x = cell_x(end_date)+1;
    var aspect = 1;

    var plot = document.getElementById(element_id);

    while (plot.hasChildNodes())
    {
        plot.removeChild(plot.firstChild);
    }
    
    var cellSize = (plot.offsetWidth-margin_left-margin_right)/max_x; 
    
    var width = plot.offsetWidth,
        height = 7*cellSize*aspect+margin_top+margin_bottom; // cell size

    var coord_x = function(cell){return Math.floor(margin_left+cellSize*cell);};
    var coord_y = function(cell){return Math.floor(margin_top+aspect*cellSize*cell);};
        
    var day = d3.time.format("%w"),
        week = d3.time.format("%U"),
        percent = d3.format(".1%"),
        format = d3.time.format(date_format);
    
    var color = d3.scale.quantize()
        .domain(d3.extent(values, function(d) { return d; }))
        .range(d3.range(11).map(function(d) { return "q" + d + "-11"; }));
    
    var svg = d3.select("#"+element_id).append("svg")
        .attr("width", width)
        .attr("height", height)
        .attr("class", "RdYlGn")
    
    var get_stress_value = function(d){return values[days_since_ref(d)];};
    
    var rect = svg.selectAll(".day")
        .data(function(d) { return d3.time.days(start_date, end_date); })
        .enter().append("rect")
        .attr("class", "day")
        .attr("width", cellSize)
        .attr("height", cellSize*aspect)
        .attr("x", function(d) { return coord_x(cell_x(d)) ; })
        .attr("y", function(d) { return coord_y(cell_y(d)) ; })
        .datum(format);

    var format_interval_data = function(d){format(d[0]);};
        
    if (interval_data)
    {
        var intervals = svg.selectAll(".interval")
        .data(function(d) { return interval_data; })
        .enter()
        .append("rect")
        .filter(function(d){return d[0] > start_date && d[0] < end_date;})
        .attr("class", "interval")
        .attr("width", cellSize*0.25)
        .attr("height", function(d){return Math.abs(d[2]-d[1])*cellSize*aspect})
        .attr("x", function(d) { return coord_x(cell_x(d[0])+0.375) ; })
        .attr("y", function(d) { return coord_y(cell_y(d[0])+d[1]) ; })
        .datum(format_interval_data);
    }
    
    rect.append("title")
        .text(function(d) { return d; });

    var week_strs = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'];
    var month_strs = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
        
    var weekday_labels = svg.selectAll(".weekday")
        .data(function(d) { return d3.range(0,7);})
      .enter().append("text")
        .attr("class", "label")
        .attr("text-anchor","end")
        .attr("x", function(d) {return coord_x(0)-6 ; })
        .attr("y", function(d) { return coord_y(d+1)-cellSize*0.3; })
        .text(function(d) {return week_strs[d]; });

    var displayed_months = d3.time.months(start_date, end_date);
        
    var months_labels = svg.selectAll(".month")
        .data(function(d) {return displayed_months;})
        .enter().append("text")
        .datum(function (d){if (d.getDay() != 1){d.setDate(d.getDate()+7);};return d;})
        .attr("class", "label")
        .attr("text-anchor","begin")
        .attr("x", function(d) {return coord_x(cell_x(d)); })
        .attr("y", function(d) {return coord_y(0)-10; })
        .text(function(d) {if (d.getMonth() == 0 || d == displayed_months[0]){return month_strs[d.getMonth()]+" "+d.getFullYear();}else{return month_strs[d.getMonth()];} });

    if (values)
    {
        rect.filter(function (d){if (dates_str.indexOf(d)==-1){return false;};return true;})
        .attr("class", function(d) {i = dates_str.indexOf(d);return "day " + color(values[i]); })
        .select("title")
        .text(function(d) {i = dates_str.indexOf(d); return d + ": " + Math.floor(100*values[i])/100.0; });
    }
    
    function monthPath(t0) {
      var xpos = cell_x(t0);
      var ypos = cell_y(t0);
      return "M"+coord_x(xpos)+","+coord_y(7)
            +"H"+coord_x(xpos)+"V"+coord_y(ypos)
            +"H"+coord_x(xpos+1)+"V"+coord_y(ypos)
            +"H"+coord_x(xpos+1)+"V"+coord_y(0);
    }

    svg.selectAll(".month")
        .data(function(d) { return d3.time.months(start_date, end_date); })
      .enter().append("path")
        .attr("class", "month")
        .attr("d", monthPath);
}
