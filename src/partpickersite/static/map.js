const csrftoken = Cookies.get('csrftoken');

$(document).ready(function(){
// create the table for the user to select parts to highlight
parts_table = $('#parts_table').DataTable({
select: 'row',
data: parts,
bLengthChange: false,
bInfo: false,
bPaginate: false,
columns: [
{title: "Part Number"},
{title: "Description"},
{title: "Location"}
],
dom: 'Bfrtip',
buttons: [{
            text: 'Found Selected Item',
            action: function ( e, dt, node, config ) {
                found_items();
            }}],

});
blink_interval = []
parts_table.on('select', function(e, dt, type, indexes){

if(type=="row"){

part_number = parts_table.row(indexes).data()[4]
for(i=0;i< parts_indexes.length; i++){

if(part_number == parts_indexes[i][1]){
            //iterate through the racks to blink the led selected on the map
            for(key in racks){
            if(parts_indexes[i][0][0] == key){

            //console.log(parts_indexes[i][0][1], part_number)
            x_coord = racks[key][0]
            height = (racks_separator[parts_indexes[i][0][1]][0] + racks_separator[parts_indexes[i][0][1]][1])/2
            y_coord = height
            async function blink(x_coord, y_coord){
            ctx.fillStyle = `rgb(175,175,175)`
            ctx.beginPath();
            ctx.arc((x_coord + cell_width/2),y_coord + 50,led_radius,0,2* Math.PI);
            ctx.stroke();
            ctx.fill();
            ctx.closePath();
            return_blinker = setTimeout(function blink_return(){
            ctx.beginPath();
            ctx.fillStyle = fill_command;
            ctx.arc((x_coord + cell_width/2),y_coord + 50,led_radius,0,2* Math.PI);
            ctx.stroke();
            ctx.fill();
            ctx.closePath();
            },750);

            };
            blink_interval[i] = [setInterval(blink, 1500, x_coord, y_coord), part_number];

}}};
}};
});

parts_table.on('deselect', function(e, dt, type, indexes){

if(type=="row"){

part_number = parts_table.row(indexes).data()[4]

for(i=0;i< parts_indexes.length; i++){

if(part_number == parts_indexes[i][1]){
            //iterate through the racks to blink the led selected on the map
            for(key in racks){
            if(parts_indexes[i][0][0] == key){

            x_coord = racks[key][0]
            height = (racks_separator[parts_indexes[i][0][1]][0] + racks_separator[parts_indexes[i][0][1]][1])/2
            y_coord = height
            ctx.fillStyle = fill_command
            for(item in blink_interval){
            if(blink_interval[item][1] == part_number){
            clearInterval(blink_interval[item][0])

            }};
            ctx.beginPath();
            ctx.arc((x_coord + cell_width/2),y_coord + 50,led_radius,0,2* Math.PI);
            ctx.stroke();
            ctx.fill();
            ctx.closePath();
}}};

}};
});
function found_items(){
selected_rows = parts_table.rows({'selected': true})[0]
reset_leds = []
for(e=0; e < selected_rows.length; e++){
parts_table.row(selected_rows[e]).deselect();
clearLED(parts_table.rows(selected_rows[e]));
//TODO fix the redraw issue
//TODO Tell server to turn led off unless another user is looking for the same part
reset_leds.push(parts_table.rows(selected_rows[e]).data()[0][4])
}
parts_table.rows(selected_rows).remove().draw();
if(selected_rows.length > 0){
reset_led(reset_leds)
};
};
function clearLED(row_ID){


part_number = row_ID.data()[0][4]
for(i=0;i< parts_indexes.length; i++){

if(part_number == parts_indexes[i][1]){
            //iterate through the racks to blink the led selected on the map
            for(key in racks){
            if(parts_indexes[i][0][0] == key){

            x_coord = racks[key][0]
            height = (racks_separator[parts_indexes[i][0][1]][0] + racks_separator[parts_indexes[i][0][1]][1])/2
            y_coord = height
            for(item in blink_interval){
            if(blink_interval[item][1] == part_number){

            ctx.clearRect((x_coord + cell_width/2) - led_radius - 1, (y_coord + 50 - led_radius - 1), led_radius * 2 + 2, led_radius * 2 + 2)
            }};
}}};

}};

function reset_led(part_nums){
parts_string = ''
for(part_index in part_nums){
if(part_index != (part_nums.length - 1)){
parts_string += part_nums[part_index]+'/'

}else{
parts_string += part_nums[part_index]
console.log(parts_string)

}};

$.ajaxSetup({
            beforeSend: function(xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }});
    //send a request to the server to light up the led for each part selected
$.ajax({
    type: "POST",
    data: {'parts_string':JSON.stringify(parts_string)},
    dataType: "json",
    url: "reset_led"
}).done(function (res) {
console.log(res)
});

};
});

