const csrftoken = Cookies.get('csrftoken');
$(document).ready(function(){
console.log(parts)
// creates the table for the user to select parts to highlight
parts_table = $('#parts_table').DataTable({
select: 'row',
scrollY: '300px',
scrollCollapse: true,
data: parts,
bLengthChange: false,
bInfo: false,
bPaginate: false,
columns: [
{title: "Part Number"},
{title: "Description"},
{title: "Location"}
],
scrollCollapse: true,
dom: 'Bfrtip',
buttons: [{
            text: 'Found Selected Item',
            action: function ( e, dt, node, config ) {
                found_items();
            }}],

});
blink_interval = [];
reset_leds = [];
parts_table.on('select', function(e, dt, type, indexes){

if(type=="row"){

locations = parts_table.row(indexes).data()[2].split('/')
for(i=0; i < locations.length; i++){
if(locations[i] in blinking_locations){
blinking_locations[locations[i]] = blinking_locations[locations[i]] + 1;
}else{
blinking_locations[locations[i]] = 1;
};

};
};
});

parts_table.on('deselect', function(e, dt, type, indexes){
if(type=="row"){
locations = parts_table.row(indexes).data()[2].split('/')

for(i=0; i < locations.length; i++){
blinking_locations[locations[i]] = blinking_locations[locations[i]] - 1
if(blinking_locations[locations[i]] == 0){

ctx.beginPath()
ctx.arc(lights[locations[i]].x, lights[locations[i]].y + 50, lights[key].radius, 0, 2 * Math.PI)
ctx.stroke();
ctx.fillStyle = lights[locations[i]].fill_command;
ctx.fill();
ctx.closePath();
delete blinking_locations[locations[i]]
}};

};
});
//everything is pretty messed up here
function found_items(){
part_numbers = []
part_locations = []
selected_rows = parts_table.rows({'selected': true})[0];
for(e=0; e < selected_rows.length; e++){
part_location = parts_table.row(selected_rows[e]).data()[2].split('/')
part_numbers.push([part_location , parts_table.row(selected_rows[e]).data()[4]])
for(i=0; i< part_location.length; i++){
part_locations.push(part_location[i])
}

parts_table.row(selected_rows[e]).deselect();

}

parts_table.rows(selected_rows).remove().draw();
for(i=0; i < part_locations.length; i++){
//Check for multiple leds for one part
console.log(lights[part_locations[i]].x, lights[part_locations[i]].y, lights[part_locations[i]].radius)
ctx.clearRect((lights[part_locations[i]].x - lights[part_locations[i]].radius - 1) , (lights[part_locations[i]].y + 50 - lights[part_locations[i]].radius - 1), lights[part_locations[i]].radius * 2 + 2, lights[part_locations[i]].radius * 2 + 2);
}
reset_led(part_numbers)
};


function reset_led(part_nums){
parts_string = '';
console.log(part_nums)
for(i=0; i < part_nums.length; i++){
for(e=0; e < part_nums[i][0].length; e++){
if(part_nums[i][0][e] != part_nums[i][0][part_nums[i][0].length -1]){
parts_string += part_nums[i][0][e] + '/'
console.log(parts_string)
}else if(part_nums[i] != part_nums[part_nums.length -1]){
parts_string += part_nums[i][0][e] + '|' + part_nums[i][1]+ '\\';
}else{
parts_string += part_nums[i][0][e] + '|' + part_nums[i][1];
console.log(parts_string)

}
}
};

$.ajaxSetup({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }});
    //send a request to the server to light up the led for each part selected
$.ajax({
    type: "POST",
    data: {'parts_string':parts_string},
    dataType: "json",
    url: "reset_led"
}).done(function (res) {
console.log(res)
});

if(parts_table.rows().data().length == 0){
// code to execute when the table is empty
box = document.getElementsByClassName("complete_modal")
console.log($(".complete_modal").show())
document.getElementById("#back_button").onclick = function() {

$.ajaxSetup({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }});

//sends a post request with the data for the parts in the checkout table
    $.ajax({
        type: "GET",
        url: ""
    }).done(function (res) {
    console.log(res)
    });
    //TODO maybe change this when hosting the site
    history.back();

};


};

};
});

