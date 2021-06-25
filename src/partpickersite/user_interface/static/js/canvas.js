var canvas = document.getElementById("map_canvas");
var ctx = canvas.getContext('2d');
blink_color = [175, 175, 175]
console.log(colors)
class Rack {
constructor(location,x=0,y=50){
this.location = location;
this.width  = 50;
this.height = 300;
this.x = x;
this.y = y;
}
}

class Led {

constructor(rack, separator, radius, blinking_color, color, part_num, x, y){
var canvas = document.getElementById("map_canvas");
var ctx = canvas.getContext('2d');
this.racks = rack;
this.separator = separator;
this.radius = radius;
this.blink_color = `rgb(${blinking_color[0]}, ${blinking_color[1]}, ${blinking_color[2]})`;
this.x = x;
this.y = y;
this.fill_command = `rgb(${color[0]}, ${color[1]}, ${color[2]})`;
}

draw_self(){
ctx.beginPath();

ctx.arc(this.x ,this.y + 50,this.radius,0,2* Math.PI); //draw the led
ctx.stroke();
ctx.fillStyle = this.fill_command;
ctx.fill();
ctx.closePath();
}

}

var led_radius = 6; //radius in pixels of the led to be drawn on the screen
var blinking_locations = {};
canvas.width = 1600;
canvas.height = 800;
canvas.style.width = "800px";
canvas.style.height = "400px";
//TODO Set width and height based on browser resolution
ctx.scale(2,2)
other_colors = colors[1];
colors = colors[0];
// Test positions for racks: Position in pixels for each rack to be drawn
//TODO potentially get racks as part of the ajax request
var racks = {'A1': [50,50],
'A2': [100,50],
'B1':[250,50],
'B2':[300,50],
'C1': [450, 50],
'C2': [500,50],
'GL Cube': [650,50],
'GL Cube2': [700,50]
}
// Each rack will be separated into a certain number of sections depending on how many neopixels are in each section
var racks_separator = {'0' :[0,60],
'1':[60,120],
'2':[120,180],
'3':[180,240],
'4':[240,300],
}
console.log(other_colors);
cell_width = 50; // Width of each rack to be drawn
cell_height = 300; // Height of each rack to be drawn
//the rgb values are defined from the list colors which is defined by django
red_val = colors[0];
green_val = colors[1];
blue_val = colors[2];

var fill_command = `rgb(${red_val},${green_val}, ${blue_val})` //set the color to the color decided by the server
console.log(fill_command);
ctx.fillStyle = fill_command;

for(key in racks){
racks[key] = new Rack(key,racks[key][0] , racks[key][1])
ctx.beginPath();
ctx.rect(racks[key].x,racks[key].y, racks[key].width, racks[key].height); // Draw each rack
//ctx.rect(racks[key][0],racks[key][1], cell_width, cell_height); // Draw each rack
ctx.stroke();
ctx.closePath();

}
part_locations = []
var lights = {}
var parts_indexes = []
for(i=0;i< parts.length; i++){
part_locations[i] = parts[i][2].split('/') //If a part is located at several racks or locations, they need to be split up to act individually

for(index=0;index< part_locations[i].length; index++){
separator = part_locations[i][index].split('-') //Take the number of where the part is located on that particular rack example 255/255/255-"0"
parts_indexes.push([separator, parts[i][4]]);

}};
for(light = 0; light < parts_indexes.length; light++){
temp_location = parts_indexes[light][0][0] + '-' + parts_indexes[light][0][1]
if(other_colors[temp_location]){
console.log(other_colors[temp_location])
lights[temp_location] = new Led(rack = parts_indexes[light][0][0], separator = parts_indexes[light][0][1], radius = led_radius, blinking_color= blink_color, color=other_colors[temp_location], part_num=parts_indexes[light][1], x=(racks[parts_indexes[light][0][0]].x + cell_width/2), y= (racks_separator[parts_indexes[light][0][1]][0] + racks_separator[parts_indexes[light][0][1]][1])/2)
}else{
lights[temp_location] = new Led(rack=parts_indexes[light][0][0], separator=parts_indexes[light][0][1], radius = led_radius, blinking_color=  blink_color, color=colors, part_num=parts_indexes[light][1], x=(racks[parts_indexes[light][0][0]].x + cell_width/2), y= (racks_separator[parts_indexes[light][0][1]][0] + racks_separator[parts_indexes[light][0][1]][1])/2)
}}
console.log(lights)
for(light in lights){
    lights[light].draw_self();
    };
setInterval(function(){

if(blinking_locations){
for(key in blinking_locations){
ctx.beginPath()
ctx.arc(lights[key].x, lights[key].y + 50, lights[key].radius, 0, 2 * Math.PI)
ctx.stroke();
ctx.fillStyle = lights[key].blink_color;
ctx.fill();
ctx.closePath();
}
}
setTimeout(function(){

for(key in blinking_locations){
ctx.beginPath();
ctx.arc(lights[key].x, lights[key].y + 50, lights[key].radius, 0, 2 * Math.PI)
ctx.stroke();
ctx.fillStyle = lights[key].fill_command;
ctx.fill();
ctx.closePath();
}

}, 750)

}, 1500)
