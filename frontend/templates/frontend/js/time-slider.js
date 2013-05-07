function slideTime(event, ui){
    var val = $("#time-slider").slider("value"),
        hours = parseInt(val / 60 % 24, 10),
        minutes = parseInt(val % 60, 10),
    currentdate = new Date()
    startTime = getTime(currentdate.getHours(), currentdate.getMinutes());
    endTime = getTime(hours, minutes);
    $("#time").text(startTime + ' - ' + endTime);
}

function getTime(hours, minutes) {
    var time = null;
    minutes = minutes + "";
    if (hours < 12) {time = "AM";}
    else {  time = "PM";}
    if (hours == 0) {hours = 12;}
    if (hours > 12) {hours = hours - 12; }
    if (minutes.length == 1) {minutes = "0" + minutes;}
    return hours + ":" + minutes + " " + time;
}

$("#scheduleSubmit").on('click', function(){
    console.log(startTime);
    console.log(endTime);
    $('#Schedule tbody').append('<tr>' +
        '<td>' + startTime + '</td>' +
        '<td>' + endTime + '</td>' +
        '</tr>');
});
slideTime();