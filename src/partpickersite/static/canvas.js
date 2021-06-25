var canvas = document.getElementById("map_canvas");
ctx = canvas.getContext('2d');
var led_radius = 5;
//ctx.scale(0.5,0.5)
colors = colors[0]
var racks = {'A1': [50,50],
'A2': [100,50],
'B1':[250,50],
'B2':[300,50],
'C1': [450, 50],
'C1': [450, 50],
'C2': [500,50],
'GL Cube': [650,50],
'GL Cube2': [700,50]
}
var racks_separator = {'0' :[0,60],
'1':[60,120],
'2':[120,180],
'3':[180,240],
'4':[240,300],
}
console.log(racks)
console.log(parts, "PARTS");
console.log(colors);
cell_width = 50
cell_height = 300
//color = colors;
red_val = colors[0];
green_val = colors[1];
blue_val = colors[2];
//fill_command = `rgb(${red_val},${green_val}, ${blue_val})`

var fill_command = `rgb(${red_val},${green_val}, ${blue_val})`
console.log(fill_command)
ctx.fillStyle = fill_command

for(key in racks){
ctx.beginPath();

ctx.rect(racks[key][0],racks[key][1], cell_width, cell_height);
ctx.stroke();
ctx.closePath();

}
part_locations = []
var parts_indexes = []
for(i=0;i< parts.length; i++){
part_locations[i] = parts[i][2].split('/')
//console.log(part_locations)
for(index=0;index< part_locations[i].length; index++){
separator = part_locations[i][index].split('-')
parts_indexes.push([separator, parts[i][4]]);
};
};

for(key in racks){
for(i=0;i< parts_indexes.length; i++){
if(parts_indexes[i][0][0] == key){
height = (racks_separator[parts_indexes[i][0][1]][0] + racks_separator[parts_indexes[i][0][1]][1])/2
ctx.beginPath();
ctx.arc((racks[key][0] + cell_width/2),height + 50,led_radius,0,2* Math.PI);

ctx.stroke();
ctx.fillStyle = fill_command;
ctx.fill();
ctx.closePath();

}}};
//ctx.drawImage(ctx,0,0,500,500)